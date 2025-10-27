import sys

def leer_pozo_acumulado(nombre_archivo):
    try:
        # Existe el pozo
        with open(nombre_archivo, 'r') as f:
            monto_str = f.readline().strip()
            return float(monto_str)
    except (FileNotFoundError, ValueError, TypeError):
        # Para cualquier otro caso diremos que es 0
        return 0 


def leer_caballos(nombre_archivo):
    colores = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                color = linea.strip().lower() 
                if color: 
                    colores.append(color)
    except FileNotFoundError:
        print(f"¡ERROR! No se encontró el archivo de caballos: '{nombre_archivo}'")
        sys.exit(1)
    if not colores:
        print(f"¡ERROR! El archivo '{nombre_archivo}' está vacío.")
        sys.exit(1)
    return colores


def mostrar_informacion():
    CABALLOS_FILE = "caballos.txt"
    APUESTAS_FILE = "apuestas.txt"
    POZO_FILE = "pozo_acumulado.txt"

    print("\n" + "="*40)
    print("--- INFORMACIÓN ACTUAL DE LA CARRERA ---")
    print("="*40)

    pozo_acumulado = leer_pozo_acumulado(POZO_FILE)
    if pozo_acumulado > 0:
        print(f"\n Pozo Acumulado (Bonus): ${pozo_acumulado}")

    try:
        lista_caballos = leer_caballos(CABALLOS_FILE)
    except SystemExit as e:
        print(e)
        return

    total_apostado_actual = 0
    apostadores_por_caballo = {color: [] for color in lista_caballos}
    apuestas_invalidas = 0

    try:
        with open(APUESTAS_FILE, 'r', encoding='utf-8') as f:
            for i, linea in enumerate(f):
                linea = linea.strip()
                if not linea:
                    continue
                
                partes = linea.split(',')
                
                if len(partes) == 3:
                    try:
                        nombre = partes[0].strip()
                        monto = int(partes[1].strip())
                        color = partes[2].strip().lower()

                        if color in apostadores_por_caballo:
                            total_apostado_actual += monto
                            apostadores_por_caballo[color].append(nombre)
                        else:
                            apuestas_invalidas += 1
                    
                    except (ValueError, IndexError):
                        print(f"Advertencia: Línea {i+1} en '{APUESTAS_FILE}' tiene formato inválido.")
                else:
                    print(f"Advertencia: Línea {i+1} en '{APUESTAS_FILE}' tiene formato inválido.")

    except FileNotFoundError:
        print(f"\nNo se ha encontrado '{APUESTAS_FILE}'. Se asume $0 apostado.")
    
    print(f"\nTotal Actual Apostado: ${total_apostado_actual}")
    if pozo_acumulado > 0:
        total_efectivo = total_apostado_actual + pozo_acumulado
        print(f"POZO TOTAL EFECTIVO: ${total_efectivo}")

    print("\n" + "-"*40)
    print("--- CABALLOS INSCRITOS Y APOSTADORES ---")
    print("="*40)

    for color, lista_nombres in apostadores_por_caballo.items():
        print(f"\nCaballo: {color.capitalize()}")
        
        if lista_nombres:
            for nombre in lista_nombres:
                print(f"  - {nombre}")
        else:
            print("  (Sin apuestas)")
    
    if apuestas_invalidas > 0:
        print("\n" + "-"*40)
        print(f"Aviso: Se descartaron {apuestas_invalidas} apuestas a caballos no inscritos.")

    print("\n" + "="*40)


if __name__ == "__main__":
    mostrar_informacion()