# src/widgets/settings_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QSpinBox, QPushButton, QDialog)
from PyQt6.QtCore import pyqtSignal, Qt
from core.theme_manager import ThemeManager
from core.settings import Settings
from widgets.theme_editor_widget import ThemeEditorWidget

class SettingsWidget(QDialog):
    settingsChanged = pyqtSignal()

    def __init__(self, settings: Settings, theme_manager: ThemeManager, parent=None):
        """
        Constructor for the SettingsWidget class.

        Args:
            settings (Settings): The settings instance.
            theme_manager (ThemeManager): The theme manager instance.
            parent (_type_, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager
        self.setWindowTitle("Settings")
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface.
        """

        # Theme selection
        theme_label = QLabel("Theme:")
        theme_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.theme_editor = ThemeEditorWidget(self.theme_manager, self)
        theme_layout = QHBoxLayout()
        theme_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(4)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_editor)

        # Window size
        self.width_spin = QSpinBox()
        self.width_spin.setRange(400, 3840)
        self.width_spin.setValue(self.settings.get("window_size", {}).get("width", 800))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 2160)
        self.height_spin.setValue(self.settings.get("window_size", {}).get("height", 600))
        size_layout = QHBoxLayout()
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(4)
        size_layout.addWidget(QLabel("Window Size:"))
        size_layout.addWidget(self.width_spin)
        size_layout.addWidget(self.height_spin)

        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "es", "fr", "de"])  # Add more languages as needed
        self.lang_combo.setCurrentText(self.settings.get("language", "en"))
        lang_layout = QHBoxLayout()
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(4)
        lang_layout.addWidget(QLabel("Language:"))
        lang_layout.addWidget(self.lang_combo)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        layout.addLayout(theme_layout)
        layout.addLayout(size_layout)
        layout.addLayout(lang_layout)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def save_settings(self):
        """
        Save the settings to the settings file.
        """
        # Save theme
        self.theme_editor.save_theme()
        self.settings.set("theme", self.theme_manager.get_current_theme())

        # Save window size
        self.settings.set("window_size", {
            "width": self.width_spin.value(),
            "height": self.height_spin.value()
        })

        # Save language
        self.settings.set("language", self.lang_combo.currentText())

        self.settingsChanged.emit()