import os

from libs.cli import Cli

from .filemanager import FileManager

def setup():
    replacements = {
        "/usr/share/applications/org.kde.konsole.desktop": (
            "Exec=konsole", 
            """Exec=bash -ic 'cd "%k"; pwd=$(echo $PWD); konsole --new-tab --workdir "$pwd"; wmctrl -l | grep " "$(xdotool get_desktop)" " | grep Konsole && jumpapp -w konsole'"""
            ),
        
        "/usr/share/applications/org.kde.kate.desktop": (
            "Exec=kate -b %U", 
            "Exec=kate -b -s Default %U"
            ),
        
        "/var/lib/snapd/desktop/applications/chromium_chromium.desktop": (
            "Icon=/snap/chromium/1691/chromium.png",
            f"Icon={FileManager.get_path('icons', 'chrome.png')}"
            ),
        }
        
    for filename, (old, new) in replacements.items():
        if os.path.exists(filename):
            replace(filename, old, new)

def replace(path, old, new):
    content_list = FileManager.load(path).split("\n")
    content_list = [l if l != old else new for l in content_list]
    content = "".join(content_list)
    FileManager.save(content, path)
        
if __name__ == "__main__":
    setup()
