import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QListWidget, QLineEdit, QPushButton,
                             QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

COMMANDS = {
    "MSINFO32": "Información del sistema",
    "WINVER": "Versión de Windows",
    "PERFMON": "Monitor de rendimiento",
    "CALC": "Calculadora",
    "SNIPPINGTOOL": "Herramienta de recorte",
    # ... (agrega el resto de los comandos y descripciones aquí)
    "CONTROL": "Panel de control",
    "MSCONFIG": "Configuración del sistema",
    "CMD": "CMD",
    "DISKPART": "Administración de discos",
}

class CommandRunnerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejecutor de Comandos Windows")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_commands()
        
    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Cabecera
        header = QLabel("Ejecutor de Comandos de Windows")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2c3e50; padding: 15px;")
        
        # Barra de búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar comandos...")
        self.search_bar.textChanged.connect(self.filter_commands)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
                color: #000000;
                background-color: #ffffff;
            }
        """)
        
        # Lista de comandos
        self.command_list = QListWidget()
        self.command_list.itemDoubleClicked.connect(self.execute_command)
        self.command_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border-radius: 5px;
                padding: 5px;
                color: #000000;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #dcdde1;
            }
            QListWidget::item:hover {
                background-color: #3498db; 
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: #ffffff;
            }
        """)
        
        # Botones
        btn_execute = QPushButton("Ejecutar Comando")
        btn_execute.clicked.connect(self.execute_command)
        btn_execute.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Diseño
        layout.addWidget(header)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.command_list)
        layout.addWidget(btn_execute)
        
    def load_commands(self):
        self.command_list.clear()
        for cmd, desc in COMMANDS.items():
            self.command_list.addItem(f"{cmd} - {desc}")
            
    def filter_commands(self):
        search_text = self.search_bar.text().upper()
        for i in range(self.command_list.count()):
            item = self.command_list.item(i)
            item.setHidden(search_text not in item.text())
            
    def execute_command(self):
        selected = self.command_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Selecciona un comando primero")
            return
            
        cmd = selected.text().split(" - ")[0]
        try:
            subprocess.Popen(f"start {cmd}", shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo ejecutar el comando:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CommandRunnerApp()
    window.show()
    sys.exit(app.exec())