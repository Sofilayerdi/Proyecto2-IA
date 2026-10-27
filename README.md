# Clasificación de diabetes con indicadores de salud del CDC

Proyecto 2, Inteligencia Artificial, UVG.

Clasificamos a una persona en **sin diabetes, prediabetes o diabetes** (`Diabetes_012`) a partir de 21 indicadores de salud, hábitos y variables sociodemográficas de la encuesta BRFSS 2015 del CDC. La métrica principal es el **F1-score macro**.

**Resultado:** el mejor modelo es un random forest, con F1 macro de 0.438 en el conjunto de prueba (el baseline trivial obtiene 0.305). Detecta al 70% de las personas con diabetes, pero casi no detecta prediabetes.

## Entregables

| Archivo | Qué contiene |
|---|---|
| `Informe-Proyecto2.docx` | Informe final: problema, objetivos, datos, análisis exploratorio, decisiones de preprocesamiento, comparación de modelos, evaluación en prueba, análisis de errores, limitaciones, conclusiones, uso de IA y referencias. |
| `Presentacion-Proyecto2.pptx` | Presentación de 13 diapositivas; cada una tiene notas del orador con datos de apoyo. |
| `notebooks/01_EDA.ipynb` | Diccionario de variables, análisis exploratorio (desbalance, outliers, correlaciones, factores de riesgo), decisiones de preprocesamiento y creación de la partición train/test. |
| `notebooks/02_Baselines_Arbol.ipynb` | Baseline trivial, regresión logística y árbol de decisión con búsqueda de hiperparámetros, análisis de sobreajuste del árbol por profundidad e importancia de variables. |
| `notebooks/03_Modelos_Evaluacion.ipynb` | Random forest y gradient boosting con búsqueda de hiperparámetros, comparación de los cinco modelos, evaluación única en el conjunto de prueba, análisis de errores con ejemplos, desempeño por subgrupos, importancia por permutación, conclusiones y limitaciones. |
| `resultados/` | Hiperparámetros y métricas de validación cruzada (`*_integrante1` sale de `02_Baselines_Arbol.ipynb` y `*_integrante2` de `03_Modelos_Evaluacion.ipynb`) y las figuras del informe en `figuras/`. |
| `data/` | Dataset original comprimido (`raw/`) y la partición compartida (`processed/particion.csv`). |
| `scripts/descargar_datos.py` | Vuelve a descargar el dataset desde Kaggle y verifica su huella SHA-256. |

## Dataset

| | |
|---|---|
| Nombre | CDC Diabetes Health Indicators (BRFSS 2015) |
| Referencia | [UCI ML Repository #891](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators), DOI 10.24432/C53919, CC BY 4.0 |
| Archivo usado | `diabetes_012_health_indicators_BRFSS2015.csv` de [Kaggle (Alex Teboul)](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset), CC0 1.0 |
| Fecha de obtención | 26 de octubre de 2026 |
| Tamaño | 253,680 filas × 22 columnas |

Usamos el archivo de Kaggle porque el CSV de UCI solo trae la etiqueta binaria y agrupa la prediabetes con "sin diabetes". Las 21 predictoras son idénticas en ambas fuentes (verificado al comparar ambos archivos).

El archivo ya viene comprimido en `data/raw/`; no hace falta descargarlo. Para volver a obtenerlo desde Kaggle (requiere credenciales de la API de Kaggle):

```bash
python scripts/descargar_datos.py
```

## Estructura

```
├── data/
│   ├── raw/          # dataset original (.csv.zip)
│   └── processed/    # particion.csv: división train/test compartida por todo el grupo
├── notebooks/
│   ├── 01_EDA.ipynb                 # documentación del dataset y análisis exploratorio
│   ├── 02_Baselines_Arbol.ipynb     # baseline trivial, regresión logística y árbol de decisión
│   └── 03_Modelos_Evaluacion.ipynb  # random forest, gradient boosting, evaluación final en test y análisis de errores
├── resultados/       # mejores hiperparámetros y tabla de métricas de cada integrante
│   └── figuras/      # gráficas de 03_Modelos_Evaluacion.ipynb usadas en el informe
├── scripts/
│   └── descargar_datos.py
├── Informe-Proyecto2.docx       # informe final
├── Presentacion-Proyecto2.pptx  # presentación
└── requirements.txt
```

## Cómo correrlo

Probado con Python 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Ejecutar los notebooks en este orden, con *Run All* y el kernel de `.venv`:

1. `01_EDA.ipynb`: crea la partición (menos de 1 minuto).
2. `02_Baselines_Arbol.ipynb`: baselines y árbol de decisión (unos 3 minutos).
3. `03_Modelos_Evaluacion.ipynb`: random forest, gradient boosting, evaluación final en el conjunto de prueba y análisis de errores (unos 3 minutos).

Funcionan abriéndolos desde la raíz del repo o desde `notebooks/`. También se pueden correr sin abrir Jupyter:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_EDA.ipynb notebooks/02_Baselines_Arbol.ipynb notebooks/03_Modelos_Evaluacion.ipynb
```

## Partición compartida

`01_EDA.ipynb` genera `data/processed/particion.csv` (80% train / 20% test, estratificado, `random_state=42`). **Todos los notebooks deben usar esta partición** para que los modelos sean comparables y el test se use una sola vez al final:

```python
particion = pd.read_csv(RAIZ / "data" / "processed" / "particion.csv", index_col="indice")["conjunto"]
train = df.loc[particion == "train"]
test = df.loc[particion == "test"]
```

La validación y la búsqueda de hiperparámetros se hacen con validación cruzada estratificada de 5 particiones sobre `train`.
