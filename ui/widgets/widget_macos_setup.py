from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QPlainTextEdit,
    QListWidgetItem,
)

import core.string_utils as su
import core.terminal_commands as tc

BREW_INSTALL = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
BREW_VERSIONS = "brew tap homebrew/cask-versions"
BREW_INSTALL_FORMULAE = "brew install {}"
BREW_INSTALL_CASK = "brew install --cask {}"
SUGGESTED_FORMULAS: list[str] = ["git", "node@18", "go", "poetry", "python@3.11"]
SUGGESTED_CASKS: list[str] = [
    "android-file-transfer",
    "google-chrome",
    "postman",
    "temurin17",
    "bitwarden",
    "intellij-idea",
    "skype",
    "tiles",
    "dbeaver-community",
    "keka",
    "spotify",
    "transmission",
    "docker",
    "microsoft-edge",
    "spybuster",
    "visual-studio-code",
    "drawio",
    "opera",
    "steam",
    "firefox",
    "origin",
    "tad",
]


class WidgetMacOsSetup(QWidget):
    """
    A custom QWidget that provides a user interface for setting up a macOS
    environment using Homebrew. The widget allows the user to add formulae and
    casks to install and generates a script to run all commands.
    """

    def __init__(self):
        """
        Initializes the WidgetMacOsSetup object by creating a layout with widgets
        for installing Homebrew, activating custom versions of formulae, adding
        formulae and casks to install and generating a script to run all commands.

        :param self: The instance of this class that is calling this method
        :return: None
        """
        super().__init__()
        self._all_commands: dict[str, list[str]] = {}
        self._main_layout_vertical_box = QVBoxLayout()

        # Top label and text box
        brew_install_widget = self._create_widget_with_label_and_command_to_copy(
            label_text="To install all apps from this tab - Brew should be installed",
            command_text=BREW_INSTALL,
        )
        brew_versions_widget = self._create_widget_with_label_and_command_to_copy(
            label_text="To be able install custom version via Brew they need to be activated",
            command_text=BREW_VERSIONS,
        )
        self._main_layout_vertical_box.addWidget(brew_install_widget)
        self._main_layout_vertical_box.addWidget(brew_versions_widget)

        # Formulae
        formulae_widget = self._create_commands_add_widget(
            "Add your Formulae", SUGGESTED_FORMULAS, BREW_INSTALL_FORMULAE
        )
        self._main_layout_vertical_box.addWidget(formulae_widget)

        # Cask
        cask_widget = self._create_commands_add_widget(
            "Add your Cask", SUGGESTED_CASKS, BREW_INSTALL_CASK
        )
        self._main_layout_vertical_box.addWidget(cask_widget)

        generate_common_script_btn = QPushButton(
            "Generate common script for all commands"
        )
        self._main_layout_vertical_box.addWidget(generate_common_script_btn)

        common_command_text_edit = QPlainTextEdit()
        common_command_text_edit.setReadOnly(True)
        self._main_layout_vertical_box.addWidget(common_command_text_edit)

        generate_common_script_btn.clicked.connect(
            lambda: self._on_generate_common_script_clicked(common_command_text_edit)
        )

        self.setLayout(self._main_layout_vertical_box)

    def _create_widget_with_label_and_command_to_copy(
        self, label_text: str, command_text: str
    ) -> QWidget:
        """
        Creates a widget with a label and a command to copy.

        :param label_text: The text to display in the label.
        :param command_text: The text to display in the command box.
        :return: The created widget.
        """
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        input_widget = QWidget()
        input_layout = QHBoxLayout()

        top_label = QLabel(label_text)
        command_text_box = QLineEdit()
        command_copy_btn = QPushButton("Copy command")

        command_text_box.setReadOnly(True)
        command_text_box.setText(command_text)
        command_copy_btn.clicked.connect(
            lambda: self._on_copy_btn_for_input_clicked(command_text_box)
        )

        input_layout.addWidget(command_text_box)
        input_layout.addWidget(command_copy_btn)
        input_widget.setLayout(input_layout)

        main_layout.addWidget(top_label)
        main_layout.addWidget(input_widget)
        main_widget.setLayout(main_layout)

        return main_widget

    def _create_commands_add_widget(
        self, label_text: str, apps_list: list[str], command_template: str
    ) -> QWidget:
        """
        Creates a widget to add commands.

        :param label_text: The text to display in the label.
        :param apps_list: The list of applications.
        :param command_template: The template for the command.
        :return: The created widget.
        """
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top widget -> add_custom_command_widget
        add_custom_command_widget = QWidget()
        add_custom_command_layout = QHBoxLayout()
        add_custom_command_label = QLabel(label_text)
        add_custom_command_line_edit = QLineEdit()
        add_custom_command_add_btn = QPushButton("Add")

        add_custom_command_layout.addWidget(add_custom_command_label)
        add_custom_command_layout.addWidget(add_custom_command_line_edit)
        add_custom_command_layout.addWidget(add_custom_command_add_btn)
        add_custom_command_widget.setLayout(add_custom_command_layout)

        # Middle widget -> list_management_widget
        list_management_widget = QWidget()
        list_management_layout = QHBoxLayout()

        left_list = QListWidget()
        right_list = QListWidget()

        add_item_to_right_btn = QPushButton("Add")
        add_all_item_to_right_btn = QPushButton("Add All")
        remove_item_from_right = QPushButton("Remove")
        remove_all_from_right = QPushButton("Remove All")
        generate_script_btn = QPushButton("Generate Script")
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(add_item_to_right_btn)
        buttons_layout.addWidget(add_all_item_to_right_btn)
        buttons_layout.addWidget(remove_item_from_right)
        buttons_layout.addWidget(remove_all_from_right)
        buttons_layout.addWidget(generate_script_btn)
        buttons_widget.setLayout(buttons_layout)

        list_management_layout.addWidget(left_list)
        list_management_layout.addWidget(buttons_widget)
        list_management_layout.addWidget(right_list)
        list_management_widget.setLayout(list_management_layout)

        # Bottom widget
        result_plain_text_edit = QPlainTextEdit()
        result_plain_text_edit.setReadOnly(True)
        copy_button = QPushButton("Copy command")

        # Config main widget
        main_layout.addWidget(add_custom_command_widget)
        main_layout.addWidget(list_management_widget)
        main_layout.addWidget(result_plain_text_edit)
        main_layout.addWidget(copy_button)
        main_widget.setLayout(main_layout)

        # Add handlers to buttons
        add_custom_command_add_btn.clicked.connect(
            lambda: self._on_add_custom_item_clicked(
                add_custom_command_line_edit, right_list
            )
        )
        add_item_to_right_btn.clicked.connect(
            lambda: self._on_add_item_to_list_clicked(left_list, right_list)
        )
        add_all_item_to_right_btn.clicked.connect(
            lambda: self._on_add_item_to_list_clicked(
                left_list, right_list, add_all=True
            )
        )
        remove_item_from_right.clicked.connect(
            lambda: self._on_remove_item_from_list_clicked(right_list)
        )
        remove_all_from_right.clicked.connect(
            lambda: self._on_remove_item_from_list_clicked(right_list, remove_all=True)
        )
        copy_button.clicked.connect(
            lambda: self._on_copy_btn_for_text_edit_clicked(result_plain_text_edit)
        )
        generate_script_btn.clicked.connect(
            lambda: self._on_generate_script_clicked(
                right_list, result_plain_text_edit, command_template
            )
        )

        left_list.addItems(apps_list)

        return main_widget

    def _on_copy_btn_for_input_clicked(self, text_field: QLineEdit) -> None:
        """
        Selects all text in a QLineEdit and copies it to the clipboard.

        :param text_field: The QLineEdit to copy from.
        """
        text_field.selectAll()
        text_field.copy()
        text_field.deselect()

    def _on_copy_btn_for_text_edit_clicked(self, text_field: QPlainTextEdit) -> None:
        """
        Selects all text in a QPlainTextEdit and copies it to the clipboard.

        :param text_field: The QPlainTextEdit to copy from.
        """
        text_field.selectAll()
        text_field.copy()

    def _on_add_custom_item_clicked(
        self, line_edit: QLineEdit, list_right: QListWidget
    ) -> None:
        """
        Adds an item to a QListWidget.

        :param line_edit: The QLineEdit containing the text to add.
        :param list_right: The QListWidget to add the item to.
        """
        self.add_item_to_the_list(line_edit.text(), list_right)

    def _on_add_item_to_list_clicked(
        self, left_list: QListWidget, list_right: QListWidget, add_all: bool = False
    ) -> None:
        """
        Adds selected items from one QListWidget to another.

        :param left_list: The QListWidget to add items from.
        :param list_right: The QListWidget to add items to.
        :param add_all: If True, adds all items. Otherwise only adds selected items.
        """
        if add_all:
            items: list[QListWidgetItem] = []
            for i in range(left_list.count()):
                items.append(left_list.item(i))
        else:
            items: list[QListWidgetItem] = left_list.selectedItems()
        for item in items:
            self.add_item_to_the_list(item.text(), list_right)
        self._all_commands.clear()

    def _on_remove_item_from_list_clicked(
        self, list_right: QListWidget, remove_all=False
    ) -> None:
        """
        Removes selected items from a QListWidget.

        :param list_right: The QListWidget to remove items from.
        :param remove_all: If True, removes all items. Otherwise only removes selected items.
        """
        if remove_all:
            list_right.clear()
        else:
            items: list[QListWidgetItem] = list_right.selectedItems()
            for item in items:
                for index in range(list_right.count()):
                    if list_right.item(index).text() == item.text():
                        list_right.takeItem(index)
                        break
        self._all_commands.clear()

    def _on_generate_script_clicked(
        self, items_list: QListWidget, text_area: QPlainTextEdit, command_template: str
    ) -> None:
        """
        Generates a script from a list of items and a command template.

        :param items_list: The QListWidget containing the items to generate commands for.
        :param text_area: The QPlainTextEdit to display the generated script in.
        :param command_template: The template for generating commands.
        """
        apps: list[str] = []
        for index in range(items_list.count()):
            apps.append(items_list.item(index).text())
        commands = list(map(lambda item: command_template.format(item), apps))
        joined_commands = tc.join_commands_in_one(commands)
        text_area.setPlainText(joined_commands)

        self._all_commands[command_template] = []
        for command in commands:
            self._all_commands[command_template].append(command)

    def add_item_to_the_list(self, value: str, list_widget: QListWidget) -> None:
        """
        Adds an item to a QListWidget if it doesn't already exist.

        :param value: The value to add.
        :param list_widget: The QListWidget to add the item to.
        """
        if (
            value
            and len(value.strip()) > 0
            and not list_widget.findItems(value.strip(), Qt.MatchFlag.MatchExactly)
        ):
            list_widget.addItem(value.strip())
        self._all_commands.clear()

    def _on_generate_common_script_clicked(
        self, common_command_text_edit: QPlainTextEdit
    ):
        """
        Generates a common script by joining and sorting all commands.

        :param common_command_text_edit: The text edit widget to display the result.
        """
        values = self._all_commands.values()
        commands = []
        for value in values:
            commands.extend(value)
        result = tc.join_commands_in_one(
            su.sort_lines(list(commands), case_insensitive=True, order=su.DESC)
        )
        common_command_text_edit.setPlainText(result)
