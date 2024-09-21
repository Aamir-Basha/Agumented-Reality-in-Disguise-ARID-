# the CVTest version of main is setup to test multiple transformations of the raw data at once
# for performance use Servertest

import asyncio
import io
from brilliant import *
import PIL.Image as Image
from monocle import get_image, display
from qr_code import * #detect_laptop_test , detect_monocle, detect_monocle_thresholding_a
import cv2


# Will be replaced with a function from 'Device lib' ! 
mon_id = 420

async def main():

	while True:

		for n in range(0, 99, 4):
            # take image
			data = await get_image()
			img =  Image.open(io.BytesIO(data))

			# result greyscale via PIL     
			jpgImgGS = img.convert('L')
			jpgImgGS.save(f'output\\output{n}.jpg') # 'L' for greyscale, splitt at 127
			qr_data_GS = await detect_monocle(n)
			await display(qr_data_GS)
			print(qr_data_GS)
                  
			# result greyscale via OCV / CV2     
			jpgImgRGB = img.convert('RGB')
			jpgImgRGB.save(f'output\\output{n+1}.jpg')
			qr_data_RGB2GS = await detect_monocle_GS(n+1) #converts to greyscale via CV2
			await display(qr_data_RGB2GS)
			print(qr_data_RGB2GS)
                  
			# result thesholding otsu via CV2
			jpgImgT1 = img.convert('RGB')
			jpgImgT1.save(f'output\\output{n+2}.jpg')
			qr_data_T1 = await detect_monocle_thresholding_bi(n+2)
			await display(qr_data_T1)
			print(qr_data_T1)
                  
			
			

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")











