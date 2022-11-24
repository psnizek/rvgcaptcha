import smtplib, ssl

context = ssl.create_default_context()
port = 465
sender = 'contactform@ravegroup.cz'
receivers = 'psnizek@ravegroup.cz'
smtp_password = 'TmX.921972'

message = "From: RVG Contact Form <contactform@ravegroup.cz> \n"
message = message + "To: Peter Snizek <psnizek@ravegroup.cz> \n"
message = message + "Subject: SMTP e-mail test \n\n"
message = message + "This is the test e-mail message block"

with smtplib.SMTP_SSL('smtp.hostinger.com', port, context=context) as server:
    server.login("contactform@ravegroup.cz", smtp_password)
    server.sendmail(sender, receivers, message)
    print("Successfully sent email")
