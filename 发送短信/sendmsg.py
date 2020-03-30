# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC577b8d009c3deca4b7e1282f709dcf94'
auth_token = 'dcc1ceb6567b3d7d2c74953acefdc55b'
client = Client(account_sid, auth_token)
message = client.messages \
                .create(
                     body="测试信息",
                     from_='+',
                     to='+'
                 )

print(message.sid)
