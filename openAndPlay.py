import pyautogui
import time
import psutil
import time

pyautogui.press('win')  # Press Windows key to open Start menu
time.sleep(1)
pyautogui.write('Spotify')  # Type "Spotify" to search for Spotify
time.sleep(1)
pyautogui.press('enter')  # Open Spotify

program_name = "Spotify.exe"

# Set a timeout of 2 minutes
timeout = time.time() + 120  # 120 seconds = 2 minutes

while True:
    # Check if the program is open
    for process in psutil.process_iter():
        try:
            if process.name() == program_name:
                print("Spotify is open!")
                break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    else:
        # If the program is not open, check if we have timed out
        if time.time() > timeout:
            print("Timed out!")
            break

        else:
            # Wait for a short amount of time before checking again
            time.sleep(1)
            continue
    # If we reach this point, the program is open, so break out of the loop
    break
time.sleep(7)  # Wait for Spotify to load
pyautogui.press('space')  # Play the song

