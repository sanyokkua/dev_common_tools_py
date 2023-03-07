from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QDialogButtonBox,
)
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QWidget, QToolBar

import core.json_utils as ju


class JSONHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter for JSON data.
    Inherits from QSyntaxHighlighter.
    """

    def __init__(self, parent=None):
        """
        Initializes the JSONHighlighter object.
        :param parent: The parent widget.
        """
        super(JSONHighlighter, self).__init__(parent)
        self.highlightingRules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["true", "false", "null"]
        for word in keywords:
            pattern = QRegularExpression(r"\b" + word + r"\b")
            self.highlightingRules.append((pattern, keyword_format))
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("red"))
        self.highlightingRules.append((QRegularExpression(r"\".*\""), string_format))
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("green"))
        self.highlightingRules.append(
            (
                QRegularExpression(r"\b[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\b"),
                number_format,
            )
        )

    def highlightBlock(self, text):
        """
        Highlights the given text block.
        :param text: The text block to highlight.
        """
        for pattern, format_rule in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(), match.capturedLength(), format_rule
                )


class JsonFormatDialog(QDialog):
    """
    A dialog for choosing JSON format parameters.
    Inherits from QDialog.
    """

    def __init__(self, parent=None):
        """
        Initializes the JsonFormatDialog object.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Choose format params")
        self._dialog_layout = QVBoxLayout(self)
        self._indentation_label = QLabel("Indentation of JSON")
        self._indentation_input = QLineEdit()
        self._indentation_input.setValidator(QIntValidator(0, 100))
        self._indentation_input.setText("4")
        self._indentation_layout = QHBoxLayout()
        self._indentation_layout.addWidget(self._indentation_label)
        self._indentation_layout.addWidget(self._indentation_input)
        self._dialog_layout.addLayout(self._indentation_layout)
        self._sort_label = QLabel("Sort JSON keys?")
        self._sort_checkbox = QCheckBox()
        self._sort_layout = QHBoxLayout()
        self._sort_layout.addWidget(self._sort_label)
        self._sort_layout.addWidget(self._sort_checkbox)
        self._dialog_layout.addLayout(self._sort_layout)
        self._dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self._dialog_buttons.accepted.connect(self.accept)
        self._dialog_buttons.rejected.connect(self.reject)
        self._dialog_layout.addWidget(self._dialog_buttons)

    @property
    def indentation(self) -> int:
        """
        Returns the indentation value.
        :return: The indentation value as an integer.
        """
        return int(self._indentation_input.text())

    @property
    def sort_keys(self) -> bool:
        """
        Returns the sort keys value.
        :return: The sort keys value as a boolean.
        """
        return self._sort_checkbox.isChecked()


class WidgetJsonUtils(QWidget):
    """
    A widget for JSON utilities.
    Inherits from QWidget.
    """

    def __init__(self):
        """
        Initializes the WidgetJsonUtils object.
        """
        QWidget.__init__(self)

        self._json_toolbar = QToolBar()
        self._json_toolbar.addAction("Copy", self.copy_handler)
        self._json_toolbar.addAction("Paste", self.paste_handler)
        self._json_toolbar.addAction("Cut", self.cut_handler)
        self._json_toolbar.addAction("Clear", self.clear_handler)
        self._json_toolbar.addAction("Format", self.format_handler)
        self._json_toolbar.addAction("Flat", self.flat_handler)
        self._json_toolbar.addAction("Validate", self.validate_handler)

        self._json_editor: QPlainTextEdit = QPlainTextEdit()
        JSONHighlighter(self._json_editor.document())

        self._error_label = QLabel()
        self._error_label.setStyleSheet("color: red; font-weight: bold;")

        self._widget_layout = QVBoxLayout()
        self._widget_layout.addWidget(self._json_toolbar)
        self._widget_layout.addWidget(self._json_editor)
        self._widget_layout.addWidget(self._error_label)
        self.setLayout(self._widget_layout)

    def copy_handler(self) -> None:
        """
        Handles the copy action.
        """
        self._json_editor.selectAll()
        self._json_editor.copy()

    def paste_handler(self) -> None:
        """
        Handles the paste action.
        """
        self._json_editor.paste()

    def cut_handler(self) -> None:
        """
        Handles the cut action.
        """
        self._json_editor.selectAll()
        self._json_editor.cut()

    def clear_handler(self) -> None:
        """
        Handles the clear action.
        """
        self._json_editor.clear()

    def format_handler(self) -> None:
        """
        Handles the format action.
        """
        content: str = self._json_editor.toPlainText()
        if content and len(content) > 0:
            result: str = ju.validate_json(content)
            if len(result) == 0:
                dialog = JsonFormatDialog()
                dialog.show()
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    formatted: str = ju.format_json(
                        content,
                        indentation=dialog.indentation,
                        sort_keys=dialog.sort_keys,
                    )
                    self._json_editor.setPlainText(formatted)
            else:
                self._error_label.setText(result)

    def flat_handler(self) -> None:
        """
        Handles the flat action.
        """
        content: str = self._json_editor.toPlainText()
        if content and len(content) > 0:
            result: str = ju.validate_json(content)
            if len(result) == 0:
                json_flatten = ju.flatten_json(content)
                self._json_editor.setPlainText(json_flatten)
            else:
                self._error_label.setText(result)

    def validate_handler(self) -> None:
        """
        Handles the validate action.
        """
        content: str = self._json_editor.toPlainText()
        if content and len(content) > 0:
            result: str = ju.validate_json(content)
            if result and len(result) > 0:
                self._error_label.setText(result)
            else:
                self._error_label.setText("")
        else:
            self._error_label.setText("No Content")
