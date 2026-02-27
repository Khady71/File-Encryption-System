from ibe_utils import IBEEncryption
import random
import time
import requests
from user import User



def get_michael_scott_quote():
    quotes = [
        "I'm not superstitious, but I am a little stitious.",
        "Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me.",
        "I declare BANKRUPTCY!",
        "I feel like my kids grew up, and then they married each other. It’s every parent’s dream.",
        "I’m an early bird and I’m a night owl. So I’m wise and I have worms.",
        "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way.",
        "Toby is in HR, which technically means he works for corporate, so he's really not a part of our family.",
        "The worst thing about prison was the Dementors.",
        "Identify theft is not a joke, Jim! Millions of families suffer every year! (Wait, that was Dwight.)",
        "You miss 100% of the shots you don’t take. — Wayne Gretzky — Michael Scott"
    ]
    
    
    return random.choice(quotes)
    

def create_user_from_server():

    print("\n Connecting to IBE server")
    try:
        response = requests.get("http://localhost:8000/setup")
        response.raise_for_status()
        data = response.json()

        user = User(P=data['P'], P_pub=data['P_pub'])
        print(f" User created with server's public parameters")
        return user
    except Exception as e:
        print(f" Failed to connect to server: {e}")
        return None

def menu_principal(user):
    while True:
        print("\n" + "="*60)
        print(" Welcome To ENCRYPT AND SEND ")
        print("\n" + "="*60)
        print(f" Current user: {user.ID if user.ID else "Not set"}")
        print(f" Private key:{ "Loaded" if user.d_id else "Not loaded"}")
        print(f"Public params: {'Configured' if user.ibe else 'Not configured'}")
        
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
            U = input("Enter U: ")
            cipher = str(input("Enter ciphertext: "))
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