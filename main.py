# =========================================================
# main.py
# Orquestador del sistema modular de clasificación
# =========================================================

import config
from core.io_utils import read_input
from core.text_builder import build_semantic_text
from core.scoring import load_model, compute_scores, classify
from core.methodology import classify_methodology
from core.bibliometrics import compute_citations_per_year, detect_seminal
from core.selection import apply_rescue, generate_audit
from core.export import export_results
import datetime


def main():
    """
    Función principal que orquesta inyectando configuración global.
    """
    print("=" * 60)
    print("📊 SISTEMA MODULAR BIBLIOMÉTRICO (REFACTORIZADO & RIGUROSO)")
    print("=" * 60)

    # Metadata global para reproducibilidad
    meta = {
        "Ejecución": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modelo SBERT": config.MODEL_NAME,
        "Input File": config.INPUT_FILE,
        "Topic Text (Parcial)": config.TOPIC_TEXT.strip()[:100],
        "TH_HIGH": config.TH_HIGH,
        "TH_MID": config.TH_MID,
        "TH_LOW": config.TH_LOW,
        "RESCUE_RATE": config.RESCUE_RATE,
        "AUDIT_RATE": config.AUDIT_RATE
    }

    print("\n📂 Leyendo archivo de entrada...")
    df = read_input(config.INPUT_FILE)

    print("\n📝 Validando columnas y texto...")
    df = build_semantic_text(df, config.TEXT_COLS)

    model = load_model(config.MODEL_NAME)

    df["score_semantic"] = 0.0
    df["FINAL_SCORE"] = 0.0
    df["DECISION"] = "❌ DESCARTAR (Inválido/Incompleto)"
    df["TipoMetodologico"] = "Indeterminado"

    valid_mask = df["isValid"] == True
    
    if valid_mask.sum() > 0:
        scores = compute_scores(model, df.loc[valid_mask, "text_semantic"], config.TOPIC_TEXT)
        
        df.loc[valid_mask, "score_semantic"] = scores
        df.loc[valid_mask, "FINAL_SCORE"] = scores
        df.loc[valid_mask, "DECISION"] = df.loc[valid_mask, "FINAL_SCORE"].apply(
            lambda x: classify(x, config.TH_HIGH, config.TH_MID, config.TH_LOW)
        )
        
        print("\n🔬 Clasificando metodología heurística...")
        df.loc[valid_mask, "TipoMetodologico"] = df.loc[valid_mask, "Abstract"].apply(classify_methodology)

    df = compute_citations_per_year(df)
    df = detect_seminal(df)

    df, df_final = apply_rescue(df, config.RESCUE_RATE, config.RESCUE_MIN)
    audit = generate_audit(df, df_final, config.AUDIT_RATE, config.AUDIT_MIN, config.AUDIT_MAX)

    export_results(df, df_final, audit, config.INPUT_FILE, meta)

    print("\n✅ Trazabilidad completada. Pipeline escalable resuelto.")
    print("=" * 60)

if __name__ == "__main__":
    main()
