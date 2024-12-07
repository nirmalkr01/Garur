from twilio.rest import Client

account_sid = 'ACe3e4e904dfbbee3eef624cb8e998864b'
auth_token = '42bbf2741420d1ec68c73d4171ab8051'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13202686290',
  to='+919508671771'
)

print(message.sid)