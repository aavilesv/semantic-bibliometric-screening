# =========================================================
# core/text_builder.py
# Construcción del texto semántico académico
# =========================================================

def clean_keywords(text):
    """
    Convierte keywords separadas por ';' en texto normal y asegura minúsculas.
    """
    if not isinstance(text, str):
        return ""
    return text.lower().replace(";", " ").strip()

def merge_keywords(row):
    """
    Fusiona Author Keywords e Index Keywords sin duplicados.
    """
    ak = str(row.get("Author Keywords", "")).split()
    ik = str(row.get("Index Keywords", "")).split()
    
    seen = set()
    merged = []
    for word in (ak + ik):
        if word not in seen:
            seen.add(word)
            merged.append(word)
            
    return " ".join(merged)

def build_semantic_text(df, text_cols):
    """
    Construye la columna 'text_semantic'.
    Maneja validaciones lógicas de texto faltante y keywords.
    """
    print("🧹 Limpiando y planificando columnas de texto...")

    # Rellena NaN solo en las columnas que existan (las faltantes ya saltaron en io_utils)
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    df["Author Keywords"] = df.get("Author Keywords", "").apply(clean_keywords)
    df["Index Keywords"] = df.get("Index Keywords", "").apply(clean_keywords)

    df["bothkeywords"] = df.apply(merge_keywords, axis=1)

    df["isValid"] = (df.get("Title", "").str.strip() != "") & (df.get("Abstract", "").str.strip() != "")
    
    invalid_text_count = (~df["isValid"]).sum()
    print(f"📉 Artículos marcados como inválidos (Sin título/abstract): {invalid_text_count}")

    print("🧠 Construyendo texto semántico...")
    df["text_semantic"] = df[text_cols].agg(" ".join, axis=1)

    short_text_mask = df["text_semantic"].str.len() <= 50
    df.loc[short_text_mask, "isValid"] = False
    
    print(f"✅ Textos válidos listos para análisis: {df['isValid'].sum()} registros")

    df.loc[~df["isValid"], "text_semantic"] = "INVALID_EMPTY_DOCUMENT"

    return df
