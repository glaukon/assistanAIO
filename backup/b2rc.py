import sys
import subprocess
import os
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QFileDialog, QMessageBox, QCheckBox)

CONFIG_FILE = "config.json"
RCLONE_CONFIG_PATH = "C:\\rclone\\rclone.conf"
WINFSP_URL = "https://winfsp.dev/rel/"

class BackupB2App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_config()
        self.check_winfsp()
    
    def init_ui(self):
        self.setWindowTitle("Backup App con B2")
        self.setGeometry(100, 100, 500, 400)
        
        layout = QVBoxLayout()

        self.bucket_label = QLabel("Nombre del bucket B2:")
        self.bucket_input = QLineEdit()
        layout.addWidget(self.bucket_label)
        layout.addWidget(self.bucket_input)
        
        self.access_key_label = QLabel("B2 Account ID:")
        self.access_key_input = QLineEdit()
        layout.addWidget(self.access_key_label)
        layout.addWidget(self.access_key_input)

        self.secret_key_label = QLabel("B2 Application Key:")
        self.secret_key_input = QLineEdit()
        self.secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.secret_key_label)
        layout.addWidget(self.secret_key_input)
        
        self.save_credentials_button = QPushButton("Guardar Credenciales B2")
        self.save_credentials_button.clicked.connect(self.save_b2_credentials)
        layout.addWidget(self.save_credentials_button)
        
        self.mount_button = QPushButton("Montar B2")
        self.mount_button.clicked.connect(self.mount_b2)
        layout.addWidget(self.mount_button)
        
        self.unmount_button = QPushButton("Desmontar B2")
        self.unmount_button.clicked.connect(self.unmount_b2)
        layout.addWidget(self.unmount_button)
        
        self.autostart_checkbox = QCheckBox("Montar B2 en el arranque")
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        layout.addWidget(self.autostart_checkbox)
        
        self.backup_button = QPushButton("Seleccionar Carpeta para Backup")
        self.backup_button.clicked.connect(self.select_backup_folder)
        layout.addWidget(self.backup_button)
        
        self.setLayout(layout)
    
    def check_winfsp(self):
        try:
            result = subprocess.run(["fsptool-x64", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise FileNotFoundError
        except FileNotFoundError:
            QMessageBox.warning(self, "WinFsp no encontrado", "WinFsp no está instalado. Se procederá a descargar e instalar automáticamente.")
            self.install_winfsp()
            self.add_winfsp_to_path()
    
    def install_winfsp(self):
        installer_path = os.path.join(os.getcwd(), "winfsp-installer.exe")
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {WINFSP_URL} -OutFile {installer_path}"], shell=True)
        subprocess.run([installer_path, "/S"], shell=True)
        QMessageBox.information(self, "Instalación Completa", "WinFsp ha sido instalado. Reinicie el sistema si es necesario.")
    
    def add_winfsp_to_path(self):
        winfsp_path = "C:\\Program Files (x86)\\WinFsp\\bin"
        current_path = os.environ.get("PATH", "")
        if winfsp_path not in current_path:
            os.environ["PATH"] = f"{winfsp_path};{current_path}"
            subprocess.run(f'setx PATH "{os.environ["PATH"]}"', shell=True)
            QMessageBox.information(self, "PATH Actualizado", "WinFsp ha sido agregado al PATH del sistema. Reinicie el sistema si es necesario.")
    
    def save_b2_credentials(self):
        access_key = self.access_key_input.text().strip()
        secret_key = self.secret_key_input.text().strip()

        if not access_key or not secret_key:
            QMessageBox.warning(self, "Error", "Debe ingresar Account ID y Application Key")
            return

        os.makedirs(os.path.dirname(RCLONE_CONFIG_PATH), exist_ok=True)
        with open(RCLONE_CONFIG_PATH, "w") as f:
            f.write(f"[b2]\n")

        
        QMessageBox.information(self, "Éxito", "Credenciales guardadas correctamente")
        self.save_config()
    
    def mount_b2(self):
        # Implementar la lógica para montar B2
        pass

    def unmount_b2(self):
        # Implementar la lógica para desmontar B2
        pass

    def toggle_autostart(self):
        # Implementar la lógica para habilitar/deshabilitar el arranque automático
        pass

    def select_backup_folder(self):
        # Implementar la lógica para seleccionar la carpeta de respaldo
        pass

    def load_config(self):
        # Implementar la lógica para cargar la configuración
        pass

    def save_config(self):
        # Implementar la lógica para guardar la configuración
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackupB2App()
    window.show()
    sys.exit(app.exec())