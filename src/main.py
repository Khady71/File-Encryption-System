from ibe_utils import IBEEncryption
import random
import time
import requests
from user import User
from fun_fact import get_michael_scott_quote
from charm.toolbox.pairinggroup import serialize, deserialize, PairingGroup
import ast
from colorama import init, Fore, Back, Style


    
def create_user_from_server():

    print("\n Connecting to IBE server")
    try:    
        user = User()  
        user.get_public_params_from_server() 
       
         
        print(f" User created with server's public parameters")
        return user
    except Exception as e:
        print(f" Failed to connect to server: {e}")
        return None
    

def menu_principal(user):
    while True:
        BANNER = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                 🔐 IBE-AES: ENCRYPT & SEND                    ║
        ║           Identity-Based Encryption Suite v1.0.0               ║
        ║        https://github.com/Khady71/file-encryption-system       ║
        ╚════════════════════════════════════════════════════════════════╝
        """
       
        print(Fore.CYAN + BANNER + Style.RESET_ALL)
        print(f" Current user: {user.ID if user.ID else "Not set"}")
        print(f" Private key:{ "Loaded" if user.d_id else "Not loaded"}")
        print(f" Public params: {'Configured' if user.ibe else 'Not configured'}")
        
        print("\nOptions:")
        print("[1] Encrypt a message")
        print("[2] Get private key")
        print("[3] Decrypt a message")
        print("[4] Fun Fact : Michael Scott once said : ")
        print("[5] Quit")   

        choice = input("\nChoose : ")

        if choice == "1":
            recipient_email = str(input("Recipient email : "))
            plain_message = str(input("Message : "))
            U, ciphertext = user.encrypt(recipient_email, plain_message)
            
            if U and ciphertext:
                print("\nEncrypted message:")
                print(f"U: {U}")
                print(f"Ciphertext: {ciphertext}")

        
        elif choice == "2":
            email = str(input("Your email: "))
            user.get_private_key(email)

        
        elif choice == "3":
            if not user.d_id:
                print("Get private key first!")
                continue
            U_hex = input("Enter U: ")
            U = user.ibe.group.deserialize(bytes.fromhex(U_hex))
            cipher = int(input("Enter ciphertext: "))
            decrypted = user.decrypt(U, cipher)
            if decrypted:
                print(f"\n Decrypted: '{decrypted}'")
        
        
        elif choice == "4":            
            print(get_michael_scott_quote())

        elif choice == "5":
            print("Goodbye, catch you on the flippity flip!")
            break



def main():
    print(f"Starting IBE Encryption System ....")

    user = create_user_from_server()
    if not user:
        print("Cannot start without server connection")
        return 

    menu_principal(user)



if __name__ == "__main__":
    main()