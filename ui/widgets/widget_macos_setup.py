from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QPlainTextEdit,
)

import core.app_utils as utils
import core.string_utils as su
import core.terminal_commands as tc
from ui.widgets.custom.custom_generic_widgets import WebLinksWidget, ChoseAppsWidget
from ui.widgets.custom.custom_macos_setup_widgets import MacOsSetupTopWidget

WEB_LINKS_LABEL = "Below you can find useful links related to brew:"
BREW_WEB_SITE: str = "https://brew.sh/"

BREW_INSTALL_LABEL: str = "To install all apps from this tab - Brew should be installed"
BREW_INSTALL_COMMAND: str = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'

BREW_VERSION_LABEL: str = (
    "To be able install custom version of casks via Brew they needs to be activated"
)
BREW_VERSIONS_COMMAND: str = "brew tap homebrew/cask-versions"

BREW_INSTALL_FORMULAE: str = "brew install {}"
BREW_INSTALL_CASK: str = "brew install --cask {}"

SUGGESTED_FORMULAS: list[str] = utils.load_text("brew_apps_formulas.txt")
SUGGESTED_CASKS: list[str] = utils.load_text("brew_apps_casks.txt")

LABEL_YOUR_FORMULAE = "Add your Formulae"
LABEL_ADD_YOUR_CASK = "Add your Cask"

BTN_TEXT_SCRIPT_FOR_ALL_COMMANDS = "Generate common script for all commands"
BTN_TEXT_COPY_SCRIPT = "Copy final script"


class WidgetMacOsSetup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout_main = QVBoxLayout()

        widget_web_links = WebLinksWidget(WEB_LINKS_LABEL, [BREW_WEB_SITE])
        widget_top_install_brew = MacOsSetupTopWidget(
            BREW_INSTALL_LABEL, BREW_INSTALL_COMMAND
        )
        widget_top_activate_versions = MacOsSetupTopWidget(
            BREW_VERSION_LABEL, BREW_VERSIONS_COMMAND
        )
        widget_chose_formulas = ChoseAppsWidget(
            LABEL_YOUR_FORMULAE, SUGGESTED_FORMULAS, BREW_INSTALL_FORMULAE
        )
        widget_chose_casks = ChoseAppsWidget(
            LABEL_ADD_YOUR_CASK, SUGGESTED_CASKS, BREW_INSTALL_CASK
        )
        widget_btn_generate_final_script = QPushButton(BTN_TEXT_SCRIPT_FOR_ALL_COMMANDS)
        widget_final_script_text_edit = QPlainTextEdit()
        widget_final_script_text_edit.setReadOnly(True)
        widget_btn_copy_final_script = QPushButton(BTN_TEXT_COPY_SCRIPT)

        layout_main.addWidget(widget_web_links)
        layout_main.addWidget(widget_top_install_brew)
        layout_main.addWidget(widget_top_activate_versions)
        layout_main.addWidget(widget_chose_formulas)
        layout_main.addWidget(widget_chose_casks)
        layout_main.addWidget(widget_btn_generate_final_script)
        layout_main.addWidget(widget_final_script_text_edit)
        layout_main.addWidget(widget_btn_copy_final_script)

        self.setLayout(layout_main)

        # Handlers
        widget_btn_generate_final_script.clicked.connect(
            lambda: self._on_generate_common_script_clicked(
                widget_final_script_text_edit,
                widget_chose_formulas.chosen_apps_commands,
                widget_chose_casks.chosen_apps_commands,
            )
        )
        widget_btn_copy_final_script.clicked.connect(
            lambda: self._on_copy_final_script_btn_clicked(
                widget_final_script_text_edit
            )
        )

    @staticmethod
    def _on_generate_common_script_clicked(
        common_command_text_edit: QPlainTextEdit, formulas: list[str], casks: list[str]
    ):
        commands = []
        commands.extend(formulas)
        commands.extend(casks)
        result = tc.join_commands_in_one(
            su.sort_lines(list(commands), case_insensitive=False, order=su.DESC)
        )
        common_command_text_edit.setPlainText(result)

    @staticmethod
    def _on_copy_final_script_btn_clicked(text_field: QPlainTextEdit) -> None:
        text_field.selectAll()
        text_field.copy()
