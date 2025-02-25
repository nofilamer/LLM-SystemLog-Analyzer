import openai
import os
import pandas as pd
import re
from tabulate import tabulate  # Import tabulate for table formatting

# OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def read_last_n_lines(file_path, n=1000):
    """Efficiently read the last N lines of a file."""
    try:
        with open(file_path, "rb") as f:
            f.seek(0, 2)  # Move to the end of the file
            buffer = bytearray()
            pointer = f.tell()
            while pointer > 0 and len(buffer) < 100000:  # Prevent excessive memory usage
                f.seek(max(pointer - 4096, 0))
                chunk = f.read(pointer - f.tell())
                buffer[:0] = chunk
                pointer = f.tell()
                if buffer.count(b"\n") >= n:
                    break

            return buffer.decode(errors="ignore").splitlines()[-n:]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def analyze_logs_with_openai(logs):
    """Send logs to OpenAI for analysis using the latest API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a system log analyst. Identify any unusual patterns, errors, or security threats. Format your response as a list of issues, each with a title and detailed analysis."},
                {"role": "user", "content": "\n".join(logs)}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in OpenAI API call: {e}"

def parse_analysis_to_table(analysis_text):
    """Extracts issues and descriptions from OpenAI's response and structures them into a table."""
    issues = []
    descriptions = []

    # Use regex to extract issue names and descriptions
    matches = re.findall(r"\*\*(.*?)\*\*\s*[:-]?\s*(.*)", analysis_text, re.DOTALL)
    
    for match in matches:
        issue, description = match
        issues.append(issue.strip())
        descriptions.append(description.strip())

    # Convert to DataFrame
    df = pd.DataFrame({"Issue Name": issues, "Analysis": descriptions})
    return df

if __name__ == "__main__":
    log_file = "/var/log/syslog"
    logs = read_last_n_lines(log_file, 1000)
    
    if logs:
        print("Sending logs to OpenAI for analysis...")
        analysis = analyze_logs_with_openai(logs)
        
        if analysis:
            df_analysis = parse_analysis_to_table(analysis)

            # Display table using tabulate
            print("\n--- OpenAI Log Analysis ---\n")
            print(tabulate(df_analysis, headers="keys", tablefmt="pretty"))
        else:
            print("No valid response from OpenAI.")
    else:
        print("No logs found or error reading the file.")

