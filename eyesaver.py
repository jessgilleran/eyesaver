#Displays a countdown timer that can be adjusted by user. When timer finishes, a 20 second
#eye break timer starts and the cycle repeats. User can adjust time, pause and start the timer.

import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import math
import winsound
import os.path
from pathlib import Path

class Timer:
    def __init__(self,master):
        self.master = master
        master.title('Eye Saver')
        master.resizable(0,0)

        width = 220 # width of master
        height = 150 # height of master

        #Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        #Calculate x and y coordinates for the Tk master window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        #Set master dimensions and placement
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #master.grid_columnconfigure(0, minsize=100)
        #master.grid_columnconfigure(1, minsize=100)
        #master.grid_columnconfigure(2, minsize=100)
        
        self.timer_state = 'off'

        #Create a label for the timer
        self.timer_label = tk.Label(master,font=('Helvetica','35'),fg='#1ec7ae')
        #Display default timer of 20 minutes upon start up
        self.timer_label.config(text='20:00')
        self.timer_label.pack(side='top',pady=5)

        #Create a container for the buttons
        self.button_container = tk.Label(master)
        self.button_container.pack(side='top')

        #Start button
        self.start_button = tk.Button(self.button_container,text='Start',font=('Helvetica','10'),command = self.start,)
        self.start_button.grid(row=0,column=2)

        #Pause button
        self.pause_button = tk.Button(self.button_container,text='Pause',font=('Helvetica','10'),command=self.pause,state='disabled')
        self.pause_button.grid(row=0,column=1,padx=5)
        
        #Adjust timer button
        self.adjust_timer_button = tk.Button(self.button_container,text='Adjust timer',font=('Helvetica','10'),command=self.adjust_timer)
        self.adjust_timer_button.grid(row=0,column=0)

        #Message field
        self.message_label = tk.Label(master,font=('Helvetica','15'),text='Hi! Ready to work?')
        self.message_label.pack(pady=10)
        
        #self.message_label.grid(row=2,column=0,columnspan = 3,pady=20)

        #Timer setpoint variables, set to default of 20 mins
        self.mins_setpoint = 20
        self.secs_setpoint = 0

        #Timer variables that count down the time, set to default of 20 mins
        self.minutes = 20
        self.seconds = 0

        #Break timer duration
        self.break_timer = 20

    def adjust_timer(self):
        
        self.pause()
        self.timer_state = 'off'

        valid_input = False

        while not valid_input: 

            time_input = simpledialog.askfloat('Adjust Timer','Enter timer duration in minutes to\n1 decimal place (60 minute maximum):',parent=self.master)
            #Check if the user selected cancel, time_input will be NoneType
            if time_input is None:
                break
            #If input is valid, assign the new time and display the new time, ensure pause button is active
            if time_input >0 and time_input <= 60.0:
                valid_input = True
                
                self.mins_setpoint = int(math.modf(time_input)[1])
                self.secs_setpoint = int(math.modf(time_input)[0]*60)
                
                self.timer_label.config(text="{:02d}:{:02d}".format(self.mins_setpoint,self.secs_setpoint))
                #self.pause_button['state'] = 'normal'
    
    def start(self):
        #Change message box
        self.message_label['text'] = 'Go time!'
        self.message_label['fg'] = '#32a88d'

        #Disable the start button
        self.start_button['state'] = 'disabled'
        #Enable the pause button
        self.pause_button['state'] = 'normal'
        #Enable the adjust timer button
        self.adjust_timer_button['state'] = 'normal'
        
        #If start button is hit from a paused state, do not reassign variables, if it's from 'no' state
        #then populate the countdown variables with the self.mins and self.secs values
        if self.timer_state != 'paused':
            self.minutes = self.mins_setpoint
            self.seconds = self.secs_setpoint
        
        self.timer_state = 'running'
        self.decrease_timer()
    
    def decrease_timer(self):
        #Update the timer display with the current timer variables
        self.timer_label['text'] = "{:02d}:{:02d}".format(self.minutes,self.seconds)
        
        if self.timer_state == 'running':
            #Check if timer is at zero, if it is invoke the twenty_secs function
            if self.minutes ==0 and self.seconds == 0:
                self.timer_state = 'off'
                self.play_sound()
                #Make the timer appear when it is time to break
                self.master.wm_attributes("-topmost", 1)
                self.master.wm_attributes("-topmost", 0)
                self.timer_label.after(1000, self.twenty_secs)

            else:
                if self.seconds == 0:
                    self.minutes -= 1
                    self.seconds = 59
                else:
                    self.seconds -= 1

                self.timer_label.after(1000, self.decrease_timer)
        
    #Function to countdown 20 seconds when the timer is up
    def twenty_secs(self):
        
        #Change message box
        self.message_label['text'] = 'Take a screen break!'
        self.message_label['fg'] = '#b3365b'
        
        #Disable all buttons
        self.adjust_timer_button['state'] = 'disabled'
        self.pause_button['state'] = 'disabled'
        self.start_button['state'] = 'disabled'

        self.timer_label.config(text="00:{:02d}".format(self.break_timer))

        if self.break_timer > 0:
            self.break_timer -= 1
            self.master.after(1000,self.twenty_secs)
        else:
            #Reset the break timer
            self.break_timer = 5
            self.timer_state = 'running'
            #Make the timer appear when it is time to work again
            self.master.wm_attributes("-topmost", 1)
            self.master.wm_attributes("-topmost", 0)
            self.play_sound()
            self.master.after(1000,self.start)
            
    def play_sound(self):
        
        path1 = Path(__file__).parent.absolute()
        file_location = os.path.join(path1,"chime.wav")
        winsound.PlaySound(file_location, winsound.SND_FILENAME|winsound.SND_ASYNC)
    
    def pause(self):
        #Change message box
        self.message_label['text'] = "I'll wait here!"
        self.message_label['fg'] = '#4275bd'
        #Deactive pause button
        self.pause_button['state'] = 'disabled'
        #Activate start button
        self.start_button['state'] = 'normal'
        self.timer_state = 'paused'

root = tk.Tk()
the_timer = Timer(root)
root.mainloop()