import requests
from packaging.version import Version

def get_latest():
  response = requests.get("https://api.github.com/repos/TheCobraBoy2/VToolbox/releases/latest")
  response.raise_for_status()

  if response.status_code != 200:
    return None

  data = response.json()
  version = data["tag_name"].lstrip("v")
  return version

def is_outdated(current):
  return Version(current) < Version(get_latest())