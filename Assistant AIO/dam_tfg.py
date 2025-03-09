import sys
import platform
import psutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, 
                             QFrame, QStackedWidget)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt

class SystemInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Information Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)
        
        # Configuración principal de la UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_sidebar()
        self.setup_main_content()
        
        # Cargar datos iniciales
        self.load_system_info()
        self.show_system_info()

    def setup_sidebar(self):
        """Configura la barra lateral con estilos y botones"""
        sidebar = QWidget()
        sidebar.setFixedWidth(150)
        sidebar.setStyleSheet("""
            background-color: #2c3e50;
            padding: 20px 0;
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Botón de Inicio
        self.btn_home = QPushButton("Inicio")
        self.btn_home.setIcon(QIcon.fromTheme("go-home"))
        self.btn_home.setIconSize(QSize(24, 24))
        self.btn_home.setStyleSheet("""
            QPushButton {
                color: white;
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        self.btn_home.clicked.connect(self.show_system_info)
        
        sidebar_layout.addWidget(self.btn_home)
        sidebar_layout.addStretch()
        
        self.main_layout.addWidget(sidebar)

    def setup_main_content(self):
        """Configura el área de contenido principal"""
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Página de información del sistema
        self.system_info_page = QWidget()
        self.stacked_widget.addWidget(self.system_info_page)

    def load_system_info(self):
        """Carga y procesa la información del sistema"""
        try:
            self.system_data = {
                'os': f"{platform.system()} {platform.release()}",
                'hostname': platform.node(),
                'processor': platform.processor() or "Desconocido",
                'cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True),
                'ram': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                'cpu_freq': f"{(psutil.cpu_freq().current or 0) / 1000:.2f} GHz",
                'architecture': platform.machine()
            }
        except Exception as e:
            print(f"Error obteniendo información del sistema: {e}")
            self.system_data = {
                'os': "No disponible",
                'hostname': "No disponible",
                'processor': "No disponible",
                'cores': 0,
                'threads': 0,
                'ram': "0 GB",
                'cpu_freq': "0 GHz",
                'architecture': "No disponible"
            }

    def create_info_row(self, title, value):
        """Crea una fila de información con estilos"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #34495e;")
        title_label.setFixedWidth(200)
        
        value_label = QLabel(str(value))
        value_label.setStyleSheet("color: #7f8c8d;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return widget

    def show_system_info(self):
        """Muestra la información del sistema en el área principal"""
        # Limpiar contenido anterior
        if self.system_info_page.layout():
            QWidget().setLayout(self.system_info_page.layout())
        
        layout = QVBoxLayout(self.system_info_page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Encabezado
        header = QLabel("Información del Sistema")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(header)
        
        # Sección principal
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        
        # Agregar filas de información
        main_layout.addWidget(self.create_info_row("Sistema Operativo:", self.system_data['os']))
        main_layout.addWidget(self.create_info_row("Nombre del Equipo:", self.system_data['hostname']))
        main_layout.addWidget(self.create_info_row("Procesador:", self.system_data['processor']))
        main_layout.addWidget(self.create_info_row("Arquitectura:", self.system_data['architecture']))
        main_layout.addWidget(self.create_info_row("Núcleos Físicos:", self.system_data['cores']))
        main_layout.addWidget(self.create_info_row("Núcleos Lógicos:", self.system_data['threads']))
        main_layout.addWidget(self.create_info_row("Frecuencia CPU:", self.system_data['cpu_freq']))
        main_layout.addWidget(self.create_info_row("Memoria RAM:", self.system_data['ram']))
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #bdc3c7;")
        main_layout.addWidget(separator)
        
        # Estadísticas en tiempo real
        realtime_stats = QLabel("Estadísticas en Tiempo Real")
        realtime_stats.setStyleSheet("""
            font-size: 16px;
            color: #34495e;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(realtime_stats)
        
        # Widgets de estadísticas
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        # Uso de CPU
        cpu_usage = QLabel(f"CPU: {psutil.cpu_percent()}%")
        cpu_usage.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
        """)
        
        # Uso de Memoria
        mem = psutil.virtual_memory()
        mem_usage = QLabel(f"RAM: {mem.percent}%")
        mem_usage.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
        """)
        
        stats_layout.addWidget(cpu_usage)
        stats_layout.addWidget(mem_usage)
        main_layout.addWidget(stats_widget)
        
        layout.addWidget(main_content)
        self.stacked_widget.setCurrentWidget(self.system_info_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Configurar fuente global
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    window = SystemInfoApp()
    window.show()
    sys.exit(app.exec())