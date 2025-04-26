import tkinter as tk
import webbrowser

# Dictionary of website names and URLs
sites = {
    "YouTube": "https://www.youtube.com",
    "Google": "https://www.google.com",
    "Amazon": "https://www.amazon.com",
    "Play Store": "https://play.google.com"
}

# Function to open the URL
def open_site(url):
    webbrowser.open(url)

# Create GUI window
root = tk.Tk()
root.title("Open Website Links")
root.geometry("300x250")
root.config(bg="#f0f0f0")

# Heading label
label = tk.Label(root, text="Click a site to open", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
label.pack(pady=10)

# Create a button for each site
for name, url in sites.items():
    btn = tk.Button(root, text=name, font=("Arial", 12), width=20, command=lambda url=url: open_site(url))
    btn.pack(pady=5)

# Run the GUI
root.mainloop()
