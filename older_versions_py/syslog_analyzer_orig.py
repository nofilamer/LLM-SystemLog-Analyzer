import openai
import os

# OpenAI API Key (Use environment variable for security)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the latest API version
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
                {"role": "system", "content": "You are a system log analyst. Identify any unusual patterns, errors, or security threats."},
                {"role": "user", "content": "\n".join(logs)}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in OpenAI API call: {e}"

if __name__ == "__main__":
    log_file = "/var/log/syslog"
    logs = read_last_n_lines(log_file, 1000)
    
    if logs:
        print("Sending logs to OpenAI for analysis...")
        analysis = analyze_logs_with_openai(logs)
        print("\n--- OpenAI Analysis ---\n")
        print(analysis)
    else:
        print("No logs found or error reading the file.")

