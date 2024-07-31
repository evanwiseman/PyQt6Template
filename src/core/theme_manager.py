# src/core/theme_manager.py
import os
import xml.etree.ElementTree as ET

class ThemeManager:
    def __init__(self, settings):
        """
        Constructor for the ThemeManager class.

        Args:
            settings (_type_): The settings instance.
        """
        
        self.settings = settings
        self.themes_dir = os.path.join(os.path.dirname(__file__), '..', 'resources', 'themes')
        self.current_theme = self.settings.get("theme", "light")
        self.ensure_default_themes()

    def ensure_default_themes(self):
        """
        Ensure that the default themes are available.
        """
        
        if not os.path.exists(self.themes_dir):
            os.makedirs(self.themes_dir)
        
        default_themes = {
            "light": {
                "primaryColor": "#2979ff",
                "primaryLightColor": "#75a7ff",
                "secondaryColor": "#f5f5f5",
                "secondaryLightColor": "#ffffff",
                "secondaryDarkColor": "#e6e6e6",
                "primaryTextColor": "#000000",
                "secondaryTextColor": "#000000"
            },
            "dark": {
                "primaryColor": "#1a237e",
                "primaryLightColor": "#534bae",
                "secondaryColor": "#212121",
                "secondaryLightColor": "#484848",
                "secondaryDarkColor": "#000000",
                "primaryTextColor": "#ffffff",
                "secondaryTextColor": "#ffffff"
            }
        }

        for theme_name, colors in default_themes.items():
            theme_file = os.path.join(self.themes_dir, f"{theme_name}.xml")
            if not os.path.exists(theme_file):
                self.save_theme(theme_name, colors)

    def get_current_theme(self):
        """
        Get the current theme.

        Returns:
            _type_: The current theme name.
        """
        
        return self.current_theme

    def set_theme(self, theme_name):
        """
        Set the current theme.

        Args:
            theme_name (_type_): The name of the theme to set.

        Returns:
            _type_: True if the theme was set, False otherwise.
        """
        
        if theme_name in self.get_available_themes():
            self.current_theme = theme_name
            self.settings.set("theme", theme_name)
            return True
        return False

    def get_theme_colors(self, theme_name=None):
        """
        Get the colors of the selected

        Args:
            theme_name (_type_, optional): The name of the theme. Defaults to None.

        Returns:
            _type_: The colors of the selected theme.
        """
        
        if theme_name is None:
            theme_name = self.current_theme
        
        theme_file = os.path.join(self.themes_dir, f"{theme_name}.xml")
        if os.path.exists(theme_file):
            tree = ET.parse(theme_file)
            root = tree.getroot()
            return {color.attrib['name']: color.text for color in root.findall('color')}
        return {}

    def save_theme(self, name, colors):
        """
        Save the theme to a file.

        Args:
            name (_type_): The name of the theme.
            colors (_type_): The colors of the theme.
        """

        theme_file = os.path.join(self.themes_dir, f"{name}.xml")
        root = ET.Element("resources")
        for color_name, color_value in colors.items():
            color_elem = ET.SubElement(root, "color", name=color_name)
            color_elem.text = color_value
        
        tree = ET.ElementTree(root)
        tree.write(theme_file, encoding="UTF-8", xml_declaration=True)

    def get_available_themes(self):
        """
        Get a list of available themes

        Returns:
            _type_: A list of available theme names.
        """
        
        return [os.path.splitext(f)[0] for f in os.listdir(self.themes_dir) if f.endswith('.xml')]

    def delete_theme(self, theme_name):
        """
        Delete a theme.

        Args:
            theme_name (_type_): The name of the theme to delete.

        Returns:
            _type_: True if the theme was deleted, False otherwise.
        """
        
        if theme_name in ['light', 'dark']:
            return False  # Prevent deletion of default themes
        
        theme_file = os.path.join(self.themes_dir, f"{theme_name}.xml")
        if os.path.exists(theme_file):
            os.remove(theme_file)
            return True
        return False