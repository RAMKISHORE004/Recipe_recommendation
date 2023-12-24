#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import re
from datetime import datetime


#connecting to the Mysql workbench Database connected to AWS
try:
    conn = mysql.connector.connect(user='root', 
                               password='asdf', 
                               host='localhost', 
                               database='recipe_recomm_db', port='3303')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print('connected')
    #conn.close()
cursor = conn.cursor()

def check_profile(UserId):
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (UserId,))
    account = cursor.fetchone()
    firstname = account[1]
    lastname = account[2]
    email = account[3]
    username = account[4]
    print('---------------------------------------------')
    print('|                                           |')
    print(f'| Hi, {username}                             |')
    print(f'| First Name : {firstname}                  |')
    print(f'| Last Name  : {lastname}                   |')
    print(f'| Email      : {email}              |')
    print('|                                           |')
    print('---------------------------------------------')
    print('\n0 : To Delete your account Enter 0')
    edit_p = input('\nDo you want to edit profile? Yes Enter 1 else Enter any key to go to Home:')
    if edit_p == '1':
        print('1 : To edit firstname Enter 1')
        print('2 : To edit lastname Enter 2')
        print('3 : To edit email Enter 3')
        print('4 : To edit password Enter 4')
        print('0 : To Go to profile Enter 0')
        while(True):
            edit_op = input('Enter a Number from the above options to edit : ')
            if edit_op == '1':
                fn = input('Enter New First Name : ')
                #cursor.execute('update users SET first_name = %s Where user_id = %s',(fn,UserId,))
                #conn.commit()
                print('First Name Updated!')
            elif edit_op == '2':
                ln = input('Enter New Last Name : ')
                #cursor.execute('update users SET last_name = %s Where user_id = %s',(ln,UserId,))
                #conn.commit()
                print('Last Name Updated!')
            elif edit_op == '3':
                em = input('Enter New Email ID : ')
                #cursor.execute('update users SET email = %s Where user_id = %s',(em,UserId,))
                #conn.commit()
                print('Email ID Updated!')
            elif edit_op == '4':
                pw = input('Enter New Password : ')
                #cursor.execute('update users SET password = %s Where user_id = %s',(pw,UserId,))
                #conn.commit()
                print('Password Updated!')
            elif edit_op == '0':
                check_profile(UserId)
                return
            else:
                print('Please Enter Correct Input from the options')
    elif edit_p == '0':
        d_p = input('Do you Really want to delete the account? Yes Enter 1 or any key to go back')
        if (d_p == '1'):
            #cursor.execute('delete from users Where user_id = %s',(UserId,))
            #conn.commit()
            print('User Deleted!! :(')
        else:
            check_profile(UserId)
            return
    else:
        return
            

def recomm_diet(UserId):
    cursor.callproc('RecipeRecommUserdiet',[UserId])
    # print out the result
    for result in cursor.stored_results():
        a = result.fetchall()
    for a1 in a:
        print('-----------------------------------------------------------')
        print('Recipe Name    : ',a1[1])
        print('-----------------------------------------------------------')
        print('Steps          : ')
        for a2 in re.split("',",a1[2]):
            print('> ',a2)
        print()
        print('Serving weight : ',a1[3])
        print('Servings       : ',a1[4])
        print()

def recomm_alle(UserId):
    cursor.callproc('RecipeRecommUserAllergyFree',[UserId])
    # print out the result
    for result in cursor.stored_results():
        a = result.fetchall()
    for a1 in a:
        print('-----------------------------------------------------------')
        print('Recipe Name    : ',a1[1])
        print('-----------------------------------------------------------')
        print('Steps          : ')
        for a2 in re.split("',",a1[2]):
            print('> ',a2)
        print()
        print('Serving weight : ',a1[3])
        print('Servings       : ',a1[4])
        print()

def recomm_macro(macros):
    print(macros)
    cursor.callproc('RecipeRecommUserMacros',macros)
        # print out the result
    recipe_ids = []
    for result in cursor.stored_results():
        a = result.fetchall()
        
    ids = [a[0][2],a[1][2],a[2][2]]
    
    for i in ids:
        cursor.execute('SELECT name,steps,servings FROM recipe WHERE recipe_id = %s', (i,))

        res = cursor.fetchone()
        recipeName = res[0]
        steps = res[1]
        servings = res[2]
        
        print(f"Recipe Name: {recipeName},\nSteps: {steps},\nNumber of servings: {servings}")
    
        
        
