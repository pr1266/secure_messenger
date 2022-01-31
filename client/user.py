from client import *
import vals
import requests
from os import system
import time

def contact_page():
    
    system('cls')
    print(f'user : {vals.USERNAME}\n\n')
    username = vals.USERNAME
    # for i in range(100):
    r = requests.post(url = vals.URL + 'get_my_contact/', headers = vals.header, data = {'username': username}).json()

    contact_list = set()
    if(len(r) > 0):
        for i in r:
            if i['sender'] != username:
                contact_list.add(i['sender'])
            if i['reciever'] != username:
                contact_list.add(i['reciever'])
        chat_array = []
        contact_list = list(contact_list)
        for i in range(len(contact_list)):
            chat_list = []
            for j in range(len(r)):
                if(r[j]['sender'] == contact_list[i]):
                    chat_list.append(r[j])
                if(r[j]['reciever'] == contact_list[i]):
                    chat_list.append(r[j])
            content = {
                'id' : str(contact_list[i]),
                'content' : chat_list
            }
            chat_array.append(content)

        for i in range(len(contact_list)):
            print(f'{i+1} . {contact_list[i]} \n')

        n = len(contact_list)
        print('choose contact to see the chat list')
        print('to start a new chat with a new user please enter s or leave it blank to go back\n')
        choice = input('')

        if choice == 's':
            new_chat()
        if choice == '':
            main_page()
        else:
            if int(choice) > n:
                print('invalid user index')
                time.sleep(1)
                contact_page()
            else:
                chat_page(chat_array[int(choice)-1])
    else:
        print('to start a new chat with a new user please enter s\n')
        choice = input('')

        if choice == 's':            
            new_chat()
        else:
            contact_page()

def chat_page(chat_list):
    system('cls')
    print(f'user : {vals.USERNAME}\n\n')
    chats = chat_list['content']
    target_user = chat_list['id']
    for index, i in enumerate(chats):
        
        print('\n\n')
        print(f'{index+1}.')
        sender = i['sender']
        reciever = i['reciever']
        content = i['content']

        print(f'sender : {sender}')
        print(f'reciever : {reciever}')
        print(f'message : {content}')
        print('\n\n')
    message = input('please enter your message or leave it blank to go back\n\n')
    send_message_user_url = vals.URL + 'send_message/'
    if(message == ''):
        contact_page()
    else:
        data = {
            'sender': vals.USERNAME,
            'reciever': target_user,
            'content': message
        }        
        r = requests.post(url = send_message_user_url, data = data, headers = vals.header).json()
        print('message sent successfuly')
        time.sleep(1)
        contact_page()

def new_chat():

    system('cls')
    target_username = input('please enter the username of contact that you want to send message\n')
    message_content = input('please enter content of your message\n')    
    data = {
        'sender': vals.USERNAME,
        'reciever': target_username,
        'content': message_content
    }
    send_message_user_url = vals.URL + 'send_message/'
    r = requests.post(data = data, url = send_message_user_url, headers = vals.header).json()
    if 'id' in r.keys():
        print('message sent successfuly')
        time.sleep(1)
        contact_page()
    else:
        print('something went wrong, please try again')
        time.sleep(1)
        contact_page()