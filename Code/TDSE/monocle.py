import asyncio
import threading

from brilliant import *




remote_script = '''
import bluetooth, camera, time, led, touch, display, device

bat = device.battery_level()
if bat > 70:
    t_bat = display.Rectangle(180, 340, 240, 370, display.GREEN)
elif bat < 71 and bat > 39:
    t_bat = display.Rectangle(180, 340, 220, 370, display.YELLOW)
else:
    t_bat = display.Rectangle(180, 340, 200, 370, display.RED)


t_status_b = display.Text('B:' +str(bat) +' %', 10, 330, display.MAGENTA, justify=display.TOP_LEFT)
t_line1 = display.Text('Press L to scan', 320, 140, display.WHITE, justify=display.TOP_CENTER)
display.show(t_line1, t_bat, t_status_b)
    

def trigger_capture(button):
    length = bluetooth.max_length()

    t_line2 = display.Text('Transferring data...', 320, 140, display.WHITE, justify=display.TOP_CENTER)
    display.show(t_line2, t_bat, t_status_b)  

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
    

def nav_input(button):

    t_line3 = display.Text('Starting Over...', 320, 140, display.YELLOW, justify=display.TOP_CENTER)
    display.show(t_line3, t_bat, t_status_b)

    led.on(led.GREEN)
    bluetooth.send(b"txt:" + "b")
    led.off(led.GREEN)
    bluetooth.send(b'end:')

touch.callback(touch.A, nav_input)
touch.callback(touch.A, )
touch.callback(touch.B, trigger_capture)
touch.callback(touch.B, )
'''

# Need to make sure how to get the monocle mac-address // Or use the git_tag function (maybe better than a mac-address?)
#mon_id = device.mac.address()
#mon_id = device.GET_TAG 

mon_id = 420
lockBLE = threading.Lock()

# Start the remote-script on the 'Monocle'. This will start the Camera and await to 'Capture'(Has been changed!)
async def get_image():
   async with Monocle() as m:
    #    with lockBLE:
            # await displayUI("","Daten werden übertragen","","")
            await m.send_command(remote_script)
            await ev.wait()
            data = await m.get_all_data()
            print("Step 3: Recieving image data")
            print("data recieved")
            return data


# Displaying the output on the Monocle
async def display(data):
   async with Monocle() as m:
       await m.send_command(f"import display \ntext = display.Text('{data}', 100, 0, display.WHITE, justify=display.TOP_LEFT) \ndisplay.show(text)")

# Displaying the output ont the Monocle in two lines from two input strings
async def display2(line1, line2):
   async with Monocle() as m:
       await m.send_command(f"import display \nt_line1 = display.Text('{line1}', 40, 40, display.WHITE, justify=display.TOP_LEFT) \nt_line2 = display.Text('{line2}', 40, 120, display.WHITE, justify=display.TOP_LEFT) \ndisplay.show(t_line1, t_line2)")

