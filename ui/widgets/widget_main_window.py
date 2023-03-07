import logging

from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

import ui.widgets.widget_json_utils as ju
import ui.widgets.widget_string_utils as wsu

log: logging.Logger = logging.getLogger(__name__)


class QApplicationDevTool(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Developer tools")

        self._tab_widget = QTabWidget()
        self._tab_string_utils = wsu.WidgetStringUtils()
        self._tab_json_utils = ju.WidgetJsonUtils()
        self._tab_terminal_utils = QWidget()
        self._tab_git_utils = QWidget()
        self._tab_windows_setup = QWidget()
        self._tab_macos_setup = QWidget()

        self._tab_widget.addTab(self._tab_string_utils, "String Utils")
        self._tab_widget.addTab(self._tab_json_utils, "Json Utils")
        self._tab_widget.addTab(self._tab_terminal_utils, "Terminal Utils")
        self._tab_widget.addTab(self._tab_git_utils, "Git Setup")
        self._tab_widget.addTab(self._tab_windows_setup, "Windows Setup")
        self._tab_widget.addTab(self._tab_macos_setup, "MacOS Setup")

        self._window_layout = QVBoxLayout()
        self._window_layout.setContentsMargins(0, 0, 0, 0)
        self._window_layout.setSpacing(0)
        self._window_layout.addWidget(self._tab_widget)

        self._main_window_widget = QWidget()
        self._main_window_widget.setLayout(self._window_layout)

        self.setCentralWidget(self._main_window_widget)
