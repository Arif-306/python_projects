import customtkinter as ctk
import random
import json
import speech_recognition as sr
import pyttsx3
from tkinter import scrolledtext
import os
from PIL import Image  # Icons ke liye


# Initialize Tkinter
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("ALPHA Bot")
app.iconbitmap("chatbot.ico")  # Ensure "chatbot.ico" exists
app.geometry("700x450")  # Bigger window for sidebar

# Initialize TTS Engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # 0 for Male, 1 for Female

# AI Responses List
bot_responses = [
    "Hello! How can I assist you?",
    "I'm here to help! Tell me what you need.",
    "That's interesting! Can you elaborate?",
    "I'm not sure, but I can try to find out.",
    "Can you provide more details?",
    "Let me think... 🤔"
]

# Chat History File
CHAT_HISTORY_FILE = "chat_history.json"
user_name = None  # Store user name globally

# Function to Save Chat History
def save_chat_history():
    chat_data = chat_text.get("1.0", "end").strip()
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump({"history": chat_data}, f)

# Function to Load Chat History
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data.get("history", "")
    return ""

# Function to Show Chat History in Popup Window
def show_chat_history():
    history_window = ctk.CTkToplevel(app)
    history_window.title("Chat History")
    history_window.geometry("500x400")
    history_window.configure(fg_color="black")

    history_frame = ctk.CTkFrame(history_window, fg_color="black", border_width=2, border_color="green")
    history_frame.pack(pady=10, padx=10, fill="both", expand=True)

    history_text = scrolledtext.ScrolledText(history_frame, wrap="word", bg="black", fg="lime",
                                             font=("Courier", 12), state="normal")
    history_text.pack(padx=10, pady=10, fill="both", expand=True)

    previous_chat = load_chat_history()
    history_text.insert("1.0", previous_chat if previous_chat else "No chat history found.")
    history_text.config(state="disabled")

# Function to Show Messages in Chatbox
def show_message(sender, message):
    chat_text.config(state="normal")
    chat_text.insert("end", f"> {sender}: {message}\n", sender)
    chat_text.config(state="disabled")
    chat_text.yview("end")

    app.after(10, save_chat_history)

# Function to Speak Text
import threading

def speak(text):
    def run_tts():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run_tts).start()


# Function to Send Message
def send_message():
    global user_name

    user_text = user_input.get().strip()
    user_input.delete(0, "end")

    if not user_name:
        if user_text:
            user_name = user_text
            welcome_message = f"Nice to meet you, {user_name}! How can I help you today?"
            show_message("ALPHA", welcome_message)
            speak(welcome_message)
        else:
            show_message("ALPHA", "Please enter your name first.")
            speak("Please enter your name first.")
        return

    if user_text:
        show_message(user_name, user_text)
        bot_reply = random.choice(bot_responses)
        show_message("ALPHA", bot_reply)

        app.after(500, lambda: speak(bot_reply))