# Special intro screen
# shifted to preload
async def displayStart(line1, line2, line3, line4, line5):
    async with Monocle() as m:
        status = 0
        text = f"import display, time, device\nbat = device.battery_level()\nt_line1 = display.Text('{line1}', 320, 175, display.WHITE, justify=display.BOTTOM_CENTER)\nt_line2 = display.Text('{line2}', 278, 235, display.RED, justify=display.BOTTOM_CENTER)\nt_line3 = display.Text('{line3}', 306, 235, display.YELLOW, justify=display.BOTTOM_CENTER)\nt_line4 = display.Text('{line4}', 334, 235, display.GREEN, justify=display.BOTTOM_CENTER)\nt_line5 = display.Text('{line5}', 362, 235, display.BLUE, justify=display.BOTTOM_CENTER)"
        input = f"\nt_input = display.Text('L: scan     R: reset', 320, 0, display.MAGENTA, justify=display.TOP_CENTER)"
        bat_status = "\nif bat > 70:\n    t_bat = display.Rectangle(180, 340, 240, 370, display.GREEN)\nelif bat < 71 and bat > 39:\n    t_bat = display.Rectangle(180, 340, 220, 370, display.YELLOW)\nelse:\n    t_bat = display.Rectangle(180, 340, 200, 370, display.RED)"
        con_status = f"\nif {status} == 1:\n    t_con = display.Rectangle(580, 340, 610, 370, display.RED)\n    t_status_con = display.Text('<<disconnected>>', 250, 330, display.MAGENTA, justify=display.TOP_LEFT)\nelse:\n    t_con = display.Rectangle(580, 340, 610, 370, display.GREEN)\n    t_status_con = display.Text('<<connected>>', 260, 330, display.MAGENTA, justify=display.TOP_LEFT)"
        statusBar = "\nt_status_b = display.Text('B:' +str(bat) +' %', 20, 330, display.MAGENTA, justify=display.TOP_LEFT)"
        show = "\ndisplay.show(t_input, t_line1, t_line2, t_line3, t_line4, t_line5, t_bat, t_con, t_status_b, t_status_con)"
        disconnected = f"\ntime.sleep(10)\nstatus = 1\n"
        await m.send_command(text + input + statusBar + bat_status + con_status + show + disconnected + con_status + show)
            


async def displayUI(line1, line2, line3, line4):
    async with Monocle() as m:
        
        # with lockBLE:
        text = f"import display, time, device\nbat = device.battery_level()\nt_line1 = display.Text('{line1}', 320, 78, display.WHITE, justify=display.TOP_CENTER)\nt_line2 = display.Text('{line2}', 320, 140, display.WHITE, justify=display.TOP_CENTER)\nt_line3 = display.Text('{line3}', 320, 206, display.WHITE, justify=display.TOP_CENTER)\nt_line4 = display.Text('{line4}', 320, 272, display.WHITE, justify=display.TOP_CENTER)"
        input = f"\nt_input = display.Text('L: scan     R: reset', 320, 0, display.MAGENTA, justify=display.TOP_CENTER)"
        bat_status = "\nif bat > 70:\n    t_bat = display.Rectangle(170, 340, 230, 370, display.GREEN)\nelif bat < 71 and bat > 39:\n    t_bat = display.Rectangle(170, 340, 210, 370, display.YELLOW)\nelse:\n    t_bat = display.Rectangle(170, 340, 190, 370, display.RED)"
        con_status_0 = f"\nt_con = display.Rectangle(600, 340, 630, 370, display.GREEN)\nt_status_con = display.Text('<<connected>>', 260, 330, display.MAGENTA, justify=display.TOP_LEFT)"
        statusBar = f"\nt_status_b = display.Text('B:' +str(bat) +' %', 10, 330, display.MAGENTA, justify=display.TOP_LEFT)"
        show = "\ndisplay.show(t_input, t_line1, t_line2, t_line3, t_line4, t_bat, t_con, t_status_b, t_status_con)"
        # disconnected = f"\ntime.sleep(25)\n"
        # con_status_1 = f"\nt_con = display.Rectangle(600, 340, 630, 370, display.RED)\nt_status_con = display.Text('<disconnected>', 245, 330, display.MAGENTA, justify=display.TOP_LEFT)"
        
        await m.send_command(text + input + statusBar + bat_status + con_status_0 + show) #for updates add  + disconnected + con_status_1 + show
        # await ev.wait()     

              
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



navigation_script = '''
import bluetooth, time, touch

def nav_input(button):

    led.on(led.GREEN)
    while True:
        try:
            bluetooth.send(b'b')
        except OSError:
            continue
        break
    led.off(led.GREEN)
    bluetooth.send(b'end:')

touch.callback(touch.A, nav_input)
touch.callback(touch.A,)
'''


#short interation via BLE to navigate through main
#eg A for new picture, B for reset, settings, etc
async def get_nav():
    async with Monocle() as n:
          await n.send_command(remote_script)
          await ev.wait()
          input = await n.get_all_data()
          ev.clear()
          return input
