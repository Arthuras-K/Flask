import requests

response = requests.post('http://127.0.0.1:5000/users',
                                json={'username': "Popa",
                                    'email': 'pukpuk@yandex.ru', 
                                    'password': 'qwerzxcvAc6ll&bnm'})

# response = requests.post('http://127.0.0.1:5000/ads',
#                                 json={'title': "baby me",
#                                     'description': 'lnb fofof tyum', 
#                                     'user_id': '46'})

#response = requests.delete('http://127.0.0.1:5000/users/46', headers={"token": 'qwerzxcvAc6ll&bn'})

#response = requests.get('http://127.0.0.1:5000/users/46')
#response = requests.get('http://127.0.0.1:5000/users/38')

print()
print(response.status_code)
print(response.json())
print()