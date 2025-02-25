# **LLM System Log Analyzer** 🚀

**LLM System Log Analyzer** is a Flask-based web application that reads and analyzes system logs (**/var/log/syslog**) using **OpenAI's GPT-4-turbo**. It identifies potential **errors, warnings, and anomalies**, categorizing them by severity (**Critical 🔴, Warning 🟠, Informational 🟢**). The results are displayed in an interactive, color-coded web UI.

---

## **🌟 Features**
✅ **Automated Log Analysis** – Reads and processes the last 1000 lines from `/var/log/syslog`.  
✅ **AI-Powered Insights** – Uses OpenAI’s GPT-4-turbo to identify issues and suggest fixes.  
✅ **Severity Classification** – Issues are categorized as **Critical 🔴, Warning 🟠, Informational 🟢**.  
✅ **User-Friendly Web Interface** – Built with **Flask, HTML, JavaScript, and CSS** for easy interaction.  
✅ **Color-Coded Table** – Quickly spot system issues.  
✅ **Live Analysis Button** – Runs real-time log analysis with one click.  

---

## **🛠 Installation & Setup**
### 
**1️⃣ Clone the Repository**
git clone https://github.com/nofilamer/LLM-SystemLog-Analyzer.git
cd LLM-SystemLog-Analyzer

2️⃣ Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up OpenAI API Key
You'll need an OpenAI API key to use GPT-4. Export it like this:
export OPENAI_API_KEY="your-api-key-here"  # Linux/macOS
set OPENAI_API_KEY="your-api-key-here"  # Windows

5️⃣ Run the Flask App
python syslog_analyzer.py

📌 Technologies Used
Python (Flask)
OpenAI GPT-4-turbo
HTML, CSS, JavaScript
Pandas (for data processing)

📜 License
This project is open-source and available under the MIT License.
