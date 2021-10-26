from tkinter import *
from tkinter import messagebox
import pygame
from datetime import datetime
from win10toast import ToastNotifier


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Alarm Clock")
        self.root.iconbitmap("C:/Users/paula/PycharmProjects/AlarmClock/alarm.ico")
        self.root.config(bg='white')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # make the main window pop on the middle of the screen
        y = (screen_height / 2) - (300 / 2)
        self.root.geometry(f'{500}x{300}+{int(x)}+{int(y)}')

        self.toaster = ToastNotifier()

    @staticmethod
    def validate_time(time):
        if len(time) != 11:
            raise Exception("Invalid time format!")
        if int(time[0:2]) > 12:
            raise Exception("Invalid hour format!")
        if int(time[3:5]) > 59:
            raise Exception("Invalid minute format!")
        if int(time[6:8]) > 59:
            raise Exception("Invalid second format!")
        return True

    def write_message(self, arg):
        self.message_entry.config(state=NORMAL)
        self.message_entry.delete(0, END)
        self.message_entry.config(fg='orange', font=('Arial', 15, 'bold'))

    def set_alarm_entry(self, arg):
        self.set_alarm()

    def set_alarm(self):
        alarm_time = self.alarm_entry.get()

        self.alarm_entry.delete(0, END)

        try:
            self.validate_time(alarm_time)
            self.root.iconify()
            self.wait_alarm(alarm_time)
        except Exception as e:
            messagebox.showerror('Error', e)

    def wait_alarm(self, alarm_time):
        message = self.message_entry.get()
        self.message_entry.delete(0, END)
        while True:
            now_time = datetime.now()
            current_hour = now_time.strftime("%I")          # Hour (12-hour clock) as a zero-padded decimal number.
            current_minutes = now_time.strftime("%M")       # Minute as a zero-padded decimal number
            current_seconds = now_time.strftime("%S")       # Second as a zero-padded decimal number.
            current_period = now_time.strftime("%p")        # Locale’s equivalent of either AM or PM.

            if alarm_time[9:].upper() == current_period:
                if alarm_time[0:2] == current_hour:
                    if alarm_time[3:5] == current_minutes:
                        if alarm_time[6:8] == current_seconds:
                            pygame.mixer.init()
                            pygame.mixer.music.load("C:/Users/paula/PycharmProjects/AlarmClock/alarm.wav")
                            pygame.mixer.music.play()
                            self.toaster.show_toast('Alarm!', message, icon_path="C:/Users/paula/PycharmProjects/AlarmClock/alarm.ico", duration=20, threaded=True)
                            break

    def start(self):
        alarm_frame = Frame(self.root, bg='white')
        alarm_frame.pack(pady=20)

        self.message_entry = Entry(alarm_frame, justify='center', bg='white', width=30, border=3, fg='black', font=('Arial', 8))
        self.message_entry.insert(0, "Click to write a message")
        self.message_entry.pack()
        self.message_entry.config(state='readonly')
        self.message_entry.bind('<ButtonPress-1>', self.write_message)

        message_label = Label(alarm_frame, text='Introduce alarm message ↑', bg='white', fg='orange', font=('Arial', 15, 'bold'))
        message_label.pack(pady=5)

        self.alarm_entry = Entry(alarm_frame, justify='center', bg='white', width=30, border=3, fg='orange', font=('Arial', 15, 'bold'))
        self.alarm_entry.pack(pady=10)
        self.alarm_entry.bind('<Return>', self.set_alarm_entry)

        alarm_label = Label(alarm_frame, text='Format: HH:MM:SS AM/PM', bg='white', fg='orange', font=('Arial', 15, 'bold'))
        alarm_label.pack()

        self.alarm_button = Button(alarm_frame, bg='white', fg='orange', text='Set alarm', font=('Arial', 15, 'bold'), command=self.set_alarm)
        self.alarm_button.pack(pady=15)

        self.root.mainloop()
