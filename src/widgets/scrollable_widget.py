from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QBoxLayout, QLayout, QVBoxLayout, QScrollArea, QFrame, QSizePolicy

class ScrollableWidget(QWidget):
    def __init__(self, parent:QWidget=None):
        """
        A widget that can be scrolled.
        
        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):

        self.scrollLayout = QVBoxLayout()
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
    
    def addWidget(self, widget:QWidget, scrollBottom:bool=True):
        """
        Add a widget to the scroll area.

        Args:
            widget (QWidget): The widget to add.
            scrollBottom (bool, optional): Whether to scroll to the bottom after adding the widget. Defaults to True.
        """
        minimum = self.scrollArea.verticalScrollBar().minimum()
        maximum = self.scrollArea.verticalScrollBar().maximum()
        
        widget.setParent(self.scrollWidget)
        self.scrollLayout.addWidget(widget)
        self.scrollArea.verticalScrollBar().setValue(maximum if scrollBottom else minimum)
    
    def removeWidget(self, widget:QWidget):
        """
        Remove a widget from the scroll area.

        Args:
            widget (QWidget): The widget to remove.
        """
        if widget in self.scrollLayout.findChild(QWidget):
            self.scrollLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
    
    def removeLayout(self, layout:QLayout):
        """
        Remove a layout from the scroll area.

        Args:
            layout (QLayout): The layout to remove.
        """
        if layout in self.scrollLayout.findChild(QLayout):
            self.scrollLayout.removeItem(layout)
            layout.setParent(None)
            layout.deleteLater()
    
    def iterateWidgets(self):
        """
        Iterate over all widgets in the scroll area.

        Returns:
            QWidget: The next widget.
        """
        for i in range(self.scrollLayout.count()):
            yield self.scrollLayout.itemAt(i).widget()