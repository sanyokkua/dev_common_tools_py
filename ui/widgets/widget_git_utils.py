from PySide6.QtWidgets import (
    QWidget,
    QToolBar,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)

import core.terminal_commands as tc


class WidgetGitUtils(QWidget):
    """
    A custom QWidget that provides a user interface for Git utilities.

    This widget contains a toolbar with actions for generating local and global Git configurations,
    as well as resetting the configuration. It also has input fields for entering a username and email,
    and a read-only text field for displaying output.
    """

    def __init__(self):
        """
        Initializes the WidgetGitUtils instance.

        This method creates the user interface elements and adds them to the layout.
        """
        super().__init__()

        self._git_utils_toolbar = QToolBar()
        self._git_utils_toolbar.addAction(
            "Generate Local Config", self.generate_local_config
        )
        self._git_utils_toolbar.addAction(
            "Generate Global Config", self.generate_global_config
        )
        self._git_utils_toolbar.addAction("Reset", self.reset)

        self._username_label = QLabel("Username")
        self._email_label = QLabel("Email")

        self._username_line_edit = QLineEdit()
        self._email_line_edit = QLineEdit()

        self._username_pair = QHBoxLayout()
        self._username_pair.addWidget(self._username_label)
        self._username_pair.addWidget(self._username_line_edit)
        self._username_widget = QWidget()
        self._username_widget.setLayout(self._username_pair)

        self._email_pair = QHBoxLayout()
        self._email_pair.addWidget(self._email_label)
        self._email_pair.addWidget(self._email_line_edit)
        self._email_widget = QWidget()
        self._email_widget.setLayout(self._email_pair)

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._git_utils_toolbar)
        self._main_layout.addWidget(self._username_widget)
        self._main_layout.addWidget(self._email_widget)
        self._main_layout.addWidget(self._text_edit)
        self.setLayout(self._main_layout)

    def generate_local_config(self):
        """
        Generates local Git configuration commands.

        This method retrieves the username and email entered in the input fields,
        and uses them to generate Git configuration commands for setting the local
        user.name and user.email. The generated commands are displayed in the read-only
        text field.
        """
        username: str = self._username_line_edit.text().strip()
        email: str = self._email_line_edit.text().strip()
        if len(username) > 0 and len(email) > 0:
            result: str = tc.generate_git_config_commands(
                username, email, is_global=False
            )
            self._text_edit.setPlainText(result)

    def generate_global_config(self):
        """
        Generates global Git configuration commands.

        This method retrieves the username and email entered in the input fields,
        and uses them to generate Git configuration commands for setting the global
        user.name and user.email. The generated commands are displayed in the read-only
        text field.
        """
        username: str = self._username_line_edit.text().strip()
        email: str = self._email_line_edit.text().strip()
        if len(username) > 0 and len(email) > 0:
            result: str = tc.generate_git_config_commands(
                username, email, is_global=True
            )
            self._text_edit.setPlainText(result)

    def reset(self):
        """
        Resets the input fields and text field.

        This method clears the text in the username and email input fields,
        as well as the read-only text field.
        """
        self._username_line_edit.setText("")
        self._email_line_edit.setText("")
        self._text_edit.setPlainText("")
