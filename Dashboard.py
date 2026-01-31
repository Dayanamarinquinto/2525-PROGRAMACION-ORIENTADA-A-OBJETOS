import os
import json
import subprocess
from datetime import datetime

# =========================
# CONFIGURACIÓN GENERAL
# =========================
DATA_FILE = "proyectos.json"

# =========================
# UTILIDADES DE DATOS
# =========================
def cargar_datos():
    """Carga los proyectos desde un archivo JSON"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    """Guarda los proyectos en un archivo JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# =========================
# EJECUCIÓN DE SCRIPTS
# =========================
def ejecutar_codigo(ruta_script):
    """Ejecuta un script Python en una nueva terminal"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Linux / Mac
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Error al ejecutar el script: {e}")

# =========================
# GESTIÓN DE TAREAS
# =========================
def agregar_tarea(datos, materia):
    nombre = input("Nombre de la tarea: ")
    fecha = input("Fecha límite (YYYY-MM-DD): ")
    prioridad = input("Prioridad (Alta / Media / Baja): ")

    tarea = {
        "estado": "Pendiente",
        "fecha_limite": fecha,
        "prioridad": prioridad,
        "creada": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    datos.setdefault(materia, []).append({nombre: tarea})
    guardar_datos(datos)
    print("✅ Tarea agregada correctamente.")

def listar_tareas(datos, materia):
    print(f"\n📚 Tareas de {materia}")
    if materia not in datos or not datos[materia]:
        print("No hay tareas registradas.")
        return

    for i, tarea in enumerate(datos[materia], 1):
        for nombre, info in tarea.items():
            print(f"{i}. {nombre}")
            print(f"   Estado: {info['estado']}")
            print(f"   Fecha límite: {info['fecha_limite']}")
            print(f"   Prioridad: {info['prioridad']}")

def cambiar_estado(datos, materia):
    listar_tareas(datos, materia)
    indice = int(input("Número de tarea: ")) - 1
    nuevo_estado = input("Nuevo estado (Pendiente / En progreso / Completada): ")

    tarea = datos[materia][indice]
    nombre = list(tarea.keys())[0]
    tarea[nombre]["estado"] = nuevo_estado

    guardar_datos(datos)
    print("🔄 Estado actualizado.")

# =========================
# MENÚ PRINCIPAL
# =========================
def mostrar_menu():
    datos = cargar_datos()

    while True:
        print("\n🎓 Dashboard Académico")
        print("1 - Ver materias")
        print("2 - Agregar tarea")
        print("3 - Listar tareas")
        print("4 - Cambiar estado de tarea")
        print("0 - Salir")

        opcion = input("Elige una opción: ")

        if opcion == "0":
            print("👋 Saliendo del sistema.")
            break

        elif opcion == "1":
            if not datos:
                print("No hay materias registradas.")
            else:
                for materia in datos:
                    print(f"- {materia}")

        elif opcion == "2":
            materia = input("Nombre de la materia: ")
            agregar_tarea(datos, materia)

        elif opcion == "3":
            materia = input("Materia a consultar: ")
            listar_tareas(datos, materia)

        elif opcion == "4":
            materia = input("Materia: ")
            cambiar_estado(datos, materia)

        else:
            print("❌ Opción no válida.")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    mostrar_menu()
