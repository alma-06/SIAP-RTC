"""Application entry point for SIAP-RTC Foundation."""

from __future__ import annotations


def main() -> int:
    """Start the SIAP-RTC application shell."""
    from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

    application = QApplication.instance() or QApplication([])
    window = QMainWindow()
    window.setWindowTitle("SIAP-RTC")
    window.resize(1100, 700)
    window.setCentralWidget(QLabel("SIAP-RTC — Foundation v0.1.0-alpha1"))
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
