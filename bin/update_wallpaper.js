var desktop = desktops()[0]
desktop.wallpaperPlugin = 'org.kde.image';
desktop.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');
desktop.writeConfig('Image', '__wallpaper_uri__');
