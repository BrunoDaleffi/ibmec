"""Funções de I/O para leitura e escrita de datasets do curso."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from jurimetria.paths import PROCESSED_DATA_DIR, RAW_DATA_DIR


def load_raw_csv(filename: str, **read_csv_kwargs) -> pd.DataFrame:
    """Carrega um CSV da pasta ``data/raw``.

    Args:
        filename: Nome do arquivo (ex.: ``"processos_tjsp.csv"``).
        **read_csv_kwargs: Argumentos extras repassados a ``pandas.read_csv``.

    Returns:
        DataFrame com o conteúdo do arquivo.
    """
    path = RAW_DATA_DIR / filename
    return pd.read_csv(path, **read_csv_kwargs)


def save_processed(df: pd.DataFrame, filename: str, **to_csv_kwargs) -> Path:
    """Salva um DataFrame na pasta ``data/processed`` em formato CSV.

    Args:
        df: DataFrame a salvar.
        filename: Nome do arquivo de saída.
        **to_csv_kwargs: Argumentos extras repassados a ``DataFrame.to_csv``.

    Returns:
        Caminho do arquivo gravado.
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DATA_DIR / filename
    df.to_csv(path, index=False, **to_csv_kwargs)
    return path
