# vboard
*A virtual keyboard for Linux with Wayland support and extensive customization options.*


<img src="https://github.com/Varfolomeus/vboard/releases/download/v1_22/vboard_with_locale_switching.png" width="400">

## Overview
vboard is a lightweight, customizable virtual keyboard designed for Linux systems with Wayland support. It provides an on-screen keyboard solution that's especially useful for:

- Touchscreen devices without physical keyboards
- Systems with malfunctioning physical keyboards
- For only mouse / air-mouse usage of any computer - logon to system not supported but you can configure autologon and awakening without password required,
- Accessibility needs
- Kiosk applications

The keyboard supports customizable colors, opacity settings, and can be easily modified to support different layouts.

## Features
- **Customizable appearance**: Change background color, text color, and opacity
- **Persistent settings**: Configuration is saved between sessions
- **Modifier key support**: Use Shift, Ctrl, Alt and Super keys
- **Hold for repetitive clicks**: Keep holding the mouse button to trigger repeated clicks
- **Compact interface**: Headerbar with minimal controls to save screen space
- **Multilingual support**: In options section where you changing color and transparemcy you can switch locales (US, UA, RU)
- **Program reads and syncronizes system settings**: at start
- **Always-on-top**: Stays above other windows for easy access

### **1. Install Dependencies**  
Install on KDE  `python-uinput steam-devices` packages using your package manager:  
Install on GNOME  `python-uinput steam-devices` packages, GNOME Extensions Tool and `Shyriiwook Gnome extension` using your package manager and Internet browser:  


**For Debian/Ubuntu-based distributions:**  
```bash
sudo apt install python3-uinput steam-devices
```

additional for GNOME **!!! applicable on every distribution !!!**
Installing the Shyriiwook Gnome extension requires a little trick, as it is prohibited for some security reasons.
```bash
sudo apt update
sudo apt install gnome-shell-extensions
```
go to web page 
https://extensions.gnome.org/extension/6691/shyriiwook/
and install Shyriiwook Gnome extension using webpage interface
to make switchable on/off Shyriiwook Gnome extension switcher do the following trick:
```bash
gsettings set org.gnome.shell disable-extension-version-validation true
```
Run `Gnome Extensions` from app-menu
find and turn on this extension


**For Fedora-based distributions:**  
```bash
sudo dnf install python3-uinput steam-devices
```

**For arch-based distributions:**  
```bash
yay -Syu python-uinput steam-devices
```


### **2. Download vboard**  
Retrieve the latest version of `vboard.py` using `wget`:  
```bash
wget https://github.com/mdev588/vboard/releases/download/v1.21/vboard.py
```
multilocale version
KDE users
```bash
wget https://github.com/Varfolomeus/vboard/releases/download/v1_22/vboard_kde6+.py
```
GNOME v48 users
```bash
wget https://github.com/Varfolomeus/vboard/releases/download/v1_22/vboard_gnome_48+.py
```



### **3. Run**  

```bash choose your case
python3 vboard.py
python3 vboard_kde6+.py
python3 vboard_gnome_48+.py
```

### **4. Create shortcut (optional)**  
#### English only
```bash
mkdir -p ~/.local/share/applications/
cat > ~/.local/share/applications/vboard.desktop <<EOF
[Desktop Entry]
Exec=bash -c 'python3 ~/vboard.py'
Icon=preferences-desktop-keyboard
Name=Vboard
Terminal=false
Type=Application
Categories=Utility
NoDisplay=false
EOF
```
#### for multilocale versions:
KDE users
```bash
mkdir -p ~/.local/share/applications/
cat > ~/.local/share/applications/vboard.desktop <<EOF
[Desktop Entry]
Exec=bash -c 'python3 ~/vboard_kde6+.py'
Icon=preferences-desktop-keyboard
Name=Vboard
Terminal=false
Type=Application
Categories=Utility
NoDisplay=false
EOF
```
#### GNOME users
```bash
mkdir -p ~/.local/share/applications/
cat > ~/.local/share/applications/vboard.desktop <<EOF
[Desktop Entry]
Exec=bash -c 'python3 ~/vboard_gnome_48+.py'
Icon=preferences-desktop-keyboard
Name=Vboard
Terminal=false
Type=Application
Categories=Utility
NoDisplay=false
EOF
```
Make shortcut executable
```
chmod +x ~/.local/share/applications/vboard.desktop
```
Now you should find it in menu insdie Utility section

### Usage
When launched, vboard presents a compact keyboard with a minimal interface. The keyboard includes:
- Standard QWERTY layout keys
- Arrow keys
- Modifier keys (Shift, Ctrl, Alt, Super)

#### Interface Controls
- ☰ (menu) - Toggle visibility of other interface controls
- **Background dropdown** - Change the keyboard background color
- + - Increase opacity
- - - Decrease opacity
- US/UA/RU - Change locale to write on diferent language


### Configuration
vboard saves its settings to ~/.config/vboard/settings.conf. This configuration file stores:
- Background color
- Opacity level
- Text color
You can manually edit this file or use the built-in interface controls to customize the appearance.

### Customizing Keyboard Layout
The keyboard layout is defined in the rows list in the source code. To modify the layout:
1. Download the source code
2. Locate the rows definition (around line 175) search line with `#locales` `#rows depended on locale` if I did it you would to
3. Modify the key arrangement as needed
4. The format follows a nested list structure where each inner list represents a row of keys

## Troubleshooting
### 1. Error: 'no such device'
 Make sure uinput kernel module is loded with
```bash
sudo modprobe uinput
```

to make sure it auto load on boot create file with
```bash
echo 'uinput' | sudo tee /etc/modules-load.d/module-uinput.conf
```
---
### 2. Error: 'Permission Denied'
Reload udev rules with
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```
---
### 3. Error: 'steam-devices package not found'.
- in Fedora make sure the RPM Fusion repository is enabled. You can follow the guide here:
https://rpmfusion.org/Configuration
- Others can follow steps in here https://github.com/mdev588/vboard/issues/8
## Contributing 
Contributions to vboard are welcome! Here are some ways you can help:

- Add support for more keyboard layouts
- Improve the UI
- Fix bugs or implement new features
- Improve documentation

Please make sure to test your changes before submitting a pull request.

## License
vboard is licensed under the GNU Lesser General Public License v2.1. See LICENSE.md for the full license text.

## Note

* Currently only the QWERTY US layout is supported, so other layouts may cause some keys to produce different keystrokes. But this could easily be fixed by modifying the row list arrangement.

* Currently do not work correctly on wlroots based window managers.

