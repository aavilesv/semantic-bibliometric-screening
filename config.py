# =========================================================
# config.py
# Archivo de configuración global del sistema de clasificación
# =========================================================

# =========================
# RUTA DEL ARCHIVO DE ENTRADA
# =========================

# Ruta del archivo CSV o Excel con los artículos
# Cambia esta ruta según tu computadora
INPUT_FILE = r"G:\Mi unidad\bibliometric_review\RESULTS\datawos_scopus.csv"


# =========================
# MODELO SEMÁNTICO
# =========================

# Modelo SBERT utilizado para similitud semántica
# Este modelo funciona muy bien con textos académicos en inglés
MODEL_NAME = "all-mpnet-base-v2"


# =========================
# UMBRALES DE CLASIFICACIÓN
# =========================

# Clasificación por relevancia temática
# Estos valores pueden ajustarse según tu dataset

TH_HIGH = 0.80   # ≥ 0.80 → Alta relevancia
TH_MID  = 0.65   # ≥ 0.65 → Media relevancia
TH_LOW  = 0.45   # ≥ 0.45 → Baja relevancia
# < 0.45 → Descartar


# =========================
# PARÁMETROS DE RESCATE
# =========================

# Porcentaje de artículos rescatados desde MEDIA relevancia
RESCUE_RATE = 0.15   # 15%

# Mínimo de artículos rescatados
RESCUE_MIN = 5


# =========================
# PARÁMETROS DE AUDITORÍA
# =========================

# Porcentaje de artículos descartados para auditoría PRISMA
AUDIT_RATE = 0.10   # 10%

# Tamaño mínimo y máximo de auditoría
AUDIT_MIN = 20
AUDIT_MAX = 50


# =========================
# COLUMNAS DE TEXTO
# =========================

# Columnas necesarias para construir el texto semántico
# Estas deben existir en tu archivo de datos
TEXT_COLS = [
    "Title",
    "Abstract",
    "Author Keywords",
    "Index Keywords"
]


# =========================
# TEXTO DEL TEMA (ANCLA SEMÁNTICA)
# =========================

# Este texto define el tema de tu revisión sistemática
# Puedes modificarlo según tu investigación

TOPIC_TEXT = """
This study focuses on the influence of financial technologies (FinTech)
on financial inclusion within the microfinance sector.

Financial technologies include digital financial services such as
mobile money, digital payments, online lending platforms, and
technology-based financial innovations that facilitate access
to financial services.

Financial inclusion refers to the accessibility and effective use
of formal financial services by underserved populations and
micro-enterprises.

The scope prioritizes studies related to microfinance institutions,
financial inclusion, digital finance, and FinTech adoption
in developing and emerging economies.
"""
