import webbrowser
import customtkinter as ctk
import sys
import patchers
from app import App

root = App()

CONFIG = {
  "show_welcome": True
}

root.new_config(CONFIG)
root.reconcile_config()

def patch_spotify():
  root.open_popup("Patch Spotify", "This has only been tested on Windows.\n This is platform dependent and may not work on linux distros or MacOS.\n Do you want to continue?", yes=patchers.patch_spotify)

def open_source():
  webbrowser.open_new_tab("")

root.welcome()

root.register_button("spicetify", text="Patch Spotify", command=patch_spotify)
root.place_button("spicetify", row=0, column=0, sticky="nw", padx=0, pady=10)

root.register_button("open_source", text="Open Source", command=open_source, width=80, height=30)
root.place_button("open_source", row=0, column=1, sticky="ne", padx=10, pady=10)

root.run()