
from os import system
import vals
import getpass
import requests
import time

def login():

    system('cls')
    username = input("enter your user name\n")
    password = getpass.getpass(prompt = "enter your password\n")

    data = {
        'username': username,
        'password': password
    }

    r = requests.post(data = data, url = vals.login_url).json()
    if 'token' in r.keys(): 
        token = r['token']        
        vals.header = {'Authorization': 'JWT {}'.format(token)}        
        vals.USERNAME = username
        system('cls')
        print('login successful')
        time.sleep(1)
        return True
    else:
        for i in range(3, 0, -1):
            system('cls')
            print(f'username or password is wrong please try again in {i}')
            time.sleep(1)           
            system('cls')
        vals.header = None
        return False

def sign_up():

    system('cls')
    username = input("enter your user name\n")
    password = getpass.getpass(prompt = "enter your password\n")
    if len(password) < 4:
        system('cls')
        print('password must be at least 4 characters')
        time.sleep(1)
        first_page()
    else:
        system('cls')
        data = {
            'username': username,
            'password': password,
            'is_active': True
        }
        r = requests.post(data = data, url = vals.signup_url).json()
        if 'username' in r.keys():
            print('signed up successfuly')
            time.sleep(1)
            r = requests.post(data = data, url = vals.login_url).json()
            token = r['token']
            vals.header = {'Authorization': 'JWT {}'.format(token)}
            vals.USERNAME = username
            for i in range(3, 0, -1):
                system('cls')
                print(f'redirect to main page in {i} seconds')
                time.sleep(1)
            system('cls')
            return True
        else:
            for i in range(3, 0, -1):
                system('cls')
                print(f'cannot register with provided information, please try again in {i} seconds')
                time.sleep(1)
            system('cls')
            return False