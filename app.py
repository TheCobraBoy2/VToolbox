import customtkinter as ctk
from typing import TypedDict, Callable, Optional, Union, Tuple
import os
import json

DEFAULT_CONFIG = {
  "show_welcome": True,
}

home_dir = os.path.expanduser("~")
config_dir = os.path.join(home_dir, ".VToolBox")
config_path = os.path.join(config_dir, "config.json")

def should_show_welcome(config_key: str="show_welcome") -> bool:
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
  config = {}

  def __init__(self, title="Toolbox", size="500x400", resizable=(False, False), column_config=(0, 1)):
    self.root = ctk.CTk()
    self.root.title(title)
    self.root.geometry(size)
    self.root.resizable(resizable[0], resizable[1])
    self.root.grid_columnconfigure(column_config[0], weight=column_config[1])

  def new_config(self, config: Optional[dict]=None):
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
  
  def welcome(self, config_key: str="show_welcome"):
    if not should_show_welcome(config_key):
      return
    popup = ctk.CTkToplevel(self.root)
    popup.title("Welcome to Toolbox")
    popup.geometry("500x300")
    popup.resizable(False, False)
    popup.transient(self.root)
    popup.grab_set()

    outer_frame = ctk.CTkFrame(popup, corner_radius=15)
    outer_frame.pack(expand=True, fill="both", padx=20, pady=20)

    header = ctk.CTkLabel(
      outer_frame,
      text="Welcome to Toolbox!",
      font=ctk.CTkFont(size=18, weight="bold")
    )
    header.pack(pady=(0, 10))

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
    message.pack(expand=True, fill="both", pady=(0, 15))

    dont_show_again = ctk.CTkCheckBox(
      outer_frame,
      text="Don't show this again",
    )

    dont_show_again.pack(pady=(0, 10))

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

    ok_button = ctk.CTkButton(
      outer_frame,
      text="OK",
      width=100,
      command=ok_clicked
    )
    ok_button.pack(pady=(0, 10))
    popup.focus()
  
  def open_popup(self, title, label, yes=None, no=None):
    if no is None:
      no = lambda p: p.destroy()
    popup = ctk.CTkToplevel(self.root)
    popup.title(title)
    popup.geometry("400x200")
    popup.resizable(False, False)
    popup.transient(self.root)
    popup.grab_set()

    label = ctk.CTkLabel(popup, text=label)
    label.pack(pady=15)

    button_frame = ctk.CTkFrame(popup, fg_color="transparent")
    button_frame.pack(pady=10)
    yes_button = ctk.CTkButton(button_frame, text="Yes", command=lambda: yes(popup))
    yes_button.pack(side="left", padx=10)
    no_button = ctk.CTkButton(button_frame, text="No", command=lambda: no(popup))
    no_button.pack(side="left", padx=10)

  def register_button(self, id: str, text="New Button", command=None, width=140, height=28):
    btn = ctk.CTkButton(self.root, text=text, width=width, height=height, command=command)
    self.buttons[id] = btn

  def place_button(self, id: str, row=0, column=1, sticky="ne", padx=10, pady=10):
    button = self.buttons.get(id)
    button.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)

  def run(self):
    self.root.mainloop()