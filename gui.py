import tkinter as tk
from tkinter import ttk
from backend import chat_history, ai_response
import json
import sv_ttk
import sys
from mood_graph import mood_graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    with open("preferences.json", 'r') as f:
        preferences = json.load(f)
except FileNotFoundError:
    with open("preferences.json", 'w') as f:
        json.dump(preferences, f)

def window_closed(event):
    with open("preferences.json", 'w') as f:
        json.dump(preferences, f)

def change_theme():
    if sv_ttk.get_theme() == "light":
        sv_ttk.set_theme("dark")
        preferences["theme"] = "dark"
    else:
        sv_ttk.set_theme("light")
        preferences["theme"] = "light"

def end():
    root.destroy()

def on_send_button_click():
    user_message = input_text_box.get()
    if user_message:
        input_text_box.delete(0, tk.END)
        if sv_ttk.get_theme() == "light":
            user_message_frame = tk.Frame(chat_frame, bg="white")
            user_message_label = tk.Label(user_message_frame, text=user_message, bg="lightblue", fg = "black", wraplength=250, anchor='e', justify='right')
            user_message_label.pack(side=tk.RIGHT, padx=10, pady=5)
            user_message_frame.pack(anchor='e', fill=tk.BOTH)

            response_message = ai_response(chat_history, user_message)
            response_frame = tk.Frame(chat_frame, bg="white")
            response_label = tk.Label(response_frame, text=response_message[11:], bg="lightgreen", fg = "black", wraplength=250, anchor='w', justify='left')
            response_label.pack(side=tk.LEFT, padx=10, pady=5)
            response_frame.pack(anchor='w', fill=tk.X)
        else:
            user_message_frame = tk.Frame(chat_frame, bg="#3C3A3D")
            user_message_label = tk.Label(user_message_frame, text=user_message, bg="lightblue", fg = "black", wraplength=250, anchor='e', justify='right')
            user_message_label.pack(side=tk.RIGHT, padx=10, pady=5)
            user_message_frame.pack(anchor='e', fill=tk.BOTH)

            response_message = ai_response(chat_history, user_message)
            response_frame = tk.Frame(chat_frame, bg="#3C3A3D")
            response_label = tk.Label(response_frame, text=response_message[11:], bg="lightgreen", fg = "black", wraplength=250, anchor='w', justify='left')
            response_label.pack(side=tk.LEFT, padx=10, pady=5)
            response_frame.pack(anchor='w', fill=tk.X)
        chat_display.update_idletasks()
        chat_display.yview_moveto(1.0)

def on_frame_configure(event):
    chat_display.config(scrollregion=chat_display.bbox("all"))

def on_canvas_configure(event):
    chat_display.itemconfig(chat_window_id, width=event.width)

def settings():
    def nameee():
        preferences['theme'] = sv_ttk.get_theme()

    popup = tk.Toplevel()
    popup.grab_set()
    popup.title("Settings")
    popup.geometry("400x300")   
    tabControl = ttk.Notebook(popup) 

    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 

    tabControl.add(tab1, text='Appearance') 
    tabControl.pack(expand=1, fill="both") 

    theme_frame = tk.Label(tab1)
    theme_frame.pack(side=tk.TOP, anchor="nw")
    theme = tk.Checkbutton(theme_frame, command=change_theme)
    theme.grid(column=0, row=0)
    theme_text = tk.Label(theme_frame, text="Toggle the dark or light mode")
    theme_text.grid(column=1, row=0)
    save = tk.Button(tab1, text="Save", command=popup.destroy)     
    save.pack(side=tk.BOTTOM, anchor="se", padx=15, pady=15)
# Initialize the main window

def moodGraph():
    graph = tk.Toplevel()
    graph.title("My Mood Graph")
    graph.geometry("800x600")
    fig = mood_graph()
    print(type(mood_graph()))
    # Create a canvas and add the figure to it
    canvas = FigureCanvasTkAgg(fig, master=graph)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root = tk.Tk()
sv_ttk.set_theme(preferences["theme"])
root.update_idletasks()

root.title("Chat GUI")
root.geometry('500x700')
style = ttk.Style()
style.configure("TLabel", foreground="black")
style.configure("TButton", foreground= "black")
style.configure("TEntry", foreground = "black")

menu_bar = tk.Menu(root)
menu_bar.config(borderwidth = 0)
menu_frame = tk.Frame(root, background="white")
menu_frame.pack(side=tk.LEFT, fill=tk.BOTH)


file = tk.Menu(menu_bar, tearoff = 0) 
menu_bar.add_cascade(label ='Settings', menu = file)
file.add_command(label ='Preferences', command = settings) 
file.add_separator() 
file.add_command(label ='Exit', command = root.destroy)

you = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "You", menu = you)
you.add_command(label = "Your Mood Graph", command = moodGraph)
if sv_ttk.get_theme() == "light":
    chat_display = tk.Canvas(root, bg="white")
else:
    sv_ttk.get_theme() == "dark"
    chat_display = tk.Canvas(root, bg="#3C3A3D")   
chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.config(yscrollcommand=scrollbar.set)

chat_frame = tk.Frame(chat_display)
chat_window_id = chat_display.create_window((0, 0), window=chat_frame, anchor="nw")

chat_frame.bind("<Configure>", on_frame_configure)
chat_display.bind("<Configure>", on_canvas_configure)

input_text_box = tk.Entry(root, width=50)
input_text_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
input_text_box_style = ttk.Style()
input_text_box_style.configure("Rounded.TEntry", borderwidth=10, relief="sunken", padding=(5, 5))


send_button = tk.Button(root, text="Send", command=on_send_button_click)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)
root.config(menu = menu_bar)
# Start the main event loop
root.bind("<Destroy>", window_closed)
root.mainloop()
