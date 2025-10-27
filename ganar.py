import sys


def declarar_ganador():
    color_ganador = sys.argv[1].lower() 
    archivo_nombre = "ganador.txt"

    with open(archivo_nombre, 'w', encoding='utf-8') as f:
            f.write(color_ganador)


if __name__ == "__main__":
    declarar_ganador()