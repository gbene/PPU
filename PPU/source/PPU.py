# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:40:09 2020

@author: gabri
"""
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import scripts
from main_builder import main_builder



from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty




from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem,OneLineListItem
from kivymd.uix.list import MDList

from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.picker import MDThemePicker



## SWITCH STATEMENTS


#Switch stat for parameters:

def switchpar(name):
    global active_screen
    global_list = MDList()
    global_scroll = ScrollView()
    def false_geodata():
        ext = CustomTextEntry(text="Input files extension: ",example='for example .png',tag='in_ext')
        global_list.add_widget(ext)
        phi = CustomTextEntry(text="Cameras latitude: ",example='for example 30',tag='lat')
        global_list.add_widget(phi)
        dist = CustomTextEntry(text="Camera distance from object: ",example='in centimeters',tag='dist')
        global_list.add_widget(dist)
        rings = CustomTextEntry(text="Added focal length: ",example='in millimeters',tag='rings')
        global_list.add_widget(rings)
        corr = CustomSwitchEntry(text="Apply correction",tag='corr')
        global_list.add_widget(corr)
        global_scroll.add_widget(global_list)
        return global_scroll
    
    def raw_conv():
        ext = CustomTextEntry(text="Input files extension: ",example='for example .nef',tag='in_ext')
        global_list.add_widget(ext)
        output = CustomTextEntry(text="Output files extension: ",example='for example .tiff',tag='out_ext')
        global_list.add_widget(output)
        global_scroll.add_widget(global_list)
        return global_scroll
    
    def mask():
        input_ext = CustomTextEntry(text="Input files extension: ",example='for example .jpg',tag='in_ext')
        global_list.add_widget(input_ext)
        output_ext = CustomTextEntry(text="Mask files extension: ",example='for example .png',tag='out_ext')
        global_list.add_widget(output_ext)
        strength = CustomTextEntry(text="Strength value: ",example='from 0 to 255',tag='stren')
        global_list.add_widget(strength)
        save = CustomSwitchEntry(text='Save mask:',tag='save')
        global_list.add_widget(save)
        apply = CustomSwitchEntry(text='Apply mask:',tag='apply')
        global_list.add_widget(apply)
        global_scroll.add_widget(global_list)
        return global_scroll
    
    def exif_copy():
        src = CustomTextEntry(text="Source files extension: ",example='for example .jpg',tag='in_ext')
        global_list.add_widget(src)
        targ = CustomTextEntry(text="Target files extension: ",example='for example .tiff',tag='out_ext')
        global_list.add_widget(targ)
        global_scroll.add_widget(global_list)
        return global_scroll
    
    table={
        'false_geodata': false_geodata,
        'raw_conv': raw_conv,
        'mask': mask,
        'exif_copy': exif_copy
        }
    active_screen = name
    out = table.get(name,lambda:'Not found')
    return out()

def switchinput(name):
    name_str = list(name.ids.keys())[0]
    
    def text_input():
        par_dict[name.tag] = name.ids.text_input.text
    def switch_input():
        par_dict[name.tag] = name.ids.switch_input.active
    
    table = {
        'text_input': text_input,
        'switch_input': switch_input
        }
    table.get(name_str,lambda:'Not found')()


def switchscript(name,valid_path,par_dict):

    def false_geodata():
        for path in valid_path:
            print(f'\nProcessing {path}')
            scripts.run_geo(path, par_dict)
        print('Done')
    def raw_conv():
        for path in valid_path:
            print(f'\nProcessing {path}')
            scripts.run_conv(path,par_dict)
        print('\nDone')
        
    def mask():
        for path in valid_path:
            print(f'\nProcessing {path}')
            scripts.run_mask(path,par_dict)
        print('\nDone')
    def exif():
        for path in valid_path:
            print(f'\nProcessing {path}')
            scripts.run_exif(path,par_dict)
        print('\nDone')
    table={
        'false_geodata': false_geodata,
        'raw_conv':raw_conv,
        'mask': mask,
        'exif_copy': exif,
        }
    table.get(name,lambda:'Not found')()
        

        
    
## MAIN FUNCTIONS


# Function used to open the file explorer
def Addroot():
    window = tk.Tk()
    window.withdraw()
    root = filedialog.askdirectory(initialdir='/',title='Select starting directory')
    root = root.replace('/','\\')
    window.destroy()
    return root



# Function used to trace the paths from the path to the root
def deconstruct(path,root):
    paths = []
    while path != root:
        if os.path.exists(path):
            paths.append(path)
        path,tail = os.path.split(path)
        
    paths.append(root) 
    paths = paths[::-1]

    return paths

# Function used to create the lists
def list_create(selected_dir,obj='?'):
    
    
    # list of files present 
    expl = os.listdir(selected_dir)
    file_dirs_list = [os.path.join(selected_dir,name) for name in expl]

    # start Kivymd objects
    ui_list = MDList()
    scroll = ScrollView()
    grid = GridLayout(rows=1)

    for c,i in enumerate(expl):

        # Assign id
        item_id = str(np.random.bytes(20))
        list_items[item_id] = file_dirs_list[c]

        # Conditional for the left icon
        if os.path.isdir(file_dirs_list[c]):
            icon = "folder"
        else:
            icon = "file"
        # Conditional used to modify the selected item
        if file_dirs_list[c] in obj:
            icon_dx = 'chevron-right'
            item = CustomList(text=str(i),icon=icon,bg_color=(0,1,1,0.15),icon_dx=icon_dx,item_id=item_id) #add the list item with the left and right icons
            item.ids.icon_right.remove_widget(item.ids.checkbox) #if the conditional holds it clears the checkbox on the right
        else:
            icon_dx = ''
            item = CustomList(text=str(i),icon=icon,icon_dx=icon_dx,item_id=item_id) #add the list item with the left and right icons
        
        
        ui_list.add_widget(item) #add the item to the list
    scroll.add_widget(ui_list) #add the list to the scroll
    grid.add_widget(scroll) #add the scroll to the grid
    return grid


## VARIABLES
    
list_items = dict()

start_dir = '/'

sel_file=[]
valid_path = []
save_theme = []

par_dict= dict()
active_screen = ''



## CLASSES

class CustomTextEntry(MDList):
    text = StringProperty()
    example = StringProperty()
    tag = StringProperty()
    
class CustomSwitchEntry(MDList):
    text = StringProperty()
    tag = StringProperty()
    
# Class for the lists in the main menu

class CustomList(OneLineAvatarIconListItem):
    text = StringProperty()    
    icon = StringProperty()   
    icon_dx = StringProperty()
    item_id = StringProperty()

# Class fot the navigation drawer
    
class NavDraw(BoxLayout):

    screen_manager = ObjectProperty()
    nav_draw = ObjectProperty()
    float_button = ObjectProperty()
    toolbar = ObjectProperty()

    
    def click(self,obj):
        global par_dict
        global prova
        par_dict = {}
        ui_list = MDList()
        scroll = Scriptstruc()
        
        scroll.ids.option_scroll.clear_widgets()
        for file in valid_path:
            item = OneLineListItem(text=file)
            ui_list.add_widget(item)
        scroll.ids.option_scroll.add_widget(ui_list)
        obj.add_widget(scroll)

        ##Construct diff. parameters with switch stat. SO GOOD!!

        par_scroll = switchpar(obj.name)
        par_scroll_child = par_scroll.children[:]
        
        for i in par_scroll_child[0].children: #this is stupid
            switchinput(i)
        
        scroll.ids.par_list.add_widget(par_scroll)
        return scroll

    
#Class for structure of the secondary screens (false_geodata etc..)
        
class Scriptstruc(BoxLayout):
    dirs = sel_file
    script_struct = ObjectProperty()
    screen_manager = ObjectProperty()
    nav_draw = ObjectProperty()
    


# Main app
    
class PPU(MDApp):
    
    
    ## MAIN STUFF
    
    def build(self):
        screen = Builder.load_string(main_builder)
        return screen
    
 
    # What to do on start
    
    def on_start(self):  
        try: 
            with open('styles.txt','r') as f:
                style = f.read()
                prova = style.split(';')
                self.theme_cls.theme_style,self.theme_cls.primary_palette,self.theme_cls.accent_palette, _ = prova
        except:
            self.theme_cls.theme_style = "Dark"
        start_screen = MDLabel(text='Import directory',halign="center",theme_text_color ='Hint')
        self.root.ids.main_grid.add_widget(start_screen)
    
    # Function used to add a list to the grid when an item from the list is clicked
        
    def add_list(self,item_id):
        
        global list_items
        
        #take the path corresponding to the id. SO GOOD!!
        
        dir_path = list_items[str(item_id)]
        dec = deconstruct(dir_path,start_dir)
        
        if not os.path.isfile(dir_path):
            list_items = dict()
            self.root.ids.main_grid.clear_widgets() #clear all the widgets in the main grid
            for d in dec: #cicle through the dirs list and create the corresponding list
                grid = list_create(d,dec)
                self.root.ids.main_grid.add_widget(grid)
        else:
            None
        
    ## THEME
            
    def theme(self):

        theme_dialog = MDThemePicker()
        theme_dialog.open()
    
    ## SPEED DIALS
    
    main_data = {
        'import': 'Import',
        'selection-off':'Deselect all',
        'restore': 'Reset',
        'information-outline': 'Help'
    }
    script_data = {
        'play': 'Run',
        'information-outline': 'Help'
        }
    
    # function called when one of the main menu icons is pressed
    
    def callback(self, instance):
        action = instance.icon # the icon type is read and then used for the conditionals
        #needs a switch but it doesn't work WHY!!!!
        if action == 'import':
            
            global start_dir
            global sel_file,valid_path
            start_dir = Addroot()
            if os.path.exists(start_dir):
                grid = list_create(start_dir)
                self.root.ids.main_grid.clear_widgets()
                self.root.ids.main_grid.add_widget(grid)
            else:
                self.dialog = MDDialog(text='Invalid path',buttons=[MDFlatButton(text='Ok',on_release=self.closedialog)])
                self.dialog.open()
                sel_file = []
                self.root.ids.main_grid.clear_widgets()
                self.on_start()
            self.root.ids.main_floatbutton.close_stack()
        elif action == 'selection-off':
            if sel_file: #controllo se sel_file è vuoto
                sel_file = []
                valid_path = []
                grid = list_create(start_dir)
                self.root.ids.main_grid.clear_widgets()
                self.root.ids.main_grid.add_widget(grid)
            else:
                None
        elif action == 'restore':
            sel_file = []
            valid_path = []
            self.root.ids.main_grid.clear_widgets()
            self.on_start()
        
    def script_callback(self, instance):
        action = instance.icon
        if action =='play':
            screen = self.root.ids.screen_manager.children[0].name   
            paths = valid_path
            parameters = par_dict
            switchscript(screen, paths, parameters)
        elif action == 'information-outline':
            print('NO HELP FOR YOU!')
       



    ## FUNCTION FOR CHECKBOXES

    # Function used to check if the item list was previously selected
    def checkactive(self,item_id=0):
        
        # take path to the corresponding id. SO GOOD!!
        path = list_items.get(item_id) 

        if path in sel_file:
            return True
        else:
            return False
    
    # Functions used to add or remove the checked dirs from the sel_file list          
    def selection(self,obj):
        sel_path = str(list_items[str(obj)])
        for root,path,_ in os.walk(sel_path):
            sel_file.append(root)
            if not path:
                valid_path.append(root)

    def deselection(self,obj):
        sel_path = str(list_items[str(obj)])
        for root,path,_ in os.walk(sel_path):
            if root in sel_file:
                sel_file.remove(root)
                if root in valid_path:
                    valid_path.remove(root)
        

    ## FUNCTION FOR ALERTS
        
    # Function used to close the dialog window
    def closedialog(self,obj):
        self.dialog.dismiss()
        
    def parameters(self,key,value):
        
        try:
            float(value)
        except ValueError:
            par_dict[key] = value
        else:
            par_dict[key] = float(value)
    
        
if __name__=='__main__':
    PPU().run()
    exit_theme = [PPU().theme_cls.theme_style,PPU().theme_cls.primary_palette,PPU().theme_cls.accent_palette]
    with open('styles.txt','w') as f:
        for i in exit_theme:
            f.write(f'{i};')
        
    
        
        