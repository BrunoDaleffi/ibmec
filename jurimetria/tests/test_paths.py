"""Smoke tests para o módulo ``jurimetria.paths``."""

from jurimetria.paths import AULAS_DIR, DATA_DIR, ROOT_DIR


def test_root_dir_exists() -> None:
    assert ROOT_DIR.is_dir()


def test_data_dir_exists() -> None:
    assert DATA_DIR.is_dir()


def test_aulas_dir_exists() -> None:
    assert AULAS_DIR.is_dir()
