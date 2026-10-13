from __future__ import annotations

import csv
import random
import sys
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

MEDIDAS = ["largo_sep", "ancho_sep", "largo_pet", "ancho_pet"]


class DatosInvalidosError(Exception):
    """El fichero de entrada no tiene el formato esperado."""


# --------------------------------------------------------------------- datos
@dataclass
class Muestra:
    """Una observación del conjunto: sus medidas y su clase real."""

    medidas: list[float]
    clase: str

    @classmethod
    def desde_fila(cls, fila: dict[str, str]) -> "Muestra":
        faltan = set(MEDIDAS + ["clase"]) - set(fila)
        if faltan:
            raise DatosInvalidosError(f"Faltan columnas: {sorted(faltan)}")
        try:
            medidas = [float(fila[c]) for c in MEDIDAS]
        except ValueError as e:
            raise DatosInvalidosError(f"Medida no numérica: {e}") from e
        return cls(medidas, fila["clase"])

    def __len__(self) -> int:
        return len(self.medidas)


@dataclass
class Dataset:
    """Colección de muestras con las operaciones habituales."""

    muestras: list[Muestra] = field(default_factory=list)

    @classmethod
    def desde_csv(cls, ruta: Path | str) -> "Dataset":
        ruta = Path(ruta)
        if not ruta.exists():
            raise FileNotFoundError(f"No existe el fichero {ruta}")
        with open(ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        if not filas:
            raise DatosInvalidosError("El fichero no contiene datos")
        return cls([Muestra.desde_fila(fila) for fila in filas])

    def __len__(self) -> int:
        return len(self.muestras)

    def __iter__(self):
        return iter(self.muestras)

    def __getitem__(self, i):
        return self.muestras[i]

    @property
    def clases(self) -> list[str]:
        return sorted({m.clase for m in self.muestras})

    def dividir(self, proporcion: float = 0.8, semilla: int = 42):
        """Baraja y parte en entrenamiento y prueba de forma reproducible."""
        ...
        random.Random(semilla).shuffle(muestras) # Esta línea baraja la lista de muestras        ...
        ...

    def rangos(self) -> list[tuple[float, float]]:
        """Mínimo y máximo de cada característica."""
        ...

    def normalizar(self, rangos: list[tuple[float, float]]) -> "Dataset":
        """Escala cada característica al rango 0-1 con los rangos dados."""
        ...

    def resumen_por_clase(self) -> dict[str, dict[str, float]]:
        """Estadísticas básicas por clase (reutiliza el proyecto 1)."""
        resumen = {}
        for clase in self.clases:
            valores = [m.medidas[2] for m in self if m.clase == clase]
            resumen[clase] = {
                "n": len(valores),
                "media": sum(valores) / len(valores),
                "min": min(valores),
                "max": max(valores),
            }
        return resumen


# -------------------------------------------------------------------- modelos
class Modelo(ABC):
    """Contrato que cumple cualquier clasificador del proyecto."""

    nombre = "modelo"

    @abstractmethod
    def entrenar(self, datos: Dataset) -> "Modelo": ...

    @abstractmethod
    def predecir(self, muestras) -> list[str]: ...

    def evaluar(self, datos: Dataset) -> float:
        predicciones = self.predecir(datos)
        aciertos = sum(p == m.clase for p, m in zip(predicciones, datos))
        return aciertos / len(datos)

    def __str__(self) -> str:
        return self.nombre


class ModeloMayoritario(Modelo):
    """Referencia mínima: siempre predice la clase más frecuente."""

    nombre = "Clase mayoritaria"

    def __init__(self) -> None:
        self._clase: str | None = None

    def entrenar(self, datos: Dataset) -> "ModeloMayoritario":
        self._clase = Counter(m.clase for m in datos).most_common(1)[0][0]
        return self

    def predecir(self, muestras) -> list[str]:
        if self._clase is None:
            raise RuntimeError("El modelo no está entrenado")
        return [self._clase for _ in muestras]


class ClasificadorKNN(Modelo):
    """k vecinos más cercanos con distancia euclídea y voto mayoritario."""

    def __init__(self, k: int = 3) -> None:
        self.k = k
        self.nombre = f"k-NN (k={k})"
        self._entrenamiento: Dataset | None = None

    def entrenar(self, datos: Dataset) -> "ClasificadorKNN":
        if len(datos) < self.k:
            raise ValueError("Hay menos muestras de entrenamiento que k")
        self._entrenamiento = datos
        return self

    @staticmethod
    def distancia(a: list[float], b: list[float]) -> float:
        ...

    def _votar(self, muestra: Muestra) -> str:
        vecinos = sorted(
            self._entrenamiento,
            key=lambda m: self.distancia(muestra.medidas, m.medidas),
        )[: self.k]
        ...

    def predecir(self, muestras) -> list[str]:
        if self._entrenamiento is None:
            raise RuntimeError("El modelo no está entrenado")
        return [self._votar(m) for m in muestras]

