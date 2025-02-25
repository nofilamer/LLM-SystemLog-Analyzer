import openai
import os
import pandas as pd
import re
from flask import Flask, render_template, request, jsonify

# OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

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
        return [f"Error reading file: {e}"]

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

def categorize_severity(issue_name):
    """Categorizes issue severity based on keywords in the issue name."""
    critical_keywords = ["Corruption", "Failure", "Timeout", "Crash", "Unresponsive"]
    warning_keywords = ["Lost", "Errors", "Restart", "Repeated", "High Usage"]
    informational_keywords = ["Activation", "Log", "Monitor"]

    if any(word in issue_name for word in critical_keywords):
        return "Critical"
    elif any(word in issue_name for word in warning_keywords):
        return "Warning"
    elif any(word in issue_name for word in informational_keywords):
        return "Informational"
    return "Unknown"

def parse_analysis_to_table(analysis_text):
    """Extracts issues and descriptions from OpenAI's response and structures them into a table."""
    issues = []
    descriptions = []
    severities = []

    # Updated regex to match each issue separately
    pattern = r"\d+\.\s\*\*(.*?)\*\*\s*[:-]?\s*(.*?)(?=\n\d+\.|\Z)"  
    matches = re.findall(pattern, analysis_text, re.DOTALL)

    for match in matches:
        issue_name, description = match
        severity = categorize_severity(issue_name)

        issues.append(issue_name.strip())  # Extract issue title
        descriptions.append(description.strip())  # Extract details
        severities.append(severity)  # Assign severity level

    # Convert to DataFrame
    df = pd.DataFrame({
        "Issue Name": issues,
        "Analysis": descriptions,
        "Severity": severities
    })
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    log_file = "/var/log/syslog"
    logs = read_last_n_lines(log_file, 1000)
    
    if logs:
        analysis = analyze_logs_with_openai(logs)
        if analysis:
            df_analysis = parse_analysis_to_table(analysis)
            return jsonify(df_analysis.to_dict(orient="records"))
        else:
            return jsonify({"error": "No valid response from OpenAI."})
    else:
        return jsonify({"error": "No logs found or error reading the file."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

