# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 23:21:14 2020

@author: gabri
"""

main_builder ="""
#:import NoTransition kivy.uix.screenmanager.NoTransition


<CustomTextEntry>:
    padding: "30dp"
    MDGridLayout:
        rows:1
        padding:"5dp"
        MDLabel:
            text:root.text
            theme_text_color:"Primary"
        MDTextField:
            id: text_input
            helper_text: root.example
            helper_text_mode: "on_focus"
            on_focus: app.parameters(root.tag,self.text)
            color_mode: 'accent'

<CustomSwitchEntry>:
    padding: "30dp"
    MDGridLayout:
        rows:1
        padding:"5dp"
        MDLabel:
            text:root.text
            theme_text_color:"Primary"
        MDSwitch:
            id: switch_input
            width: dp(64)
            on_press: 
                app.parameters(root.tag,not self.active)
            on_release:
                app.parameters(root.tag,not self.active) #this is horrible but without it it doesn't work properly
            on_active:
                app.parameters(root.tag,self.active)



<CustomList>:
    on_release:
        app.add_list(self.item_id)

    IconLeftWidget:
        
        icon: root.icon
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    IconRightWidget:
        id: icon_right
        
        icon: root.icon_dx
        MDCheckbox:
            id: checkbox
            selected_color: app.theme_cls.accent_color
            active: app.checkactive(root.item_id)
            on_release: 
                app.selection(root.item_id) if self.active else app.deselection(root.item_id)






<NavDraw>:
    
    ScrollView:
        MDList:
            OneLineIconListItem:
                text: 'Main menu'
                on_release:
                    root.nav_draw.set_state("close")
                    root.toolbar.title = self.text
                    root.floatbutton.close_stack()
                    root.screen_manager.current = "main_menu"
                    
                    
                IconLeftWidget:
                    icon:'home'
                
            OneLineIconListItem:
                text: 'False geodata'
                on_release:
                    root.nav_draw.set_state("close")
                    root.toolbar.title = self.text
                    root.screen_manager.current = "false_geodata"
                    root.click(root.screen_manager.children[0])
                    
                    
                IconLeftWidget:
                    icon:'globe-model'
            OneLineIconListItem:
                text: 'Raw conversion'
                on_release:
                    root.nav_draw.set_state("close")
                    root.toolbar.title = self.text
                    root.screen_manager.current = "raw_conv"
                    root.click(root.screen_manager.children[0])
                    
                IconLeftWidget:
                    icon:'image-move'
            OneLineIconListItem:
                text: 'Mask'
                on_release:
                    root.nav_draw.set_state("close")
                    root.toolbar.title = self.text
                    root.screen_manager.current = "mask"
                    root.click(root.screen_manager.children[0])
                    
                IconLeftWidget:
                    icon:'transition-masked'
            OneLineIconListItem:
                text: 'Exif copy'
                on_release:
                    root.nav_draw.set_state("close")
                    root.toolbar.title = self.text
                    root.screen_manager.current = "exif_copy"
                    root.click(root.screen_manager.children[0])
                    
                IconLeftWidget:
                    icon:'content-copy'              
    
<Scriptstruc>:

        
    GridLayout:
        rows:2
        BoxLayout:
            size_hint:(None,None)
            size:(300,64)

    
        MDBoxLayout:
            id: main_cont
            md_bg_color: app.theme_cls.divider_color


            GridLayout:
                
                cols:2
                padding: [0,2,0,0]
    
                GridLayout:
                    id: sel_dir
                    rows:3
                    MDBoxLayout:
                        id: sel_dir_container
                        md_bg_color: app.theme_cls.primary_color
                        size_hint: (None,None)
                        size:(root.ids.sel_dir.width*0.997,root.ids.sel_dir.height*0.1)
                        MDLabel:
                            text: "Selected dirs"
                            halign: 'center'
                            theme_text_color:'Primary'
                            font_style : 'H6'
                    MDBoxLayout:
                        size_hint: (None,None)
                        size:(root.ids.sel_dir_container.width,root.ids.sel_dir.height)
                        md_bg_color: app.theme_cls.bg_normal
                        ScrollView:
                            id: option_scroll
                    
                             
                
                GridLayout:
                    id: par
                    rows:3
                    MDBoxLayout:
                        id: par_container
                        md_bg_color: app.theme_cls.primary_color
                        size_hint: (None,None)
                        size:(root.ids.sel_dir.width,root.ids.sel_dir.height*0.1)
                        MDLabel:
                            text: "Parameters"
                            halign: 'center'
                            theme_text_color:'Primary'
                            font_style : 'H6'
                    MDBoxLayout:
                        id: par_list
                        size_hint: (None,None)
                        size:(root.ids.par.width,root.ids.par.height)
                        md_bg_color: app.theme_cls.bg_normal

                    AnchorLayout:
                        anchor_x:'right'
                        anchor_y:'bottom'
                        MDFloatingActionButtonSpeedDial:
                            id: script_floatbutton
                            data: app.script_data
                            rotation_root_button: False
                            icon: "dots-vertical"
                            bg_color_root_button: app.theme_cls.accent_color
                            bg_color_stack_button: app.theme_cls.accent_color
                            callback: app.script_callback


                            

                    
                            

            

Screen:
    MDToolbar:
        id:toolbar
        pos_hint: {"top": 1}
        title:"Main menu"
        left_action_items: [["menu",lambda x: nav_draw.set_state("toggle")]]
        right_action_items: [["cogs",lambda x: app.theme()]]
        elevation: 10
    
    NavigationLayout:
        ScreenManager:
            id: screen_manager
            transition: NoTransition()
            Screen:
                id: main_menu
                name: "main_menu"
                GridLayout:
                    rows:3
                    BoxLayout:
                        size_hint:(None,None)
                        size:(root.ids.toolbar.width,root.ids.toolbar.height)
                    GridLayout:
                        id:main_grid
                        rows: 1
                    BoxLayout:
                        size_hint:(None,None)
                        size:(root.ids.toolbar.width,root.ids.toolbar.height*1.2)
                        MDFloatingActionButtonSpeedDial:
                            id: main_floatbutton
                            data: app.main_data
                            rotation_root_button: False
                            icon: "dots-vertical"

                            callback: app.callback
            Screen:
            
                name: "false_geodata"


            Screen:
                
                name: "raw_conv"

            Screen:
                
                name: "mask"

            Screen:
                
                name: "exif_copy"

                    
        MDNavigationDrawer:
            id: nav_draw
            MDGridLayout:
                
                rows:2
                BoxLayout:
                    orientation:'vertical'
                    padding: '10dp'
                    size_hint:(1,0.2)
                    MDLabel:
                        text:'Script list'
                        theme_text_color:'Primary'
                        font_style:'H6'
                NavDraw:
                    screen_manager: screen_manager
                    nav_draw: nav_draw
                    floatbutton: main_floatbutton
                    toolbar: toolbar
                    
                
"""