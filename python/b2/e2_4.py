texto="Podrías haber escrito el código con cualquier otro nombre de variable y funcionaría exactamente igual. Por ejemplo, esto hace exactamente lo mismo"

SIGNOS = ".,:;!?¡¿()\"'"

def contar_palabras(texto: str) -> dict[str, int]:
    limpio = texto.lower()

    for s in SIGNOS:
        limpio = limpio.replace(s, " ") # quitar puntuación
    # antes de separar

    conteo: dict[str, int]={}

