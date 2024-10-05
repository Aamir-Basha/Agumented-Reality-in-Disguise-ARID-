import rsa
import base64

async def encrypt_hidden(hidden,public_key):
    # Use utf-8 to be able to use rsa.encrypt
    utf8 = hidden.encode('utf-8')
   
    # Using rsa.encrypt 
    cipher = rsa.encrypt(utf8, public_key)
   
    # Base64 encode to be able to send it to the Server without losing frames!
    base64_encoded = base64.b64encode(cipher)
    encoded_str = base64_encoded.decode('utf-8')
    return encoded_str


async def decrypt_hidden(hidden, private_key):
    # Base64 Decode to be able to decrypt the cipher
    base64_decoded = base64.b64decode(hidden)
    
    # Using rsa.decrypt
    plain_hidden = rsa.decrypt(base64_decoded, private_key)
    
    # Use utf-8 to be able to read it as a string
    decoded_str = plain_hidden.decode('utf-8')
    return decoded_str


