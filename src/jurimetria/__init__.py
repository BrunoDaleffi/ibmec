"""Pacote de utilidades do curso de Jurimetria e Análise de Dados.

Reúne funções e helpers compartilhados entre as aulas (carregamento de dados,
formatação, gráficos, etc.) para evitar duplicação nos notebooks.
"""

from jurimetria.paths import DATA_DIR, EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR, ROOT_DIR

__all__ = [
    "DATA_DIR",
    "EXTERNAL_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "RAW_DATA_DIR",
    "ROOT_DIR",
]

__version__ = "0.1.0"
