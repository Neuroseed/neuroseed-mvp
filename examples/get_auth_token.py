import utils

user_id = input('Enter user ID: ')
token = utils.get_auth_token(user_id)
print('Token:', token)
