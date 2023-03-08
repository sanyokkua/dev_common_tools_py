import logging

from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea

import ui.widgets.widget_git_utils as gu
import ui.widgets.widget_json_utils as ju
import ui.widgets.widget_macos_setup as ms
import ui.widgets.widget_string_utils as wsu
import ui.widgets.widget_terminal_utils as wtu
import ui.widgets.widget_windows_setup as wws

log: logging.Logger = logging.getLogger(__name__)


class QApplicationDevTool(QMainWindow):
    """
    A class that represents a developer tool application.

    :param QMainWindow: Inherits from QMainWindow class
    :type QMainWindow: class
    """

    def __init__(self) -> None:
        """
        Initializes the QApplicationDevTool object.

        :return: None
        """
        super().__init__()
        self.setWindowTitle("Developer tools")

        self._tab_widget = QTabWidget()
        self._tab_string_utils = wsu.WidgetStringUtils()
        self._tab_json_utils = ju.WidgetJsonUtils()
        self._tab_terminal_utils = wtu.WidgetTerminalUtils()
        self._tab_git_utils = gu.WidgetGitUtils()
        self._tab_windows_setup = wws.WidgetWindowsSetup()
        self._tab_macos_setup = ms.WidgetMacOsSetup()

        self._tab_mac_scrollable = QScrollArea()
        self._tab_mac_scrollable.setWidget(self._tab_macos_setup)

        self._tab_windows_scrollable = QScrollArea()
        self._tab_windows_scrollable.setWidget(self._tab_windows_setup)

        self._tab_widget.addTab(self._tab_string_utils, "String Utils")
        self._tab_widget.addTab(self._tab_json_utils, "Json Utils")
        self._tab_widget.addTab(self._tab_terminal_utils, "Terminal Utils")
        self._tab_widget.addTab(self._tab_git_utils, "Git Base Setup")
        self._tab_widget.addTab(self._tab_windows_scrollable, "Windows Setup (WinGet)")
        self._tab_widget.addTab(self._tab_mac_scrollable, "MacOS Setup (Brew)")

        self._window_layout = QVBoxLayout()
        self._window_layout.setContentsMargins(0, 0, 0, 0)
        self._window_layout.setSpacing(0)
        self._window_layout.addWidget(self._tab_widget)

        self._main_window_widget = QWidget()
        self._main_window_widget.setLayout(self._window_layout)

        self.setCentralWidget(self._main_window_widget)
