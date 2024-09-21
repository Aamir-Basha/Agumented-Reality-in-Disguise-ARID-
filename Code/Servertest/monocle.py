import asyncio

from brilliant import *




remote_script = '''
import bluetooth, camera, time, led, touch, display

text = display.Text('Press a button to start capturing a QR-Code', 100, 0, display.WHITE, justify=display.TOP_LEFT)
display.show(text)
def trigger_capture(button):
   length = bluetooth.max_length()
   text = display.Text('Capturing...', 100, 0, display.WHITE, justify=display.TOP_LEFT)
   display.show(text)
   camera.capture()
   time.sleep_ms(100)
   while data := camera.read(bluetooth.max_length() - 4):
       led.on(led.GREEN)
       while True:
           try:
               bluetooth.send((b"img:" + data)[:length])
           except OSError:
               continue
           break
   led.off(led.GREEN)
   bluetooth.send(b'end:')
   done = display.Text('Done', 100, 0, display.WHITE, justify=display.TOP_LEFT)
   display.show(done)
touch.callback(touch.EITHER, trigger_capture)
'''

# Need to make sure how to get the monocle mac-address // Or use the git_tag function (maybe better than a mac-address?)
#mon_id = device.mac.address()
#mon_id = device.GET_TAG 

mon_id = 420

# Start the remote-script on the 'Monocle'. This will start the Camera and await to 'Capture'(Has been changed!)
async def get_image():
   async with Monocle() as m:
       await m.send_command(remote_script)
       await ev.wait()
       data = await m.get_all_data()
       return data


# Displaying the output on the Monocle
async def display(data):
   async with Monocle() as m:
       await m.send_command(f"import display \ntext = display.Text('{data}', 100, 0, display.WHITE, justify=display.TOP_LEFT) \ndisplay.show(text)")

# Displaying the output ont the Monocle in two lines from two input strings
async def display2(line1, line2):
   async with Monocle() as m:
       await m.send_command(f"import display \nt_line1 = display.Text('{line1}', 40, 40, display.WHITE, justify=display.TOP_LEFT) \nt_line2 = display.Text('{line2}', 40, 120, display.WHITE, justify=display.TOP_LEFT) \ndisplay.show(t_line1, t_line2)")

# Telling the Monocle that a button was pressed via code (no actual button needs to be pressed)
# used to navigate
async def button(input):
	async with Monocle() as m:
			if input == 'A':
				await m.send_command(f'import touch \ntouch.callback(touch.A)')
				asyncio.run(main())
			else:
				input == 'B'
				await m.send_command(f'import touch \ntouch.callback(touch.B)')
                        
# Waiting for button press from Monocle / User Input
# not tested, maybe better to use get_char, events necessary?, script auslagern?
# async def button_pressed():
#     async with Monocle() as m:
#           ev.clear()
#           await m.send_command('''
#                     import touch, logic
#                     def button_touched(button_f_callback):
#                         length = bluetooth.max_length()
#                         if button_f_callback == A:
#                             bluetooth.send(A)[:length]
#                         elif button_f_callback == B:
#                             bluetooth.send(B)[:length]   
#                     touch.callback(touch.EITHER, button_touched)')
#                     ''')
#           await ev.wait()
#           button_pressed = await m.get_all_data()
#           return button_pressed

# basic ui via display update (concept)
# new info stored in elements (eg ui_upper_text ui_lower_text), ui_update to show all current elements incl statusbar
# async def ui_update(elements):
#    async with Monocle() as m:
#        await m.send_command(f"import display
#                             status bar, fixed, just updated
#                             optional elements")


