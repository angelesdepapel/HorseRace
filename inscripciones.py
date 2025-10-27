import os
import sys

def validar_apuesta(partes):
    if len(partes) != 3:
        print("Error: Formato incorrecto. Se esperan 3 campos separados por coma.")
        return False
    
    nombre = partes[0].strip()
    monto_str = partes[1].strip()
    color = partes[2].strip()

    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return False
    if not color:
        print("Error: El color no puede estar vacío.")
        return False

    try:
        monto = int(monto_str)
        # Verifica si el monto es positivo
        if monto <= 0:
            print("Error: El monto debe ser un número positivo.")
            return False
        
        # Verifica si el monto es múltiplo de 10
        if monto % 10 != 0:
            print(f"Error: El monto '{monto}' no es un múltiplo de 10.")
            return False

    except ValueError:
        print(f"Error: El monto '{monto_str}' no es un número válido.")
        return False
    
    # Si todo está OK, retorna los datos 
    return f"{nombre},{monto_str},{color.lower()}\n"

def iniciar_inscripciones():
    archivo_apuestas = "apuestas.txt"
    
    print("--- Centro de Inscripción de Apuestas ---")
    print(f"Las apuestas se guardarán en '{archivo_apuestas}'.")
    print("Ingrese las apuestas con el formato: Nombre,Monto,Color")
    print("IMPORTANTE: El monto debe ser un múltiplo de 10 (ej. 10, 50, 120).")
    print("Ejemplo: Ana,100,rojo")
    print("Escriba 'FIN' para cerrar las inscripciones e iniciar la carrera.")
    print("-" * 40)

    contador_apuestas = 0
    try:
        with open(archivo_apuestas, 'a', encoding='utf-8') as f:
            while True:
                entrada = input("Nueva apuesta > ")
                entrada_limpia = entrada.strip()
                
                if entrada_limpia.lower() == 'fin':
                    print("...Inscripciones cerradas.")
                    break

                partes = entrada_limpia.split(',')
                apuesta_validada = validar_apuesta(partes)
                
                if apuesta_validada:
                    f.write(apuesta_validada)
                    f.flush() 
                    print(f"   Apuesta registrada: {apuesta_validada.strip()}")
                    contador_apuestas += 1
                else:
                    print("   Intente de nuevo.")

    except Exception as e:
        print(f"\nError fatal al escribir en '{archivo_apuestas}': {e}")
        sys.exit(1)

    print("-" * 40)
    if contador_apuestas > 0:
        print(f"Se registraron {contador_apuestas} apuestas.")
    else:
        print("No se registraron nuevas apuestas.")
    
    print("Llamando a 'carrera.py' para iniciar la carrera...")
    print("=" * 40 + "\n")

    os.system("py carrera.py")

if __name__ == "__main__":
    iniciar_inscripciones()