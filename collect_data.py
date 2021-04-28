import pyautogui
import pydirectinput as pdin
from win32 import win32gui
import win32.win32process as wproc
import win32.win32api as wapi
import time
import xml.etree.ElementTree as ET
import os
from shutil import copy

def generate_label_to_idx():
    gfx_tree = ET.parse('extracted_res/resources/items.xml')

    root = gfx_tree.getroot()
    data_root_dir = './data'
    item_label_to_idx = {}
    trinket_label_to_idx = {}

    for child in root:
        if child.tag == "null":
            continue

        item_id = child.attrib['id'].lower()
        item_label = child.attrib['gfx'].lower().replace('.png', '')

        if child.tag == "trinket":
            item_label = item_label.replace('trinkets_', '')
            trinket_label_to_idx[item_label] = item_id
        else:
            item_label = item_label.replace('collectibles_', '')
            item_label_to_idx[item_label] = item_id

    return item_label_to_idx, trinket_label_to_idx

def key_down_delay(key, delay=1):
    pdin.keyDown(key)
    time.sleep(delay)
    pdin.keyUp(key)

    
# focus isaac window and return x,y, w, h position
def focus_isaac():
    print('focus isaac')
    win = win32gui.FindWindow(None, 'Binding of Isaac: Repentance')
    remote_thread, _ = wproc.GetWindowThreadProcessId(win)
    wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
    win32gui.SetForegroundWindow(win)
    win32gui.SetFocus(win)
    rect = win32gui.GetWindowRect(win)
    return (rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])


def move_isaac():
    key_down_delay('d', 0.5)

def clear_console():
    key_down_delay('backspace', 0.5)
    
def execute_command(command):
    pdin.press('`')
    clear_console()
    pdin.typewrite(command, interval=0.0, _pause=False)
    pdin.press('enter')
    pdin.press('esc')

def change_stage(stage):
    execute_command(f'stage {stage}')
    move_isaac()

def take_item_screenshot(path, dim):
    x, y, w, h = dim
    time.sleep(1)
    pyautogui.screenshot(path, region=(x+w/2-45,y+h/2-105, 90, 80))

def take_item_rock_screenshot(path, dim):
    x, y, w, h = dim
    pyautogui.screenshot(path, region=(x+w/2 - 48,y+h/2 - 105, 95, 160))


if __name__ == '__main__':
    root_data_dir = './data'
    item_to_idx, trinket_to_idx= generate_label_to_idx()

    
    win_dim = focus_isaac()
    pdin.press('esc')

    
    stages = {  '1' : ['', 'a', 'b', 'c', 'd'], 
                '2' : ['', 'a', 'b', 'c', 'd'], 
                '3' : ['', 'a', 'b', 'c', 'd'], 
                '4': ['', 'a', 'b', 'c', 'd'], 
                '5': ['', 'a', 'b', 'c', 'd'], 
                '6': ['', 'a', 'b', 'c', 'd'], 
                '7': ['', 'a', 'b', 'c'],
                '8': ['', 'a', 'b', 'c'], 
                '9': [''],
                '10': ['', 'a'], 
                '11': ['', 'a'], 
                '12' : ['']}

    # print(stages)

    # while True:
    #     print(pyautogui.position())

    for item_name, label_id in item_to_idx.items():
        curr_id = 0
        for stage, variants in stages.items():
            for variant in variants:
                change_stage(f'{stage}{variant}')
                execute_command(f'spawn 5.100.{label_id}')
                item_path = os.path.join(root_data_dir, item_name)
                ss_path = os.path.join(item_path, f'{str(curr_id)}.png')
                ss_path_rock = os.path.join(item_path, f'{str(curr_id)}_rock.png')
                print('currently processing ', item_path, ss_path)
                if not os.path.exists(item_path):
                    os.mkdir(item_path)
                take_item_screenshot(ss_path, win_dim)
                take_item_rock_screenshot(ss_path_rock, win_dim)
                curr_id+=1


    
