from flask import Flask, request, jsonify
import requests
import schedule
import time
import threading
import pandas as pd

app = Flask(__name__)

# Function to fetch and process data
def fetch_and_process_data():
    print("Fetching and processing data...")
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    
    # Process data (example: calculate summary statistics)
    summary = df.describe()
    print(summary)
    
    # Save processed data to a CSV file
    df.to_csv('processed_data.csv', index=False)
    
    # Automate workflow task (example: send email with summary)
    send_email('Daily Data Summary', summary.to_string(), 'recipient@example.com')

# Function to send email notifications
def send_email(subject, body, to):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = to

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', to, msg.as_string())

# Schedule the task to run daily at 9 AM
schedule.every().day.at("09:00").do(fetch_and_process_data)

# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Process the data here
    print(data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5000)
