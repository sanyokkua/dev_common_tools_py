from PySide6.QtWidgets import QWidget, QToolBar, QPlainTextEdit, QVBoxLayout

import core.string_utils as su
import core.terminal_commands as tc


class WidgetTerminalUtils(QWidget):
    """
    A custom QWidget that provides a toolbar with actions for copying,
    pasting, cutting and clearing text as well as joining commands with
    or without ignoring errors. The widget also contains a text edit area.
    """

    def __init__(self):
        """
        Initializes the WidgetTerminalUtils object by creating a toolbar and
        a text edit widget. The toolbar has actions for copying, pasting,
        cutting and clearing text as well as joining commands with or without
        ignoring errors. These actions are connected to methods in the class
        that have not been provided in this code snippet. The toolbar and text
        edit widget are added to a layout which is set as the layout for this
        widget.

        :param self: The instance of this class that is calling this method
        :return: None
        """
        super().__init__()

        self._terminal_util_toolbar = QToolBar()
        self._text_edit = QPlainTextEdit()

        self._terminal_util_toolbar.addAction("Copy", self.copy)
        self._terminal_util_toolbar.addAction("Paste", self.paste)
        self._terminal_util_toolbar.addAction("Cut", self.cut)
        self._terminal_util_toolbar.addAction("Clear", self.clear)
        self._terminal_util_toolbar.addAction("Join commands", self.join_commands)
        self._terminal_util_toolbar.addAction(
            "Join Commands ignore errors", self.join_commands_ignore_errors
        )

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._terminal_util_toolbar)
        self._main_layout.addWidget(self._text_edit)
        self.setLayout(self._main_layout)

    def copy(self):
        """
        Selects all text in the text edit widget and copies it to the clipboard.
        """
        self._text_edit.selectAll()
        self._text_edit.copy()

    def paste(self):
        """
        Pastes text from the clipboard into the text edit widget.
        """
        self._text_edit.paste()

    def cut(self):
        """
        Selects all text in the text edit widget and cuts it to the clipboard.
        """
        self._text_edit.selectAll()
        self._text_edit.cut()

    def clear(self):
        """
        Selects all text in the text edit widget and clears it.
        """
        self._text_edit.selectAll()
        self._text_edit.clear()

    def join_commands(self):
        """
        Joins multiple commands into one command separated by '&&'.
        The commands are taken from the text in the text edit widget,
        split by newline characters. The resulting command is set as
        the new content of the text edit widget.

        :param self: The instance of this class that is calling this method
        :return: None
        """
        commands_text: str = self._text_edit.toPlainText()
        commands: list[str] = su.make_lines(commands_text, "\n")
        result: str = tc.join_commands_in_one(commands, ignore_errors=False)
        self._text_edit.setPlainText(result)

    def join_commands_ignore_errors(self):
        """
        Joins multiple commands into one command separated by '||'.
        The commands are taken from the text in the text edit widget,
        split by newline characters. The resulting command is set as
        the new content of the text edit widget.

        :param self: The instance of this class that is calling this method
        :return: None
        """
        commands_text: str = self._text_edit.toPlainText()
        commands: list[str] = su.make_lines(commands_text, "\n")
        result: str = tc.join_commands_in_one(commands, ignore_errors=True)
        self._text_edit.setPlainText(result)
