import os
from os import system
import time
import requests

import vals
from auth import *
from user import *
from group import create_group, group_page, group_details

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
               
def first_page():
    system('cls')
    print("choose a choice")
    print("1 . login")
    print("2 . signup")
    choice = input()
    
    if(choice == '1'):
        login_result = login()
        if login_result == True:
            main_page()
        else:
            first_page()
    else:
        signup_result = sign_up()
        if signup_result == True:
            main_page()
        else:
            first_page()

def main():
    
    first_page()

if __name__ == "__main__":

    main()