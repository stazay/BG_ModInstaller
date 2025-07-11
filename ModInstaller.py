import json
import os
import subprocess
import zipfile


class SimpleModExtractor:
    def __init__(self, config_file='mod_config.json'):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.source_folder = self.config['source_folder']
        self.destination_folder = self.config['destination_folder']
        self.mod_components = self.config['mod_components']
        self.install_order = self.config.get('install_order', [])

        # Path to bundled 7z.exe — adjust if needed
        self.seven_zip = os.path.join(os.path.dirname(__file__), '7z', '7z.exe')

    def extract_mods(self):
        print("Starting mod extraction...")
        os.makedirs(self.destination_folder, exist_ok=True)
        extracted_count = 0

        for root, dirs, files in os.walk(self.source_folder):
            for filename in files:
                filepath = os.path.join(root, filename)

                if filename.lower().endswith('.zip'):
                    if self.extract_zip(filepath):
                        extracted_count += 1

                elif filename.lower().endswith('.exe'):
                    if self.extract_exe_with_7zip(filepath):
                        extracted_count += 1

        print(f"Extraction complete. {extracted_count} mods extracted.")
        return extracted_count > 0

    def extract_zip(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                namelist = zip_ref.namelist()
                has_setup = any(
                    name.lower().startswith('setup-') and name.lower().endswith('.exe') and '/' not in name.rstrip('/')
                    for name in namelist
                )

                if has_setup:
                    zip_ref.extractall(self.destination_folder)
                    print(f"✓ Extracted {os.path.basename(zip_path)} (direct contents)")
                else:
                    top_level = set(name.split('/')[0] for name in namelist if '/' in name)
                    if len(top_level) == 1:
                        top_folder = top_level.pop()
                        members = [name for name in namelist if name.startswith(top_folder + '/')]
                        for member in members:
                            target_path = os.path.join(self.destination_folder, member[len(top_folder) + 1:])
                            if member.endswith('/'):
                                os.makedirs(target_path, exist_ok=True)
                            else:
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with open(target_path, 'wb') as f:
                                    f.write(zip_ref.read(member))
                        print(f"✓ Extracted {os.path.basename(zip_path)} (from folder '{top_folder}/')")
                    else:
                        zip_ref.extractall(self.destination_folder)
                        print(f"! Extracted {os.path.basename(zip_path)} (fallback — structure unknown)")
            return True
        except Exception as e:
            print(f'✗ Error extracting {os.path.basename(zip_path)}: {str(e)}')
            return False

    def extract_exe_with_7zip(self, exe_path):
        if not os.path.exists(self.seven_zip):
            print("⚠️  7z.exe not found! Skipping .exe extraction.")
            return False

        try:
            result = subprocess.run([
                self.seven_zip,
                'x',
                exe_path,
                f'-o{self.destination_folder}',
                '-y'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ Extracted {os.path.basename(exe_path)} (with 7-Zip)")
                return True
            else:
                print(f'✗ 7-Zip extraction failed: {result.stderr}')
                return False

        except Exception as e:
            print(f'✗ Error running 7-Zip: {str(e)}')
            return False

    def list_setup_files(self):
        print(f"\nSetup files found in {self.destination_folder}:")
        setup_files = []

        if not os.path.exists(self.destination_folder):
            print("Destination folder doesn't exist!")
            return setup_files

        for file in os.listdir(self.destination_folder):
            if file.lower().startswith('setup-') and file.lower().endswith('.exe'):
                setup_files.append(file)
                print(f"  - {file}")

        if not setup_files:
            print("  No setup files found!")

        return setup_files

    def create_simple_batch(self, output_file='install_mods.bat'):
        batch_path = os.path.join(self.destination_folder, output_file)
        batch_content = [
            '@echo off',
            'echo BG Enhanced Edition Mod Installer',
            'echo =====================================',
            f'cd /d "{self.destination_folder}"',
            'echo Changed to mod directory',
            'echo.',
            ''
        ]

        for mod_name in self.install_order:
            mod_config = self.mod_components.get(mod_name)
            if not mod_config:
                print(f"Warning: Mod '{mod_name}' not found in mod_components, skipping.")
                continue

            setup_file = mod_config['setup_file']
            inputs = mod_config.get('inputs', [])
            description = mod_config.get('description', '')

            input_filename = f'{mod_name}_inputs.txt'
            input_path = os.path.join(self.destination_folder, input_filename)
            with open(input_path, 'w') as f:
                f.write('\n'.join(inputs))

            batch_content.extend([
                f'echo Installing {mod_name}: {description}',
                f'echo Running {setup_file} with input from {input_filename}...',
                '',
                f'{setup_file} < {input_filename}',
                '',
                f'echo Finished installing {mod_name}',
                'echo.',
                ''
            ])

        batch_content.extend([
            'echo All installations complete!',
            'pause'
        ])

        with open(batch_path, 'w') as f:
            f.write('\n'.join(batch_content))

        print(f"\nBatch file created: {batch_path}")
        print("This batch file uses input redirection from text files for installers.")

def main():
    extractor = SimpleModExtractor()

    print("Simple BG Enhanced Edition Mod Extractor")
    print("=" * 45)

    if extractor.extract_mods():
        print("\n" + "=" * 45)
        extractor.list_setup_files()
        extractor.create_simple_batch()
    else:
        print("No mods were extracted.")

if __name__ == "__main__":
    main()
