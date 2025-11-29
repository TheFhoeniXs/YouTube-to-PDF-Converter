import json
import os

class SettingsManager:
    """
    #! Simple settings manager - API key, download path and auto save
    #? Manages application configuration and persists settings to JSON file
    """
    
    def __init__(self, settings_file: str = "app_settings.json"):
        self.settings_file = settings_file
        #! Default configuration values
        self.default_settings = {
            "api_key": "",
            "download_path": None,
            "auto_save": False
        }
        #? Load existing settings or create default
        self.settings = self.load_settings()
    
    def load_settings(self) -> dict:
        """
        #! Load settings from file
        #? Reads JSON settings file and merges with defaults for missing keys
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    #? Add missing keys from defaults
                    for key in self.default_settings:
                        if key not in loaded:
                            loaded[key] = self.default_settings[key]
                    return loaded
            else:
                #? First time use - save default settings
                self.save_settings()
                return self.default_settings.copy()
        except:
            #! Return defaults on error
            return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """
        #! Save settings to file
        #? Writes current settings to JSON file with UTF-8 encoding
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except:
            #! Return False on save failure
            return False
    
    # API Key
    def get_api_key(self) -> str:
        #? Retrieve stored API key
        return self.settings["api_key"]
    
    def set_api_key(self, api_key: str):
        #! Update API key and save
        self.settings["api_key"] = api_key
        self.save_settings()
    
    # Download Path
    def get_download_path(self):
        #? Retrieve download directory path
        return self.settings["download_path"]
    
    def set_download_path(self, path: str):
        #! Update download path and save
        self.settings["download_path"] = path
        self.save_settings()
    
    # Auto Save
    def get_auto_save(self) -> bool:
        #? Check if auto-save is enabled
        return self.settings["auto_save"]
    
    def set_auto_save(self, enabled: bool):
        #! Toggle auto-save feature and save
        self.settings["auto_save"] = enabled
        self.save_settings()