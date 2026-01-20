import sys
import os
import subprocess
import shutil
import threadutil

powershell = "iwr -useb https://raw.githubusercontent.com/spicetify/cli/main/install.ps1 | iex"
linux_sh = "curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh"
mac_os = "curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh"

independent = "spicetify restore backup apply"

def installed():
  return shutil.which("spicetify") is not None

def spicetify_config_exists():
  if sys.platform == "win32":
    path = os.path.join(os.environ["APPDATA"], "spicetify", "config-xpui.ini")
  else:
    path = os.path.expanduser("~/.config/spicetify/config-xpui.ini")

  return os.path.isfile(path)

def get_sys_dependent():
  if sys.platform == "win32":
    return powershell
  elif sys.platform == "linux":
    return linux_sh
  elif sys.platform == "darwin":
    return mac_os
  
def patch_spotify(popup):
  def threaded():
    command = get_sys_dependent()
    if not command:
      print("Unsupported operating system")
      popup.destroy()
      return
    if not installed():
      try:
        if sys.platform == "win32":
          subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            check=True)
        else:
          subprocess.run(command, shell=True, check=True)

      except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    elif installed():
      if sys.platform == "win32":
        subprocess.run(
          ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", independent],
          check=True)
      else:
          subprocess.run(independent, shell=True, check=True)

  threadutil.run_in_thread(threaded)
  popup.destroy()

__all__ = ["patch_spotify"]