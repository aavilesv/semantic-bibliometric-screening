# =========================================================
# main.py
# Orquestador del sistema modular de clasificación
# =========================================================

# Importa la ruta del archivo desde config
from config import INPUT_FILE

# Importa funciones de los módulos del sistema
from core.io_utils import read_input
from core.text_builder import build_semantic_text
from core.scoring import load_model, compute_scores, classify
from core.methodology import classify_methodology
from core.bibliometrics import compute_citations_per_year, detect_seminal
from core.selection import apply_rescue, generate_audit
from core.export import export_results


def main():
    """
    Función principal que ejecuta todo el pipeline.
    """

    print("=" * 60)
    print("📊 SISTEMA MODULAR DE CLASIFICACIÓN BIBLIOMÉTRICA")
    print("=" * 60)

    # =========================
    # 1. LECTURA DE DATOS
    # =========================
    print("\n📂 Leyendo archivo de entrada...")
    df = read_input(INPUT_FILE)

    # =========================
    # 2. CONSTRUCCIÓN DEL TEXTO SEMÁNTICO
    # =========================
    print("\n🧠 Construyendo texto semántico...")
    df = build_semantic_text(df)

    # =========================
    # 3. CARGA DEL MODELO
    # =========================
    model = load_model()

    # =========================
    # 4. CÁLCULO DE SCORES
    # =========================
    df["score_semantic"] = compute_scores(model, df["text_semantic"])

    # Score final (por ahora igual al semántico)
    df["FINAL_SCORE"] = df["score_semantic"]

    # Clasificación por relevancia
    df["DECISION"] = df["FINAL_SCORE"].apply(classify)

    # =========================
    # 5. CLASIFICACIÓN METODOLÓGICA
    # =========================
    print("\n🔬 Clasificando tipo metodológico...")
    df["TipoMetodologico"] = df["Abstract"].apply(classify_methodology)

    # =========================
    # 6. CÁLCULOS BIBLIOMÉTRICOS
    # =========================
    df = compute_citations_per_year(df)
    df = detect_seminal(df)

    # =========================
    # 7. RESCATE DESDE MEDIA
    # =========================
    df, df_final = apply_rescue(df)

    # =========================
    # 8. GENERAR AUDITORÍA
    # =========================
    audit = generate_audit(df, df_final)

    # =========================
    # 9. EXPORTACIÓN
    # =========================
    export_results(df, df_final, audit)

    print("\n✅ Proceso completado con éxito.")
    print("=" * 60)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
