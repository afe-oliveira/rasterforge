from typing import Type

import numpy as np
from matplotlib.colors import Normalize

from RasterForge.containers.layer import Layer
from RasterForge.gui.common.adaptative_elements import _adaptative_input
from RasterForge.gui.data import _data
from RasterForge.gui.processes.process_panel import _ProcessPanel
from RasterForge.processes.composite import PRESET_COMPOSITES, composite
from RasterForge.processes.topography import aspect, slope

ARRAY_TYPE: Type[np.ndarray] = np.ndarray


class _TopographyPanel(_ProcessPanel):
    def __init__(self, name=None, selector=False, parent=None):
        super().__init__(name=name, selector=selector, parent=parent)

        for process in ["Slope", "Aspect"]:
            self.selector_combo.addItem(process)

        self._scroll_content_callback()

    def _scroll_content_callback(self):
        self._widgets = {}
        self._references = {}

        # Add DEM
        self._widgets["DEM"], self._references["DEM"] = _adaptative_input(
            "DEM", ARRAY_TYPE
        )

        # Add Units
        self._widgets["Units"], self._references["Units"] = _adaptative_input(
            "Units", list, ["Degrees", "Radians"]
        )

        # Add Alpha
        self._widgets["Alpha"], self._references["Alpha"] = _adaptative_input(
            "Alpha", ARRAY_TYPE, "None"
        )

        super()._scroll_content_callback()

    def _build_callback(self):
        input_dem = _data.raster.layers[self._references["DEM"].currentText()].array
        input_units = self._references["Units"].currentText().lower()
        input_alpha = (
            _data.raster.layers[self._references["Alpha"].currentText()].array
            if self._references["Alpha"].currentText() != "None"
            else None
        )

        layer = Layer()
        if self.selector_combo.currentText() == "Slope":
            layer.array = slope(dem=input_dem, units=input_units, alpha=input_alpha)
        elif self.selector_combo.currentText() == "Aspect":
            layer.array = aspect(dem=input_dem, units=input_units, alpha=input_alpha)
        _data.viewer = layer
        _data.viewer_changed.emit()

        super()._build_callback()
