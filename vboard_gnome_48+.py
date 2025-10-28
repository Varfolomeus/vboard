import dbus
import subprocess
import gi
import uinput
import time
import os
import configparser
from gi.repository import GLib
import dbus.mainloop.glib 
#  install Shyriiwook Gnome extension https://extensions.gnome.org/extension/6691/shyriiwook/

os.environ['GDK_BACKEND'] = 'x11'

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

keymapList = ["us", "ru", "uk", "ua"]
current_keymap = keymapList[0]

# GNOME Layout Management Functions
def get_current_layout_from_gnome():
    """Get the current keyboard layout from GNOME via gsettings"""
    try:
        bus = dbus.SessionBus()

        # 2. Визначаємо цільові параметри
        SERVICE_NAME = 'org.gnome.Shell'
        OBJECT_PATH = '/me/madhead/Shyriiwook'
        CUSTOM_INTERFACE = 'me.madhead.Shyriiwook' 
        
        # 3. Отримуємо проксі-об'єкт для сервісу
        proxy = bus.get_object(SERVICE_NAME, OBJECT_PATH)

        # 4. Підключаємося до стандартного інтерфейсу властивостей D-Bus
        properties_interface = dbus.Interface(
            proxy, 
            dbus.PROPERTIES_IFACE # 'org.freedesktop.DBus.Properties'
        )

        # 5. Читаємо властивості:
        
        # Читаємо 'currentLayout' (повертає рядок)
        current_layout = str(properties_interface.Get(CUSTOM_INTERFACE, 'currentLayout'))
        
        # Читаємо 'availableLayouts' (повертає масив D-Bus, який треба конвертувати)
        available_layouts_dbus = properties_interface.Get(CUSTOM_INTERFACE, 'availableLayouts')
        
        # Конвертуємо масив D-Bus в список рядків
        available_layouts = [str(l) for l in available_layouts_dbus]
        return current_layout, available_layouts
    except Exception as e:
        print(f"Error getting layout: {e}")
        return None, None

key_mapping_en = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Q", uinput.KEY_W: "W", uinput.KEY_E: "E", uinput.KEY_R: "R",
    uinput.KEY_T: "T", uinput.KEY_Y: "Y", uinput.KEY_U: "U", uinput.KEY_I: "I", uinput.KEY_O: "O", uinput.KEY_P: "P",
    uinput.KEY_LEFTBRACE: "[", uinput.KEY_RIGHTBRACE: "]", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "A",
    uinput.KEY_S: "S", uinput.KEY_D: "D", uinput.KEY_F: "F", uinput.KEY_G: "G", uinput.KEY_H: "H", uinput.KEY_J: "J", uinput.KEY_K: "K",
    uinput.KEY_L: "L", uinput.KEY_SEMICOLON: ";", uinput.KEY_APOSTROPHE: "'", uinput.KEY_GRAVE: "`", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "\\", uinput.KEY_Z: "Z", uinput.KEY_X: "X", uinput.KEY_C: "C", uinput.KEY_V: "V", uinput.KEY_B: "B",
    uinput.KEY_N: "N", uinput.KEY_M: "M", uinput.KEY_COMMA: ",", uinput.KEY_DOT: ".", uinput.KEY_SLASH: "/", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PageUp", uinput.KEY_DELETE: "Delete", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PageDown",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R"}

key_mapping_ru = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Й", uinput.KEY_W: "Ц", uinput.KEY_E: "У", uinput.KEY_R: "К",
    uinput.KEY_T: "Е", uinput.KEY_Y: "Н", uinput.KEY_U: "Г", uinput.KEY_I: "Ш", uinput.KEY_O: "Щ", uinput.KEY_P: "З",
    uinput.KEY_LEFTBRACE: "Х", uinput.KEY_RIGHTBRACE: "Ъ", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "Ф",
    uinput.KEY_S: "Ы", uinput.KEY_D: "В", uinput.KEY_F: "А", uinput.KEY_G: "П", uinput.KEY_H: "Р", uinput.KEY_J: "О", uinput.KEY_K: "Л",
    uinput.KEY_L: "Д", uinput.KEY_SEMICOLON: "Ж", uinput.KEY_APOSTROPHE: "Э", uinput.KEY_GRAVE: "Ё", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "\\", uinput.KEY_Z: "Я", uinput.KEY_X: "Ч", uinput.KEY_C: "С", uinput.KEY_V: "М", uinput.KEY_B: "И",
    uinput.KEY_N: "Т", uinput.KEY_M: "Ь", uinput.KEY_COMMA: "Б", uinput.KEY_DOT: "Ю", uinput.KEY_SLASH: ".", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PageUp", uinput.KEY_DELETE: "Delete", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PageDown",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R"}

