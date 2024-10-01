import requests

response = requests.post('http://127.0.0.1:5000/jwt-confirm/', )

response2 = requests.get('http://127.0.0.1:5000/jwt-confirm/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1vdGNoZWxsb0BnbWFpbC5jb20iLCJleHAiOjE3MDgyMzg5MzF9.nQ1WHY7kbXx7U42wf9SWNdd6iFVFLmL-z110OyLX3xI', )

# {{ url_for('reset_password', token=token, _external=True) }}

# print(response)
# print(response2)
# print(response2.content)
print(response2.headers)
# print(response2.cookies)