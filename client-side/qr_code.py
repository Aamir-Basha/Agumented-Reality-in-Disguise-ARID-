# this file is for testing functions of cv2 and pil to enhance qr code detection

import cv2
import numpy as np
import io
import PIL.Image as Image
from qreader import QReader

async def detect_monocle(n):
    image = cv2.imread(f'output{n}.jpg')
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)
    
    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()

    if data:
        return data
    else:
        print("No QR Code found in the image.")
        return ("no data found")
     

async def detect_monocle_GS(n):
    image = cv2.imread(f'output\\output{n}.jpg',0) # 0 = greyscale
    cv2.imwrite(f'output\\cv2gs{n+1}.jpg', image)
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)

    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()

    if data:
        return data
    else:
        print("No QR Code found in the image.")
        return ("no data found")
    
async def detect_monocle_thresholding_bi(n):
    image = cv2.imread(f'output\\output{n}.jpg', 0) #greyscale required für thresholding
    detector = cv2.QRCodeDetector()
    
    #scan original first (might be faster)
    data = detector.detectAndDecode(image)
    if data[0]:
        print(data, " original")
        return data
    
    # looping thru various thresholds == lighting conditions in main via second argument for ret
    # for i in range(3):
    #    threshold_value = 180 - 40 * i 
    ret, thresh0 = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    ret1, thresh1 = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    ret3, thresh3 = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY)
    ret4, thresh4 = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)

    cv2.imwrite(f'output\\thresh_bi_{ret}_{n}.jpg', thresh0)
    cv2.imwrite(f'output\\thresh_bi_{ret1}_{n}.jpg', thresh1)
    cv2.imwrite(f'output\\thresh_bi_{ret2}_{n}.jpg', thresh2)
    cv2.imwrite(f'output\\thresh_bi_{ret3}_{n}.jpg', thresh3)
    cv2.imwrite(f'output\\thresh_bi_{ret4}_{n}.jpg', thresh4)
    # data = detector.detectAndDecode(thresh1)

    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()
    

  


async def detect_qreader_monocle(n):

    qreader = QReader()

#  min_confidence=0.0, model_size='l'
    image = cv2.cvtColor(cv2.imread(f'output//output{n}.jpg'), cv2.COLOR_BGR2RGB)
    # cv2.imwrite(f'output//output{n}.jpg', f'output//output{n}.jpg', [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    imgJPG = cv2.imread(f'output//output{n}.jpg', 0)
    
    decoded_text = qreader.detect_and_decode(image=image)
    print(decoded_text)

    
    # looping thru various thresholds == lighting conditions in main via second argument for ret
    # for i in range(3):
    #    threshold_value = 180 - 40 * i 
    ret, thresh0 = cv2.threshold(imgJPG, 200, 255, cv2.THRESH_BINARY)
    ret1, thresh1 = cv2.threshold(imgJPG, 150, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(imgJPG, 120, 255, cv2.THRESH_BINARY)
    ret3, thresh3 = cv2.threshold(imgJPG, 80, 255, cv2.THRESH_BINARY)
    ret4, thresh4 = cv2.threshold(imgJPG, 50, 255, cv2.THRESH_BINARY)

    cv2.imwrite(f'output\\thresh_bi_{ret}_{n}.jpg', thresh0)
    cv2.imwrite(f'output\\thresh_bi_{ret1}_{n}.jpg', thresh1)
    cv2.imwrite(f'output\\thresh_bi_{ret2}_{n}.jpg', thresh2)
    cv2.imwrite(f'output\\thresh_bi_{ret3}_{n}.jpg', thresh3)
    cv2.imwrite(f'output\\thresh_bi_{ret4}_{n}.jpg', thresh4)


    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()
         
    if decoded_text != ():
        print("opfer")
        if decoded_text[0] != None: return decoded_text
        else: print("-.-")
    
    data = qreader.detect_and_decode(image=thresh0)
    print(data, " thresh 0")
    if data != (): 
        if data[0] != None: return data
    data = qreader.detect_and_decode(image=thresh1)
    print(data, " thresh 1")
    if data != (): 
        if data[0] != None: return data
    data = qreader.detect_and_decode(image=thresh2)
    print(data, " thresh 2")
    if data != (): 
        if data[0] != None: return data
    data = qreader.detect_and_decode(image=thresh3)
    print(data, " thresh 3")
    if data != (): 
        if data[0] != None: return data
    data = qreader.detect_and_decode(image=thresh4)
    print(data, " thresh 4")
    if data != (): 
        if data[0] != None: return data
    else:
        print("No QR Code found in the image.")
        return ()



## This Function is only for testing the script without the Monocle !!
async def detect_laptop_test():
    try:
        with open('sample_image.jpg', 'rb') as f:
            qr_code = f.read()

        image = Image.open(io.BytesIO(qr_code))  # Open the img in in bytes format
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert it to BGR 
        detector = cv2.QRCodeDetector()
        data, vertices_array, _ = detector.detectAndDecode(image)   # Detect the QR-Code data (This will be ASCII)

        if data:
            # Have to change print to -> display() to get it on the Monocle!!
            return data
        else:
            # Have to change print to -> display() to get it on the Monocle!!
            print("No QR Code found in the image.")
            return None
    except FileNotFoundError:
        print("Error: Image file 'sample_image.jpg' not found.")
        return None
    except Exception as e:
        print(f"Error reading image or detecting QR code: {e}")
        return None

