import xml.etree.ElementTree as ET
import os
from shutil import copy

gfx_tree = ET.parse('extracted_res/resources/items.xml')

root = gfx_tree.getroot()

print(root, root.tag, root.attrib)
gfx_root_dir = os.path.join('./extracted_res/resources/', root.attrib['gfxroot'])
gfx_dir = os.path.join(gfx_root_dir, 'collectibles')
data_root_dir = './data'


for child in root:
    if child.tag == "null":
        continue
    
    if child.tag == "trinket":
        gfx_dir = os.path.join(gfx_root_dir, 'trinkets')
        
    src_dir = os.path.join(gfx_dir, child.attrib['gfx'].lower())
    item_name = child.attrib['name']

    if item_name == '<3':
        item_name = 'heart'

    for symb in [{'symbol': '?', 'replace': 'qm'}, {'symbol': '/', 'replace': 'slash'}]:
        if symb['symbol'] in item_name:
            item_name = item_name.replace(symb['symbol'], symb['replace'])

    target_dir = os.path.join(data_root_dir, item_name)
    if not os.path.exists(target_dir):
        print(src_dir, target_dir)
        os.makedirs(target_dir)
        copy(src_dir, target_dir)

