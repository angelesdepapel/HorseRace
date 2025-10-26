import os

archivos_a_limpiar = ["apuestas.txt", "ganador.txt", "pagos.txt"] 

print("Iniciando reseteo de archivos de estado...")

for nombre_archivo in archivos_a_limpiar:
    with open(nombre_archivo, 'w') as f:
        pass
    print(f"'{nombre_archivo}' ha sido limpiado.")
    
print("\nReseteo completado.")
print("-" * 40)
print("Llamando a 'inscripciones.py'...")
print("=" * 40 + "\n")

os.system("py inscripciones.py")
    