from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)


class MacOsSetupTopWidget(QWidget):
    def __init__(self, label_text: str, command_text: str) -> None:
        QWidget.__init__(self)

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

        self.setLayout(main_layout)

    @staticmethod
    def _on_copy_btn_for_input_clicked(text_field: QLineEdit) -> None:
        text_field.selectAll()
        text_field.copy()
        text_field.deselect()
