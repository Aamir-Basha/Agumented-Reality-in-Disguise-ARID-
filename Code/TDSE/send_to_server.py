import aiohttp
import time
from monocle import display, display2
from encryption import decrypt_hidden, encrypt_hidden
from keys import load_public_key, load_private_key


# Load/Retrieve the private key
private_key = load_private_key('private_key.pem')
# Load/Retrieve the public key
public_key = load_public_key('public_key.pem')



##################
async def submit_search_text(plaintext, url, add_to_db=False, hidden_text=None, mon_id=None):
    try:
        async with aiohttp.ClientSession() as session:
            data = {'search_text': plaintext}
            if add_to_db:
                data['add_to_db'] = 'yes'
                data['hidden_text'] = hidden_text
                data['mon_id'] = mon_id
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    # This if-statmaent will handle the case that the hidden text was found, to use json
                    # Why JSON! So that we can get the hidden_text "encrypted" but the Monocle ID in plain_text

                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' in content_type:
                        json_data = await response.json()
                        encrypted_msg = json_data.get('encrypted_msg', '')
                        mon_id = json_data.get('mon_id', '')
                        plain_hidden = await decrypt_hidden(encrypted_msg, private_key)
                        full_msg = plain_hidden
                        return full_msg
                        # This elf will hanlde the response when the hidden text is not found, thus 
                        # we use response.text() to exctract the "No hidden text found" in response: 

                    elif 'text/html' in content_type: 
                        plain_text = await response.text()
                        return plain_text
                    else:
                        return f'Error: Unexpected content type: {content_type}'
                else:
                    return f'Error: Response status code {response.status}'
    except aiohttp.ClientError as e:
        return f'Error from aiohttp: {e}'


################## This function is to be used only when testing the Monocle!!
async def process_response_monocle(qr_text, response, url, mon_id):
    try:
        if "No hidden text found" in response:
            # Ask to add a hidden text or not using the buttons
            await display("Do you want to add this plaintext to the database? NO/YES")

            async def add_to_db_or_not(button):
                if button == touch.A:
                    hidden_text = input("Enter hidden text: ")
                    encrypted_txt = await encrypt_hidden(hidden_text)    
                    response = await submit_search_text(qr_text, url, add_to_db=True, hidden_text=encrypted_txt,mon_id=mon_id)
                    if 'successfully added the data.' in response:
                        print('Data was added successfully.')
                    else:
                        print('Error while adding new Data')
                elif button == touch.B:  
                    print("No plaintext added.", response)             

            touch.callback(touch.EITHER, add_to_db_or_not)
        else:
            plain = await decrypt_hidden(response, private_key)
            print('Hidden message:', plain)  # Print the response from the server if the hidden-text was already stored
    except aiohttp.ClientError as e:
        print(f"Error submitting search text: {e}")
##################


################## This function is to be used only when testing the WITHOUT the Monocle!!
async def process_response_laptop(qr_text, response, url,mon_id):
   try:
    if "No hidden text found" in response:
        add_to_db =  input("Do you want to add this plaintext to the database? (yes/no): ").lower()
        #input
        if add_to_db == 'yes':
            abc = input("Enter hidden text: ")
            encrypted_txt = await encrypt_hidden(abc,public_key)    
            response = await submit_search_text(qr_text, url, add_to_db=True, hidden_text=encrypted_txt,mon_id=mon_id)
            if 'successfully added the data.' in response:
                print('Data was added successfully.\n')
            else:
                print('Error while adding new Data')

        else:
            print("No plaintext added.\n")

    else:
        print(f'Nachricht für dich: {response} \n' )  # Print the response from the server if the hidden-text was already stored
        return response
   except aiohttp.ClientError as e:
       print(f"Error submitting search text: {e}")
##################


