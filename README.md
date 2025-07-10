# BG Mod Installer Tool

Ever found it annoying to install all your Baldurs Gate Enhanced Edition mods manually?
This will help you automate that process for the future!

1. Download the contents of this repository.
2. Simply download all of your desired mods into a source folder.
3. Update mod_config.json to include the required parameters, like in the example provided.
- source_folder
- destination_folder
- mods + install inputs
- install order
5. Important note: the first component installed for your very first mod should include the language parameter, eg. "2" for English. 
6. Run the script in ModInstaller.py.
7. A file should be created in your destination folder, named: "install_mods.bat".
8. Run this file as administrator.
9. Watch the mods install...
