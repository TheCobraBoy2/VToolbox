import webbrowser
import customtkinter as ctk
import sys
import patchers
from app import App
from versionverifier import get_latest

WINDOW_SIZE = "600x500"
WINDOW_TITLE = "VToolbox"
WINDOW_RESIZABLE = (False, False)
CURRENT_VERSION = "0.0.2"

CONFIG = {
  "show_welcome": True
}

def patch_spotify():
  root.platform_dependent_conformation("Patch Spotify", yes=patchers.spotify.patch_spotify)

def open_source():
  webbrowser.open_new_tab("https://github.com/TheCobraBoy2/VToolbox")

root = App(WINDOW_TITLE, WINDOW_SIZE, WINDOW_RESIZABLE)

root.new_config(CONFIG)
root.reconcile_config()

root.register_version(CURRENT_VERSION)

root.welcome()

# Home Page
home_page = root.register_page("home", flexible=True)
root.default_home(home_page)

# Patchers Page
patchers_page = root.register_page("patchers", flexible=True)
root.register_patcher(patchers.spotify, command=patch_spotify)
# root.register_button("spicetify", host=patchers_page, text="Patch Spotify", command=patch_spotify)
# root.place_button("spicetify", row=0, column=0, padx=20, pady=20, sticky="w") 

# Info Page
info_page = root.register_page("info", flexible=True)
#Configuring 2nd column for button alignment
info_page.grid_columnconfigure(1, weight=1)
root.register_label("info_header", host=info_page, text=f"VToolbox v{CURRENT_VERSION}",
                    font=ctk.CTkFont(size=20, weight="bold"))
root.register_label("info_latest", host=info_page, 
                    text=f"Latest version: v{get_latest()}", 
                    font = ctk.CTkFont(size=12, weight="bold"))
root.register_label("info_text", host=info_page,
                    text="Visit our GitHub for source code and contributions.",
                    font=ctk.CTkFont(size=14), justify="left", wraplength=400)

root.place_label("info_header", row=0, column=0, pady=(20, 0), padx=50, columnspan=2, sticky="n")
root.place_label("info_latest", row=1, column=0, pady=(0, 5), padx=50, columnspan=2, sticky="n")
root.place_label("info_text", row=2, column=0, pady=(0, 10), padx=50, columnspan=2, sticky="n")

root.register_button("github", host=info_page, text="Open GitHub", command=open_source)
root.register_button("config", host=info_page, text="Open Config Folder", command=root.open_config)
root.place_button("github", row=3, column=0, pady=20, padx=50, sticky="w")
root.place_button("config", row=3, column=1, pady=20, padx=50, sticky="e")


# Add pages to root with human readable names
root.add_page("home", "Home", home_page, starting_page=True) # Sets this page as default when opening the application
root.add_page("patchers", "Patchers", patchers_page)
root.add_page("info", "Info", info_page)

root.run()