#     for a1 in a:
#         print('-----------------------------------------------------------')
#         print('Recipe Name    : ',a1[1])
#         print('-----------------------------------------------------------')
#         print('Steps          : ')
#         for a2 in re.split("',",a1[2]):
#             print('> ',a2)
#         print()
#         print('Serving weight : ',a1[3])
#         print('Servings       : ',a1[4])
#         print()

def logRecipeSelection(recipe_name,username):
    
    
    cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
    account = cursor.fetchone()
    userId = account[0]
    
    cursor.execute('SELECT recipe_id FROM recipe WHERE name = %s', (recipe_name,))
    account = cursor.fetchone()
    recipeId = account[0]
    
    
    cursor.callproc('CalculateTotalCostAndLeastCostForRecipe',[recipeId])
    
    
    a,b,c = cursor.stored_results()
    
    storeId_totalCost = a.fetchall()
    ingredient_leastCost = b.fetchall()
    leastCost = c.fetchall()
    
    
    sorted_storeId_totalCost = sorted(storeId_totalCost, key=lambda x: x[1], reverse=True)
    
    largest_store_cost = sorted_storeId_totalCost[0][1]
    optimizedCost = leastCost[0][0]
    
    savingsPercent = ((largest_store_cost-optimizedCost)/largest_store_cost)*100
    
    # Displaying money I will save if I bought x ingre from y store
    
    print(f'You will save {savingsPercent:.2f}% if you buy the following ingredients from the following stores: ')
    print()
    
    for (ingredient_id,store_id) in ingredient_leastCost:
        cursor.execute('SELECT name FROM ingredient WHERE ingredient_id = %s', (ingredient_id,))
        rec = cursor.fetchone()
        ingredientName = rec[0]
        
        cursor.execute('SELECT name,web_link FROM online_store WHERE store_id = %s', (store_id,))
        rec = cursor.fetchone()
        
        print(f"Buy {ingredientName} from {rec[0]}. Link: {rec[1]}")
    
    # Log the result in user_recipe_log
    #specific_datetime = datetime(2022, 1, 2, 1, 30, 0)
    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('INSERT INTO user_recipe_log (user_id,recipe_id,date_time,savings_percent) VALUES (%s, %s, %s,%s)', (userId, recipeId, formatted_datetime, savingsPercent))
    conn.commit()
    
