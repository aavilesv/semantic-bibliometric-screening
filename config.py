# =========================================================
# config.py
# Archivo de configuración global del sistema de clasificación
# =========================================================

# =========================
# RUTA DEL ARCHIVO DE ENTRADA
# =========================

# Ruta del archivo CSV o Excel con los artículos
# Cambia esta ruta según tu computadora
INPUT_FILE = r"H:\Mi unidad\Artículo latindex\article\data\datawos_scopus.csv"


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
This study focuses on the relationship between financial technology (FinTech),
financial inclusion, and economic development in the context of modern financial systems.
The topic includes research on digital financial services such as mobile banking,
mobile money, digital payments, and financial technology platforms that facilitate
access to financial services for individuals and businesses, particularly in
underserved and unbanked populations.
The review examines how FinTech contributes to financial inclusion through
improved access, usage, and quality of financial services, including access to credit,
savings, insurance, and digital transactions.

It also considers the economic impacts associated with financial inclusion driven
by FinTech, such as economic growth, poverty reduction, productivity, entrepreneurship,
and reduction of inequality.

The scope includes studies that analyze determinants, enabling factors, and barriers
to financial inclusion, including digital infrastructure, financial literacy,
regulatory frameworks, and socioeconomic conditions.

Relevant studies are those that evaluate the role of FinTech in promoting or limiting
financial inclusion and its broader implications for economic development,
using empirical, theoretical, or review-based approaches.


"""