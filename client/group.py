
from os import system
import time
import requests
import vals
# from client import main_page
from user import *

def main_page():

    system('cls')
    print('Main Page\n\n')
    print(f'user : {vals.USERNAME}\n')
    print('1 . contacts\n')
    print('2 . groups\n\n')
    choice = input('choose a choice\n')
    if choice == '1':
        contact_page()
    if choice == '2':
        group_page()

def group_page():

    system('cls')
    print(f'user : {vals.USERNAME}\n\n')
    get_group_list_url = vals.URL + 'my_groups/'    
    r = requests.get(url = get_group_list_url, headers = vals.header).json()
    for index, i in enumerate(r):
        print(f'{index+1}.')
        group_id = i['group']
        print(f'Group ID : {group_id}')
        print('\n\n')

    n = len(r)
    print('choose group to see the chat list')
    print('to create a new group please enter s or leave it blank to go back\n')
    choice = input('')

    if(choice == 's'):
        create_group()
    if(choice == ''):
        main_page()
    elif int(choice) > n:
        print('invalid user index')
        time.sleep(1)
        group_page()

    else:
        group_details(r[int(choice)-1])

def create_group():
    
    create_group_url = vals.URL + 'creategroup/'
    data = {
        'owner': vals.USERNAME
    }

    r = requests.post(data = data, headers = vals.header, url = create_group_url).json()
    g_id = r['id']

    data = {
        'user': vals.USERNAME,
        'group': g_id,
        'biba': True,
        'blp': True,
        'delete_permission': True
    }

    r = requests.post(url = vals.URL + vals.add_permission_url, data = data, headers = vals.header).json()
    print(r)
    print('Group Created Successfuly\n')
    time.sleep(1)    
    while True:
        system('cls')
        username = input('enter id of user to add in group\nleave it blank if you want to stop adding to group\n')
        if(username == ''):
            break
        biba_access = int(input('enter biba access of user to add in group, 0 for false and 1 for true\n'))
        blp_access = int(input('enter blp access of user to add in group, 0 for false and 1 for true\n'))
        delete_permission = int(input('enter delete permission of user to add in group, 0 for false and 1 for true\n'))

        data = {
            'user': username,
            'biba': bool(biba_access),
            'blp': bool(blp_access),
            'delete_permission': bool(delete_permission),
            'group': g_id
        }

        r = requests.post(url = vals.URL + vals.add_permission_url, data = data, headers = vals.header).json()
        print(r)

    group_page()

