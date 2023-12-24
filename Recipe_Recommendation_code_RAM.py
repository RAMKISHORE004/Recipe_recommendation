import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import re
import matplotlib.pyplot as plt

"""
#connecting to the Mysql workbench Database connected to AWS
try:
    conn = mysql.connector.connect(user='admin', 
                               password='ProjectPwd3#', 
                               host='database-1.c4v6idmg4tyl.us-east-2.rds.amazonaws.com', 
                               database='recipe_db')
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
"""

try:
    conn = mysql.connector.connect(user='root', 
                               password='Ram@12345', 
                               host='localhost', 
                               database='recipe_recom')
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
            exit()
        else:
            check_profile(UserId)
            return
    else:
        return


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

def check_recipe(a,i,UserId):
    for a1 in a:
        #print(i,a1[-1])
        if a1[-1] == i:
            print('===========================================================')
            print('Recipe Name    : ',a1[1])
            print('===========================================================')
            print('Steps          : ')
            print('-----------------------------------------------------------------')
            for a2 in re.split("',",a1[2]):
                print('>> ',a2)
            print('-----------------------------------------------------------------')
            print()
            print('Serving weight : ',a1[3])
            print('Servings       : ',a1[4])
            print()
            nut_i = input('To check nutritional info Per serving, Yes Enter 1 or else Enter any Key : ')
            if(nut_i == '1'):
                data = np.array([a1[7],a1[8],a1[9]])
                labels = ['fats per serving', 'carbs per serving', 'protein per serving']
                plt.pie(data, labels=labels, autopct="%1.1f%%")
                plt.title(f"{a1[1]}\n Pie Chart for calories per serving : {a1[6]}")
                plt.show()
                con_i = input('To continue press any key?')
                
            nut_i = input('Do you want to check other reviews on Recipe, Yes Enter 1 or else Enter any Key : ')
            if(nut_i == '1'):

                cursor.execute("SELECT rating FROM recipe_recom.user_recipe where recipe_id = %s",a1[0])
                rec = pd.DataFrame(cursor.fetchall())
                dups = rec.pivot_table(index = [0], aggfunc ='size')
                print(list(dups.index))
                print(list(dups.values))
                rat = list(dups.index)
                cou = list(dups.values)
                fig = plt.figure(figsize = (10, 5))
                 
                # creating the bar plot
                plt.bar(rat, cou,  width = 0.5)
                 
                plt.xlabel("Rating")
                plt.ylabel("No. of Users")
                plt.title("Rating for Recipe : ")
                plt.show()
                con_i = input('To continue press any key?')
                
                
            print("Do you want to rate Recipe : ", a1[1])
            rate_rec = input('Enter 1 to Rate Recipe, Enter Any Key to go Back')
            if(rate_rec == '1'):
                while(True):
                    rat = input("Enter Rating from 0 to 5 : ")
                    try:
                        rat = int(rat)
                        if(rat>5 or rat<0):
                            print("Enter Rating Between the range")
                        else:
                            break
                    except:
                        print("Please enter Rating correctly")
                
                review = input("Enter Review:")
                print("Thank you for the Review and Rating")
                #cursor.execute('INSERT INTO user_recipe(fuser_id, recipe_id, review, rating) VALUES (%s, %s, %s,%s)', (UserId, a1[0], review, rating,))
                #conn.commit()
            else:
                return


def recomm_diet(UserId):
    cursor.callproc('RecipeRecommUserdiet',[UserId])
    # print out the result
    for result in cursor.stored_results():
        a = result.fetchall()
    i = 1
    print('-----------------------------------------------------------')
    
    for a1 in a:
        print(i,'. Recipe Name    : ',a1[1])
        print('-----------------------------------------------------------')
        a1 += (i,)
        a[i-1]=a1
        i=i+1
        
    while(True):
        rec_sel = input('Enter Number with respect to Recipe to check Steps Or Enter 0 to go Home: ')
        try:
            rec_sel = int(rec_sel)
            if(rec_sel<0 or rec_sel >=i):
                print('Please Enter correct Input')
                continue
            elif rec_sel == 0:
                return
            else:
                check_recipe(a,rec_sel,UserId)
        except:
            print('Please Enter correct Input')
            continue
        
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
    i = 1
    print('-----------------------------------------------------------')
    
    for a1 in a:
        print(i,'. Recipe Name    : ',a1[1])
        print('-----------------------------------------------------------')
        a1 += (i,)
        a[i-1]=a1
        i=i+1
        
    while(True):
        rec_sel = input('Enter Number with respect to Recipe to check Steps Or Enter 0 to go Home: ')
        try:
            rec_sel = int(rec_sel)
            if(rec_sel<0 or rec_sel >=i):
                print('Please Enter correct Input')
                continue
            elif rec_sel == 0:
                return
            else:
                check_recipe(a,rec_sel,UserId)
        except:
            print('Please Enter correct Input')
            continue
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
        

while(True):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@                                                   @")
    print("@      WELCOME TO RECIPE RECOMMENDATION SYSTEM      @")
    print("@                                                   @")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("#############                          ##############")
    print()
    print("If you are a New User Create an Account :), to Create an Account Enter 2")
    print()
    print("If you are a Existing User, to Login Enter 1 ")
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
                print('2 : Do you Want Recommendation that relates your Diet prefernce : Enter 2')
                print('3 : Do you Want Recommendation that relates your Allergies : Enter 3')
                print('4 : Do you Want Recommendation with macro prefernces : Enter 4')
                print('0 : Do you Want LogOut : Enter 0')
                after_login = input("Enter from above list")
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
                    print('Recommendation macro preference')
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
            email = input("Enter Email ID: ")
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                print('Invalid email address format!')
                print()
            else:
                break
        while(True):
            username = input("Enter Username: ")
            #cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            #account = cursor.fetchone()
            # If account exists show error and validation checks
            account = False
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

            
        # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
        #cursor.execute('INSERT INTO users(first_name, last_name, email, username, password) VALUES (%s, %s, %s,%s,%s)', (firstname, lastname, email, username, password,))
        #conn.commit()
        print("\nRegistered!! Account created Successfully!")
        print("\nYou can add your diet prefernce and allergies if any")
        
        cursor.execute('select prefer_id, name,description from dietry_prefer')
        records = cursor.fetchall()
        i=1
        for row in records:
            print(i,' : ',row[1],'--',row[2])
            i=i+1
        print('\n0 : No diet Prefernce')
        while(True):
            try:
                diet_prefer = input('\nEnter respective number for any Diet prefernce you require from above list : ')
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
                alergy = input('\nEnter respective number for any Allergy you require from above list : ')
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
