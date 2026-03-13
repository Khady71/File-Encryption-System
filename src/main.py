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
        ╔════════════════════════════════════════════════════════════════╗
        ║                 Welcome to ENCRYPT & SEND FILES                ║
        ║           Identity-Based Encryption Suite v1.0.0               ║
        ║        https://github.com/Khady71/file-encryption-system       ║
        ╚════════════════════════════════════════════════════════════════╝
        """
       
        print(Fore.CYAN + BANNER + Style.RESET_ALL)
        print(f" Current user: {Fore.RED}{user.ID if user.ID else "Not set"}")
        print(f" {Style.RESET_ALL}Private key: {Fore.GREEN}{ "Loaded" if user.d_id else "Not loaded"}")
        print(f" {Style.RESET_ALL}Public params: {Fore.CYAN}{'Configured' if user.ibe else 'Not configured'}")
        
        print(f"\n{Fore.WHITE}Options:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}[1]{Style.RESET_ALL} Encrypt a file for a recipient")
        print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Get a private key from server")
        print(f"  {Fore.YELLOW}[3]{Style.RESET_ALL} Decrypt a file")
        print(f"  {Fore.MAGENTA}[4]{Style.RESET_ALL} Fun Fact")
        print(f"  {Fore.RED}[5]{Style.RESET_ALL} Quit")  

        choice = input("\nYour Choice : ")

        if choice == "1":
            recipient_email = str(input("Recipient email : "))
            file_path = str(input("File path to be encrypted : "))
            output_path = user.encrypt_and_pack(file_path, recipient_email)
            
            if output_path:
                print("\nThe encrypted file to be send is available here : ", output_path)


        
        elif choice == "2":
            email = str(input("Your email: "))
            user.get_private_key(email)

        
        elif choice == "3":
            if not user.d_id:
                print("Get private key first!")
                continue
            file_path = input("File path to be decrypted :")    
            output_path = user.unpack_and_decrypt(file_path)
            if output_path:
                print(f"\n The decrypted file is available here: '{output_path}'")
        
        
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