while(True):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@                                                   @")
    print("@      WELCOME TO RECIPE RECOMMENDATION SYSTEM      @")
    print("@                                                   @")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("#############                          ##############")
    print()
    print("If you are a New User Create an Account :), to Create an Account Enter 1")
    print()
    print("If you are a Existing User, to Login Enter 2 ")
    print()
    print("To logout or end Enter 0 or quit ")
    print()
    print("===========================================================")
    print("||  Enter # 1 # to Login or # 2 # to Create New Account  ||")
    print("===========================================================")

    session = {}
    acc = input("Enter >>1 to Login or >>2 to Create New Account")
    if(acc == '1'):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[-2]
            print("Login Successfully!!")
            print()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("@                                                   @")
            print(f" @                WELCOME {session['username']}               @")
            print("@                                                   @")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("#############                          ##############")
            
            while(True):
                print('1 : Do you Want to check your Profile: Enter 1')
                print('2 : Do you Want Recommendation that relates your Diet preference : Enter 2')
                print('3 : Do you Want Recommendation that relates your Allergies : Enter 3')
                print('4 : Do you Want Recommendation with macro preferences : Enter 4')
                print('5 : Do you want to select Recipe : Enter 5')
                print('0 : Do you Want LogOut : Enter 0')
                after_login = input("Enter from about list ")
                if after_login == '1':
                    print('Your profile!')
                    check_profile(session['id'])
                elif after_login == '2':
                    print('Recommendation Diet prefernce')
                    recomm_diet(session['id'])
                elif after_login == '3':
                    print('Recommendation Allergy')
                    recomm_alle(session['id'])
                elif after_login == '4':
                    macros_str = input('Enter macros as (calories,protein,carbs,fats): ')
                    macors_str_list = macros_str.split(",")
                    macros_int_list = list(map(int, macors_str_list))
                    print()
                    print('Recommendation macro preference')
                    recomm_macro(macros_int_list)
                elif after_login == '5':
                    recipe_name = input('Enter recipe name: ')
                    logRecipeSelection(recipe_name,username)
                    print('Enjoy :)')
                    print()
                elif after_login == '0':
                    print('Logging out...')
                    exit()
                else:
                    print('Enter Correct input')
        else:
            print('Incorrect Username/Password! Please Enter again')
            print()
    elif(acc == '2'):
        firstname = input("Enter First Name: ")
        lastname = input("Enter last Name: ")
        while(True):
            username = input("Enter Username: ")
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                print('Account already exists! Please Enter other User name')
                print()
            elif not re.match(r'[A-Za-z0-9]+', username):
                print('Username must contain only characters and numbers!')
                print()
            else:
                break
        while(True):
            password = input("Enter Password: ")
            if not re.match(r'[A-Za-z0-9]+', password):
                print('password must contain only characters and numbers!')
                print()
            else:
                break
        while(True):
            email = input("Enter Email ID: ")
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                print('Invalid email address format!')
                print()
            else:
                break
            
        # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
        #cursor.execute('INSERT INTO users(first_name, last_name, email, username, password) VALUES (%s, %s, %s,%s,%s)', (firstname, lastname, email, username, password,))
        #conn.commit()
        print("\nRegistered!! Account created Successfully! You can add your diet prefernce and allergies if any")
        
        cursor.execute('select prefer_id, name,description from dietry_prefer')
        records = cursor.fetchall()
        i=1
        for row in records:
            print(i,' : ',row[1],'--',row[2])
            i=i+1
        print('\n0 : No diet Prefernce')
        while(True):
            try:
                diet_prefer = input('\nEnter respective number for any Diet prefernce you require from above list')
                if(int(diet_prefer)>=i or int(diet_prefer)<0):
                    print('\nEnter Respective Number from the List')
                    continue
                elif(diet_prefer == '0'):
                    print('\nYou prefered No Diet preference ')
                    break
                else:
                    print('\nYou prefered diet preference : ', records[int(diet_prefer)-1][1])
            except:
                print('\nEnter Respective Number from the List')
                continue
            d_y = input('\nDo you want to continue with this diet prefernce Yes Enter any key to Continue or Do you want to change Preference Enter 1:')
            if(d_y != '1'):
                if(diet_prefer == '0'):
                    break
                #cursor.execute('select user_id from users where username = %s',username)
                #userId = cursor.fetchone()
                #cursor.execute('INSERT INTO user_dietry_prefernce(user_id, prefer_id) VALUES (%s, %s)', (userId,records[int(diet_prefer)-1][0],))
                print('\nYour Diet Prefernce added!!')
                d_a_o = input("\nDo you want to add any other diet prefernce? Yes Enter 1 else Enter any key to Continue:")
                if(d_a_o != '1'):
                    break
        cursor.execute('select allergy_id, name,description from allergy')
        records = cursor.fetchall()
        i=1
        for row in records:
            print(i,' : ',row[1],'--',row[2])
            i=i+1
        print('\n0 : No Allergy')
        while(True):
            try:
                alergy = input('\nEnter respective number for any Allergy you require from above list')
                if(int(alergy)>=i or int(alergy)<0):
                    print('\nEnter Respective Number from the List')
                    continue
                elif(alergy== '0'):
                    print('\nYou prefered No Allergy ')
                else:
                    print('\nYou prefered Allergy : ', records[int(alergy)-1][1])
            except:
                print('\nEnter Respective Number from the List')
                continue
            d_y = input('\nDo you want to continue with this Allergy Yes Enter any key to Continue or Do you want to change Preference Enter 1:')
            if(d_y != '1'):
                if(alergy == '0'):
                    break
                #cursor.execute('select user_id from users where username = %s',username)
                #userId = cursor.fetchone()
                #cursor.execute('INSERT INTO user_allergy(user_id, allergy_id) VALUES (%s, %s)', (userId,records[int(alergy)-1][0],))
                print('\nYour Allergy added!!')
                d_a_o = input("\nDo you want to add any other Allergy ? Yes Enter 1 else Enter any key to Continue:")
                if(d_a_o != '1'):
                    break
    elif(acc == '0' or acc == 'quit'):
        print("\nYou are logged out")
        exit()
    else:
        print("\nPlease Enter Correct Input")
        print()
        continue


# 