key_mapping_uk = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Й", uinput.KEY_W: "Ц", uinput.KEY_E: "У", uinput.KEY_R: "К",
    uinput.KEY_T: "Е", uinput.KEY_Y: "Н", uinput.KEY_U: "Г", uinput.KEY_I: "Ш", uinput.KEY_O: "Щ", uinput.KEY_P: "З",
    uinput.KEY_LEFTBRACE: "Х", uinput.KEY_RIGHTBRACE: "Ї", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "Ф",
    uinput.KEY_S: "І", uinput.KEY_D: "В", uinput.KEY_F: "А", uinput.KEY_G: "П", uinput.KEY_H: "Р", uinput.KEY_J: "О", uinput.KEY_K: "Л",
    uinput.KEY_L: "Д", uinput.KEY_SEMICOLON: "Ж", uinput.KEY_APOSTROPHE: "Є", uinput.KEY_GRAVE: "\'", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "Ґ", uinput.KEY_Z: "Я", uinput.KEY_X: "Ч", uinput.KEY_C: "С", uinput.KEY_V: "М", uinput.KEY_B: "И",
    uinput.KEY_N: "Т", uinput.KEY_M: "Ь", uinput.KEY_COMMA: "Б", uinput.KEY_DOT: "Ю", uinput.KEY_SLASH: ".", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PageUp", uinput.KEY_DELETE: "Delete", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PageDown",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R"}

key_mapping = key_mapping_en

class VirtualKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Virtual Keyboard", name="toplevel")

        self.set_border_width(0)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.set_modal(False)
        self.set_focus_on_map(False)
        self.set_can_focus(False)
        self.set_accept_focus(False)
        self.width=0
        self.height=0

        self.CONFIG_DIR = os.path.expanduser("~/.config/vboard")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, "settings.conf")
        self.config = configparser.ConfigParser()

        self.bg_color = "0, 0, 0"
        self.opacity="0.90"
        self.text_color="white"
        self.read_settings()
        self.current_layout_index = 0
        self.available_layouts=[]
        # Get available layouts and current layout from GNOME

        current_layout_code, layout_codes = get_current_layout_from_gnome()
        # print(f"Current layout code: {current_layout_code}")
        # print(f"Available layout codes: {layout_codes}")
        if current_layout_code is not None:
            self.current_layout_index = layout_codes.index(current_layout_code)
            global current_keymap
            current_keymap = current_layout_code
            self.available_layouts = layout_codes
        else :
            print("Layouts not found")
            return

        self.modifiers = {
            uinput.KEY_LEFTSHIFT: False,
            uinput.KEY_RIGHTSHIFT: False,
            uinput.KEY_LEFTCTRL: False,
            uinput.KEY_RIGHTCTRL: False,
            uinput.KEY_LEFTALT: False,
            uinput.KEY_RIGHTALT: False,
            uinput.KEY_LEFTMETA: False,
            uinput.KEY_RIGHTMETA: False
        }
        self.colors = [
            ("Black", "0,0,0"),
            ("Red", "255,0,0"),
            ("Pink", "255,105,183"),
            ("White", "255,255,255"),
            ("Green", "0,255,0"),
            ("Blue", "0,0,110"),
            ("Gray", "128,128,128"),
            ("Dark Gray", "64,64,64"),
            ("Orange", "255,165,0"),
            ("Yellow", "255,255,0"),
            ("Purple", "128,0,128"),
            ("Cyan", "0,255,255"),
            ("Teal", "0,128,128"),
            ("Brown", "139,69,19"),
            ("Gold", "255,215,0"),
            ("Silver", "192,192,192"),
            ("Turquoise", "64,224,208"),
            ("Magenta", "255,0,255"),
            ("Olive", "128,128,0"),
            ("Maroon", "128,0,0"),
            ("Indigo", "75,0,130"),
            ("Beige", "245,245,220"),
            ("Lavender", "230,230,250")
        ]

        if (self.width!=0):
            self.set_default_size(self.width, self.height)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.buttons=[]
        self.modifier_buttons={}
        self.row_buttons=[]
        self.color_combobox = Gtk.ComboBoxText()
        self.set_titlebar(self.header)
        self.create_settings()

        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        grid.set_name("grid")
        self.add(grid)
        self.apply_css()
        self.device = uinput.Device(list(key_mapping.keys()))

        # Define rows for keys
        self.rows_en = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace" ],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift_R", "↑"],
            ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "→", "↓"]
        ]
        self.rows_ru = [
            ["Ё", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ", "\\"],
            ["CapsLock", "Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "Enter"],
            ["Shift_L", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ".", "Shift_R", "↑"],
            ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "↓", "→"]
        ]

        self.rows_uk = [
            ["\'", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ї", "Ґ"],
            ["CapsLock", "Ф", "І", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Є", "Enter"],
            ["Shift_L", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ".", "Shift_R", "↑"],
            ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "↓", "→"]
        ]

        self.rows=None
        if current_keymap in ["us", "en"]:
            self.rows = self.rows_en
        elif current_keymap == "ru":
            self.rows = self.rows_ru
        elif current_keymap in ["uk", "ua", "ukrainian"]:
            self.rows = self.rows_uk
            current_keymap = "uk"
        else:
            self.rows = self.rows_en

        for row_index, keys in enumerate(self.rows):
            self.create_row(grid, row_index, keys)

        self.layout_watcher = ShyriiwookWatcher(self.on_layout_changed_external)
        self.layout_watcher.start()

    def cycle_layout(self, widget=None):
        """Cycle to the next keyboard layout by simulating Super+Space"""
        if not self.available_layouts:
            print("No layouts available")
            return

        # Simulate Super+Space to switch layout (GNOME's native shortcut)
        try:
            """
            gdbus call --session --dest org.gnome.Shell --object-path /me/madhead/Shyriiwook --method me.madhead.Shyriiwook.activate "us"

            """
            self.current_layout_index = (self.current_layout_index + 1) % len(self.available_layouts)
            subprocess.run(["gdbus", "call", "--session", "--dest", "org.gnome.Shell", "--object-path", "/me/madhead/Shyriiwook", "--method", "me.madhead.Shyriiwook.activate", self.available_layouts[self.current_layout_index]])
        except Exception as e:
            print(f"Error simulating layout switch: {e}")
        
        # PRAY and proceed! 🙏
        # Cycle to next layout in our list
        
        # Update our internal state optimistically
        layout_info = self.available_layouts[self.current_layout_index]
        if layout_info is not None:
            layout_code = layout_info
            self.layout_button.set_label(layout_code.upper())
            
            global current_keymap, key_mapping
            current_keymap = layout_code
            
            if layout_code in ["us", "en"]:
                current_keymap = "us"
                key_mapping = key_mapping_en
            elif layout_code == "ru":
                key_mapping = key_mapping_ru
            elif layout_code in ["uk", "ua", "ukrainian"]:
                current_keymap = "uk"
                key_mapping = key_mapping_uk
            
            # print(f"🙏 Switched to: {current_keymap.upper()} (trusting GNOME...)")
            self.rebuild_keyboard()
    
    def on_layout_changed_external(self, layout_code):
        GLib.idle_add(self._handle_layout_change, layout_code)

    def _handle_layout_change(self, layout_code):
        """Called when layout is changed externally"""
        # print(f"[VirtualKeyboard] Layout changed to: {layout_code}")
        if layout_code in self.available_layouts:
            self.current_layout_index = self.available_layouts.index(layout_code)
            self.layout_button.set_label(layout_code.upper())

            global current_keymap, key_mapping
            current_keymap = layout_code
            # print(f"[VirtualKeyboard] current_keymap changed to: {layout_code}")


            if layout_code in ["us", "en"]:
                current_keymap = "us"
                key_mapping = key_mapping_en
            elif layout_code == "ru":
                key_mapping = key_mapping_ru
            elif layout_code in ["uk", "ua", "ukrainian"]:
                current_keymap = "uk"
                key_mapping = key_mapping_uk

        self.rebuild_keyboard()
    def rebuild_keyboard(self):
        """Rebuild the keyboard with the current layout"""
        global current_keymap, key_mapping

        if current_keymap in ["us", "en"]:
            key_mapping = key_mapping_en
            self.rows = self.rows_en
        elif current_keymap == "ru":
            key_mapping = key_mapping_ru
            self.rows = self.rows_ru
        elif current_keymap in ["uk", "ua", "ukrainian"]:
            key_mapping = key_mapping_uk
            self.rows = self.rows_uk
        else:
            key_mapping = key_mapping_en
            self.rows = self.rows_en

        child = self.get_child()
        if child:
            self.remove(child)

        self.row_buttons = []
        self.modifier_buttons = {}

        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        grid.set_name("grid")
        self.add(grid)

        for row_index, keys in enumerate(self.rows):
            self.create_row(grid, row_index, keys)

        self.device = uinput.Device(list(key_mapping.keys()))

        self.show_all()
        self.apply_css()

        for button in self.buttons:
            if button != self.layout_button and button.get_label() != "☰":
                if not self.buttons[1].get_visible():
                    button.set_visible(False)
        if not self.buttons[1].get_visible():
            self.color_combobox.set_visible(False)

    def create_settings(self):
        self.create_button("☰", self.change_visibility,callbacks=1)

        layout_code, layout_codes = get_current_layout_from_gnome()
        if layout_code:
            label = layout_code.upper()
        else:
            label = "US"
        self.layout_button = Gtk.Button(label=label)
        self.layout_button.set_name("headbar-button")
        self.layout_button.connect("clicked", self.cycle_layout)
        self.layout_button.set_tooltip_text("Click to change keyboard layout")
        self.header.add(self.layout_button)
        self.buttons.append(self.layout_button)

        self.create_button("+", self.change_opacity,True,2)
        self.create_button("-", self.change_opacity, False,2)
        self.create_button( f"{self.opacity}")
        self.color_combobox.append_text("Change Background")
        self.color_combobox.set_active(0)
        self.color_combobox.connect("changed", self.change_color)
        self.color_combobox.set_name("combobox")
        self.header.add(self.color_combobox)

        for label, color in self.colors:
            self.color_combobox.append_text(label)

    def on_resize(self, widget, event):
        self.width, self.height = self.get_size()

    def create_button(self, label_="", callback=None, callback2=None, callbacks=0):
        button= Gtk.Button(label=label_)
        button.set_name("headbar-button")
        if callbacks==1:
            button.connect("clicked", callback)
        elif callbacks==2:
            button.connect("clicked", callback, callback2)

        if label_==self.opacity:
            self.opacity_btn=button
            self.opacity_btn.set_tooltip_text("opacity")

        self.header.add(button)
        self.buttons.append(button)

    def change_visibility(self, widget=None):
        for button in self.buttons:
            if button.get_label()!="☰":
                button.set_visible(not button.get_visible())
        self.color_combobox.set_visible(not self.color_combobox.get_visible() )

    def change_color (self, widget):
        label=self.color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.bg_color = color_

        if (self.bg_color in {"255,255,255" ,"0,255,0" , "255,255,0", "245,245,220", "230,230,250", "255,215,0"}):
            self.text_color="#1C1C1C"
        else:
            self.text_color="white"
        self.apply_css()

    def change_opacity(self,widget, boolean):
        if (boolean):
            self.opacity = str(round(min(1.0, float(self.opacity) + 0.01),2))
        else:
            self.opacity = str(round(max(0.0, float(self.opacity) - 0.01),2))
        self.opacity_btn.set_label(f"{self.opacity}")
        self.apply_css()

    def apply_css (self):
        provider = Gtk.CssProvider()

        css = f"""
        headerbar {{
            background-color: rgba({self.bg_color}, {self.opacity});
            border: 0px;
            box-shadow: none;

        }}

        headerbar button{{
            min-width: 40px;
            padding: 0px;
            border: 0px;
            margin: 0px;
        }}

        headerbar .titlebutton {{
            min-width: 60px;  /* Set custom min-width for the close button */
            min-height: 40px
        }}

        headerbar button label{{
        color: {self.text_color};

        }}

        #headbar-button, #combobox button.combo {{
            background-image: none;
        }}

        #toplevel {{
            background-color: rgba({self.bg_color}, {self.opacity});
        }}

        #grid button label{{
            color: {self.text_color};
        }}

        #grid button {{
                    border: none ;
                    background-image: none;
                }}

        button {{
            background-color: transparent;
            color:{self.text_color};

        }}

       #grid button:hover {{
            border: 1px solid #00CACB;
        }}

       grid button:active,
       grid button:focus {{
            border: 1px solid {self.text_color};
            background-color: #d82504;
            font-size: 1.5em;
            font-weight: 700;
        }}

       tooltip {{
            color: white;
            padding: 5px;
        }}

       #combobox button.combo  {{

            color: {self.text_color};
            padding: 5px;
        }}
        """

        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.GError as e:
            print(f"CSS Error: {e.message}")
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def create_row(self, grid, row_index, keys):
        col = 0
        width=0

        for key_label in keys:
            key_event = next((key for key, label in key_mapping.items() if label == key_label), None)
            if key_event:
                if key_label in ("Shift_R", "Shift_L", "Alt_L", "Alt_R", "Ctrl_L", "Ctrl_R", "Super_L", "Super_R"):
                    button = Gtk.Button(label=key_label[:-2])
                else:
                    button = Gtk.Button(label=key_label)
                button.connect("pressed", self.on_button_press, key_event)
                button.connect("released", self.on_button_release)
                button.connect("leave-notify-event", self.on_button_release)
                self.row_buttons.append(button)
                if key_event in self.modifiers:
                    self.modifier_buttons[key_event] = button
                if key_label == "Space": width=6
                elif key_label == "CapsLock": width=2
                elif key_label == "Shift_R" : width=2
                elif key_label == "Shift_L" : width=2
                elif key_label == "Backspace": width=2
                elif key_label == "`" or key_label == "\'" or key_label == "Ё": width=1
                elif key_label == "\\" or key_label == "Ґ": width=2
                elif key_label == "Enter": width=2
                else: width=1

                grid.attach(button, col, row_index, width, 1)
                col += width

    def update_label_en(self, show_symbols):
        button_positions = [(0, "` ~"), (1, "1 !"), (2, "2 @"), (3, "3 #"), (4, "4 $"), (5, "5 %"), (6, "6 ^"), (7, "7 &"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        , (11, "- _"), (12, "= +"), (21, "U U"), (25,"[ {"), (26,"] }"), (27,"\\ |"), (38, "; :"), (39, "' \""), (49, ", <"), (50, ". >"), (51, "/ ?")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if show_symbols:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])
    
    def update_label_ru(self, show_symbols):
        button_positions = [(0, "Ё Ё"), (1, "1 !"), (2, "2 \""), (3, "3 №"), (4, "4 ;"), (5, "5 %"), (6, "6 :"), (7, "7 ?"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        , (11, "- _"), (12, "= +"), (27,"\\ /"), (51, ". ,")]

        for pos, label in button_positions:
            if pos < len(self.row_buttons):
                label_parts = label.split()
                if show_symbols:
                    self.row_buttons[pos].set_label(label_parts[1])
                else:
                    self.row_buttons[pos].set_label(label_parts[0])

    def update_label_uk(self, show_symbols):
        button_positions = [(0, "\' ʼ"), (1, "1 !"), (2, "2 \""), (3, "3 №"), (4, "4 ;"), (5, "5 %"), (6, "6 :"), (7, "7 ?"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        , (11, "- _"), (12, "= +"), (51, ". ,")]

        for pos, label in button_positions:
            if pos < len(self.row_buttons):
                label_parts = label.split()
                if show_symbols:
                    self.row_buttons[pos].set_label(label_parts[1])
                else:
                    self.row_buttons[pos].set_label(label_parts[0])

    def update_label_ukr_alt(self, show_symbols):
        button_positions = [(21, "Г Ґ")]

        for pos, label in button_positions:
            if pos < len(self.row_buttons):
                label_parts = label.split()
                if show_symbols:
                    self.row_buttons[pos].set_label(label_parts[1])
                else:
                    self.row_buttons[pos].set_label(label_parts[0])
    
    def update_modifier(self, key_event, value):
      self.modifiers[key_event] = value
      button = self.modifier_buttons[key_event]
      style_context = button.get_style_context()
      if (value):
          style_context.add_class('pressed')
      else:
          style_context.remove_class('pressed')

    def on_button_press(self, widget, key_event):
        if key_event in self.modifiers:
            self.update_modifier(key_event, not self.modifiers[key_event])

            if self.modifiers[uinput.KEY_LEFTSHIFT] and self.modifiers[uinput.KEY_RIGHTSHIFT]:
                self.update_modifier(uinput.KEY_LEFTSHIFT, False)
                self.update_modifier(uinput.KEY_RIGHTSHIFT, False)

            global current_keymap
            if self.modifiers[uinput.KEY_LEFTSHIFT] or self.modifiers[uinput.KEY_RIGHTSHIFT]:
                if current_keymap in ["us", "en"]:
                    self.update_label_en(True)
                elif current_keymap == "ru":
                    self.update_label_ru(True)
                elif current_keymap in ["uk", "ua"]:
                    self.update_label_uk(True)
            else:
                if current_keymap in ["us", "en"]:
                    self.update_label_en(False)
                elif current_keymap == "ru":
                    self.update_label_ru(False)
                elif current_keymap in ["uk", "ua"]:
                    self.update_label_uk(False)
            if self.modifiers[uinput.KEY_RIGHTALT] and current_keymap in ["uk", "ua"]:
                self.update_label_ukr_alt(True)
            elif current_keymap in ["uk", "ua"]:
                self.update_label_ukr_alt(False)

            return

        self.emit_key(key_event)
        self.delay_source = GLib.timeout_add(400, self.start_repeat, key_event)

    def on_button_release(self, widget, *args):
        if hasattr(self, "delay_source"):
            GLib.source_remove(self.delay_source)
            del self.delay_source
        if hasattr(self, "repeat_source"):
            GLib.source_remove(self.repeat_source)
            del self.repeat_source

    def start_repeat(self, key_event):
        self.repeat_source = GLib.timeout_add(100, self.repeat_key, key_event)
        return False

    def repeat_key(self, key_event):
        self.emit_key(key_event)
        return True

    def emit_key(self, key_event):
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 1)

        self.device.emit(key_event, 1)
        self.device.emit(key_event, 0)

        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 0)
                self.update_modifier(mod_key, False)

        if current_keymap in ["us", "en"]:
            self.update_label_en(False)
        elif current_keymap == "ru":
            self.update_label_ru(False)
        elif current_keymap in ["uk", "ua"]:
            self.update_label_uk(False)
            self.update_label_ukr_alt(False)
        else:
            self.update_label_en(False)

    def read_settings(self):
        try:
            os.makedirs(self.CONFIG_DIR, exist_ok=True)
        except PermissionError:
            print("Warning: No permission to create the config directory. Proceeding without it.")

        try:
            if os.path.exists(self.CONFIG_FILE):
                self.config.read(self.CONFIG_FILE)
                self.bg_color = self.config.get("DEFAULT", "bg_color" )
                self.opacity = self.config.get("DEFAULT", "opacity" )
                self.text_color = self.config.get("DEFAULT", "text_color", fallback="white" )
                self.width=self.config.getint("DEFAULT", "width" , fallback=0)
                self.height=self.config.getint("DEFAULT", "height", fallback=0)

                print(f"rgba: {self.bg_color}, {self.opacity}")

        except configparser.Error as e:
            print(f"Warning: Could not read config file ({e}). Using default values.")

    def save_settings(self):
        self.config["DEFAULT"] = {"bg_color": self.bg_color, "opacity": self.opacity, "text_color": self.text_color, "width": self.width, "height": self.height}

        try:
            with open(self.CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)

        except (configparser.Error, IOError) as e:
            print(f"Warning: Could not write to config file ({e}). Changes will not be saved.")

class ShyriiwookWatcher:
    def __init__(self, callback, poll_interval=1.0):
        import dbus
        import dbus.mainloop.glib
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        self.proxy = self.bus.get_object('org.gnome.Shell', '/me/madhead/Shyriiwook')
        self.callback = callback
        self.poll_interval = poll_interval
        self.last_layout = None

    def get_current_layout(self):
        return self.proxy.Get('me.madhead.Shyriiwook', 'currentLayout',
                              dbus_interface='org.freedesktop.DBus.Properties')

    def start(self):
        import threading
        def loop():
            while True:
                try:
                    layout = self.get_current_layout()
                    # print(f"[ShyriiwookWatcher] Layout: {layout}")
                    if layout != self.last_layout:
                        self.last_layout = layout
                        self.callback(layout)
                except Exception as e:
                    print(f"[ShyriiwookWatcher] Error: {e}")
                time.sleep(self.poll_interval)
        threading.Thread(target=loop, daemon=True).start()



if __name__ == "__main__":
    # Get current layout from GNOME
    layout_code, layout_codes = get_current_layout_from_gnome()
    if layout_code:
        current_keymap = layout_code
        if current_keymap in ["us", "en"]:
            key_mapping = key_mapping_en
        elif current_keymap == "ru":
            key_mapping = key_mapping_ru
        elif current_keymap in ["uk", "ua", "ukrainian"]:
            key_mapping = key_mapping_uk
    else:
        current_keymap = "us"
        key_mapping = key_mapping_en

    win = VirtualKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.connect("destroy", lambda w: win.save_settings())
    win.show_all()
    win.connect("configure-event", win.on_resize)
    win.change_visibility()
    Gtk.main()
