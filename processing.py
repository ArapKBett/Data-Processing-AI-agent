import matplotlib.pyplot as plt

def fetch_and_process_data():
    print("Fetching and processing data...")
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    
    # Filter data (example: filter rows where value > threshold)
    filtered_df = df[df['value'] > 10]
    
    # Generate a plot
    plt.figure(figsize=(10, 6))
    filtered_df['value'].plot(kind='bar')
    plt.title('Filtered Data')
    plt.savefig('filtered_data_plot.png')
    
    # Save processed data to a CSV file
    filtered_df.to_csv('filtered_data.csv', index=False)
    
    # Automate workflow task (example: send email with plot)
    send_email('Daily Data Summary', 'See attached plot.', 'recipient@example.com', 'filtered_data_plot.png')

def send_email(subject, body, to, attachment=None):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = to

    if attachment:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read(), Name=basename(attachment))
            part['Content-Disposition'] = f'attachment; filename="{basename(attachment)}"'
            msg.attach(part)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', to, msg.as_string())

# Schedule the task to run daily at 9 AM
schedule.every().day.at("09:00").do(fetch_and_process_data)
