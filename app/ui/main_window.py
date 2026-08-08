"""Operational PySide6 window for SIAP-RTC."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QListWidget, QMainWindow, QMessageBox, QProgressBar, QStackedWidget, QToolBar, QVBoxLayout, QPushButton, QWidget
from sqlalchemy.orm import Session

from app.application.e2e_import import EndToEndImportService
from app.application.import_report import ImportReport
from app.application.indicators import RtcIndicatorService
from app.application.queries import RtcQueryService
from app.application.rtc_import import RtcImportPipeline
from app.application.rtc_import_service import RtcImportService
from app.infrastructure.config import AppPaths
from app.infrastructure.rtc_persistence import RtcPersistence
from app.ui.dashboard import DashboardWidget
from app.ui.import_summary import ImportSummaryDialog
from app.ui.query_panel import QueryPanel


class WorkerSignals(QObject):
    finished = Signal(object)
    failed = Signal(str)


class ImportWorker(QRunnable):
    def __init__(self, service: EndToEndImportService, files: list[Path]) -> None:
        super().__init__()
        self.service = service
        self.files = files
        self.signals = WorkerSignals()

    def run(self) -> None:
        try:
            self.signals.finished.emit(self.service.execute(self.files))
        except Exception as exc:
            self.signals.failed.emit(str(exc))


class MainWindow(QMainWindow):
    """Desktop client with persistent E2E RTC import, dashboard and history query."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SIAP-RTC | Sistema de Información de Pautado RTC")
        self.resize(1200, 720)
        self.thread_pool = QThreadPool.globalInstance()
        self.files: list[Path] = []
        self.paths = AppPaths.from_environment().ensure()
        self.persistence = RtcPersistence(f"sqlite:///{self.paths.database.as_posix()}")
        self.import_service = EndToEndImportService(
            RtcImportService(RtcImportPipeline(), self.persistence)
        )
        self._build_ui()
        self.refresh_dashboard()

    def _build_ui(self) -> None:
        toolbar = QToolBar("Navegación")
        self.addToolBar(toolbar)
        for title, index in (("Inicio", 0), ("Importar RTC", 1), ("Histórico", 2)):
            action = toolbar.addAction(title)
            action.triggered.connect(lambda checked=False, i=index: self.stack.setCurrentIndex(i))
        self.stack = QStackedWidget()
        self.dashboard = DashboardWidget()
        self.import_page = self._build_import_page()
        self.query = QueryPanel()
        self.query.query_requested.connect(self.execute_query)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.import_page)
        self.stack.addWidget(self.query)
        self.setCentralWidget(self.stack)

    def _build_import_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Importación de archivos RTC"))
        self.file_list = QListWidget()
        select = QPushButton("Seleccionar archivos RTC")
        select.clicked.connect(self.select_files)
        process = QPushButton("Procesar y guardar en histórico")
        process.clicked.connect(self.process_files)
        clear = QPushButton("Limpiar")
        clear.clicked.connect(self.clear_files)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        self.status = QLabel("Seleccione uno o varios archivos Excel.")
        for widget in (select, process, clear, self.file_list, self.progress, self.status):
            layout.addWidget(widget)
        return page

    def select_files(self) -> None:
        selected, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos RTC", "", "Excel (*.xlsx *.xlsm)")
        self.files = [Path(item) for item in selected]
        self.file_list.clear()
        self.file_list.addItems([str(path) for path in self.files])
        self.status.setText(f"{len(self.files)} archivo(s) seleccionado(s).")

    def clear_files(self) -> None:
        self.files.clear()
        self.file_list.clear()
        self.status.setText("Seleccione uno o varios archivos Excel.")

    def process_files(self) -> None:
        if not self.files:
            QMessageBox.information(self, "SIAP-RTC", "Seleccione al menos un archivo RTC.")
            return
        self.progress.show()
        self.status.setText("Validando, deduplicando y guardando en histórico…")
        worker = ImportWorker(self.import_service, self.files)
        worker.signals.finished.connect(self.import_finished)
        worker.signals.failed.connect(self.import_failed)
        self.thread_pool.start(worker)

    def import_finished(self, report: ImportReport) -> None:
        self.progress.hide()
        self.status.setText(
            f"Leídas: {report.rows_read} | Aceptadas: {report.accepted} | "
            f"Duplicadas: {report.duplicates} | Rechazadas: {report.rejected}"
        )
        ImportSummaryDialog(report).exec()
        self.refresh_dashboard()

    def import_failed(self, message: str) -> None:
        self.progress.hide()
        QMessageBox.critical(self, "Error de importación", message)

    def refresh_dashboard(self) -> None:
        with Session(self.persistence.engine) as session:
            self.dashboard.update_indicators(RtcIndicatorService(session).summary())

    def execute_query(self, payload: dict) -> None:
        with Session(self.persistence.engine) as session:
            records = RtcQueryService(session).list_records(**payload)
            self.query.set_records(records)


def run() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
