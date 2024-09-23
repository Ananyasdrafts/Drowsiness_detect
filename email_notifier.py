import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self, sender_email, receiver_email, smtp_server='smtp.gmail.com', port=587):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.smtp_server = smtp_server
        self.port = port

    def send_alert(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, "your_password")  # Enter your email password here
                text = msg.as_string()
                server.sendmail(self.sender_email, self.receiver_email, text)
                print(f"Alert sent to {self.receiver_email}")
        except Exception as e:
            print(f"Error: {e}")
