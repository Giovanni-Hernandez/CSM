#import modules
from tkinter import *
import os
from os import system
from PIL import Image, ImageTk
# Generator and verificator of One Time Password (OTP)
import authenticator as gen
# Menus
import ceoMenu
# Block cipher
import aesCBC 

import filesManagement as fman

# Designing window for registration
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen['background']='black'
    register_screen.title("Register")
    register_screen.geometry("500x500")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below to register", font=("Tahoma", 18), bg="#1AB0F1",foreground="white",height="2", width="300").pack()
    Label(register_screen, text="", bg="black").pack()

    username_lable = Label(register_screen, text="Username * ", font=("Tahoma", 11), bg="black",foreground="white")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username,font=("Tahoma", 11))
    username_entry.pack()
    Label(register_screen, text="",bg="black").pack()

    password_lable = Label(register_screen, text="Password * ", font=("Tahoma", 11),bg="black",foreground="white")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*',font=("Tahoma", 11))
    password_entry.pack()
    Label(register_screen, text="", bg="black").pack()
    Label(register_screen, text="", bg="black").pack()

    Button(register_screen, text="Register", width=15, height=1, font=("Tahoma", 11), background="#E03C2E",foreground="white", activeforeground="white", activebackground="#1BB022", command = register_user).pack()
    
# Designing window for login 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen['background']='black'
    login_screen.title("Login")
    login_screen.geometry("500x450")
    Label(login_screen, text="Please enter details below to login", font=("Tahoma", 18), bg="#1AB0F1",foreground="white",height="2", width="300").pack()
    Label(login_screen, text="", bg="black").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ", font=("Tahoma", 11), bg="black",foreground="white").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify, font=("Tahoma", 13))
    username_login_entry.pack()
    Label(login_screen, text="",bg="black").pack()

    Label(login_screen, text="Password * ", font=("Tahoma", 11),bg="black",foreground="white").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*',font=("Tahoma", 13))
    password_login_entry.pack()
    Label(login_screen, text="",bg="black").pack()
    Label(login_screen, text="",bg="black").pack()

    Button(login_screen, text="Login", width=15, height=1, command = login_verify, font=("Tahoma", 11), background="#760FCD",foreground="white", activeforeground="white", activebackground="#1BB022").pack()
 
# Implementing event on register button
def register_user():
 
    username_info = username.get()
    password_info = password.get()
    
    list_of_files = os.listdir("../CSM/users/")
    if username_info not in list_of_files:
 
        file = open("../CSM/users/"+username_info, "w")
        file.write(username_info + "\n")
        file.write(password_info + "\n")
        file.close()

        Label(register_screen, text="",bg="black").pack()
        Label(register_screen, text="Registration Success", bg="#1BB022",foreground="white",font=("Tahoma", 12),height="1", width="20").pack()

        Label(register_screen, text="",bg="black").pack()
        Button(register_screen, text="Get QR", width=15, height=1, font=("Tahoma", 11), background="#E03C2E",foreground="white", activeforeground="white", activebackground="#1BB022", command = get_otp).pack()
    else:
        Label(register_screen, text="",bg="black").pack()
        Label(register_screen, text="Registration Failed", bg="#E03C2E",foreground="white",font=("Tahoma", 12),height="1", width="20").pack()
        Label(register_screen, text="",bg="black").pack()
        Button(register_screen, text="OK", width=15, height=1, font=("Tahoma", 11), background="#E03C2E",foreground="white", activeforeground="white", activebackground="#1BB022", command = delete_register_screen).pack()



