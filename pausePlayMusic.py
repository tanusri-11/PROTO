import pyautogui
import time
import psutil
import win32gui
import win32process
from pywinauto import Application
# locate physical window
def get_spotify_window_title(pids):
    titles = []
    returnpid = 0

    def _enum_cb(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            if pids is None or pid in pids:
                nonlocal returnpid
                returnpid = pid

    win32gui.EnumWindows(_enum_cb, titles)
    return returnpid
# press space to play/pause the song
def press_key(spotify_pids):
    app = Application().connect(process=get_spotify_window_title(spotify_pids))
    app.top_window().set_focus()
    time.sleep(1)  # Wait for Spotify to load
    pyautogui.press('space')  # Play the song

    # Get the window object
    window = app.top_window()

    # Minimize the window
    window.minimize()


program_name = "Spotify.exe"
process_ids = []

# Set a timeout of 2 minutes
timeout = time.time() + 120  # 120 seconds = 2 minutes
isOpen = False

while True and time.time() < timeout:
    # Check if the program is open
    for process in psutil.process_iter():
        try:
            if program_name in process.name():
                isOpen = True
                process_ids.append(process.pid)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    else:
        if isOpen:
            print("Spotify is OPEN")
            # finished looping succesfully
            time.sleep(1)
            press_key(process_ids)

        else:
            print("Spotify is CLOSED")
        break