# Function to Get Voice Input
def get_voice_input():
    if not user_name:
        show_message("ALPHA", "Please enter your name first.")
        speak("Please enter your name first.")
        return

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        show_message("ALPHA", "Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            user_text = recognizer.recognize_google(audio)
            user_input.delete(0, "end")
            user_input.insert(0, user_text)
            send_message()
        except sr.UnknownValueError:
            show_message("ALPHA", "Sorry, I didn't catch that.")
            app.after(500, lambda: speak("Sorry, I didn't catch that."))
        except sr.RequestError:
            show_message("ALPHA", "Network error, please try again.")
            app.after(500, lambda: speak("Network error, please try again."))

# 🔹 Sidebar Frame
sidebar = ctk.CTkFrame(app, width=50, height=450, fg_color="#1C1C1C")
sidebar.pack(side="left", fill="y")

# 🔹 Function to Load Icons
def load_icon(path, size=(30, 30)):
    return ctk.CTkImage(light_image=Image.open(path), size=size)

icons = {
    "profile": load_icon("profile.png"),
    "home": load_icon("home.png"),
    "chat": load_icon("chat.png"),
    "settings": load_icon("setting.png"),
    "clearchats": load_icon("clearchats.png"),
    "theme": load_icon("theme.png"),
    "help": load_icon("help.png"),
    "exit": load_icon("exit.png"),
}

# 🔹 Sidebar Buttons
profile_button = ctk.CTkButton(sidebar, image=icons["profile"], text="", width=30, height=30, fg_color="transparent",
                               command=lambda: show_message("ALPHA", f"User: {user_name if user_name else 'Not Set'}"))
profile_button.pack(pady=10)

home_button = ctk.CTkButton(sidebar, image=icons["home"], text="", width=30, height=30, fg_color="transparent")
home_button.pack(pady=10)

chat_button = ctk.CTkButton(sidebar, image=icons["chat"], text="", width=30, height=30, fg_color="transparent")
chat_button.pack(pady=10)

settings_button = ctk.CTkButton(sidebar, image=icons["settings"], text="", width=30, height=30, fg_color="transparent")
settings_button.pack(pady=10)



def toggle_theme():
    current_theme = ctk.get_appearance_mode()
    new_theme = "dark" if current_theme == "light" else "light"
    ctk.set_appearance_mode(new_theme)

theme_button = ctk.CTkButton(sidebar, image=icons["theme"], text="", width=30, height=30, fg_color="transparent",
                             command=toggle_theme)
theme_button.pack(pady=10)

def clear_chat():
    chat_text.config(state="normal")
    chat_text.delete("1.0", "end")
    chat_text.config(state="disabled")

clear_button = ctk.CTkButton(sidebar, image=icons["clearchats"], text="", width=30, height=30, fg_color="transparent",
                             command=clear_chat)
clear_button.pack(pady=10)

def show_help():
    show_message("ALPHA", "Use sidebar buttons for settings and commands.")

help_button = ctk.CTkButton(sidebar, image=icons["help"], text="", width=30, height=30, fg_color="transparent",
                            command=show_help)
help_button.pack(pady=10)

exit_button = ctk.CTkButton(sidebar, image=icons["exit"], text="", width=30, height=30, fg_color="red",
                            command=app.quit)
exit_button.pack(pady=10)

# Chat Frame
chat_frame = ctk.CTkFrame(app, fg_color="black", border_width=2, border_color="green")
chat_frame.pack(pady=10, padx=20, fill="both", expand=True)

chat_text = scrolledtext.ScrolledText(chat_frame, wrap="word", bg="black", fg="lime",
                                      font=("Courier", 14), state="normal", height=15)
chat_text.pack(padx=10, pady=10, fill="both", expand=True)

chat_text.config(state="disabled")

# Input Field
user_input = ctk.CTkEntry(app, placeholder_text="Type your name...", width=400, text_color="lime")
user_input.pack(pady=10)

# Button Frame
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(fill="x", padx=10, pady=10)

# Show History Button
history_button = ctk.CTkButton(button_frame, text="Show History", fg_color="black", hover_color="blue",
                               text_color="white", width=120, height=35, command=show_chat_history)
history_button.pack(side="left", padx=10, pady=5)

# Send Button
send_button = ctk.CTkButton(button_frame, text="SEND", fg_color="black", hover_color="green", text_color="lime",
                            width=80, height=35, command=send_message)
send_button.pack(side="left", padx=10, pady=5)

# Speak Button
voice_button = ctk.CTkButton(button_frame, text="Speak", fg_color="black", hover_color="green", text_color="lime",
                             width=60, height=35, command=get_voice_input)
voice_button.pack(side="right", padx=10, pady=5)

# Bind Enter Key to Send Message
app.bind("<Return>", lambda event: send_message())

# Ask for User Name on Start
def ask_user_name():
    show_message("ALPHA", "As-Salamu Alaikum! Please enter your name first.")
    app.after(1000, lambda: speak("As-Salamu Alaikum! Please enter your name first."))

app.after(1000, ask_user_name)

# Run App
app.mainloop()
