import json
import os

def create_default_settings(file='settings/default.json'):
    """
    Create the default settings file if it doesn't exist.

    Args:
        file (str, optional): The path to the settings file. Defaults to 'settings/default.json'.
    """
    default_settings = {
        "theme": "dark",
        "window_size": {
            "width": 800,
            "height": 600
        },
        "language": "en"
    }
    
    os.makedirs(os.path.dirname(file), exist_ok=True)
    
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(default_settings, f, indent=4)
        print(f"Default settings file created at {file}")
    else:
        pass

class Settings:
    def __init__(self, file='settings/default.json'):
        """
        Constructor for the Settings class.

        Args:
            file (str, optional): The path to the settings file. Defaults to 'settings/default.json'.
        """
        self.file = file
        self._settings = self._load_settings()
    
    def _load_settings(self):
        """
        Load the settings from the settings file.

        Raises:
            FileNotFoundError: If the settings file is not found.

        Returns:
            _type_: The settings dictionary.
        """
        if not os.path.exists(self.file):
            return {}
        try:
            with open(self.file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Settings file {self.file} not found")
    
    def _save_settings(self):
        """
        Save the settings to the settings file.
        """
        with open(self.file, 'w') as f:
            json.dump(self._settings, f, indent=4)
    
    def get(self, key, default=None):
        """
        Get a setting value.

        Args:
            key (_type_): The key of the setting.
            default (_type_, optional): Default value if key is not found. Defaults to None.

        Returns:
            _type_: The setting value.
        """
        return self._settings.get(key, default)
    
    def set(self, key, value):
        """
        Set a setting value.

        Args:
            key (_type_): The key of the setting.
            value (_type_): The value to set.
        """
        self._settings[key] = value
        self._save_settings()
    
    def remove(self, key):
        """
        Remove a setting.

        Args:
            key (_type_): The key of the setting to remove.
        """
        if key in self._settings:
            del self._settings[key]
            self._save_settings()
    
    def clear(self):
        """
        Clear all settings.
        """
        self._settings = {}
        self._save_settings()