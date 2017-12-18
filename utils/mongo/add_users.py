import sys
import json
import pymongo
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# roles:
# read, readWrite
# dbAdmin, dbOwner, userAdmin,
# readAnyDatabase, readWriteAnyDatabase
# userAdminAnyDatabase, dbAdminAnyDatabase

USERS = {
    'admin': {
        'username': 'admin',
        'password': 'admin',
        'roles': ['userAdminAnyDatabase']
    },
    'writer': {
        'username': 'writer',
        'password': 'writer',
        'roles': ['readWriteAnyDatabase']
    },
    'reader': {
        'username': 'reader',
        'password': 'reader',
        'roles': ['readAnyDatabase']
    }
}


def get_config():
    with open('metadata_config.json') as f:
        config = json.load(f)

    return config


def check_connection(client):
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print('Mongo server connection established')
    except ConnectionFailure:
        print('Mongo server not available')
        sys.exit()


def test_users(client, users):
    print('Test users')
    for user in users:
        data = users[user]
        name = data['username']
        password = data['password']

        client.admin.logout()

        client.admin.authenticate(name, password)
        print('User:', name)

        # get name
        try:
            client.admin.name
            print('\tRead ok.')
        except Exception as e:
            print('\tRead fail:', type(e))

        # insert
        try:
            test_document = {'test': True}
            client.test.test.insert(test_document)
            print('\tInsert ok.')
        except Exception as e:
            print('\tInsert fail:', type(e))


def create_users(client, users):
    print('Create users')

    for user in users:
        data = users[user]
        name = data['username']
        password = data['password']
        roles = data['roles']
        try:
            client.admin.add_user(name, password, roles=roles)
            print('User created:', name)
        except OperationFailure as e:
            print('Add user fail:', e)
            sys.exit()


def main(admin=None, password=None):
    config = get_config()
    url = config['mongo_url']
    connect_timeout = config.get('connect_timeout', 3000)
    selection_timeout = config.get('selection_timeout', 3000)
    users = config.get('users', USERS)

    client = pymongo.MongoClient(
        url,
        connectTimeoutMS=connect_timeout,
        serverSelectionTimeoutMS=selection_timeout)
    # username=username, password=password)
    # client.database.authenticate(name, password)

    check_connection(client)

    if admin and password:
        client.admin.authenticate(admin, password)

    create_users(client, users)

    test_users(client, users)


if __name__ == '__main__':
    #main()
    main('admin', 'admin')
