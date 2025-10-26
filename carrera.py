import os
import time
import sys
import subprocess

class Apuesta:
    def __init__(self, nombre_apostador, monto, color_caballo):
        self.nombre_apostador = nombre_apostador
        self.monto = int(monto)
        self.color_caballo = color_caballo

    def __repr__(self):
        return f"[Apuesta: {self.nombre_apostador} apostó {self.monto} a '{self.color_caballo}']"

class Caballo:
    def __init__(self, color):
        self.color = color
        self.total_apostado = 0
        self.apostadores = [] 

    def agregar_apuesta(self, apuesta):
        self.total_apostado += apuesta.monto
        self.apostadores.append(apuesta)

class Carrera:
    def __init__(self, colores_caballos, archivo_apuestas, pozo_acumulado_previo): 
        self.caballos = {color: Caballo(color) for color in colores_caballos}
        self.pozo_total = 0
        
        self.archivo_apuestas = archivo_apuestas
        self.archivo_ganador = "ganador.txt"
        self.archivo_pagos = "pagos.txt"
        self.archivo_pozo_acumulado = "pozo_acumulado.txt" 
        
        self.monto_acumulado = pozo_acumulado_previo 
        self.payout_ratios = {}


    def procesar_apuesta(self, apuesta):
        if apuesta.color_caballo in self.caballos:
            caballo_obj = self.caballos[apuesta.color_caballo]
            caballo_obj.agregar_apuesta(apuesta)
            self.pozo_total += apuesta.monto
            print(f"Apuesta procesada: {apuesta.monto} a {apuesta.color_caballo}")
        else:
            print(f"Advertencia: Apuesta para caballo '{apuesta.color_caballo}' inválido. Descartada.")

    def calcular_ratios_pago(self):
        pozo_efectivo = self.pozo_total + self.monto_acumulado

        if pozo_efectivo == 0:
            print("No hay apuestas y no hay pozo acumulado.")
            return

        print("\n--- Ratios de Pago ---")
        print(f"Pozo de apuestas actual: {self.pozo_total}")
        print(f"Pozo acumulado (bonus): {self.monto_acumulado}")
        print(f"POZO TOTAL EFECTIVO: {pozo_efectivo}")
        print("-" * 26)
        
        for color, caballo in self.caballos.items():
            if caballo.total_apostado > 0:
                ratio = pozo_efectivo / caballo.total_apostado
                self.payout_ratios[color] = ratio
                print(f"Caballo '{color}': {ratio:.2f} (Paga {ratio:.2f} por cada 1 apostado)")
            else:
                self.payout_ratios[color] = 0
                print(f"Caballo '{color}': Sin apuestas")

    def iniciar_monitoreo(self):
        print("\n" + "="*30)
        print(f"MONITOREANDO '{self.archivo_ganador}'...")
        print("La carrera está en curso. Esperando al ganador.")
        print("="*30)

        ganador = None
        while not ganador:
            if not esta_vacio(self.archivo_ganador):
                try:
                    with open(self.archivo_ganador, 'r') as f:
                        ganador = f.readline().strip()
                except Exception as e:
                    print(f"Error al leer el archivo ganador: {e}")
                    ganador = None 
            
            if not ganador:
                time.sleep(0.5)
        
        print(f"\n¡CARRERA TERMINADA! El ganador es: {ganador}")
        self.finalizar_carrera(ganador)

    def finalizar_carrera(self, color_ganador):
        if color_ganador not in self.caballos:
            print(f"Error: El ganador '{color_ganador}' no es un caballo válido.")
            resetear_archivo(self.archivo_ganador)
            return

        caballo_ganador = self.caballos[color_ganador]
        ratio_pago = self.payout_ratios.get(color_ganador, 0)
        pozo_efectivo = self.pozo_total + self.monto_acumulado

        print("\n--- RESULTADOS FINALES ---")
        print(f"Caballo Ganador: {caballo_ganador.color}")
        print(f"Pozo Total Efectivo: {pozo_efectivo}")
        print(f"Total Apostado al Ganador: {caballo_ganador.total_apostado}")
        
        if caballo_ganador.total_apostado > 0:
            print(f"Ratio de Pago: {ratio_pago:.2f}x")
        else:
            print("Nadie apostó por este caballo.")

        try:
            with open(self.archivo_pagos, 'w', encoding='utf-8') as f:
                f.write(f"Resultados de la Carrera - Ganador: {color_ganador}\n")
                f.write(f"Pozo de Apuestas: {self.pozo_total}\n")
                f.write(f"Pozo Acumulado (Bonus): {self.monto_acumulado}\n")
                f.write(f"POZO TOTAL REPARTIDO: {pozo_efectivo}\n")
                
                if caballo_ganador.total_apostado > 0:
                    f.write(f"Ratio de Pago: {ratio_pago:.2f}\n")
                    
                f.write("="*20 + "\n")
                f.write("Apostadores Ganadores y Pagos:\n")

                if not caballo_ganador.apostadores:
                    f.write("Nadie apostó por este caballo.\n")
                    
                    nuevo_pozo_acumulado = pozo_efectivo
                    guardar_pozo_acumulado(self.archivo_pozo_acumulado, nuevo_pozo_acumulado)
                    
                    f.write(f"El pozo total de {nuevo_pozo_acumulado} SE ACUMULA para la siguiente carrera.\n")
                
                else:
                    ganancias_casa_redondeo = 0
                    for apuesta in caballo_ganador.apostadores:
                        
                        pago_truncado = (apuesta.monto * ratio_pago) // 1
                        pago_final = (pago_truncado // 10) * 10
                        ganancias_casa_redondeo += (pago_truncado - pago_final)
                        
                        f.write(f"- {apuesta.nombre_apostador}: Recibe {pago_final} (Apostó {apuesta.monto})\n")
                    
                    f.write("\n" + "="*20 + "\n")
                    f.write(f"La casa gana {ganancias_casa_redondeo} adicionales por redondeo.\n")

                    guardar_pozo_acumulado(self.archivo_pozo_acumulado, 0)
                    f.write("El pozo acumulado ha sido pagado y reseteado a 0.\n")
                

            print(f"\nArchivo de pagos '{self.archivo_pagos}' generado exitosamente.")
            
            abrir_archivo(self.archivo_pagos)
            
        except Exception as e:
            print(f"Error al escribir el archivo de pagos: {e}")

        print(f"\nLimpiando '{self.archivo_ganador}'...")
        resetear_archivo(self.archivo_ganador)
        
        print(f"Limpiando '{self.archivo_apuestas}'...") 
        resetear_archivo(self.archivo_apuestas)


def leer_pozo_acumulado(nombre_archivo):
    """Lee el pozo acumulado. Devuelve 0 si hay error."""
    try:
        with open(nombre_archivo, 'r') as f:
            monto_str = f.readline().strip()
            return float(monto_str)
    except (FileNotFoundError, ValueError, TypeError):
        return 0 

def guardar_pozo_acumulado(nombre_archivo, monto):
    try:
        with open(nombre_archivo, 'w') as f:
            f.write(f"{monto}")
        print(f"Pozo acumulado actualizado a: {monto}")
    except Exception as e:
        print(f"Error al guardar pozo acumulado: {e}")

def abrir_archivo(filepath):
    print(f"Abriendo '{filepath}' para revisión...")
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
    except Exception as e:
        print(f"Error al intentar abrir el archivo: {e}")

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
    print(f"Caballos cargados para la carrera: {', '.join(colores)}")
    return colores

def leer_apuestas(nombre_archivo):
    lista_apuestas = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            for i, linea in enumerate(f):
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(',')
                if len(partes) == 3:
                    try:
                        nombre, monto, color = partes[0].strip(), int(partes[1].strip()), partes[2].strip().lower()
                        lista_apuestas.append(Apuesta(nombre, monto, color))
                    except ValueError:
                        print(f"Error en línea {i+1} de {nombre_archivo}: El monto '{partes[1]}' no es un número.")
                else:
                    print(f"Error en línea {i+1} de {nombre_archivo}: Formato incorrecto.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'. Creando uno vacío.")
        open(nombre_archivo, 'w').close()
    return lista_apuestas

def resetear_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'w') as f:
            pass 
        print(f"Archivo '{nombre_archivo}' reseteado.")
    except Exception as e:
        print(f"Error al resetear '{nombre_archivo}': {e}")

