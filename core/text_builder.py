# =========================================================
# core/text_builder.py
# Construcción del texto semántico académico
# =========================================================

from config import TEXT_COLS   # Importa las columnas necesarias desde config


def clean_keywords(text):
    """
    Convierte keywords separadas por ';' en texto normal.
    Ejemplo:
    "fintech; financial inclusion" → "fintech financial inclusion"
    """

    # Si el valor no es texto, devuelve cadena vacía
    if not isinstance(text, str):
        return ""

    # Reemplaza ';' por espacio
    return text.replace(";", " ")


def build_semantic_text(df):
    """
    Construye la columna 'text_semantic' unificando:
    Title + Abstract + Author Keywords + Index Keywords
    """

    print("🧹 Limpiando columnas de texto...")

    # =========================
    # LIMPIEZA DE NULOS
    # =========================

    # Asegura que las columnas de texto no tengan NaN
    df[TEXT_COLS] = df[TEXT_COLS].fillna("")

    # =========================
    # LIMPIEZA DE KEYWORDS
    # =========================

    # Limpia separadores en Author Keywords
    df["Author Keywords"] = df["Author Keywords"].apply(clean_keywords)

    # Limpia separadores en Index Keywords
    df["Index Keywords"] = df["Index Keywords"].apply(clean_keywords)

    # =========================
    # FILTRO DE FILAS VACÍAS
    # =========================

    # Guarda el número inicial de filas
    before = len(df)

    # Elimina filas sin título o abstract útil
    df = df[
        (df["Title"].str.strip() != "") &
        (df["Abstract"].str.strip() != "")
    ].copy()

    # Número de filas después del filtro
    after = len(df)

    print(f"📉 Filas eliminadas por falta de título o abstract: {before - after}")

    # =========================
    # CONSTRUCCIÓN DEL TEXTO SEMÁNTICO
    # =========================

    print("🧠 Construyendo texto semántico...")

    # Une todas las columnas de texto en una sola
    df["text_semantic"] = df[TEXT_COLS].agg(" ".join, axis=1)

    # =========================
    # FILTRO DE TEXTOS CORTOS
    # =========================

    # Guarda el número antes del filtro
    before_len = len(df)

    # Elimina textos demasiado cortos
    df = df[df["text_semantic"].str.len() > 50].copy()

    after_len = len(df)

    print(f"📉 Filas eliminadas por texto corto: {before_len - after_len}")

    print(f"✅ Textos listos para análisis: {len(df)} registros")

    # Devuelve el DataFrame limpio
    return df
