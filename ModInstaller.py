import json
import os
import zipfile


class SimpleModExtractor:
    def __init__(self, config_file='mod_config.json'):
        # Load config only, no default fallback
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.source_folder = self.config['source_folder']
        self.destination_folder = self.config['destination_folder']
        self.mod_components = self.config['mod_components']
        self.install_order = self.config.get('install_order', [])

    def extract_mods(self):
        print("Starting mod extraction...")
        os.makedirs(self.destination_folder, exist_ok=True)
        extracted_count = 0

        for root, dirs, files in os.walk(self.source_folder):
            for filename in files:
                if filename.lower().endswith('.zip'):
                    zip_path = os.path.join(root, filename)
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            namelist = zip_ref.namelist()
                            has_setup = any(
                                name.lower().startswith('setup-') and name.lower().endswith(
                                    '.exe') and '/' not in name.rstrip('/')
                                for name in namelist
                            )

                            if has_setup:
                                # Standard case: setup exe is at zip root → extract all as-is
                                zip_ref.extractall(self.destination_folder)
                                print(f"✓ Extracted {filename} (direct contents)")
                            else:
                                # Look for a single folder at the root
                                top_level = set(name.split('/')[0] for name in namelist if '/' in name)
                                if len(top_level) == 1:
                                    top_folder = top_level.pop()
                                    members = [name for name in namelist if name.startswith(top_folder + '/')]
                                    for member in members:
                                        # remove top_folder prefix
                                        target_path = os.path.join(self.destination_folder,
                                                                   member[len(top_folder) + 1:])
                                        if member.endswith('/'):
                                            os.makedirs(target_path, exist_ok=True)
                                        else:
                                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                            with open(target_path, 'wb') as f:
                                                f.write(zip_ref.read(member))
                                    print(f"✓ Extracted {filename} (from folder '{top_folder}/')")
                                else:
                                    # Fallback: just extract all
                                    zip_ref.extractall(self.destination_folder)
                                    print(f"! Extracted {filename} (fallback — structure unknown)")

                        extracted_count += 1
                    except Exception as e:
                        print(f'✗ Error extracting {filename}: {str(e)}')

        print(f"Extraction complete. {extracted_count} mods extracted.")
        return extracted_count > 0

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

            # Create input file for this mod
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
