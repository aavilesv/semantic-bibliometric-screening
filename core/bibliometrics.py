# =========================================================
# core/bibliometrics.py
# Cálculos bibliométricos y detección de artículos seminales
# =========================================================

import pandas as pd
from datetime import datetime


def compute_citations_per_year(df):
    """
    Calcula las citas por año para cada artículo.
    Esto evita sesgos hacia artículos antiguos.
    """

    print("📊 Calculando citas por año...")

    # Año actual
    current_year = datetime.now().year

    # Convertir columnas a valores numéricos
    # Si hay errores, se convierten a 0
    df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(current_year)

    # Fórmula de citas por año
    df["CitasPorAño"] = df["Cited by"] / (current_year - df["Year"] + 1)

    print("✅ Citas por año calculadas.")

    return df


def detect_seminal(df):
    """
    Detecta artículos seminales basándose en:
    - Percentil alto de citas por año
    """

    print("🏛️ Detectando artículos seminales...")

    # Si no existe la columna, se calcula primero
    if "CitasPorAño" not in df.columns:
        df = compute_citations_per_year(df)

    # Percentil 90 de citas por año
    threshold = df["CitasPorAño"].quantile(0.90)

    # Marcar artículos seminales
    df["EsSeminal"] = df["CitasPorAño"] >= threshold

    print(f"📌 Umbral de seminalidad: {round(threshold, 2)} citas/año")
    print(f"⭐ Artículos seminales detectados: {df['EsSeminal'].sum()}")

    return df
