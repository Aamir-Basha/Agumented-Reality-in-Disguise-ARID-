import threading
import asyncio
import io
from brilliant import *
import PIL.Image as Image

from monocle import get_image, displayUI, display2, get_nav, displayStart
from qr_code import * #detect_laptop_test , detect_monocle, detect_monocle_thresholding_a
from send_to_server import submit_search_text, process_response_monocle
from encryption import decrypt_hidden

import cv2
import time
import os
import shutil


mon_id = 420
URL = 'http://194.164.**.**:5000/search'
lockBLE = threading.Lock()

class mainThread(threading.Thread):
	def __init__(self, target, args=()):
		super().__init__(target=target, args=args)
		self._result = None

	def run(self):
		if self._target is not None:
			self._result = self._target(*self._args, **self._kwargs)

	def get_result(self):
		return self._result

async def main():

	print("Step 0: Setup")
	shutil.rmtree("output")
	os.mkdir("output")

	i = 0
	while True:
		print("Step 1: Start Menu")
		
		ev.clear()
		print("ready for new photo")
		try:
			print("Step 2: taking a photo")
			data = await get_image()
			ev.clear()
		except:
			print("Connection Error")
			perror_l1 = ""
			perror_l2 = "Connection error"
			perror_l3 = "Press R to restart"
			perror_l4 = ""
			await displayUI(perror_l1, perror_l2, perror_l3, perror_l4)
			ev.clear()
			continue
		
		if data == bytearray():
			print("reset")
			ev.clear()
			continue

		#  Foto wird verarbeitet
		print("Step 4: converting raw data to jpg")
		processing_l1 = ""
		processing_l2 = "Processing photo..."
		processing_l3 = ""
		processing_l4 = ""	
		# ev.clear()
		await displayUI(processing_l1, processing_l2, processing_l3, processing_l4)
		ev.clear()
		time.sleep(0.5)

		#IMG convertion
		try:
			# print("processing photo")
			img =  Image.open(io.BytesIO(data))
		except:
			print("Processing Error")
			perror_l1 = ""
			perror_l2 = "Processing error"
			perror_l3 = "Press R to restart"
			perror_l4 = ""
			await displayUI(perror_l1, perror_l2, perror_l3, perror_l4)
			ev.clear()
			continue
		jpgImg = img.convert('RGB')
		jpgImg.save(f'output//output{i}.jpg')

		#search for qr-code in picture
		print("Step 5: extracting QR Code with computer vision")
		qr_data = await detect_qreader_monocle(i)
		ev.clear()
		# qr_data = await detect_monocle_thresholding_bi(i)
		print(qr_data)	
		if qr_data == ():
			noQR_l1 = ""
			noQR_l2 = "No QR-Code found"
			noQR_l3 = "Restarting..."
			noQR_l4 = ""
			await displayUI(noQR_l1, noQR_l2, noQR_l3, noQR_l4)
			ev.clear()

		elif qr_data[0] is not None:

			# Search for Server info on QR-Code
			print("Step 6: communicating with Database")
			response = await submit_search_text(qr_data[0], URL)
			print(response)
			serverresponse_l1 = "Public message:"
			serverresponse_l2 = qr_data[0]
			serverresponse_l3 = "Hidden message:"
			serverresponse_l4 = response
			await displayUI(serverresponse_l1, serverresponse_l2, serverresponse_l3, serverresponse_l4)
			ev.clear()

			await process_response_monocle(qr_data[0], response, URL, mon_id)
			ev.clear()
			time.sleep(30)
			continue

		else:
			mptQR_l1 = ""
			mptQR_l2 = "No message found"
			mptQR_l3 = "Restarting..."
			mptQR_l4 = ""
			await displayUI(mptQR_l1, mptQR_l2, mptQR_l3, mptQR_l4)
		ev.clear()

		time.sleep(0.5)
		print("End of main loop")
		i+=1


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")











