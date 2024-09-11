import tkinter as tk
from tkinter import ttk, messagebox
from backend import chat_history, ai_response, save_chat_history
from mood_tracker import save_mood_score
import json
import sv_ttk
import sys
from mood_graph import mood_graph
from tkinter import font as tkfont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import subprocess
import os
preferences = {"theme": ["dark", "#3C3A3D"],"firstTime" : True}

try:
    with open("preferences.json", 'r') as f:
        preferences = json.load(f)
except FileNotFoundError:
    with open("preferences.json", 'w') as f:
        pass
batch_script = "safe.bat"
if preferences["firstTime"]:
    print("running bat")
    subprocess.run([batch_script], shell=True)
else:
    pass

def save_theme():
    with open("preferences.json", 'w') as f:
        json.dump(preferences, f)
    chat_frame.update_idletasks()
    popup.destroy()

def window_closed(event=None):
    messagebox.showinfo("Byebye", "Chat has been saved!")
    root.destroy()
def change_theme():
    if sv_ttk.get_theme() == "light":
        sv_ttk.set_theme("dark")
        preferences["theme"] = ["dark", "#3C3A3D"]
    else:
        sv_ttk.set_theme("light")
        preferences["theme"] = ["light", "white"]

def on_submit_button_click():
    try:
        token = token_entry.get()
        token_ = {"GROQ_API_KEY": token}
        with open(".env", "w") as f:
            for k,v in token_.items():
                f.write(f'{k}="{v}"\n')
        # Show success message
        messagebox.showinfo("Success", "API Key has been successfully saved. Please reopen the application for effects to take place. It will not work if this step is not done.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




def on_send_button_click(event=None):
    user_message = input_text_box.get()
    if user_message:
        input_text_box.delete(0, tk.END)
        # Create user message frame
        user_message_frame = tk.Frame(chat_frame, bg=preferences["theme"][1])
        user_message_label = tk.Label(user_message_frame, text=user_message, bg="lightblue", fg="black", wraplength=250, anchor='e', justify='right', font=font_style)
        user_message_label.pack(side=tk.RIGHT, padx=10, pady=5)
        user_message_frame.pack(anchor='e', fill=tk.BOTH)

        try:# Create response message frame
            response_message = ai_response(chat_history, user_message)
        except Exception as e:
            response_message = e
        response_frame = tk.Frame(chat_frame, bg=preferences["theme"][1])
        response_label = tk.Label(response_frame, text=response_message, bg="lightgreen", fg="black", wraplength=250, anchor='w', justify='left', font=font_style)
        response_label.pack(side=tk.LEFT, padx=10, pady=5)
        response_frame.pack(anchor='w', fill=tk.X)

        # Update the canvas scroll region and view
        chat_display.update_idletasks()
        chat_display.yview_moveto(1.0)

def on_frame_configure(event):
    chat_display.config(scrollregion=chat_display.bbox("all"))

def on_canvas_configure(event):
    chat_display.itemconfig(chat_window_id, width=event.width)

def onBoarding():
    pop = tk.Toplevel()
    pop.grab_set()
    pop.title("Onboarding")
    pop.geometry("370x190")
    pop.resizable(False, False)  # Prevent resizing of the onboarding window
    
    # Create a canvas to hold the pages 
    canvas = tk.Canvas(pop, bg="#3C3A3D")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the pages inside the canvas
    page_frame = tk.Frame(canvas, bg="#3C3A3D")
    canvas.create_window((0, 0), window=page_frame, anchor='nw')

    def on_canvas_resize(event):
        canvas.config(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_resize)

    def show_page1():
    # Clear the page frame
        for widget in page_frame.winfo_children():
            widget.destroy()

    # Create a centering frame inside page_frame using grid
        center_frame = tk.Frame(page_frame, bg="#3C3A3D")
        center_frame.grid(row=0, column=0, sticky='nsew')

    # Ensure the center_frame expands to fill the page_frame
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)

    # Page 1 content with enhanced visibility
        title = tk.Label(center_frame, text="Welcome to the App!", font=("Helvetica", 16, "bold"), bg="#3C3A3D", fg="black")
        title.grid(row=0, column=0, pady=20, sticky='n')

        description = tk.Label(center_frame, text="This is an onboarding tutorial to help you get started.", bg="#3C3A3D", fg="black", font=("Helvetica", 12))
        description.grid(row=1, column=0, pady=10)

        next_button = tk.Button(center_frame, text="Next", command=show_page2, font=("Helvetica", 12, "bold"), bg="lightblue", fg="black")
        next_button.grid(row=2, column=0, pady=20)

    # Set canvas background color explicitly
        canvas.config(bg="white")

    # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        print("Current theme:", sv_ttk.get_theme())
    # Debugging: Print widget properties to ensure colors are set correctly
        print(f"Title text color: {title.cget('fg')}")
        print(f"Description text color: {description.cget('fg')}")
        print(f"Next button text color: {next_button.cget('fg')}")


    def show_page2():
        pop.geometry("200x400")
        # Clear the page frame
        for widget in page_frame.winfo_children():
            widget.destroy()

        # Create a centering frame inside page_frame using grid
        center_frame = tk.Frame(page_frame, bg="white")
        center_frame.grid(row=0, column=0, sticky='nsew')

        # Ensure the center_frame expands to fill the page_frame
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)

        # Page 2 content
        settings_label = tk.Label(center_frame, text="Settings", font=("Helvetica", 16), bg="white", fg="black")
        settings_label.grid(row=0, column=0, pady=20, sticky='n')

        settings_description = tk.Label(center_frame, text="Configure your preferences here.", bg="white", fg="black")
        settings_description.grid(row=1, column=0, pady=10)

        theme_label = tk.Label(center_frame, text="Choose Theme:", bg="white", fg="black")
        theme_label.grid(row=2, column=0, pady=5)
        
        def light():
            sv_ttk.set_theme("light")
            preferences["theme"] = ["light", "white"]
        def dark():
            sv_ttk.set_theme("dark")
            preferences["theme"] = ["dark", "#3C3A3D"]
         
        theme_light = tk.Radiobutton(center_frame, text="Light", value="light", command=light, bg="white", fg="black")
        theme_light.grid(row=3, column=0, pady=5, sticky='w')
    
        theme_dark = tk.Radiobutton(center_frame, text="Dark", value="dark", command=dark, bg="white", fg="black")
        theme_dark.grid(row=4, column=0, pady=5, sticky='w')


        save_button = tk.Button(center_frame, text="Save Settings", command=save_theme, font=("Helvetica", 12))
        save_button.grid(row=5, column=0, pady=20)

        back_button = tk.Button(center_frame, text="Back", command=show_page1, font=("Helvetica", 12))
        back_button.grid(row=6, column=0, pady=5)

        next_button = tk.Button(center_frame, text="Next", command=show_page3, font=("Helvetica", 12))
        next_button.grid(row=7, column=0, pady=20)

        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def show_page3():
        global token_entry
        pop.geometry("290x400")
        # Clear the page frame
        for widget in page_frame.winfo_children():
            widget.destroy()

        # Create a centering frame inside page_frame using grid
        center_frame = tk.Frame(page_frame, bg="white")
        center_frame.grid(row=0, column=0, sticky='nsew')

        # Ensure the center_frame expands to fill the page_frame
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)

        # Page 3 content
        instructions_label = tk.Label(center_frame, text="To complete the setup, please visit the following website and create an API key", font=("Helvetica", 16), bg="white", fg="black", wraplength=300)
        instructions_label.grid(row=0, column=0, pady=20, sticky='n')
        
        website_link = tk.Label(center_frame, text="https://console.groq.com/keys", font=("Helvetica", 14), bg="white", fg="blue", cursor="hand2")
        website_link.grid(row=1, column=0, pady=10)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("https://console.groq.com/keys"))

        token_label = tk.Label(center_frame, text="Enter your API Key:", font=("Helvetica", 14), bg="white", fg="black")
        token_label.grid(row=2, column=0, pady=10, sticky='w')

        token_entry = tk.Entry(center_frame, font=("Helvetica", 12))
        token_entry.grid(row=3, column=0, pady=10, sticky='ew')

        submit_button = tk.Button(center_frame, text="Submit", command=on_submit_button_click, font=("Helvetica", 12))
        submit_button.grid(row=4, column=0, pady=20)

        done_button = tk.Button(center_frame, text="Done", command=pop.destroy, font=("Helvetica", 12))
        done_button.grid(row=5, column=0, pady=20)
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Start with page 1
    show_page1()

