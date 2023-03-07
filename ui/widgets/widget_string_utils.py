from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QToolBar,
    QPlainTextEdit,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
)

import core.string_utils as su


class SeparatorDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Type Separator to use")
        self._dialog_layout = QVBoxLayout(self)
        self._separator_label = QLabel("Separator:")
        self._separator_line_edit = QLineEdit()
        self._dialog_layout.addWidget(self._separator_label)
        self._dialog_layout.addWidget(self._separator_line_edit)
        self._dialog_button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self._dialog_layout.addWidget(self._dialog_button_box)
        self._dialog_button_box.accepted.connect(self.accept)
        self._dialog_button_box.rejected.connect(self.reject)

    @property
    def separator(self):
        return self._separator_line_edit.text()


class WidgetStringUtils(QWidget):
    def __init__(self):
        super().__init__()
        self._text_edit_widget = QPlainTextEdit()

        self._action_toolbar = QToolBar("String Actions Toolbar")
        self._action_toolbar.addAction("Copy", self.copy_text)
        self._action_toolbar.addAction("Paste", self.paste_text)
        self._action_toolbar.addAction("Cut", self.cut_text)
        self._action_toolbar.addAction("Clear", self.clear_text_area)
        self._action_toolbar.addAction("Create Lines", self.make_lines)
        self._action_toolbar.addAction(
            "Sort Asc", lambda: self.sort_lines(su.ASC, False)
        )
        self._action_toolbar.addAction(
            "Sort Lines Asc Ignore Case", lambda: self.sort_lines(su.ASC, True)
        )
        self._action_toolbar.addAction(
            "Sort Lines Desc", lambda: self.sort_lines(su.DESC, False)
        )
        self._action_toolbar.addAction(
            "Sort Lines Desc Ignore Case", lambda: self.sort_lines(su.DESC, True)
        )

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self._action_toolbar)
        self.mainLayout.addWidget(self._text_edit_widget)
        self.setLayout(self.mainLayout)

    def copy_text(self) -> None:
        self._text_edit_widget.selectAll()
        self._text_edit_widget.copy()

    def paste_text(self) -> None:
        self._text_edit_widget.paste()

    def cut_text(self) -> None:
        self._text_edit_widget.selectAll()
        self._text_edit_widget.cut()

    def clear_text_area(self) -> None:
        self._text_edit_widget.selectAll()
        self._text_edit_widget.clear()

    def make_lines(self) -> None:
        dialog = SeparatorDialog()
        dialog.show()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text: str = self._text_edit_widget.toPlainText()
            non_sorted_lines: list[str] = su.make_lines(
                text, separator=dialog.separator
            )
            result = su.join_lines(non_sorted_lines, "\n")
            self._text_edit_widget.setPlainText(result)

    def sort_lines(self, direction: str, ignore_case: bool = False) -> None:
        text: str = self._text_edit_widget.toPlainText()
        non_sorted_lines: list[str] = su.make_lines(text)
        sorted_lines: list[str] = su.sort_lines(
            non_sorted_lines, order=direction, case_insensitive=ignore_case
        )
        result: str = su.join_lines(sorted_lines, "\n")
        self._text_edit_widget.setPlainText(result)
