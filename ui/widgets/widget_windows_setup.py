from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

import core.app_utils as utils
from ui.widgets.custom.custom_generic_widgets import WebLinksWidget, ChoseAppsWidget

ADD_CUSTOM_APP_BTN_LABEL = "Add your WinGet Package"

WEB_LINKS_LABEL = "Below you can find useful links related to brew:"
WIN_GET_URL: str = "https://github.com/microsoft/winget-cli"

PACKAGE_RESOURCES_LABEL: str = "By the links below you can find WinGet packages"
WIN_GET_WEB_RESOURCES: list[str] = ["https://winstall.app/", "https://winget.run/"]

WIN_GET_INSTALL_TEMPLATE: str = "winget install --id={} -e"
SUGGESTED_APPS: list[str] = utils.load_text("win_get_apps.txt")


class WidgetWindowsSetup(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        widget_link_to_win_get = WebLinksWidget(WEB_LINKS_LABEL, [WIN_GET_URL])
        widget_link_to_win_get_packages = WebLinksWidget(
            PACKAGE_RESOURCES_LABEL, WIN_GET_WEB_RESOURCES
        )
        apps_view = ChoseAppsWidget(
            ADD_CUSTOM_APP_BTN_LABEL, SUGGESTED_APPS, WIN_GET_INSTALL_TEMPLATE
        )

        main_layout.addWidget(widget_link_to_win_get)
        main_layout.addWidget(widget_link_to_win_get_packages)
        main_layout.addWidget(apps_view)

        self.setLayout(main_layout)
