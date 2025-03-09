import os
import shutil
import subprocess
from backup.b2rc import main as b2rc_main
from backup.backup7z.app import main as backup7z_main
from aplicaciones.chocoui.main import main as chocoui_main
from comandos_windows.comandawin import main as comandawin_main

def crear_estructura_tfg(base_path):
    """Crea la estructura de carpetas para el proyecto TFG."""
    # Definir rutas principales
    tfg_path = os.path.join(base_path, "TFG")
    backup_dir = os.path.join(tfg_path, "Backup")
    aplicaciones_dir = os.path.join(tfg_path, "Aplicaciones")
    comandos_win_dir = os.path.join(tfg_path, "Comandos_Windows")
    
    # Crear directorios
    os.makedirs(backup_dir, exist_ok=True)
    os.makedirs(aplicaciones_dir, exist_ok=True)
    os.makedirs(comandos_win_dir, exist_ok=True)
    
    return {
        "TFG": tfg_path,
        "Backup": backup_dir,
        "Aplicaciones": aplicaciones_dir,
        "Comandos_Windows": comandos_win_dir,
    }

def mover_archivos(base_path):
    """Mueve los archivos extraídos a sus respectivas carpetas en la estructura TFG."""
    estructura = crear_estructura_tfg(base_path)
    
    archivos_a_mover = {
        "B2RC": estructura["Backup"],
        "Backup7z": estructura["Backup"],
        "ChoCoUI": estructura["Aplicaciones"],
        "ComandaWin": estructura["Comandos_Windows"],
    }
    
    for archivo, destino in archivos_a_mover.items():
        origen = os.path.join(base_path, archivo)
        if os.path.exists(origen):
            shutil.move(origen, destino)
            print(f"Movido: {archivo} -> {destino}")
        else:
            print(f"No encontrado: {archivo}")

def main():
    """Función principal que ejecuta la aplicación TFG unificada."""
    print("Iniciando aplicación TFG...")
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Ejecutar B2RC (Backup)")
        print("2. Ejecutar Backup7z")
        print("3. Ejecutar ChocoUI (Aplicaciones)")
        print("4. Ejecutar ComandaWin (Comandos Windows)")
        print("5. Salir")
        
        opcion = input("Ingrese una opción: ")
        
        if opcion == "1":
            b2rc_main()
        elif opcion == "2":
            backup7z_main()
        elif opcion == "3":
            chocoui_main()
        elif opcion == "4":
            comandawin_main()
        elif opcion == "5":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    ruta_base = os.getcwd()  # Ruta donde se ejecuta el script
    mover_archivos(ruta_base)
    main()