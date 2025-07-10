# BGEE Mod Installer Tool

Did you ever find it tedious to install all your *Baldur’s Gate: Enhanced Edition* mods manually?  
This tool helps you automate that process for the future!

It’s very simple to use:

1. Download the contents of this repository.  
2. Download all of your desired mods into a **source folder**.  
3. Update `mod_config.json` with the required parameters, like in the example provided. You should set:
   - `source_folder`
   - `destination_folder`
   - `mod_components`
   - `install_order`
4. **Important:** The first component installed for your very first mod should include the language parameter, e.g. `"2"` for English.
5. Run the script: `ModInstaller.py`.  
6. A batch file will be created in your destination folder, named `install_mods.bat`.  
7. Run this file **as administrator** (required so that all mod prompts run in the same command line window).
8. Watch the mods install...

---

## ⚙️ What is 7-Zip and why is it included?

This tool uses [7-Zip](https://www.7-zip.org/), a popular open-source archive manager.  
**7-Zip** is needed because many BGEE mods (like some from Gibberlings3) come as **self-extracting `.exe` files**.  
These `.exe` files aren’t standard installers — they’re really just **compressed archives** in disguise. 7-Zip can extract them automatically, so you don’t have to do it by hand.

To make this tool easy to use for everyone, a **portable copy of `7z.exe` and `7z.dll`** is included.  
There’s no need to install anything — the Python script just runs `7z.exe` behind the scenes to unpack your mods.

---

## 🔒 What if I don’t want to trust the included 7-Zip?

If you prefer, you can:
- Download **7-Zip** yourself directly from [7-zip.org](https://www.7-zip.org/).
- Replace the `7z.exe` and `7z.dll` in the `7z` folder with your own copy.
- Or, if you don’t want to use `7-Zip` at all, you can manually extract `.exe` mod files to `.zip` yourself.  
  In that case, the tool will still work — it will extract the `.zip` archives using Python’s built-in zip support.