def settings():
    global popup
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
    tabControl.add(tab2, text="Onboarding")
    tabControl.pack(expand=1, fill="both")

    theme_frame = tk.Label(tab1)
    theme_frame.pack(side=tk.TOP, anchor="nw")
    theme = tk.Checkbutton(theme_frame, command=change_theme)
    theme.grid(column=0, row=0)
    theme_text = tk.Label(theme_frame, text="Toggle the dark or light mode")
    theme_text.grid(column=1, row=0)
    onboarding_frame = tk.Label(tab2)
    onboarding_frame.grid(column=1, row=0)
    onboarding = tk.Button(onboarding_frame, text="Take the onboarding tour if you missed it", command=onBoarding)
    onboarding.grid(column=3, row=1)
    save = tk.Button(tab1, text="Save", command=save_theme)
    save.pack(side=tk.BOTTOM, anchor="se", padx=15, pady=15)

def moodGraph():
    graph = tk.Toplevel()
    graph.title("My Mood Graph")
    graph.geometry("800x600")
    save_mood_score()
    fig = mood_graph()
    canvas = FigureCanvasTkAgg(fig, master=graph)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Initialize the main window
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", window_closed)
sv_ttk.set_theme(preferences["theme"][0])
root.update_idletasks()
font_size = 12
font_style = tkfont.Font(size=font_size)
root.title("Chat GUI")
root.geometry('500x700')
style = ttk.Style()
if preferences["firstTime"]:
    onBoarding()
    preferences["firstTime"] = False
    with open('preferences.json','w') as f:
        json.dump(preferences,f)

