import socket
from threading import Thread
import os
import shutil
import time


def accept_incoming_connections():
    while True:
        
        #Accepting connections
        client, client_address = sock.accept()
        
        #Keep track of addresses
        addresses[client] = client_address
        
        #Initiate Thread for handle_client 
        Thread(target=handle_client, args=(client,)).start()

        

#User Drive Creation 
def createFolder(directory):
    
    try:
        if not os.path.exists(directory):
            #Create Folder for User
            os.makedirs(directory)
            
    except OSError:
        print ('Error: Creating directory. ' +  directory)



#Username and Password Registration
def createusername(username,password):
    file = open("Login.dat","a")
    file.write (username)
    file.write (";")
    file.write (password)
    file.write(" \n")
    file.close()



def handle_client(client):
 
    while True:
            
        logged_in= False;
        decision = client.recv(1024).decode("utf8")
        
        if decision == '1':

            check='1' #If username exists check =1 else check is 0
            
            while check=='1':
                Reg_username= client.recv(1024).decode("utf8")

                #Check if this username already exists
                with open('Login.dat', 'r') as file:

                    #Check usernames one by one 
                    for line in file:  
                        username, password = line.split(';')
                        
                        # Check the username against the one supplied
                        if username == Reg_username:
                            check='1'
                            break;
                        
                        else:
                            check='0'

                    #Send result of check for client ( if check is 1 then user already exists else regiter
                    client.sendall(check.encode('utf-8'))

                    
            #Password Registration                   
            Reg_password= client.recv(1024).decode("utf8")

            #Creation of username 
            createusername(Reg_username,Reg_password)
            print("'" + Reg_username + "' registered " ) 

            #Creation of user Drive
            Path = 'C:\\Users\\elie\\Desktop\\FTP Project\\version 3.0\\Database\\' +Reg_username
            createFolder(Path)
            print("Cloud Created for : "+ Reg_username )

            username= Reg_username
            Access= '1'

            
            
                
        if decision =='2':
            user_count=0
            pass_count=1
            
            while (logged_in == False and user_count<3 and pass_count<3):
            
                Login_username= client.recv(1024).decode("utf8")

                logged_in= False;
                with open('Login.dat', 'r') as file:
                    
                    for line in file:
                        
                        username, password= line.split(';')

                        #Check if supplied username exists 
                        if (username == Login_username):
                            user_found='1'
                            print (Login_username + " trying to Log-IN")
                            client.sendall(user_found.encode('utf-8'))
                            Login_password= client.recv(1024).decode("utf8")
                            logged_in= (password == Login_password+' '+'\n') #Check password supplied by client 

                            
                            #Check if client supplied a correct username and password 
                            if logged_in == True:
                                logg= '1'
                                print (Login_username + " Logged-IN")
                                Access = '1'
                                username= Login_username
                            else:
                                logg= '0'
                                print ("Wrong Password Log-In Attempt")
                                       
                            client.sendall(logg.encode('utf-8'))

                            while (logged_in==False and pass_count<3):
                                   Login_password= client.recv(1024).decode("utf8")
                                   logged_in= (password == Login_password+' '+'\n')

                                   if logged_in == True:
                                       logg= '1'
                                   else:
                                       logg= '0'
                                
                                   client.sendall(logg.encode('utf-8'))
                                   pass_count+=1
                                   print ("Wrong Password Log-In Attempt") 
                                   
                            break;

                        
                #if username supplied by client do not exists increment the counter and ask for another username        
                if (username != Login_username):
                    user_found='0'
                    time.sleep(3)
                    client.sendall(user_found.encode('utf-8'))
                    client.sendall(user_found.encode('utf-8'))
                    user_count+=1
                    print ("Wrong Username Log-In Attempt") 
                    
                if user_count ==3 or (logged_in==False and pass_count ==3):
                    print ("Client Connection Closed After 3 Wrong Log-In Attempts")
                    Access = '0'

        
        while Access== '1' :

            Path = 'C:\\Users\\elie\\Desktop\\FTP Project\\version 3.0\\Database\\' +username
            Command= client.recv(1024).decode("utf8")
            while Command != "quit" and Command != "Quit":

                if Command == "createFolder":
                    FileName= client.recv(1024).decode("utf8")

                    try:
                        os.makedirs(Path +'\\'+ FileName)
                        print("New Folder has been created and added to the path")
                        Command= client.recv(1024).decode("utf8")

                    except OSError:
                        pass
                      # let exception propagate if we just can't
                      # cd into the specified directory
                        os.chdir(Path +'\\'+ FileName)
                        
                if Command == "List" or Command == "list":

                    print(os.listdir(Path))
                    flist=(os.listdir(Path))
                    for f in range (0, len(flist)):
                        testing=flist[f]
                        client.sendall(testing.encode("utf8"))
                    Command= client.recv(1024).decode("utf8")

                if Command == "deleteFile":

                     FileName= client.recv(1024).decode("utf8")
                     os.remove(Path +'\\'+ FileName)
                     print("File has been deleted from the path")
                     Command= client.recv(1024).decode("utf8")

                if Command == "deleteFolder":

                     FileName= client.recv(1024).decode("utf8")
                     shutil.rmtree(Path +'\\'+ FileName)
                     print("File has been deleted from the path")
                     Command= client.recv(1024).decode("utf8")
                     
                if Command == "rename":

                     OldFileName= client.recv(1024).decode("utf8")
                     NewFileName= client.recv(1024).decode("utf8")
                     OldFile = os.path.join(Path, OldFileName)
                     NewFile = os.path.join(Path, NewFileName)
                     os.rename(OldFile, NewFile)
                     print("File has been Renamed")
                     Command= client.recv(1024).decode("utf8")

                if Command == "move":

                     print(os.listdir(Path))
                     destination= client.recv(1024).decode("utf8")
                     source= client.recv(1024).decode("utf8")
                     shutil.move(Path + destination,Path + source)
                     print("File has been Moved")
                     Command= client.recv(1024).decode("utf8")


            print("Application Terminated")
            






clients = {}
addresses = {}


# Setting up server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('echalhoub', 21)
sock.bind(server_address)


sock.listen(5)
print("Waiting for connection...")
accepting_thread = Thread(target=accept_incoming_connections)
accepting_thread.start()
accepting_thread.join()
sock.close()




                
                    
                
        
