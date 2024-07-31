# src/ui/main_window.py
import os
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QMenu
from qt_material import apply_stylesheet
from core.theme_manager import ThemeManager
from core.settings import Settings
from widgets.settings_widget import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Constructor for the MainWindow class
        """
        super().__init__()
        self.settings = Settings()
        self.theme_manager = ThemeManager(self.settings)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface.
        """
        self.setWindowTitle("PyQt6 Template")
        
        # Set initial window size
        size = self.settings.get("window_size", {"width": 800, "height": 600})
        self.resize(size["width"], size["height"])

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create menu bar
        menu_bar = QMenuBar()
        file_menu = QMenu("File", self)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.apply_theme(self.theme_manager.get_current_theme())

    def apply_theme(self, theme_name):
        """
        Apply the selected theme to the application.

        Args:
            theme_name (_type_): The name of the theme to apply.
        """
        available_themes = self.theme_manager.get_available_themes()
        if theme_name not in available_themes:
            theme_name = available_themes[0]
        
        theme_file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'themes', f"{theme_name}.xml")
        
        if os.path.exists(theme_file):
            try:
                apply_stylesheet(QApplication.instance(), theme=theme_file)
            except Exception as e:
                print(f"Error applying theme: {e}")
                # Fallback to a default theme if there's an error
                apply_stylesheet(QApplication.instance(), theme='light_blue.xml')
        else:
            print(f"Theme file not found: {theme_file}")
            # Fallback to a default theme if the file doesn't exist
            apply_stylesheet(QApplication.instance(), theme='light_blue.xml')

    def open_settings(self):
        """
        Open the settings dialog.
        """
        settings_dialog = SettingsWidget(self.settings, self.theme_manager, self)
        settings_dialog.settingsChanged.connect(self.apply_settings)
        settings_dialog.exec()

    def apply_settings(self):
        """
        Apply the settings changes to the main window.
        """
        # Apply theme
        self.apply_theme(self.theme_manager.get_current_theme())

        # Apply window size
        size = self.settings.get("window_size", {"width": 800, "height": 600})
        self.resize(size["width"], size["height"])

        # Apply language (you'll need to implement language switching logic)
        language = self.settings.get("language", "en")
        print(f"Language changed to: {language}")  # Placeholder for language change logic