def esta_vacio(nombre_archivo):
    try:
        return os.path.getsize(nombre_archivo) == 0
    except FileNotFoundError:
        return True
    #return False


def main():
    CABALLOS_FILE = "caballos.txt"
    COLORES_CABALLOS = leer_caballos(CABALLOS_FILE)
    
    APUESTAS_FILE = "apuestas.txt"
    GANADOR_FILE = "ganador.txt"
    PAGOS_FILE = "pagos.txt"
    POZO_FILE = "pozo_acumulado.txt"

    print("Iniciando sistema de apuestas...")
    resetear_archivo(GANADOR_FILE)
    resetear_archivo(PAGOS_FILE)
    
    pozo_previo = leer_pozo_acumulado(POZO_FILE)
    if pozo_previo > 0:
        print(f"¡Se ha cargado un pozo acumulado (bonus) de {pozo_previo:.2f}!")

    carrera_actual = Carrera(COLORES_CABALLOS, APUESTAS_FILE, pozo_previo) 

    print(f"\nLeyendo apuestas de '{APUESTAS_FILE}'...")
    lista_de_apuestas = leer_apuestas(APUESTAS_FILE)
    if not lista_de_apuestas:
        print("No se encontraron apuestas en 'apuestas.txt'.")
    
    for apuesta in lista_de_apuestas:
        carrera_actual.procesar_apuesta(apuesta)

    carrera_actual.calcular_ratios_pago()
    carrera_actual.iniciar_monitoreo()

    print("\nSimulación finalizada. El sistema está listo para la próxima carrera.")

if __name__ == "__main__":
    main()