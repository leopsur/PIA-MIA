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

    def dividir(
        self, proporcion: float = 0.8, semilla: int = 42
    ) -> tuple["Dataset", "Dataset"]:
        """Baraja y parte en entrenamiento y prueba de forma reproducible."""
        muestras = list(self.muestras)
        random.Random(semilla).shuffle(muestras)
        corte = int(len(muestras) * proporcion)
        return Dataset(muestras[:corte]), Dataset(muestras[corte:])

    def rangos(self) -> list[tuple[float, float]]:
        """Mínimo y máximo de cada característica."""
        if not self.muestras:
            return []
        # Agrupa las medidas por columna/característica
        columnas = zip(*(m.medidas for m in self.muestras))
        return [(min(col), max(col)) for col in columnas]

    def normalizar(self, rangos: list[tuple[float, float]]) -> "Dataset":
        """Escala cada característica al rango 0-1 con los rangos dados."""
        muestras_norm = []
        for m in self.muestras:
            medidas_norm = [
                (x - r_min) / (r_max - r_min) if r_max != r_min else 0.0
                for x, (r_min, r_max) in zip(m.medidas, rangos)
            ]
            muestras_norm.append(Muestra(medidas_norm, m.clase))
        return Dataset(muestras_norm)

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
        """Calcula la distancia euclídea entre dos puntos N-dimensionales."""
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

    def _votar(self, muestra: Muestra) -> str:
        """Encuentra los k vecinos más cercanos y retorna la clase mayoritaria."""
        vecinos = sorted(
            self._entrenamiento,
            key=lambda m: self.distancia(muestra.medidas, m.medidas),
        )[: self.k]
        votos = Counter(m.clase for m in vecinos)
        return votos.most_common(1)[0][0]

    def predecir(self, muestras) -> list[str]:
        if self._entrenamiento is None:
            raise RuntimeError("El modelo no está entrenado")
        return [self._votar(m) for m in muestras]


#PROBAREMOS

if __name__ == "__main__":
    from pathlib import Path

    # 1. Crear un fichero CSV de prueba en disco
    contenido_csv = """largo_sep,ancho_sep,largo_pet,ancho_pet,clase
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
7.0,3.2,4.7,1.4,versicolor
6.4,3.2,4.5,1.5,versicolor
6.9,3.1,4.9,1.5,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
"""
    ruta_csv = Path("iris_prueba.csv")
    ruta_csv.write_text(contenido_csv, encoding="utf-8")

    try:
        # 2. Cargar el dataset
        ds = Dataset.desde_csv(ruta_csv)
        print(f"Muestras cargadas: {len(ds)}")
        print(f"Clases detectadas: {ds.clases}\n")

        # 3. Dividir en entrenamiento (70%) y prueba (30%)
        train, test = ds.dividir(proporcion=0.7, semilla=42)
        print(f"Entrenamiento: {len(train)} muestras | Prueba: {len(test)} muestras\n")

        # 4. Normalizar los datos empleando los rangos del conjunto de entrenamiento
        rangos = train.rangos()
        train_norm = train.normalizar(rangos)
        test_norm = test.normalizar(rangos)

        # 5. Probar el Modelo Mayoritario
        m_mayoritario = ModeloMayoritario().entrenar(train_norm)
        acc_mayoritario = m_mayoritario.evaluar(test_norm)
        print(f"[{m_mayoritario}] Precisión: {acc_mayoritario * 100:.1f}%")

        # 6. Probar el Clasificador k-NN
        knn = ClasificadorKNN(k=3).entrenar(train_norm)
        acc_knn = knn.evaluar(test_norm)
        print(f"[{knn}] Precisión: {acc_knn * 100:.1f}%")

    finally:
        # Limpiar el fichero temporal
        if ruta_csv.exists():
            ruta_csv.unlink()