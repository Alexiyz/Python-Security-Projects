import pandas as pd
import win32com.client as win32

'''
content.txt: first line is the email's subject, rest is the content.
recipients.xlsx: table with recipients and a sent attribute
'''


def send_outlook_email(auto=False):
    # Read subject and content from content.txt
    try:
        with open("content.txt", "r") as file:
            lines = file.readlines()
            subject = lines[0].strip()  # First line as subject
            content = ''.join(lines[1:])  # Remaining lines as content
    except FileNotFoundError:
        print("Error: 'content.txt' file not found.")
        return

    # Read recipients from recipients.xlsx
    try:
        df = pd.read_excel("recipients.xlsx")
    except FileNotFoundError:
        print("Error: 'recipients.xlsx' file not found.")
        return

    # Find the first recipient without "sent" attribute
    unsent_row = df[df['sent'].isna()].head(1)
    if unsent_row.empty:
        print("All recipients have already been sent emails.")
        return

    recipient_email = unsent_row.iloc[0]['email']

    # Set up the Outlook application
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient_email
    mail.Subject = subject
    mail.Body = content

    if auto:
        # Send the email and update the Excel sheet to mark as sent
        mail.Send()
        print(f"Email sent to {recipient_email}")
        df.loc[unsent_row.index, 'sent'] = "Yes"  # Mark as sent
        df.to_excel("recipients.xlsx", index=False)  # Save changes to the file
    else:
        # Display the email draft
        mail.Display()
        print(f"Email draft created for {recipient_email}")

# Example usage:
# send_outlook_email(auto=True)  # This will send the email
# send_outlook_email(auto=False) # This will only display the draft

send_outlook_email(auto=True)

