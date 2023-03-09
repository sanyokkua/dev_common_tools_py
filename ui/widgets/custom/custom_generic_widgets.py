from typing import Callable
from typing import Sequence

import PySide6.QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout
from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
)

import core.terminal_commands as tc


def stub(items: list[str]):
    """
    Stub handler
    :param items:
    :return:
    """
    pass


class CustomQListWidget(QListWidget):
    def __init__(self, items_amount_changed: Callable[[list[str]], None] = stub):
        QListWidget.__init__(self)
        self.items_amount_changed: Callable[[list[str]], None] = items_amount_changed

    def addItem(self, item):
        super().addItem(item)
        self.items_amount_changed(self._get_all_items())

    def addItems(self, items):
        super().addItems(items)
        self.items_amount_changed(self._get_all_items())

    def insertItem(self, row, item):
        super().insertItem(row, item)
        self.items_amount_changed(self._get_all_items())

    def takeItem(self, row):
        item = super().takeItem(row)
        self.items_amount_changed(self._get_all_items())
        return item

    def clear(self) -> None:
        super().clear()
        self.items_amount_changed(self._get_all_items())

    def editItem(self, item: PySide6.QtWidgets.QListWidgetItem) -> None:
        super().editItem(item)
        self.items_amount_changed(self._get_all_items())

    def insertItems(self, row: int, labels: Sequence[str]) -> None:
        super().insertItems(row, labels)
        self.items_amount_changed(self._get_all_items())

    def _get_all_items(self) -> list[str]:
        items: set[str] = set()
        for i in range(self.count()):
            item: QListWidgetItem = self.item(i)
            items.add(item.text().strip())
        return list(items)


class WebLinksWidget(QWidget):
    def __init__(self, header_label: str, web_urls: list[str]):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()

        top_label = QLabel(header_label)
        main_layout.addWidget(top_label)

        for link in web_urls:
            link_label = QLabel("<a href='{0}'>{0}</a>".format(link))
            link_label.setOpenExternalLinks(True)
            main_layout.addWidget(link_label)

        self.setLayout(main_layout)


class ChoseAppsWidget(QWidget):
    def __init__(
        self, label_text: str, initial_apps_list: list[str], command_template: str
    ):
        QWidget.__init__(self)
        self._generated_command: str = ""
        self._command_template: str = command_template
        self._chosen_apps: set[str] = set()

        main_layout = QVBoxLayout()

        top_widget: QWidget = self._create_top_widgets(label_text)
        middle_widget, left_list, right_list = self._create_middle_widgets()
        bottom_widget, generated_plain_text_edit = self._create_bottom_widgets()

        self._widget_left_list: QListWidget = left_list
        self._widget_right_list: QListWidget = right_list
        self._widget_command_text_edit: QPlainTextEdit = generated_plain_text_edit

        main_layout.addWidget(top_widget)
        main_layout.addWidget(middle_widget)
        main_layout.addWidget(bottom_widget)
        self.setLayout(main_layout)

        self._widget_left_list.addItems(initial_apps_list)

    def _create_top_widgets(self, label_text: str) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        add_button = QPushButton("Add")

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(add_button)
        widget.setLayout(layout)

        add_button.clicked.connect(
            lambda: self._on_user_command_btn_clicked(line_edit.text())
        )

        return widget

    def _create_middle_widgets(self) -> tuple[QWidget, QListWidget, QListWidget]:
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        left_list = CustomQListWidget()
        right_list = CustomQListWidget(self._on_chosen_items_changed)

        add_to_right = QPushButton("Add")
        add_all_to_right = QPushButton("Add All")
        remove_from_left = QPushButton("Remove")
        remove_all_from_left = QPushButton("Remove All")
        generate_script = QPushButton("Generate Script")

        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(add_to_right)
        buttons_layout.addWidget(add_all_to_right)
        buttons_layout.addWidget(remove_from_left)
        buttons_layout.addWidget(remove_all_from_left)
        buttons_layout.addWidget(generate_script)
        buttons_widget.setLayout(buttons_layout)

        main_layout.addWidget(left_list)
        main_layout.addWidget(buttons_widget)
        main_layout.addWidget(right_list)
        main_widget.setLayout(main_layout)

        add_to_right.clicked.connect(self._on_add_to_right_btn_clicked)
        add_all_to_right.clicked.connect(self._on_add_all_to_right_btn_clicked)
        remove_from_left.clicked.connect(self._on_remove_from_left_btn_clicked)
        remove_all_from_left.clicked.connect(self._on_remove_all_from_left_btn_clicked)
        generate_script.clicked.connect(self._on_generate_script_btn_clicked)

        return main_widget, left_list, right_list

    def _create_bottom_widgets(self) -> tuple[QWidget, QPlainTextEdit]:
        main_widget: QWidget = QWidget()
        main_layout: QVBoxLayout = QVBoxLayout()

        text_edit = QPlainTextEdit()
        text_edit.setReadOnly(True)
        copy_button = QPushButton("Copy command")

        main_layout.addWidget(text_edit)
        main_layout.addWidget(copy_button)

        main_widget.setLayout(main_layout)

        copy_button.clicked.connect(self._on_copy_command_btn_clicked)
        return main_widget, text_edit

    def _on_user_command_btn_clicked(self, value: str) -> None:
        if value and len(value.strip()) > 0:
            normalized_value: str = value.strip()
            if not self._widget_right_list.findItems(
                normalized_value, Qt.MatchFlag.MatchExactly
            ):
                self._widget_right_list.addItem(normalized_value)

    def _on_add_to_right_btn_clicked(self) -> None:
        items: list[QListWidgetItem] = self._widget_left_list.selectedItems()
        for item in items:
            self._on_user_command_btn_clicked(item.text())

    def _on_add_all_to_right_btn_clicked(self) -> None:
        for i in range(self._widget_left_list.count()):
            item: QListWidgetItem = self._widget_left_list.item(i)
            self._on_user_command_btn_clicked(item.text())

    def _on_remove_from_left_btn_clicked(self) -> None:
        items: list[QListWidgetItem] = self._widget_right_list.selectedItems()
        for item in items:
            for index in range(self._widget_right_list.count()):
                if self._widget_right_list.item(index).text() == item.text():
                    self._widget_right_list.takeItem(index)
                    break

    def _on_remove_all_from_left_btn_clicked(self) -> None:
        self._widget_right_list.clear()

    def _on_generate_script_btn_clicked(self) -> None:
        commands = list(
            map(lambda item: self._command_template.format(item), self._chosen_apps)
        )
        joined_commands = tc.join_commands_in_one(commands)
        self._widget_command_text_edit.setPlainText(joined_commands)

    def _on_copy_command_btn_clicked(self) -> None:
        self._widget_command_text_edit.selectAll()
        self._widget_command_text_edit.copy()

    def _on_chosen_items_changed(self, items: list[str]) -> None:
        self._chosen_apps.clear()
        for item in items:
            self._chosen_apps.add(item)

    @property
    def chosen_apps_commands(self) -> list[str]:
        return list(
            map(lambda item: self._command_template.format(item), self._chosen_apps)
        )
