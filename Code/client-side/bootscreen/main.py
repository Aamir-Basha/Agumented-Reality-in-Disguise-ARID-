# this file is to be uploaded to the Monocle without running the scrupt
# it displays a boot screen, nothing else


import display, device, time

t_line1 = display.Text('Welcome to', 320, 175, display.WHITE, justify=display.BOTTOM_CENTER)
t_line2 = display.Text('A', 278, 235, display.RED, justify=display.BOTTOM_CENTER)
t_line3 = display.Text('R', 306, 235, display.YELLOW, justify=display.BOTTOM_CENTER)
t_line4 = display.Text('I', 334, 235, display.GREEN, justify=display.BOTTOM_CENTER)
t_line5 = display.Text('D', 362, 235, display.BLUE, justify=display.BOTTOM_CENTER)
t_input = display.Text('L: scan     R: reset', 320, 0, display.MAGENTA, justify=display.TOP_CENTER)


# i = 0
# while i < 2:
bat = device.battery_level()
if bat > 70:
    t_bat = display.Rectangle(170, 340, 230, 370, display.GREEN)
elif bat < 71 and bat > 39:
    t_bat = display.Rectangle(170, 340, 210, 370, display.YELLOW)
else:
    t_bat = display.Rectangle(170, 340, 190, 370, display.RED)

t_con = display.Rectangle(600, 340, 630, 370, display.RED)
t_status_con = display.Text('<disconnected>', 245, 330, display.MAGENTA, justify=display.TOP_LEFT)
t_status_b = display.Text('B:' +str(bat) +' %', 10, 330, display.MAGENTA, justify=display.TOP_LEFT)
display.show(t_input, t_line1, t_line2, t_line3, t_line4, t_line5, t_bat, t_con, t_status_b, t_status_con)
# time.sleep(30)
    # i += 1
# device.force_sleep()