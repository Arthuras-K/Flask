import requests

response = requests.post('http://127.0.0.1:5000/users', \
                                json={'username': "Olga5", \
                                    'email': 'lal5@yandex.ru', \
                                    'password': 'rtrtrt'})

print('# '*40)
print(response.status_code)
print(response.json())
print('# '*40)