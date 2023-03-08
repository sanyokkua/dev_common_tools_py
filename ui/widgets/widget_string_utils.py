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
    """
    A custom QDialog for selecting a separator.

    This dialog contains a label and input field for entering a separator,
    as well as OK and Cancel buttons for accepting or rejecting the entered value.
    """

    def __init__(self):
        """
        Initializes the SeparatorDialog instance.

        This method creates the user interface elements and adds them to the layout.
        It also connects the accepted and rejected signals of the button box to
        the accept and reject slots of the dialog.
        """
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
        """
        Returns the separator entered in the input field.

        :return: The text entered in the separator input field.
        """
        return self._separator_line_edit.text()


class WidgetStringUtils(QWidget):
    """
    A custom QWidget for performing string manipulation actions.

    This widget contains a toolbar with actions for copying, pasting, cutting,
    and clearing text in a text area. It also has actions for creating lines from
    the text and sorting them in ascending or descending order, with or without
    case sensitivity.
    """

    def __init__(self):
        """
        Initializes the WidgetStringUtils instance.

        This method creates the user interface elements and adds them to the layout.
        """
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
        """
        Selects all text in the text edit widget and copies it to the clipboard.
        """
        self._text_edit_widget.selectAll()
        self._text_edit_widget.copy()

    def paste_text(self) -> None:
        """
        Pastes text from the clipboard into the text edit widget.
        """
        self._text_edit_widget.paste()

    def cut_text(self) -> None:
        """
        Selects all text in the text edit widget and cuts it to the clipboard.
        """
        self._text_edit_widget.selectAll()
        self._text_edit_widget.cut()

    def clear_text_area(self) -> None:
        """
        Selects all text in the text edit widget and clears it.
        """
        self._text_edit_widget.selectAll()
        self._text_edit_widget.clear()

    def make_lines(self) -> None:
        """
        Opens a dialog to get a separator character from the user. Splits
        the text in the text edit widget into lines using this separator,
        then joins these lines with newline characters and sets this as
        the new content of the text edit widget.

        :param self: The instance of this class that is calling this method
        :return: None
        """
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
        """
        Sorts lines of text in a given direction (ascending or descending)
        with an option to ignore case.

        :param self: The instance of this class that is calling this method
        :param direction: The direction to sort lines (ascending or descending)
        :param ignore_case: Whether or not to ignore case when sorting lines (default False)
        :return: None
        """
        text: str = self._text_edit_widget.toPlainText()
        non_sorted_lines: list[str] = su.make_lines(text)
        sorted_lines: list[str] = su.sort_lines(
            non_sorted_lines, order=direction, case_insensitive=ignore_case
        )
        result: str = su.join_lines(sorted_lines, "\n")
        self._text_edit_widget.setPlainText(result)
