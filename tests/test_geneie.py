from pathlib import Path
from genie import Genie
from enum import StrEnum


def test_genie():
    df = Genie.from_excel()
    assert isinstance(df, Genie)
    sheet_keys = sorted(list(df.sheets.keys()))
    exp_keys = ["G", "L", "U"]
    assert sheet_keys == exp_keys
    assert 'rank_per_(u)' not in df.columns

def test_genie_to_excel_table():
    path = Path("./data/poke_genie_clean_2025-01-31.xlsx")
    if path.exists():
        path.unlink()

    assert not path.exists()
    df = Genie.from_excel()
    df.to_clean_excel(path)
    assert path.exists()

def test_genie_form_enum():
    df = Genie.from_excel()
    f_enum = df._build_form_enum()
    assert isinstance(f_enum, str)
