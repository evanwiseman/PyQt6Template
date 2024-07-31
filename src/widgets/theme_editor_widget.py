# src/widgets/theme_editor_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QColorDialog, QInputDialog, QMessageBox, QComboBox, QLabel)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal, Qt
from core.theme_manager import ThemeManager

class ColorButton(QPushButton):
    def __init__(self, color_name:str, color_value):
        """
        Constructor for the ColorButton class.

        Args:
            color_name (str): The name of the color.
            color_value (_type_): The value of the color.
        """
        super().__init__(f"{color_name}: {color_value}")
        self.color_name:str = color_name
        self.setColor(color_value)

    def setColor(self, color):
        """
        Set the color of the button.

        Args:
            color (_type_): The color value to set.
        """
        self.color = color
        self.setText(f"{self.color_name}: {color}")
        self.setStyleSheet(f"background-color: {color}; color: {'black' if QColor(color).lightness() > 128 else 'white'};")

class ThemeEditorWidget(QWidget):
    themeChanged = pyqtSignal(str)

    def __init__(self, theme_manager:ThemeManager, parent=None):
        """
        Constructor for the ThemeEditorWidget class.

        Args:
            theme_manager (ThemeManager): The theme manager instance.
            parent (_type_, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.theme_manager:ThemeManager = theme_manager
        self.color_buttons:dict = {}
        self.init_ui()

    def init_ui(self):

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_available_themes())
        self.theme_combo.setCurrentText(self.theme_manager.get_current_theme())
        self.theme_combo.currentTextChanged.connect(self.load_theme)

        # New theme button
        add_theme_button = QPushButton("+")
        add_theme_button.setMaximumSize(16, 16)
        add_theme_button.clicked.connect(self.create_new_theme)

        # Delete theme button
        delete_theme_button = QPushButton("-")
        delete_theme_button.setMaximumSize(16, 16)
        delete_theme_button.clicked.connect(self.delete_theme)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addWidget(add_theme_button)
        button_layout.addWidget(delete_theme_button)
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addLayout(button_layout)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addLayout(theme_layout)

        # Color buttons
        colors_layout = QVBoxLayout()
        for color_name, color_value in self.theme_manager.get_theme_colors().items():
            color_button = ColorButton(color_name, color_value)
            color_button.clicked.connect(lambda checked, name=color_name: self.change_color(name))
            self.color_buttons[color_name] = color_button
            colors_layout.addWidget(color_button)

        layout.addLayout(colors_layout)

        # Save button
        save_btn = QPushButton("Save Theme")
        save_btn.clicked.connect(self.save_theme)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        self.load_theme(self.theme_manager.get_current_theme())

    def load_theme(self, theme_name):
        """
        Load the selected theme.

        Args:
            theme_name (_type_): The name of the theme to load.
        """
        colors = self.theme_manager.get_theme_colors(theme_name)
        for color_name, color_value in colors.items():
            if color_name in self.color_buttons:
                self.color_buttons[color_name].setColor(color_value)

    def change_color(self, color_name):
        """
        Change the color of a specific theme element.

        Args:
            color_name (_type_): The name of the color to change.
        """
        current_color = QColor(self.color_buttons[color_name].color)
        color = QColorDialog.getColor(current_color, self, f"Choose {color_name} color")
        if color.isValid():
            self.color_buttons[color_name].setColor(color.name())

    def save_theme(self):
        """
        Save the current theme to the theme file.
        """
        theme_name = self.theme_combo.currentText()
        colors = {btn.color_name: btn.color for btn in self.color_buttons.values()}
        self.theme_manager.save_theme(theme_name, colors)
        self.theme_manager.set_theme(theme_name)
        self.themeChanged.emit(theme_name)
        QMessageBox.information(self, "Theme Saved", f"Theme '{theme_name}' has been saved.")

    def create_new_theme(self):
        """
        Create a new theme.
        """
        name, ok = QInputDialog.getText(self, "New Theme", "Enter a name for the new theme:")
        if ok and name:
            if name in self.theme_manager.get_available_themes():
                QMessageBox.warning(self, "Theme Exists", f"A theme named '{name}' already exists.")
                return
            self.theme_manager.save_theme(name, self.theme_manager.get_theme_colors())
            self.theme_combo.addItem(name)
            self.theme_combo.setCurrentText(name)

    def delete_theme(self):
        """
        Delete the selected theme.
        """
        theme_name = self.theme_combo.currentText()
        if theme_name in ['light', 'dark']:
            QMessageBox.warning(self, "Cannot Delete", "Cannot delete default themes.")
            return
        
        reply = QMessageBox.question(self, "Delete Theme", f"Are you sure you want to delete the theme '{theme_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.theme_manager.delete_theme(theme_name):
                self.theme_combo.removeItem(self.theme_combo.currentIndex())
                QMessageBox.information(self, "Theme Deleted", f"Theme '{theme_name}' has been deleted.")
            else:
                QMessageBox.warning(self, "Delete Failed", f"Failed to delete theme '{theme_name}'.")