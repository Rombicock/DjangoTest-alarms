import requests


post = requests.post('http://127.0.0.1:8000/api/auth-token/',
                             json={'username': 'marvin',
                                   'password': '123'
                                   })
token = post.json()['token']
print(token)
get = requests.get('http://127.0.0.1:8000/api/alarms/', headers={'Authorization': token}).json()
print(get)
# token, user_id, _ = post.json().values()
# print(token, user_id)


#
# post = requests.post('http://127.0.0.1:8000/api/alarm/create/',
#                      json={'time': f'00:00:00', 'active': 'True', 'owner': user_id}
#                      )
# print(post)
# if str(post) == '<Response [500]>':
#     raise Exception('<Response [500]>')