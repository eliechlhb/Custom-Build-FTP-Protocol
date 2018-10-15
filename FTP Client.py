import socket
import os
import shutil
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = input('Enter host: ')
PORT = 21

#Connect to server
server_address = (HOST, PORT)
sock.connect(server_address)


logged_in= False;

#Choosing decision 
decision = input (" Choose one of the following options:\n 1. Register New User. \n 2. Log-In to FTP Server. \n Enter your choice [1 or 2] and press the Enter key: ")
while(decision != '1' and decision != '2' ):
    print( " Wrong Decision ! \n")
    decision = input (" Choose one of the following options:\n 1. Register New User. \n 2. Log-In to FTP Server. \n Enter your choice [1 or 2] and press the Enter key: ")

sock.sendall(decision.encode('utf-8'))

#Username Registration
if decision == '1':
    Reg_username= input ("\n Create a username : " )
    sock.sendall(Reg_username.encode('utf-8'))
    check_Reg_username= sock.recv(1024).decode("utf8") 

    #Check if username is available or not 
    while check_Reg_username == '1':
        print (" This username already exists! , Please choose another one. ")
        Reg_username= input ("\n Create a username : " )
        sock.sendall(Reg_username.encode('utf-8'))
        check_Reg_username= sock.recv(1024).decode("utf8")
        
    #Once an available username is created ask for a password                    
    Reg_password= input (" Create a password: ")
    sock.sendall(Reg_password.encode('utf-8'))

    #Enter the Application
    print (" Cloud Created")
    Access = '1'
    
    
        
if decision =='2':
    user_found_new ='1'
    user_count=0
    pass_count=1

    #Loop for checking the 3 attempts
    while (logged_in == False and user_count<3 and pass_count<3):
    
        Login_username= input ("\n Enter your username : ")
        sock.sendall(Login_username.encode('utf-8'))
        #send the username to the server to check it 


        logged_in= False;

        user_found= sock.recv(1024).decode("utf8")
        #if username exists the server will send a 1 otherwise 0 

        #if enetered username is registered ask for password 
        if (user_found == '1'):
            Login_password= input (" Enter your password : ")
            sock.sendall(Login_password.encode('utf-8'))
            logg= sock.recv(1024).decode("utf8")
            #If password is correct the server will send a 1 

            if logg == '1':
                logged_in = True
            else:
                logged_in = False
                print(" Wrong password " )
            
            while (logged_in==False and pass_count<3):

                #Ask for a new password 
                Login_password= input (" Enter your password : ")
                sock.sendall(Login_password.encode('utf-8'))
                logg= sock.recv(1024).decode("utf8")
                    
                if logg == '1':
                    logged_in = True
                else:
                    logged_in = False
                    print(" Wrong password " )
                        
                pass_count+=1
                    
                           
            break;

        
        user_found_new= sock.recv(1024).decode("utf8")
        
        if (user_found_new =='0'):
            print (" Wrong username")
            user_count+=1
            
    if user_count ==3 or (logged_in==False and pass_count ==3):
        print (" Connection Closed ")
        sock.close()
        Access = '0'
        #Terminate the application 
        
    else:
        print ( " Welcome " + Login_username )
        Access = '1'


#enter the application 
while Access == '1' :

    Command= input ("\n Enter command : " )
    sock.sendall(Command.encode('utf-8'))

    while Command != "quit" and Command != "Quit":

        if Command == "createFolder":
            FileName= input ("\n Enter Name of the file : " )
            sock.sendall(FileName.encode('utf-8'))
            print("New Folder has been created and added to the path")
            Command= input ("\n Enter command : " )
            sock.sendall(Command.encode('utf-8'))

                
        if Command == "List" or Command == "list":
 
            flist=sock.recv(1024).decode("utf8")
            print(flist)
            flist=sock.recv(1024).decode("utf8")
            print(flist)
            
            Command= input ("\n Enter command : " )
            sock.sendall(Command.encode('utf-8'))

        if Command == "deleteFile":

             FileName= input ("\n Enter Name of the File that you want to remove: " )
             sock.sendall(FileName.encode('utf-8'))
             print("File has been deleted from the path")
             Command= input ("\n Enter command : " )
             sock.sendall(Command.encode('utf-8'))

        if Command == "deleteFolder":

             FileName= input ("\n Enter Name of the Folder that you want to remove: " )
             sock.sendall(FileName.encode('utf-8'))
             print("File has been deleted from the path")
             Command= input ("\n Enter command : " )
             sock.sendall(Command.encode('utf-8'))
             
        if Command == "rename":

             OldFileName= input ("\n Enter Name of the File that you want to rename: " )
             sock.sendall(OldFileName.encode('utf-8'))
             NewFileName= input ("\n Enter Name of the new File " )
             sock.sendall(NewFileName.encode('utf-8'))
             print("File has been Renamed")
             Command= input ("\n Enter command : " )
             sock.sendall(Command.encode('utf-8'))

        if Command == "move":

             print(os.listdir(Path))
             destination= input ("\n Enter Name of the File that you want to move: " )
             sock.sendall(destination.encode('utf-8'))
             source= input ("\n Enter Name of the new Directory of the File: " )
             sock.sendall(source.encode('utf-8'))
             print("File has been Moved")
             Command= input ("\n Enter command : " )
             sock.sendall(Command.encode('utf-8'))


    print("Application Terminated")
    sock.close()
    break







        
            


        



                
                    
                
        
