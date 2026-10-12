"""Descarga el dataset CDC Diabetes Health Indicators (versión de 3 clases).

El archivo ya viene incluido en data/raw/, así que este script solo hace falta
si se borró o se quiere volver a obtener desde la fuente.

Requiere la CLI de Kaggle con credenciales configuradas
(~/.kaggle/kaggle.json o ~/.kaggle/credentials.json).
Ver: https://www.kaggle.com/docs/api

Uso (desde la raíz del repositorio):
    python scripts/descargar_datos.py
"""

import hashlib
import subprocess
import sys
from pathlib import Path

DATASET_KAGGLE = "alexteboul/diabetes-health-indicators-dataset"
ARCHIVO = "diabetes_012_health_indicators_BRFSS2015.csv"
SHA256_ESPERADO = "463b5430e1cea3c518227f3179317f2e3c9ccd4f76fb7e7ea125bf87305aee98"

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "data" / "raw"


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    ruta_zip = DESTINO / f"{ARCHIVO}.zip"

    if ruta_zip.exists():
        print(f"Ya existe: {ruta_zip}")
    else:
        comando = ["kaggle", "datasets", "download", DATASET_KAGGLE,
                   "-f", ARCHIVO, "-p", str(DESTINO)]
        try:
            subprocess.run(comando, check=True)
        except FileNotFoundError:
            sys.exit("No se encontró la CLI de Kaggle. Instalar con: pip install kaggle")
        except subprocess.CalledProcessError:
            sys.exit("Falló la descarga. Revisar las credenciales de Kaggle.")

    huella = sha256(ruta_zip)
    if huella == SHA256_ESPERADO:
        print("SHA-256 verificado: el archivo coincide con el usado en el proyecto.")
    else:
        print(f"Advertencia: el SHA-256 ({huella}) no coincide con el esperado. "
              "Kaggle pudo haber publicado una versión distinta del archivo.")


if __name__ == "__main__":
    main()