def group_details(g_content):
    message_list = []
    system('cls')
    print(f'user : {vals.USERNAME}\n')
    g_id = g_content['group']    
    get_user_url = vals.URL + f'get_group_users/{g_id}'

    r = requests.get(url = get_user_url, headers = vals.header).json()
    print("\nGroup Users : ")
    for index, i in enumerate(r):        
        user = i['user']
        print(f'{index+1}. {user}')
    print('--------------------------------')
    is_admin_url = vals.URL + 'is_admin/'
    data = {
        'group': g_id
    }
    r = requests.post(url = is_admin_url, data = data, headers = vals.header).json()
    if(r == True):
        get_group_message_url = vals.URL + f'get_group_message/{g_id}/'      
        r = requests.get(url = get_group_message_url, headers = vals.header).json()
        for index, i in enumerate(r):
            print('\n\n')
            print(f'{index+1}. ')
            message = i['message']
            sender = i['user']
            print(f'sender : {sender}')
            print(f'message : {message}')
            message_list.append(i['id'])
        print('\n\n')
        print('you are admin of group, to add users in groud enter "ADD"\nto delete a message enter "DEL"\nto send message enter the content of your message or leave it blank to go back')
        choice = input()
        if(choice == ''):
            group_page()
        elif(choice == "DEL"):
            print('please enter the index of message to delete')
            index = int(input())
            if index > len(message_list):
                group_details(g_content)
            else:
                #! inja api delete
                delete_url = vals.URL + f'group_message/{message_list[index-1]}/delete/'
                r = requests.delete(url = delete_url, headers = vals.header)
                group_page()
        elif(choice) == 'ADD':
            while True:
                system('cls')
                username = input('enter id of user to add in group\nleave it blank if you want to stop adding to group\n')
                if(username == ''):
                    break
                biba_access = int(input('enter biba access of user to add in group, 0 for false and 1 for true\n'))
                blp_access = int(input('enter blp access of user to add in group, 0 for false and 1 for true\n'))
                delete_permission = int(input('enter delete permission of user to add in group, 0 for false and 1 for true\n'))

                data = {
                    'user': username,
                    'biba': bool(biba_access),
                    'blp': bool(blp_access),
                    'delete_permission': bool(delete_permission),
                    'group': g_id
                }

                r = requests.post(url = vals.URL + vals.add_permission_url, data = data, headers = vals.header).json()
                print(r)

            group_page()
        else:
            send_message_to_group_url = vals.URL + 'send_group_message/'            
            data = {
                'message': choice,
                'user': vals.USERNAME,
                'group': g_id
            }
            r = requests.post(data = data, headers = vals.header, url = send_message_to_group_url).json()
            group_page()

    else:
        g_biba = g_content['biba']
        g_blp = g_content['blp']
        g_del = g_content['delete_permission']        
        if g_blp == True:
            get_group_message_url = vals.URL + f'get_group_message/{g_id}/'
            r = requests.get(url = get_group_message_url, headers = vals.header).json()
            for index, i in enumerate(r):
                print('\n\n')
                print(f'{index+1}. ')
                message = i['message']
                sender = i['user']
                print(f'sender : {sender}')
                print(f'message : {message}')
                message_list.append(i['id'])
        else:
            print('\n\n')
            print('--------------------------------------------------------')
            print('You Dont Have BLP Access so you cant read group_messages')
            print('--------------------------------------------------------')
            print('\n\n')

        if g_biba == True:
            if g_del == False:
                print('\n\n')
                message = input('enter your message to send to group or leave it blank to get back\n')
                if(message == ''):
                    group_page()
                else:                
                    send_message_to_group_url = vals.URL + 'send_group_message/'
                    data = {
                        'message': message,
                        'user': vals.USERNAME,
                        'group': g_id
                    }
                    r = requests.post(data = data, headers = vals.header, url = send_message_to_group_url).json()
                    group_page()
            else:
                print('\n\n')
                message = input('enter your message to send to group or leave it blank to get back and for delete a message enter "DEL"\n')
                if(message == ''):
                    group_page()
                elif(message == 'DEL'):
                    print('please enter the index of message to delete it')
                    index = int(input())
                    if index > len(message_list):
                        group_details(g_content)
                    else:
                        #! inja api delete call she :
                        delete_url = vals.URL + f'group_message/{message_list[index-1]}/delete/'
                        r = requests.delete(url = delete_url, headers = vals.header)
                        group_page()
                else:                
                    send_message_to_group_url = vals.URL + 'send_group_message/'
                    data = {
                        'message': message,
                        'user': vals.USERNAME,
                        'group': g_id
                    }
                    r = requests.post(data = data, headers = vals.header, url = send_message_to_group_url).json()
                    group_page()
        else:
            if g_del == True:
                print('\n\n')
                print('-------------------------------------------------------------')
                print('You Dont Have Biba Access so you cant send a message to group')                
                print('to delete a message enter "DEL" and to go back leave it blank')
                print('-------------------------------------------------------------')
                choice = input()
                if(choice == "DEL"):
                    print('please enter index of message to delete')
                    index = int(input(""))
                    if index > len(message_list):
                        group_details(g_content)
                    else:
                        #! inja api delete call she
                        delete_url = vals.URL + f'group_message/{message_list[index-1]}/delete/'
                        r = requests.delete(url = delete_url, headers = vals.header)
                        group_page()
                if(choice == ""):
                    group_page()            
            else:
                print('\n\n')
                print('-------------------------------------------------------------')
                print('You Dont Have Biba Access so you cant send a message to group')
                print('please press any key to get back')
                print('-------------------------------------------------------------')
                input()
                group_page()