def get_otp():
    Label(register_screen, text="",bg="black").pack()
    Label(register_screen, text="Please save your QR", bg="#1BB022",foreground="white",font=("Tahoma", 12),height="1", width="20").pack()
    Label(register_screen, text="",bg="black").pack()
    Button(register_screen, text="OK", width=15, height=1, font=("Tahoma", 11), background="#E03C2E",foreground="white", activeforeground="white", activebackground="#1BB022", command = delete_register_screen).pack()
    
    username_info = username.get()
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    # Welcome the new directive
    system("cls")
    print("---------------Welcome directive: "+username_info+"---------------")
    
    # Show the OTP to the user
    print("\nGenerating OTP (QR or secret key)...")
    gen.generate(username_info)

    #Create a directory with the username
    os.mkdir("../CSM/directives/"+username_info)
    print("\nGenerating AES key...")
    print("Successful AES key generation: "+username_info+"key.aes")

    #Create a file with the AES key
    fman.savefile("../CSM/directives/"+username_info+"/"+username_info,"key",".aes",aesCBC.generate256Key())
    print("\nGenerating rsa key pair...")
    print("The CEO's RSA public key is being shared with you...")
    print("The AES key is being encrypted with the CEO's public RSA key..")
    print("Your RSA public key and encrypted AES key are being shared with the CEO..")

# Implementing event on login button 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    list_of_files = os.listdir("../CSM/users/")
    if username1 in list_of_files:
        file1 = open("../CSM/users/"+username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            # Verificación del OTP
            var = gen.verificate_otp(username1)
            if var:
                #Verificación CEO o directivo
                if (username1 == "ceo@gmail.com") and (password1 == "umbrella") :
                    login_sucess()
                    ceoMenu.ceoPrincipalMenu()
                else:
                    login_sucess()
            else:
                password_not_recognised()
        else:
            password_not_recognised()
        file1.close()
    else:
        user_not_found()
 

# Designing popup for login success
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen['background']='black'
    login_success_screen.title("Success")
    login_success_screen.geometry("200x150")
    Label(login_success_screen, text="Login Success", font=("Tahoma", 12), bg="#1AB0F1",foreground="white",height="2", width="300").pack()
    Label(login_success_screen, text="",bg="black").pack()
    Button(login_success_screen, text="OK", bg="#1BB022",foreground="white", command=delete_login_success,font=("Tahoma", 12),height="1", width="15").pack()
 
# Designing popup for login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen['background']='black'
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("200x150")
    Label(password_not_recog_screen, text="Invalid Password ",font=("Tahoma", 12), bg="#E03C2E",foreground="white",height="2", width="300").pack()
    Label(password_not_recog_screen, text="",bg="black").pack()
    
    Button(password_not_recog_screen, text="OK",bg="#1BB022",foreground="white",command=delete_password_not_recognised,font=("Tahoma", 12),height="1", width="15").pack()
 
# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen['background']='black'
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("200x150")
    Label(user_not_found_screen, text="User Not Found",font=("Tahoma", 12), bg="#E03C2E",foreground="white",height="2", width="300").pack()
    Label(user_not_found_screen, text="",bg="black").pack()

    Button(user_not_found_screen, text="OK", bg="#1BB022",foreground="white",command=delete_user_not_found_screen,font=("Tahoma", 12),height="1", width="15").pack()
 
# Deleting popups
def delete_login_success():
    login_success_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()


def delete_register_screen():
    register_screen.destroy()
 
# Designing Main(first) window
def main_account_screen():
    global main_screen
    main_screen = Tk(className='gui')
    main_screen.geometry("500x450")
    main_screen.title("Account Login")
    main_screen['background']='black'
    # Create a photoimage object of the image in the path
    img = Image.open("../CSM/img/Logo.png")
    # Resize the image
    img = img.resize((150,155))
    img = ImageTk.PhotoImage(img)
   

    Label(text="Select your choice", bg="#1AB0F1",foreground="white", width="300", height="2", font=("Tahoma", 18)).pack()
    Label(text="",background="black").pack() # Salto de línea

    Button(text="Login", height="2", width="30", background="#760FCD",foreground="white", activeforeground="white", activebackground="#1BB022", command = login, font=("Tahoma", 13)).pack()
    Label(text="",background="black").pack()

    Button(text="Register", height="2", width="30", background="#E03C2E",foreground="white", activeforeground="white", activebackground="#1BB022",command=register, font=("Tahoma", 13)).pack()
    Label(text="",background="black").pack()

    Label(image=img, background="black" ).pack()
    main_screen.mainloop()
 
 
main_account_screen()