# Menu bar
menu_bar = tk.Menu(root)
menu_bar.config(borderwidth=0)
menu_frame = tk.Frame(root, background=preferences["theme"][1])
menu_frame.pack(side=tk.LEFT, fill=tk.BOTH)

file = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Settings', menu=file)
file.add_command(label='Preferences', command=settings)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

you = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="You", menu=you)
you.add_command(label="Your Mood Graph", command=moodGraph)

# Canvas for chat messages
chat_display = tk.Canvas(root, bg=preferences["theme"][1])
chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.config(yscrollcommand=scrollbar.set)

chat_frame = tk.Frame(chat_display)
chat_window_id = chat_display.create_window((0, 0), window=chat_frame, anchor="nw")

chat_frame.bind("<Configure>", on_frame_configure)
chat_display.bind("<Configure>", on_canvas_configure)

# Input and send button
entry_font_size = 12
button_font_size = 10

input_text_box = tk.Entry(root, width=40, font=("Helvetica", entry_font_size))
input_text_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

input_text_box_style = ttk.Style()
input_text_box_style.configure("Rounded.TEntry", borderwidth=10, relief="sunken", padding=(5, 5))

send_button = tk.Button(root, text="Send", command=on_send_button_click, font=("Helvetica", button_font_size), width=7, height=2)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.config(menu=menu_bar)
root.bind("<Return>", on_send_button_click)


root.mainloop()
