import imaplib
import email
import re
import time

def get_latest_otp_email(email_id, password):
    imap_host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_host)

    try:
        # Login to the mailbox
        mail.login(email_id, password)
        mail.select('inbox')

        search_criteria = '(FROM "corpsales@quickbase.com" SUBJECT "Quickbase verification code for sign in")'

        max_wait_time = 60  # seconds
        poll_interval = 5   # seconds
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            # Search for relevant emails
            result, data = mail.search(None, search_criteria)

            if result == 'OK':
                email_ids = data[0].split()
                if email_ids:
                    latest_email_id = email_ids[-1]

                    # Fetch the latest email
                    result, data = mail.fetch(latest_email_id, '(RFC822)')
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Get the plain text part
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Extract OTP
                    otp_match = re.search(r'\b[A-Z0-9]{6}\b', body)

                    if otp_match:
                        mail.logout()
                        return otp_match.group(0)

            time.sleep(poll_interval)

        print("OTP not received within 1 minute.")
        mail.logout()
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None
