from twilio.rest import Client

def send_sms(to, body):
    # Your Account SID from twilio.com/console
    account_sid = "AC7d2af154b87eaafe6becc0ad7ed43143"
    # Your Auth Token from twilio.com/console
    auth_token  = "07aecfd3b2932cb27434bed199e3060e"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to, 
        from_="+15855950316",
        body=body)

    print(message.sid)