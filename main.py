import tkinter as tk
#from customtkinter import *
from tkinter import ttk
import openai
import pyperclip
import time
from tkinter import StringVar
from gtts import gTTS
import playsound
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.api_key = ''
        self.request_var = StringVar()
        self.voice_switch_status = StringVar()
        self.voice_option = StringVar()
        self.voice_lang = StringVar()
        self.languages = ("de", "en", "cs", "pl", "sk")
        self.language = 'de'
        self.sound = False

        # configure window
        self.title("Desktop ChatBot")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ttk.Frame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ttk.Label(self.sidebar_frame, text="Desktop ChatBot", font=("Helvetica", 18))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.copy_btn = ttk.Button(self.sidebar_frame, text="Copy conversation", command=lambda: self.clipboard_copy(self.textbox.get("0.0", "end")))
        self.copy_btn.grid(row=1, column=0, padx=20, pady=10)

        self.print_btn = ttk.Button(self.sidebar_frame, text="Save conversation", command=self.pdf_printer)
        self.print_btn.grid(row=2, column=0, padx=20, pady=10)

        self.clear_btn = ttk.Button(self.sidebar_frame, text="Clear conversation", command=self.clear)
        self.clear_btn.grid(row=3, column=0, padx=20, pady=10)

        self.language_mode_label = ttk.Label(self.sidebar_frame, text="Voice Language:", anchor="w")
        self.language_mode_label.grid(row=9, column=0, padx=20, pady=(0, 0))

        self.language_mode_option_menu = ttk.OptionMenu(self.sidebar_frame, self.voice_lang, self.languages[0], *self.languages, command=self.change_language_mode_event)
        self.language_mode_option_menu.grid(row=10, column=0, padx=20, pady=(0, 0))

        self.voice_switch = ttk.Checkbutton(self.sidebar_frame, text="Voice", command=self.voice_select, variable=self.voice_switch_status, onvalue="On", offvalue="Off")
        self.voice_switch.grid(row=11, column=0, padx=20, pady=(20, 20))

        self.exit_btn = ttk.Button(self.sidebar_frame, text="Exit", width=20, command=self.destroy)
        self.exit_btn.grid(row=12, column=0, padx=20, pady=(20, 20))

        # create main entry and button
        self.entry = ttk.Entry(self, textvariable=self.request_var)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")

        self.send_btn = ttk.Button(master=self, text="Send Question", command=lambda: self.chatAI(self.request_var.get()))
        self.send_btn.grid(row=4, column=1, padx=(20, 20), pady=(0, 20), sticky="nsew")

        # create textbox
        self.textbox = tk.Text(self, width=300, font=("Helvetica", 18))
        self.textbox.grid(row=0, rowspan=3, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        #self.textbox.insert(0.0, 'Welcome')

    def change_language_mode_event(self, new_language_mode: str):
        self.language = new_language_mode

    def pdf_printer(self):
        try:
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
            text_file = f'conversation{timestamp}.txt'
            text_file_opn = open(text_file, "w", encoding="utf-8")
            text_file_opn.write(self.textbox.get(0.0, 'end'))
            text_file_opn.close()
        except Exception as e:
            self.textbox.insert(0.0, 'Sorry there was a problem with saving the text into a text file.\n' + str(e) + '\n')
            self.textbox.insert(0.0, '\nError:\n')

    def clear(self):
        self.textbox.delete(0.0, 'end')

    def clipboard_copy(self, text):
        pyperclip.copy(text)

    def voice_select(self):
        temp_status = self.voice_switch_status.get()
        if temp_status == 'On':
            self.sound = True
        elif temp_status == 'Off':
            self.sound = False
        else:
            pass

    @staticmethod
    def response_audio(audio, lang):
        tts = gTTS(text=audio, lang=lang)
        file = 'audio.mp3'
        tts.save(file)
        playsound.playsound(file)
        os.remove(file)

    def chatAI(self, request):
        try:
            if request != '':
                response = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=1024, api_key=self.api_key)
                answer = response.choices[0].text
                self.textbox.insert(0.0, self.request_var.get() + '\n')
                self.textbox.insert(0.0, '\nQuestion:\n')
                self.textbox.insert(0.0,  answer + '\n')
                self.textbox.insert(0.0, '\nAnswer:\n')
                if self.sound:
                    self.response_audio(answer, self.language)
                self.entry.delete(0, 'end')
            else:
                self.textbox.insert(0.0, 'Please enter any statement!\n')
                self.textbox.insert(0.0, '\nAnswer:\n')
        except Exception as e:
            self.textbox.insert(0.0, 'Sorry there is something wrong, first please check your internet connection or try again later.\n' + str(e) + '\n')
            self.textbox.insert(0.0, '\nAnswer:\n')

if __name__ == "__main__":
    app = App()
    app.mainloop()