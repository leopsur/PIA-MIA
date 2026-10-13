import sys
from pathlib import Path
 
from knn_base import DatosInvalidosError, Dataset, ModeloMayoritario
 
RUTA_POR_DEFECTO = Path(__file__).parent / "iris.csv"
 
 
def main(ruta: Path) -> None:
    datos = Dataset.desde_csv(ruta)
    print(f"{len(datos)} muestras · clases: {', '.join(datos.clases)}\n")
 
    print("Reparto de muestras por clase:")
    for clase, est in datos.resumen_por_clase().items():
        print(f"  {clase:<14}{est['n']:>3} muestras · "
              f"largo_pet medio {est['media']:.2f}")
 
    # Entrenar y evaluar con el conjunto completo (provisional: ya que luego deberás dividir en entrenamiento y prueba y normalizar los datos antes de realizar el entrenamiento)
    modelo = ModeloMayoritario().entrenar(datos)
    predicciones = modelo.predecir(datos)
 
    print(f"\nModelo: {modelo}")
    print(f"Clase aprendida: {predicciones[0]}")
    print(f"Acierto: {modelo.evaluar(datos):.1%}  "
          f"(sobre los mismos datos del entrenamiento)")
 
    print("\nAcierto por clase:")
    for clase in datos.clases:
        total = sum(1 for m in datos if m.clase == clase)
        bien = sum(1 for m, p in zip(datos, predicciones)
                   if m.clase == clase and p == clase)
        print(f"  {clase:<14}{bien:>4}/{total:<5}{bien / total:>6.0%}")
 
 
if __name__ == "__main__":
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    try:
        main(ruta)
    except (FileNotFoundError, DatosInvalidosError) as e:
        print(f"Error en los datos: {e}")
        sys.exit(1)