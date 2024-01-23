import inspect
from typing import Type

import numpy as np
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from RasterForge.containers.layer import Layer
from RasterForge.gui.data import data
from RasterForge.gui.processes.adaptative_elements import adaptative_input
from RasterForge.processes.composite import PRESET_COMPOSITES, composite
from RasterForge.processes.distance import distance
from RasterForge.processes.topographic import aspect, slope


class DistancePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget(self)
        self.scroll_area.setWidget(self.scroll_content)

        # Create a Vertical Layout for the Scroll Content (Aligned Top)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        # Add theScroll Area to the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)

        # Create a Grid Layout for the General UI
        buttons_layout = QGridLayout()

        # Add Back Button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back_clicked)
        buttons_layout.addWidget(back_button, 0, 0, 1, 1)

        # Add Progress Bar
        progress_bar = QProgressBar(self)
        buttons_layout.addWidget(progress_bar, 0, 1, 1, 23)

        # Add Build Button
        build_button = QPushButton("Build", self)
        build_button.clicked.connect(self.build_clicked)
        buttons_layout.addWidget(build_button, 0, 24, 1, 1)

        # Add the Buttons Layout to the Main Layout
        layout.addLayout(buttons_layout)

        # Set Layout
        self.setLayout(layout)

        # When Raster Data Changes, Update Inner Scroll Content
        data.raster_changed.connect(self.update_scroll_content)

        # Start Scroll at First Position
        self.update_scroll_content()

    def update_scroll_content(self):
        # Clear Existing Widgets
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        array_type: Type[np.ndarray] = np.ndarray
        self.inputs = {}

        # Add Layer Selection
        label = QLabel(f"Layer", self)
        widget = adaptative_input("Layer", array_type)
        self.scroll_layout.addWidget(label)
        self.scroll_layout.addWidget(widget)
        self.inputs["Layer"] = widget

        # Add Separator
        separator_line = QFrame(self)
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        self.scroll_layout.addWidget(separator_line)

        # Add Alpha Selection
        label = QLabel(f"Alpha", self)
        widget = adaptative_input("Alpha", array_type)
        self.scroll_layout.addWidget(label)
        self.scroll_layout.addWidget(widget)
        self.inputs["Alpha"] = widget

    def back_clicked(self):
        data.process_main.emit()

    def build_clicked(self):
        layer = Layer()
        layer.array = distance(layer=data.raster.layers[self.inputs["Layer"].currentText()].array,
                               alpha=data.raster.layers[self.inputs["Alpha"].currentText()].array)
        data.viewer = layer
        data.viewer_changed.emit()
