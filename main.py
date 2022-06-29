# import statements
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
    def create(self, path):
        if not os.path.exists(path+"passBoss.txt"):
            with open(path+"passBoss.txt","x") as f:
                f.close()
            with open(path+"passBossKey.key", "wb") as key:
                key.write(Fernet.generate_key())
        else:
            print("PassBoss vault already created in specified directory")

pm = PasswordManager()
pm.create(sys.argv[1])