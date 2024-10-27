import requests
import json
import pyperclip
import time
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext

# Enter your VT API key belonging to your account
API_KEY = 'ENTER YOUR KEY HERE'

# see https://docs.virustotal.com/reference/ip-info
def scan_ip(ip):
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {"x-apikey": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()

def update_gui(widget, new_text):
    #unlock widget
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, new_text + '\n')
    #relock it
    widget.config(state=tk.DISABLED)
    widget.see(tk.END)

def main(text_widget):
    last_ip = ""
    while True:
        # for free account api call limit
        time.sleep(15)
        clipboard_ip = pyperclip.paste()
        if clipboard_ip != last_ip:
            try:
                result = scan_ip(clipboard_ip)
                # Filter the result to only show relevant information
                filtered_result = {
                    "IP": result.get("data", {}).get("id"),
                    "whois": result.get("data", {}).get("whois"),
                    "location": result.get("data", {}).get("continent"),
                    "Last Analysis Stats": result.get("data", {}).get("attributes", {}).get("last_analysis_stats"),
                }
                update_gui(text_widget, json.dumps(filtered_result, indent=4))
                last_ip = clipboard_ip
            except Exception as e:
                update_gui(text_widget, f"Error: {e}")

if __name__ == "__main__":
    if API_KEY == 'ENTER YOUR KEY HERE':
        raise "Enter your API key first"

    gui = tk.Tk()
    gui.title("IP Scanner")
    gui.geometry("500x600")
    text = scrolledtext.ScrolledText(gui, bg='black', fg='white', font=("Courier", 11))
    text.pack(fill=tk.BOTH, expand=True)
    thread = Thread(target=main, args=(text,))
    thread.start()
    gui.mainloop()