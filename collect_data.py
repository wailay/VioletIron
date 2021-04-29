import pyautogui
import pydirectinput as pdin
from win32 import win32gui
import win32.win32process as wproc
import win32.win32api as wapi
import time
import xml.etree.ElementTree as ET
import os
from shutil import copy
import pyperclip
import random

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

def key_down_delay(key, delay=1.0):
    pdin.keyDown(key, _pause=False)
    time.sleep(delay)
    pdin.keyUp(key, _pause=False)

    
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
    key_down_delay('d', 0.3)

def clear_console():
    key_down_delay('backspace', 0.1)

def open_console():
    pdin.press('`', _pause=False)
    # clear_console()

def close_console():
    pdin.press('esc', _pause=False)

def execute_command(command):
    pyperclip.copy(command)
    pdin.keyDown('ctrl', None, _pause=False)
    pdin.press('v', _pause=False)
    pdin.keyUp('ctrl', _pause=False)
    pdin.press('enter', _pause=False)



def change_stage(stage):
    execute_command(f'stage {stage}')

def take_item_screenshot(path, dim):
    x, y, w, h = dim
    pyautogui.screenshot(path, region=(x+w/2-45,y+h/2-105, 105, 80))

def take_item_rock_screenshot(path, dim):
    random.seed()
    x, y, w, h = dim
    offsetx,offsety = random.randrange(0, 60, 5), random.randrange(0, 60, 5)
    offset_dimx, offset_dimy = random.randrange(0, 60, 5), random.randrange(0, 60, 5)
    pyautogui.screenshot(path, region=(x+w/2 - 108 - offsetx,y+h/2 - 125 - offsety, 180 + offset_dimx + offsetx/2, 230 + offset_dimy + offsety/2))


if __name__ == '__main__':
    root_data_dir = './data'
    item_to_idx, trinket_to_idx= generate_label_to_idx()


    win_dim = focus_isaac()
    pdin.press('esc')

    
    stages = {  '1' : ['c', 'd'], #removed 1, 1a, 1b for now because of tutorial room might add later 
                '2' : ['', 'a', 'b', 'c', 'd'], 
                '3' : ['', 'a', 'b', 'c', 'd'], 
                '4': ['', 'a', 'b', 'c', 'd'], 
                '5': ['', 'a', 'b', 'c', 'd'], 
                '6': ['', 'a', 'b', 'c', 'd'], 
                '7': ['', 'a', 'b', 'c'],
                '8': ['', 'a', 'b', 'c'],
                '10': ['', 'a'], 
                '11': ['', 'a'], 
                '12' : ['']}

    # print(stages)

    # while True:
    #     print(pyautogui.position())
    
    


    for item_name, label_id in item_to_idx.items():
        win = win32gui.FindWindow(None, 'Binding of Isaac: Repentance')
        if win is 0:
            print('isaac crashed')
            exit(0)
        curr_id = 0
        
        item_path = os.path.join(root_data_dir, item_name)
        if not os.path.exists(item_path):
            os.mkdir(item_path)
        else:
            continue 

        for stage, variants in stages.items():
            for variant in variants:
                open_console()
                change_stage(f'{stage}{variant}')
                execute_command(f'spawn 5.100.{label_id}')
                close_console()
                move_isaac()
                
               
                print('currently processing ', item_path, stage, variant, label_id)
                for i in range(5):
                    ss_path = os.path.join(item_path, f'{str(curr_id)}_{i}.png')
                    take_item_screenshot(ss_path, win_dim)
                    ss_path_rock = os.path.join(item_path, f'{str(curr_id)}_{i}_rock.png')
                    take_item_rock_screenshot(ss_path_rock, win_dim)
                curr_id+=1


    
