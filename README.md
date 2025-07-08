Ever found it annoying to install all your Baldurs Gate Enhanced Edition mods manually?
This will help you automate that process for the future!

1. Simply download all of your desired mods into a source folder.
2. Ensure they are all in .zip file format.
3. If any desired mod is a lone .exe file (eg. from Gibberlings3);
- Run them and extract them into a folder.
- Next, place the contents of that file into another .zip file.
4. Update mod_config.json to include the required parameters, like in the example provided.
5. The first component installed for your very first mod should include the language parameter, eg. "2" for English. 
6. Run the code in ModInstaller.py.
7. A file should be created in your destination folder, named: "install_mods.bat".
8. Run this file as administrator.
9. Watch the mods install...
