# =========================================================
# core/text_builder.py
# Construcción del texto semántico académico ponderado
# =========================================================

def merge_keywords(row):
    """
    Fusiona Author Keywords e Index Keywords sin duplicados.
    Respeta meticulosamente los N-gramas (términos compuestos) 
    separando correctamente mediante punto y coma (';').
    """
    ak_raw = str(row.get("Author Keywords", "")).split(";")
    ik_raw = str(row.get("Index Keywords", "")).split(";")
    
    # Limpiamos espacios alrededor de las expresiones compuestas
    ak = [k.lower().strip() for k in ak_raw if k.strip()]
    ik = [k.lower().strip() for k in ik_raw if k.strip()]
    
    seen = set()
    merged = []
    # Fusionamos evitando repetir el mismo concepto compuesto
    for word in (ak + ik):
        if word not in seen:
            seen.add(word)
            merged.append(word)
            
    return "; ".join(merged)

def build_semantic_text(df, text_cols):
    """
    Construye la columna 'text_semantic' dando mayor prioridad
    y prominencia al Title y Keywords dentro de la cadena concatenada,
    manteniendo al Abstract como soporte contextual.
    """
    print("🧹 Filtrando metadatos base para afinidad temática...")

    # Rellena NaN solo en las columnas requeridas si existen
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    # Generamos la super-columna preservando semántica estricta
    df["bothkeywords"] = df.apply(merge_keywords, axis=1)

    # Marcamos registros válidos base
    df["isValid"] = (df.get("Title", "").str.strip() != "") & (df.get("Abstract", "").str.strip() != "")
    
    invalid_text_count = (~df["isValid"]).sum()
    print(f"📉 Documentos omitidos del ranking (Sin título/abstract): {invalid_text_count}")

    print("🧠 Construyendo texto semántico con ponderación posicional...")
    
    def construct_weighted_text(row):
        title = str(row.get("Title", "")).strip()
        keywords = str(row.get("bothkeywords", "")).strip()
        abstract = str(row.get("Abstract", "")).strip()
        
        # Ponderación intra-texto:
        # Se estructuran los campos de modo que Title y Keywords dominen 
        # el inicio (mayor atención bidireccional SBERT) e indicando su naturaleza clave.
        return f"Research Focus: {title}. Core Keywords: {keywords}. Contextual Abstract: {abstract}"

    df["text_semantic"] = df.apply(construct_weighted_text, axis=1)

    # Marcar los inviables residuales
    short_text_mask = df["text_semantic"].str.len() <= 50
    df.loc[short_text_mask, "isValid"] = False
    
    print(f"✅ Textos armados con jerarquía semántica: {df['isValid'].sum()} válidos.")

    # Protegemos al pipe de inferencias fantasma
    df.loc[~df["isValid"], "text_semantic"] = "INVALID_EMPTY_DOCUMENT"

    return df
