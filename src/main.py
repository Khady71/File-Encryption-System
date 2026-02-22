from ibe_utils import IBEEncryption
import random
import time



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
    
def setup():
    ibe = IBEEncryption('SS512')
    P, P_pub, s = ibe.setup()
    return ibe, P, P_pub, s 

    
def extract(email):
    print("\nGénération de la clé privée ")
    private_key = ibe.extract(email)
    return private_key

def encrypt(recipient_email, message_original):
    print("\nChiffrement d'un message")
    print(f"Message original: '{message_original}'")
    U, ciphertext = ibe.encrypt(recipient_email, message_original)
    print(f"   U: {U}")
    print(f"   Ciphertext: {ciphertext}")
    return U, ciphertext

def decrypt(U, ciphertext):
    print("\Déchiffrement par Alice")
    message_dechiffre = ibe.decrypt(d_alice, (U, ciphertext), decode_to_string=True)
    print(f"   Message déchiffré: '{message_dechiffre}'")
    return message_dechiffre 



def menuPrincipal():
        print("*********************** Welcome To Encrypt and Send **********************")
        print("************************** Setting up System*********************")
        
        time.sleep(4)
        print("**************** [1] Encrypt a message to be sent to a recipient ****************")
        print("***************** [2] Generate a private key from email *******************")
        print("******************* [3] Decrypt a message sent to you *********************")
        print("******************* [4] Fun Fact : Michal Scott one said :) *********************")
        print("******************* [5] Quit App*********************")


        print("*************** Choose an option : *****************")
        option =  int(input("**************** => Choosen option : "))
        if(option == 1):
            print("******************************************************************************")
            print("**************** [1] Encrypting a message to be sent to a recipient****************%n")
            recipient_email = str(input("Write the recipient email : "))
            plain_message = str (input("Write the message : "))
            U, ciphertext = encrypt(recipient_email, plain_message)
            
            
        elif(option == 2):
            print("******************************************************************************")
            print("**************** [2] Generating a private key from email ****************%n")
            email = str(input("Write you email : "))
            time.sleep(4)
            private_key = extract(email)


        elif(option == 3):
            print("*****************************************************") 
            print("************** Decrypting a message sent to you ***************\n")
            U = str(input("Write the first part of the message : "))
            Ciphertext =  str(input("Write the second part of the message : "))
            time.sleep(4)
            message_dechiffre = decrypt(U, Ciphertext)

        elif(option == 4):
            print("******** Try not to laugh too hard x) *********%n")
            time.sleep(4)
            print(get_michael_scott_quote())
            
        else :
            print("Goodbye, catch you on the flippity flip!")
            # break


            
ibe, P, P_pub, s = setup()
menuPrincipal()