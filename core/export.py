# =========================================================
# core/export.py
# Exportación de marco analítico de resultados
# =========================================================

import pandas as pd
from pathlib import Path
import datetime


def reorder_columns(df):
    priority_cols = [
        "FINAL_SCORE", "DECISION", "Title", "bothkeywords",
        "TipoMetodologico", "AltaInfluenciaRelativa", "CitasPorAño", "YearMissing", "Year", "Cited by"
    ]
    
    existing_priority = [col for col in priority_cols if col in df.columns]
    
    skip_cols = ["isValid", "text_semantic", "score_semantic", "In_lectura"]
    other_cols = [col for col in df.columns if col not in existing_priority and col not in skip_cols]
    final_order = existing_priority + other_cols + [c for c in skip_cols if c in df.columns]
    
    return df[final_order]


def export_results(df, df_final, audit, input_file, config_meta=None):
    """
    Exporta el ranking de afinidad semántica.
    """
    print("💾 Estructurando y exportando matriz analítica...")

    input_path = Path(input_file)
    output_dir = input_path.parent
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    excel_path = output_dir / f"RESULTADO_MODULAR_{timestamp}.xlsx"
    csv_path = output_dir / f"TODOS_CLASIFICADOS_{timestamp}.csv"

    df = reorder_columns(df)
    df_final = reorder_columns(df_final)
    audit = reorder_columns(audit)

    df_all_sorted = df.sort_values("FINAL_SCORE", ascending=False)
    df_final_sorted = df_final.sort_values("FINAL_SCORE", ascending=False)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_all_sorted.to_excel(writer, sheet_name="0_RANKING_GENERAL", index=False)
        df_final_sorted.to_excel(writer, sheet_name="1_PRIORIZADOS", index=False)
        audit.to_excel(writer, sheet_name="2_AUDITORIA", index=False)

        stats = df["DECISION"].value_counts().to_frame("Total de Referencia")
        stats.to_excel(writer, sheet_name="ESTADISTICAS_REFERENCIALES")

        if config_meta is not None:
            df_meta = pd.DataFrame(list(config_meta.items()), columns=["Parametro", "Valor"])
            df_meta.to_excel(writer, sheet_name="3_METADATA", index=False)

    df_all_sorted.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"✅ Archivo Excel con Ranking priorizado: {excel_path}")
    print(f"✅ Archivo CSV general local:   {csv_path}")
