import os
import subprocess
import shutil

def crear_respaldo(ruta_origen, ruta_destino):
    """Crea un archivo comprimido en formato 7z a partir de la ruta de origen."""
    if not os.path.exists(ruta_origen):
        print(f"La ruta de origen no existe: {ruta_origen}")
        return

    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)

    nombre_respaldo = os.path.basename(ruta_origen.rstrip(os.sep)) + ".7z"
    ruta_respaldo = os.path.join(ruta_destino, nombre_respaldo)

    try:
        subprocess.run(["7z", "a", ruta_respaldo, ruta_origen], check=True)
        print(f"Copia de seguridad creada: {ruta_respaldo}")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear la copia de seguridad: {e}")

def main():
    """Función principal para ejecutar la funcionalidad de backup."""
    ruta_origen = input("Ingrese la ruta de la carpeta o archivo a respaldar: ")
    ruta_destino = input("Ingrese la ruta de destino para el respaldo: ")
    crear_respaldo(ruta_origen, ruta_destino)

if __name__ == "__main__":
    main()