import os

NOMBRE_ARCHIVO = "highscore.txt"

def cargar_high_score():
    """Lee el high score del archivo. Si no existe, retorna 0."""
    if not os.path.exists(NOMBRE_ARCHIVO):
        return 0
    try:
        with open(NOMBRE_ARCHIVO, "r") as archivo:
            contenido = archivo.read()
            return int(contenido) if contenido else 0
    except (ValueError, IOError):
        return 0

def guardar_high_score(nuevo_score):
    """Guarda el score solo si es mayor al actual."""
    score_actual = cargar_high_score()
    if nuevo_score > score_actual:
        try:
            with open(NOMBRE_ARCHIVO, "w") as archivo:
                archivo.write(str(nuevo_score))
            return True # Retorna True si hubo récord nuevo
        except IOError:
            return False
    return False