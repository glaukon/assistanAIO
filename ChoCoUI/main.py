import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, 
    QLabel, QTextEdit, QFileDialog, QWidget, QProgressBar
)
from PyQt6.QtGui import QIcon

class PackageInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChocoUI")
        self.setFixedSize(QSize(600, 700))
        self.setup_ui()
        self.check_and_install_chocolatey()
        self.config_file = None

        # Estilos CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QTextEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 5px;
                font-family: Consolas;
                font-size: 14px;
                padding: 10px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
        """)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Instalador de Paquetes")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.install_button = QPushButton("Instalar Paquetes")
        self.install_button.clicked.connect(self.install_packages)
        layout.addWidget(self.install_button)

        self.select_file_button = QPushButton("Seleccionar Archivo de Configuración")
        self.select_file_button.clicked.connect(self.select_config_file)
        layout.addWidget(self.select_file_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_and_install_chocolatey(self):
        if not self.is_chocolatey_installed():
            self.install_chocolatey()

    def is_chocolatey_installed(self):
        try:
            subprocess.run(["choco", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_chocolatey(self):
        try:
            subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                            "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"],
                           check=True)
            self.text_edit.append("Chocolatey instalado correctamente.")
        except subprocess.CalledProcessError as e:
            self.text_edit.append(f"Error al instalar Chocolatey: {e}")

    def select_config_file(self):
        file_dialog = QFileDialog()
        self.config_file, _ = file_dialog.getOpenFileName(self, "Seleccionar Archivo de Configuración", "", "Config Files (*.config);;PowerShell Scripts (*.ps1)")
        if self.config_file:
            self.text_edit.append(f"Archivo de configuración seleccionado: {self.config_file}")

    def install_packages(self):
        if not self.config_file:
            self.text_edit.append("Por favor, seleccione un archivo de configuración primero.")
            return

        try:
            if self.config_file.endswith('.xml'):
                tree = ET.parse(self.config_file)
                root = tree.getroot()
                packages = [(pkg.find('name').text, pkg.find('manager').text) for pkg in root.findall('package')]

                self.progress_bar.setMaximum(len(packages))
                self.progress_bar.setValue(0)

                for i, (package, manager) in enumerate(packages):
                    self.text_edit.append(f"Instalando {package} con {manager}...")
                    if manager.lower() == "chocolatey":
                        subprocess.run(["choco", "install", package, "-y"], check=True)
                    elif manager.lower() == "winget":
                        subprocess.run(["winget", "install", "--id", package, "-e", "--accept-package-agreements", "--accept-source-agreements"], check=True)
                    self.progress_bar.setValue(i + 1)

            elif self.config_file.endswith('.ps1'):
                with open(self.config_file, 'r') as file:
                    packages = file.readlines()

                self.progress_bar.setMaximum(len(packages))
                self.progress_bar.setValue(0)

                for i, package in enumerate(packages):
                    package = package.strip()
                    if package:
                        self.text_edit.append(f"Instalando {package} con WinGet...")
                        subprocess.run(["winget", "install", "--id", package, "-e", "--accept-package-agreements", "--accept-source-agreements"], check=True)
                        self.progress_bar.setValue(i + 1)

            self.text_edit.append("Todos los paquetes han sido instalados.")
        except ET.ParseError as e:
            self.text_edit.append(f"Error al leer el archivo de configuración: {e}")
        except subprocess.CalledProcessError as e:
            self.text_edit.append(f"Error al instalar el paquete: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackageInstaller()
    window.show()
    sys.exit(app.exec())