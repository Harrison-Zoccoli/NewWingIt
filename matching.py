from datetime import date, time, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class UserData:
    def __init__(self, email: str, name: str, date_value: date, time_value: time):
        self.email = email
        self.name = name
        self.date = date_value
        self.time = time_value

    def __repr__(self):
        return f"UserData(email='{self.email}', name='{self.name}', date={self.date}, time={self.time})"


def send_match_email(user1, user2):
    """Send email to both users about their match"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "wingittestacc@gmail.com" 
    app_password = "fmzy grbs mpgx aoqx" 

    # Creates message template
    def create_email_message(recipient, other_user):
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient.email
        message["Subject"] = "Wingit Found You An Uber Match!"

        body = f"""
        Hello {recipient.name},

        We found a match for your Uber ride!

        Match Details:
        - Date: {recipient.date}
        - Your Time: {recipient.time}
        - Matched with: {other_user.name}
        - Their Time: {other_user.time}

        You can contact them at: {other_user.email}

        Have a great trip!
        """

        message.attach(MIMEText(body, "plain"))
        return message

    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)

        # Send emails to both users
        server.send_message(create_email_message(user1, user2))
        server.send_message(create_email_message(user2, user1))

        server.quit()
        print(f"Match notification emails sent to {user1.email} and {user2.email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")



##functions for checking if dates and times match and diff in time
def calculate_time_difference_minutes(time1, time2):
    """Calculate the difference between two times in minutes"""
    time1_minutes = time1.hour * 60 + time1.minute
    time2_minutes = time2.hour * 60 + time2.minute
    return time1_minutes - time2_minutes

def are_times_compatible(time1, time2):
    """Check if two times are within acceptable range (30 min before to 45 min after)"""
    diff = calculate_time_difference_minutes(time1, time2)
    return -30 < diff < 45

def are_dates_same(date1, date2):
    """Check if two dates are the same"""
    return date1 == date2

def find_matches(current_user, all_users):
    """Find compatible travel matches for the current user"""
    compatible_matches = []
    users_to_remove = set()  # Use a set to avoid duplicates
    
    for potential_match in all_users:
        # Don't match users with themselves
        if current_user.email == potential_match.email:
            continue
            
        if are_dates_same(current_user.date, potential_match.date) and \
           are_times_compatible(current_user.time, potential_match.time):
            compatible_matches.append((current_user, potential_match))
            users_to_remove.add(current_user)
            users_to_remove.add(potential_match)
            send_match_email(current_user, potential_match)
    
    # Remove matched users from the travelers list
    for user in users_to_remove:
        if user in all_users:
            all_users.remove(user)
    
    return compatible_matches

