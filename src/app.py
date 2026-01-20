import customtkinter as ctk
from typing import Optional
import os
import sys
import json

DEFAULT_CONFIG = {"show_welcome": True}
home_dir = os.path.expanduser("~")
config_dir = os.path.join(home_dir, ".VToolBox")
config_path = os.path.join(config_dir, "config.json")

def resource_path(relative_path: str) -> str:
  try:
      base_path = sys._MEIPASS
  except AttributeError:
      base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

def should_show_welcome(config_key: str = "show_welcome") -> bool:
  if not os.path.exists(config_path):
    return True
  try:
    with open(config_path, "r", encoding="utf-8") as f:
      data = json.load(f)
      return data.get(config_key, True)
  except (json.JSONDecodeError, OSError):
    return True

class App:
  buttons = {}
  labels = {}
  config = {}
  frames = {}
    
  starting_page = None

  def __init__(self, title="Toolbox", size="500x400", resizable=(False, False)):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme(resource_path("resources/red_theme.json"))
      
    self.root = ctk.CTk()
    self.root.title(title)
    self.root.geometry(size)
    self.root.resizable(resizable[0], resizable[1])
        
    self.root.grid_columnconfigure(0, weight=0)  # Sidebar column
    self.root.grid_columnconfigure(1, weight=1)  # Content column
    self.root.grid_rowconfigure(0, weight=1)

    self.navbar = ctk.CTkFrame(self.root, width=150)
    self.navbar.grid(row=0, column=0, sticky="ns")
    self.navbar.grid_propagate(False)

    self.content_container = ctk.CTkFrame(self.root)
    self.content_container.grid(row=0, column=1, sticky="nsew")
    self.content_container.grid_rowconfigure(0, weight=1)
    self.content_container.grid_columnconfigure(0, weight=1)

  # Config Management
  def open_config(self):
    os.startfile(config_dir)

  def new_config(self, config: Optional[dict] = None):
    if config is None:
        config = DEFAULT_CONFIG.copy()
    self.config = config

  def clear_config(self):
    with open(config_path, "w", encoding="utf-8") as f:
         json.dump({}, f, indent=2)

  def reconcile_config(self):
    os.makedirs(config_dir, exist_ok=True)
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
        return self.config.copy()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError):
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
        return self.config.copy()

    updated = False
    for key, value in self.config.items():
        if key not in config:
            config[key] = value
            updated = True

    if updated:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    return config

  # Welcome Message
  def welcome(self, config_key: str = "show_welcome"):
    if not should_show_welcome(config_key):
        return
    popup = ctk.CTkToplevel(self.root)
    popup.title("Welcome to Toolbox")
    popup.geometry("500x300")
    popup.resizable(False, False)
    popup.transient(self.root)
    popup.grab_set()

    outer_frame = ctk.CTkFrame(popup, corner_radius=15)
    outer_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    outer_frame.grid_rowconfigure(2, weight=1)

    header = ctk.CTkLabel(
      outer_frame,
      text="Welcome to Toolbox!",
      font=ctk.CTkFont(size=18, weight="bold")
    )
    header.grid(row=0, column=0, pady=(0, 10))

    message_text = (
      "This is in early development, so expect bugs and missing features.\n\n"
      "Open source contributions are greatly appreciated!\n\n"
      "Note: Most patchers are multi-threaded to prevent freezing.\n"
      "So don't expect them to run instantly.\n\n"
      "-Vorrikz"
    )
    message = ctk.CTkLabel(
      outer_frame,
      text=message_text,
      wraplength=460,
      justify="left"
    )
    message.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

    dont_show_again = ctk.CTkCheckBox(outer_frame, text="Don't show this again")
    dont_show_again.grid(row=3, column=0, pady=(0, 10))

  def ok_clicked():
    try:
      with open(config_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data[config_key] = not dont_show_again.get()
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)
    except (json.JSONDecodeError, OSError):
      pass
    popup.destroy()

    ok_button = ctk.CTkButton(outer_frame, text="OK", width=100, command=ok_clicked)
    ok_button.grid(row=4, column=0, pady=(0, 10))
    popup.focus()

  # Pupups
  def open_popup(self, title, label, size="400x200", yes=None, no=None):
    if no is None:
      no = lambda p: p.destroy()
    popup = ctk.CTkToplevel(self.root)
    popup.title(title)
    popup.geometry(size)
    popup.resizable(False, False)
    popup.transient(self.root)
    popup.grab_set()

    label = ctk.CTkLabel(popup, text=label)
    label.grid(row=0, column=0, pady=15)

    button_frame = ctk.CTkFrame(popup, fg_color="transparent")
    button_frame.grid(row=1, column=0, pady=10)
    yes_button = ctk.CTkButton(button_frame, text="Yes", command=lambda: yes(popup))
    yes_button.grid(row=0, column=0, padx=10)
    no_button = ctk.CTkButton(button_frame, text="No", command=lambda: no(popup))
    no_button.grid(row=0, column=1, padx=10)

  # Nav
    
  # You need to configure columns if you want more than one to be flexible
  def register_page(self, id: str, flexible: bool = False):
    frame = ctk.CTkFrame(self.content_container)
    if flexible:
      frame.grid_columnconfigure(0, weight=1)
    self.frames[id] = frame
    return frame

  # If starting_page has already been passed true once then it will be ignored on subsequent calls
  def add_page(self, page_name: str, frame: ctk.CTkFrame, starting_page: bool=False):
    # Add a page to the content area and create a navbar button
    self.frames[page_name] = frame
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_remove()

    def show():
      self.show_page(page_name)

    button = ctk.CTkButton(self.navbar, text=page_name, width=130, command=show)
    button.grid(pady=10, padx=10, sticky="ew")

    if starting_page and self.starting_page is None:
      self.starting_page = page_name

  def show_page(self, page_name: str):
    # Hide all frames and show the selected one
    for name, frame in self.frames.items():
      frame.grid_remove()
    self.frames[page_name].grid()

  # Buttons
  def register_button(self, id: str, host=None, text="New Button", command=None, width=140, height=28):
    if host is None:
      host = self.root
    btn = ctk.CTkButton(host, text=text, width=width, height=height, command=command)
    self.buttons[id] = btn

  def place_button(self, id: str, row=0, column=1, sticky=None, padx=10, pady=10):
    button = self.buttons.get(id)
    button.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        
  # Labels
  def register_label(self, id: str, host=None, text="New Label", font=None, **kwargs: any):
    if host is None:
      host = self.root
    lbl = ctk.CTkLabel(host, text=text, font=font, **kwargs)
    self.labels[id] = lbl

  def place_label(self, id: str, row=0, column=1, padx=10, pady=10, **kwargs: any):
    label = self.labels.get(id)
    label.grid(row=row, column=column, padx=padx, pady=pady, **kwargs)

  def run(self):
    if self.starting_page:
      self.show_page(self.starting_page)
    self.root.mainloop()
