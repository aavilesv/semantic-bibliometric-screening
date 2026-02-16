# =========================================================
# core/io_utils.py
# Lectura y validación del archivo de entrada
# =========================================================

import pandas as pd              # Librería para manejo de datos
from pathlib import Path         # Manejo robusto de rutas
from config import TEXT_COLS     # Columnas necesarias definidas en config


def read_input(path: str) -> pd.DataFrame:
    """
    Lee un archivo CSV o Excel y devuelve un DataFrame limpio.
    También valida que existan las columnas necesarias.
    """

    # Convertimos la ruta a objeto Path para manejo seguro
    path = Path(path)

    # Verificamos que el archivo exista
    if not path.exists():
        raise FileNotFoundError(f"❌ El archivo no existe: {path}")

    # Detectamos la extensión del archivo
    ext = path.suffix.lower()

    # =========================
    # LECTURA DEL ARCHIVO
    # =========================

    # Si es CSV
    if ext == ".csv":
        df = pd.read_csv(path, dtype=str)

    # Si es Excel
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(path, dtype=str)

    # Si el formato no es válido
    else:
        raise ValueError("❌ Formato no soportado. Use CSV o Excel.")

    # =========================
    # LIMPIEZA DE NULOS
    # =========================

    # Reemplaza valores NaN por cadenas vacías
    df = df.fillna("")

    # =========================
    # VALIDACIÓN DE COLUMNAS
    # =========================

    # Verifica que existan las columnas necesarias
    missing_cols = [col for col in TEXT_COLS if col not in df.columns]

    # Si falta alguna columna, se detiene el sistema
    if missing_cols:
        raise ValueError(
            f"❌ Faltan columnas obligatorias en el dataset: {missing_cols}"
        )

    # =========================
    # REPORTE DE CARGA
    # =========================

    print(f"📂 Archivo cargado correctamente: {path}")
    print(f"📊 Total de registros leídos: {len(df)}")

    # Devuelve el DataFrame listo para procesar
    return df
