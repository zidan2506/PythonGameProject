limit = 3
print('\033[1;30;47mRegistation\033[m')
username = input('Enter your username: ')
useraccount = input("Create your Username: ")
userpassword = input("Create your password: ")
print('Ur account have been created!\nPls login')
loginuser = input("Enter ur username: ")
loginpassword = input("Enter ur password: ")
if loginuser == useraccount and loginpassword == userpassword:
    print('Welcome ' + username + '🙌')
else:
    # print("wrong username or password\nplease try again")
    # loginuser = input("Enter your Username: ")
    # loginpassword = input("Enter your password: ")
    while limit > 0:
        print(f"\033[31m⚠️Wrong username or password⚠️\n⚠️Please try again⚠️\n⚠️You have {limit} attempts left⚠️\033[0m")
        loginuser = input("Enter your Username: ")
        loginpassword = input("Enter your password: ")
        limit = limit - 1
        if loginuser == useraccount and loginpassword == userpassword:
            print('Welcome ' + username + '🙌')
            break
        elif limit == 0:
            print("Access Denied ❌")
