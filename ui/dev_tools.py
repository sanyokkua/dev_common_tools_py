import logging

from PySide6.QtWidgets import QApplication

import ui.widgets.widget_main_window as mw

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s",
)

log: logging.Logger = logging.getLogger(__name__)


class QApplicationDevTool(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self._main_widget: mw.QApplicationDevTool = mw.QApplicationDevTool()
        self._main_widget.show()


def start_app() -> None:
    app: QApplicationDevTool = QApplicationDevTool()
    app.exec()


if __name__ == "__main__":
    start_app()
