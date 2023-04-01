from twilio.rest import Client

def send_sms(to, body):
    # Your Account SID from twilio.com/console
    account_sid = "AC7d2af154b87eaafe6becc0ad7ed43143"
    # Your Auth Token from twilio.com/console
    auth_token  = "756fe374adc33489f4384452eb380c23"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to, 
        from_="+15855950316",
        body=body)

    print(message.sid)