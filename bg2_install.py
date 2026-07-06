from ModInstaller import SimpleModExtractor

extractor = SimpleModExtractor('mod_config_bg2.json')
extractor.extract_mods()
extractor.list_setup_files()
extractor.create_simple_batch()
