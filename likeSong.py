import pyautogui
import time
import psutil
import win32gui
import win32process
from pywinauto import Application


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


# Specify the name of the program you want to check

program_name = "Spotify.exe"

# Set a timeout of 2 minutes

timeout = time.time() + 120  # 120 seconds = 2 minutes

isOpen = False

# Check if the program is open

for process in psutil.process_iter():

    try:

        if process.name() == program_name:
            print("Spotify is open!")

            isOpen = True

            break

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

        pass

else:

    print("Spotify is not open!")

    exit()

if isOpen:

    spotify_pids = []

    process_name = "Spotify.exe"

    for proc in psutil.process_iter():

        if process_name in proc.name():
            spotify_pids.append(proc.pid)

    app = Application().connect(process=get_spotify_window_title(spotify_pids))

    app.top_window().set_focus()

    time.sleep(1)

    pyautogui.hotkey('alt', 'shift', 'b', interval=0.25)

    # Get the window object

    window = app.top_window()

    # Minimize the window

    window.minimize()