import asyncio
import io
import time
import brilliant
import PIL.Image as Image
from monocle import get_image, display
from keys import load_private_key, load_public_key
from qr_code import detect_laptop_test , detect_monocle
from encryption import encrypt_hidden, decrypt_hidden
from send_to_server import submit_search_text, process_response_laptop, process_response_monocle



# Need to make sure how to get the monocle mac-address // Or use the git_tag function (maybe better than a mac-address?)
#mon_id = device.mac.address()
#mon_id = device.GET_TAG 
# client/config.py

# For using the php-server-side
#URL = 'http://134.169.202.248/submit.php'

# For using the python-server-side
URL = 'http://194.164.48.22:5000/search'


# Will be replaced with a function from 'Device lib' ! 
mon_id = 420


#
#  async def tap_to_continue(arg):
#     if arg == button.A:
#         asyncio.run(main())

async def button(input):
	async with Monocle() as m:
			if input == 'A':
				await m.send_command(f'import touch \ntouch.callback(touch.A)')
				asyncio.run(main())

			else:
				input == 'B'
				await m.send_command(f'import touch \ntouch.callback(touch.B)')


async def main():

	while True:
		## For Testing
		########################################
		#with open('word_list.txt', 'r') as file:
			#word_list = file.readlines()

		#for word in word_list:
			#qr_data = word.strip()
			#print(f'plain text: {qr_data}')
			#response = await submit_search_text(qr_data, URL)
			#await process_response_laptop(qr_data, response, URL,mon_id)
			#input("\nPress Enter to scan the next QR code...\n")
		########################################
    	

		for n in range(100):
			ev.clear()
			data = await get_image()
			img =  Image.open(io.BytesIO(data))
			jpgImg = img.convert('RGB')
			jpgImg.save(f'output{n}.jpg')
			qr_data = await detect_monocle(n)

			#qr_data = await detect_laptop_test()
			if  qr_data == "no data found":
				continue
			#print(qr_data)
			await display(qr_data)
			response = await submit_search_text(qr_data, URL)
			await process_response_laptop(qr_data, response, URL,mon_id)
			#await button(input)
			time.sleep(1)
			input("Press Enter to scan the next QR code...\n")



			# continue_scanning = display.Text("Tap either keys to scan the next QR code...", 100, 0, display.WHITE, justify=display.TOP_LEFT)
			# display.show(continue_scanning)
			# touch.callback(touch.EITHER, tap_to_continue)
asyncio.run(main())














