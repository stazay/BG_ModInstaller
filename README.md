# 🔧 BGEE & BG2EE Mod Installer Tool

Did you ever find it tedious to install all your _Baldur's Gate: Enhanced Edition_ mods manually?  
This script helps you automate that process for the future, using Python!

---

## 📁 File Structure

| File | Purpose |
|------|---------|
| `ModInstaller.py` | Shared base class — extraction, batch generation logic |
| `bg1_install.py` | Launcher for Baldur's Gate 1 |
| `bg2_install.py` | Launcher for Baldur's Gate 2 |
| `mod_config_bg1.json` | BG1 mod configuration |
| `mod_config_bg2.json` | BG2 mod configuration |
| `mod_notes_bg1.json` | Notes explaining each input choice for BG1 mods |
| `mod_notes_bg2.json` | Notes explaining each input choice for BG2 mods |
| `example_mod_config.json` | Minimal example config to get started |

---

## 🚀 How to Use

1. Download the contents of this repository.
2. Download all of your desired mods into a **source folder**.
3. Update the relevant config file (`mod_config_bg1.json` or `mod_config_bg2.json`) with the required parameters:
   - `source_folder` — where your downloaded mod archives are
   - `destination_folder` — your game directory
   - `mod_components` — one entry per mod, with:
     - `setup_file` — the WeiDU `.exe` filename
     - `inputs` — array of answers you would enter when installing manually
     - `description` — readable name shown in logs
     - `active` — whether the mod is actively being updated
     - `download_url` — where to download the mod
     - `version` — current version
     - `latest_update` — date of latest update
   - `install_order` — list of mod keys in the order they should be installed. Only mods listed here will be installed.
   > ⚠️ Mod keys (the names used in `mod_components` and `install_order`) must not contain spaces or apostrophes, as they are used to generate filenames. Use underscores instead, e.g. `Jims_Fix_Pack`.
4. **Important:** The first input for your very first mod should include the language parameter, e.g. `"2"` for English.
5. Run the relevant launcher:
   - `python bg1_install.py` for BG1
   - `python bg2_install.py` for BG2
6. A batch file will be created in your destination folder named `install_mods.bat`.
7. Run this file **as administrator** (required so that all mod prompts run in the same command line window).
8. Watch the mods install...

---

## ⚙️ What is 7-Zip and why is it included?

This tool uses [7-Zip](https://www.7-zip.org/), a popular open-source archive manager.  
**7-Zip** is needed because many BGEE mods (like some from Gibberlings3) come as **self-extracting `.exe` files**.  
These `.exe` files aren't standard installers — they're really just **compressed archives** in disguise. 7-Zip can extract them automatically, so you don't have to do it by hand.

To make this tool easy to use for everyone, a **portable copy of `7z.exe` and `7z.dll`** is included.  
There's no need to install anything — the Python script just runs `7z.exe` behind the scenes to unpack your mods.

---

## 🔒 What if I don't want to trust the included 7-Zip?

If you prefer, you can:

- Download **7-Zip** yourself directly from [7-zip.org](https://www.7-zip.org/), and then replace the `7z.exe` and `7z.dll` in the `7z` folder with your own copy.
- Or, if you don't want to use 7-Zip at all, you can manually extract `.exe` mod files to a `.zip` format yourself.  
  In that case, the tool will still work — it will extract the `.zip` archives using Python's built-in zip support.
