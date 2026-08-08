"""Initial PySide6 desktop shell for SIAP-RTC."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QListWidget, QMainWindow,
    QMessageBox, QPushButton, QProgressBar, QVBoxLayout, QWidget,
)

from app.application.rtc_import import RtcImportPipeline


class ImportWorkerSignals(QObject):
    finished = Signal(object)
    failed = Signal(str)


class ImportWorker(QRunnable):
    """Run the import pipeline off the GUI thread."""

    def __init__(self, files: list[Path]) -> None:
        super().__init__()
        self.files = files
        self.signals = ImportWorkerSignals()

    def run(self) -> None:
        try:
            result = RtcImportPipeline().run(self.files)
            self.signals.finished.emit(result)
        except Exception as exc:  # pragma: no cover - GUI safety boundary
            self.signals.failed.emit(str(exc))


class MainWindow(QMainWindow):
    """Main application window for the SIAP-RTC desktop client."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SIAP-RTC | Sistema de Información de Pautado RTC")
        self.resize(980, 650)
        self.thread_pool = QThreadPool.globalInstance()
        self.files: list[Path] = []
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        title = QLabel("SIAP-RTC")
        subtitle = QLabel("Importación y análisis histórico de pautado de la Cámara de Senadores")
        self.file_list = QListWidget()
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        self.status = QLabel("Seleccione uno o varios archivos Excel de RTC.")

        buttons = QHBoxLayout()
        select = QPushButton("Seleccionar archivos RTC")
        select.clicked.connect(self.select_files)
        process = QPushButton("Procesar")
        process.clicked.connect(self.process_files)
        clear = QPushButton("Limpiar")
        clear.clicked.connect(self.clear_files)
        buttons.addWidget(select)
        buttons.addWidget(process)
        buttons.addWidget(clear)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(buttons)
        layout.addWidget(self.file_list)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        self.setCentralWidget(central)

    def select_files(self) -> None:
        selected, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar archivos RTC", "", "Excel (*.xlsx *.xlsm)"
        )
        self.files = [Path(item) for item in selected]
        self.file_list.clear()
        self.file_list.addItems([str(path) for path in self.files])
        self.status.setText(f"{len(self.files)} archivo(s) seleccionado(s).")

    def clear_files(self) -> None:
        self.files.clear()
        self.file_list.clear()
        self.status.setText("Seleccione uno o varios archivos Excel de RTC.")

    def process_files(self) -> None:
        if not self.files:
            QMessageBox.information(self, "SIAP-RTC", "Seleccione al menos un archivo RTC.")
            return
        self.progress.show()
        self.status.setText("Procesando archivos…")
        worker = ImportWorker(self.files)
        worker.signals.finished.connect(self.on_import_finished)
        worker.signals.failed.connect(self.on_import_failed)
        self.thread_pool.start(worker)

    def on_import_finished(self, result: object) -> None:
        self.progress.hide()
        self.status.setText(
            f"Filas leídas: {result.rows_read} | Aceptadas: {len(result.accepted)} | "
            f"Duplicadas: {result.duplicates} | Rechazadas: {result.rejected}"
        )

    def on_import_failed(self, message: str) -> None:
        self.progress.hide()
        self.status.setText("La importación terminó con error.")
        QMessageBox.critical(self, "Error de importación", message)


def run() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
