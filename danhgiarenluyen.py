import pyautogui
import sys
import pyperclip
import keyboard

sys.stdout.reconfigure(encoding="utf-8")


def press_key_sequence(key, repeat, next_key=None):
    for _ in range(repeat):
        pyautogui.press(key)
        if next_key:
            pyautogui.press(next_key)


def type_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


def auto_execute():
    press_key_sequence("tab", 2)
    press_key_sequence("3", 10, "tab")
    press_key_sequence("2", 4, "tab")
    press_key_sequence("3", 13, "tab")
    press_key_sequence("4", 11, "tab")
    press_key_sequence("5", 18, "tab")
    press_key_sequence("tab", 2)
    type_text("Hoàn thành xuất sắc")
    press_key_sequence("tab", 1)
    type_text("Hoàn thành xuất sắc")
    press_key_sequence("tab", 2)
    pyautogui.press("enter")


keyboard.add_hotkey("end", auto_execute)

print("Press End to run automatically...")

keyboard.wait("esc")
