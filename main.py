# import statements
from difflib import Match
from cryptography.fernet import Fernet
import os
import sys

# password manager class
# backbone of the whole passBoss
class PasswordManager:
    # constructor
    # only for making an instance of the class
    def __init__(self):
        pass
    
    # create method
    # @params
    # path - path to a folder in which passBoss vault is to be created
    
    # creates passBoss.txt and passBossKey.key files
    # passBoss.txt - vault
    # passBossKey.key - fernet key created to encrypt login details
    # if necessary files exist in the directory, program throws an error, saying a vault is already created 
    def create(self, path : str):
        if not (os.path.exists(path+"/passBossKey.key") and os.path.exists(path+"/passBoss.txt")):
            with open(path+"/passBoss.txt","x") as f:
                f.close()
            with open(path+"/passBossKey.key", "wb") as key:
                key.write(Fernet.generate_key())
                key.close()
        else:
            print("PassBoss vault already created in specified directory")
    # add method
    # @params
    # path - path to a folder in which passBoss vault is existant
    
    # adds login credentials to passBoss.txt if it exists
    # takes service name, username and password from the user in the console
    # encrypts them using a key taken from passBossKey.key
    # and writes them to the vault
    def add(self, path):
        if not (os.path.exists(path+"/passBossKey.key") and os.path.exists(path+"/passBoss.txt")):
            print("No passBoss vault found in specified directory")
            return
        service = input("Input service name: \n")
        username = input("Input username/email: \n")
        password = input("Input password: \n")

        details = bytes(f'{service}\t{username}\t{password}',"utf-8")
        with open(path+"/passBossKey.key", "rb") as keyFile:
            key = keyFile.read()
            keyFile.close()
        with open(path+"/passBoss.txt", "ab") as f:
            fer = Fernet(key)
            encrypted = fer.encrypt(details)
            f.write(b''+encrypted+b"\n")
            f.close()
        print("Details successfully added")

    # read method
    # @params
    # path - path to a folder in which passBoss vault is existant
    
    # reads login credentials from passBoss.txt if it exists
    # takes a line from the file which constains encrypted service name, username and password
    # decrypts them using a key taken from passBossKey.key
    # and writes them to the console

    def read(self, path):
        if not (os.path.exists(path+"/passBossKey.key") and os.path.exists(path+"/passBoss.txt")):
            print("No passBoss vault found in specified directory")
            return
        service = bytes(input("Input service name to read: \n"), "utf-8")
        with open(path+"/passBossKey.key", "rb") as keyFile:
            key = keyFile.read()
            keyFile.close()
        with open(path+"/passBoss.txt", "rb") as f:
            fer = Fernet(key)
            for line in f:
                if line == '':
                    continue
                decrypted = fer.decrypt(line)
                dec = decrypted.split(b'\t')
                if dec[0] == service:
                    for i in range(len(dec)):
                        dec[i] = dec[i].decode('utf-8')
                    print(f'Username: {dec[1]}')
                    print(f'Password: {dec[2]}')
            f.close()
            
def main():
    pm = PasswordManager()
    if(len(sys.argv) == 3):
        match sys.argv[1]:
            case "new":
                pm.create(sys.argv[2])
            case "add":
                pm.add(sys.argv[2])
            case "read":
                pm.read(sys.argv[2])
            case _:
                print("Use help argument for help with the arguments")
    elif len(sys.argv) == 2:
        match sys.argv[1]:
            case "help":
                print("\npassBoss argument helper:\n - new [path] - creates a passBoss vault in the specified directory, if doesn't exist\n - add [path] - adds new details into a passBoss vault in the specified directory\n - read [path] - reads details from a passBoss vault in the specified directory using the service name\n")
            case "version":
                print("passBoss 1.0.0")
            case _:
                print("Use help argument for help with the arguments")
    else:
        print("Use help argument for help with the arguments")

if __name__ == "__main__":
    main()