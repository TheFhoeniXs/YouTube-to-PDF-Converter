import json
import os

class SettingsManager:
    """Basit ayar yönetimi - API key, download path ve auto save"""
    
    def __init__(self, settings_file: str = "app_settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "api_key": "",
            "download_path": None,
            "auto_save": False
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> dict:
        """Ayarları yükle"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Eksik anahtarları ekle
                    for key in self.default_settings:
                        if key not in loaded:
                            loaded[key] = self.default_settings[key]
                    return loaded
            else:
                # İlk kullanımda varsayılan ayarları kaydet
                self.save_settings()
                return self.default_settings.copy()
        except:
            return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Ayarları kaydet"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    # API Key
    def get_api_key(self) -> str:
        return self.settings["api_key"]
    
    def set_api_key(self, api_key: str):
        self.settings["api_key"] = api_key
        self.save_settings()
    
    # Download Path
    def get_download_path(self):
        return self.settings["download_path"]
    
    def set_download_path(self, path: str):
        self.settings["download_path"] = path
        self.save_settings()
    
    # Auto Save
    def get_auto_save(self) -> bool:
        return self.settings["auto_save"]
    
    def set_auto_save(self, enabled: bool):
        self.settings["auto_save"] = enabled
        self.save_settings()