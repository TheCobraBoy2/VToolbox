import threading

def run_in_thread(func, *args):
  thread = threading.Thread(target=func, args=args, daemon=True)
  thread.start()