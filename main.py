import webbrowser
import customtkinter as ctk
import sys
import patchers
from app import App

def patch_spotify():
  root.open_popup("Patch Spotify",
                   "This has only been tested on Windows.\n"
                    "This is platform dependent and may not work on linux distros or MacOS.\n"
                    "Do you want to continue?", size="425x150", yes=patchers.patch_spotify)

def open_source():
  webbrowser.open_new_tab("https://github.com/TheCobraBoy2/VToolbox")

root = App(size="600x500", title="VToolBox")

CONFIG = {
  "show_welcome": True
}

CURRENT_VERSION = "1.0.0"

root.new_config(CONFIG)
root.reconcile_config()

# Home Page
home_page = root.register_page("home", flexible=True)
root.register_label("welcome", host=home_page, text="Welcome to VToolbox!",
                    font=ctk.CTkFont(size=24, weight="bold"))
root.register_label("instruction", host=home_page, text="Use the sidebar to navigate the pages.",
                    font=ctk.CTkFont(size=16))

root.place_label("welcome", row=0, column=0, pady=50, sticky="new")
root.place_label("instruction", row=1, column=0, pady=10, sticky="new")

# Patchers Page
patchers_page = root.register_page("patchers", flexible=True)
root.register_button("spicetify", host=patchers_page, text="Patch Spotify", command=patch_spotify)
root.place_button("spicetify", row=0, column=0, padx=20, pady=20, sticky="w")

# Info Page
info_page = root.register_page("info", flexible=True)
#Configuring 2nd column for button alignment
info_page.grid_columnconfigure(1, weight=1)
root.register_label("info_header", host=info_page, text=f"VToolbox v{CURRENT_VERSION}",
                    font=ctk.CTkFont(size=20, weight="bold"))
root.register_label("info_text", host=info_page,
                    text="Visit our GitHub for source code and contributions.",
                    font=ctk.CTkFont(size=14), justify="left", wraplength=400)

root.place_label("info_header", row=0, column=0, pady=(20, 10), padx=50, columnspan=2, sticky="n")
root.place_label("info_text", row=1, column=0, pady=10, padx=50, columnspan=2, sticky="n")

root.register_button("github", host=info_page, text="Open GitHub", command=open_source)
root.register_button("config", host=info_page, text="Open Config Folder", command=root.open_config)
root.place_button("github", row=2, column=0, pady=20, padx=50, sticky="w")
root.place_button("config", row=2, column=1, pady=20, padx=50, sticky="e")


root.add_page("Home", home_page, starting_page=True)
root.add_page("Patchers", patchers_page)
root.add_page("Info", info_page)

root.run()