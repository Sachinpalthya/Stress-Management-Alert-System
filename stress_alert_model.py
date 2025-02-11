import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Button, messagebox

# Step 1: Load and Preprocess Data
df = pd.read_csv('data.csv')

# Debug: Check the columns in the dataset
print("Columns in the dataset:", df.columns)

# Validate required columns
required_columns = ['mood', 'engagement', 'stress_level', 'task_completion', 'response_time']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

df['mood'] = df['mood'].map({'Happy': 0, 'Neutral': 1, 'Sad': 2})
df['engagement'] = df['engagement'].map({'Engaged': 0, 'Disengaged': 1})

X = df[['stress_level', 'mood', 'engagement', 'task_completion', 'response_time']]
y = df['stress_level']

# Step 2: Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 3: Evaluate the Model
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Step 4: Email Notification Logic
def send_email_alert(employee_id, stress_level):
    sender_email = "sachinpalthya45@gmail.com"
    sender_password = "nwiq rite utph rxpa"  # Use an app password for Gmail
    receiver_email = "palthyasachin45@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Stress Alert for Employee {employee_id}"

    body = f"Employee {employee_id} has reached a stress level of {stress_level}. Please review the situation."
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Alert sent for Employee {employee_id}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Step 5: Create the GUI (Tkinter)
def check_stress():
    try:
        stress_level = int(stress_entry.get())
        if stress_level > 7:  # Threshold for high stress
            employee_id = "E001"  # Example employee ID
            messagebox.showwarning("Stress Alert", "Employee stress level is high! Sending alert...")
            send_email_alert(employee_id, stress_level)
        else:
            messagebox.showinfo("Stress Level", "Stress level is normal.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid stress level (1-10).")

root = Tk()
root.title("Stress Management Dashboard")

Label(root, text="Enter Stress Level (1-10):").pack(pady=5)
stress_entry = Entry(root)
stress_entry.pack(pady=5)

Button(root, text="Check Stress", command=check_stress).pack(pady=10)

root.mainloop()
# Loop through the dataset and check the stress level for each employee
for index, row in df.iterrows():
    employee_id = row['employee_id']  # Assuming you have an 'employee_id' column in your dataset
    stress_level = row['stress_level']  # Assuming stress_level column exists
    if stress_level > 7:  # Threshold for high stress
        send_email_alert(employee_id, stress_level)
