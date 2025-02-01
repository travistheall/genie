from pathlib import Path
import pandas as pd
from utils.enums import PvpMark, ShadowPurified, Gender, FormEnum
from utils.containers import EnumKeyDict
from xlsxwriter.worksheet import Worksheet


# excel fucks this up
class Genie(pd.DataFrame):
    # TODO: https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas

    _sheets: EnumKeyDict[pd.DataFrame] | None = None
    _gl: pd.DataFrame | None = None
    _ul: pd.DataFrame | None = None
    _lc: pd.DataFrame | None = None
    

    unicode_map = {
        "√©": "é",
        "‚ôÇ": "♂",
        "‚ôÄ": "♀",
    }
    str_to_num_cols = {
        "weight": "kg",
        "height": "m",
    }
    man_col_map = {
        "Pokemon Number": "num",
        "Shadow/Purified": "sha_pur",
        "Marked for PvP use": "pvp_mark",
        "Atk IV": "iv_atk",
        "Def IV": "iv_def",
        "Sta IV": "iv_sta",
        "Favorite": "fav",
        "Original Scan Date": "orig_scan_dt",
        "Scan Date": "scan_dt",
    }

    def get_pvp_cols(self, ind: PvpMark) -> list[str]:
        fmt_ind = f"_({ind.value})".lower()
        return [col for col in self.columns if col.endswith(fmt_ind)]

    def get_name_repl(self, col: str) -> str:
        name_repls = {
            " ": "_",
            "/": "_",
            "%": "per",
            "#": "num",
        }
        new_col = col
        for _old, _new in name_repls.items():
            new_col = new_col.replace(_old, _new)
        new_col = new_col.lower()
        return new_col

    @property
    def rename_map(self) -> dict[str, str]:
        name_map: dict[str, str] = {
            col: self.get_name_repl(col) for col in self.columns
        }
        name_map |= self.man_col_map
        return name_map

    def get_pvp_new_name_map(self, ind: PvpMark) -> dict[str, str]:
        fmt_ind = f"_({ind.value})".lower()
        pvp_new_name_map: dict[str, str] = {
            col: col.replace(fmt_ind, "")
            for col in self.columns
            if col.endswith(fmt_ind)
        }
        return pvp_new_name_map

    def get_pvp_df(self, ind: PvpMark) -> pd.DataFrame:
        pvp_cols = self.get_pvp_cols(ind)
        rename_map = self.get_pvp_new_name_map(ind)
        pvp_df = self[pvp_cols][:]
        pvp_df.dropna(how="all", inplace=True)
        pvp_df.rename(rename_map, axis="columns", inplace=True)
        pvp_df["sha_pur"] = pvp_df["sha_pur"].apply(ShadowPurified.clean)
        pvp_df["form"] = pvp_df["form"].apply(FormEnum.clean)
        self.drop(columns=pvp_cols, inplace=True)
        return pvp_df

    @property
    def gl(self) -> pd.DataFrame:
        if self._gl is not None:
            return self._gl

        self._gl = self.get_pvp_df(PvpMark.gl)
        return self._gl

    @property
    def ul(self) -> pd.DataFrame:
        if self._ul is not None:
            return self._ul

        self._ul = self.get_pvp_df(PvpMark.ul)
        return self._ul

    @property
    def lc(self) -> pd.DataFrame:
        if self._lc is not None:
            return self._lc

        self._lc = self.get_pvp_df(PvpMark.lc)
        return self._lc

    @property
    def sheets(self) -> EnumKeyDict[pd.DataFrame]:
        if self._sheets is not None:
            return self._sheets

        self._sheets: EnumKeyDict[pd.DataFrame] = EnumKeyDict(
            {
                PvpMark.gl: self.gl,
                PvpMark.ul: self.ul,
                PvpMark.lc: self.lc,
            }
        )
        return self._sheets

    @property
    def str_cols(self):
        str_cols: list[str] = []
        for col in self.columns:
            try:
                self[col].str
                str_cols.append(col)
            except AttributeError:
                continue
        return str_cols

    def fix_unicode(self):
        for bad, good in self.unicode_map.items():
            for col in self.str_cols:
                if not self[col].str.contains(bad).any():
                    continue
                self[col] = self[col].str.replace(bad, good)

    def fix_weight_height(self):
        for col, rm in self.str_to_num_cols.items():
            self[col] = self[col].str.replace(rm, "")
            self[col] = self[col].astype(float)

    @classmethod
    def from_excel(cls, path=Path("./data/poke_genie_export_2025-01-31.xlsx")):
        df = pd.read_excel(
            path,
            index_col="Index",
        )
        return cls(df)

    def to_excel_table(self, writer: pd.ExcelWriter, df:pd.DataFrame, sheet_name: str):
        # https://xlsxwriter.readthedocs.io/example_pandas_table.html

        # Write the dataframe data to XlsxWriter. Turn off the default header and
        # index and skip one row to allow us to insert a user defined header.
        df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)
        # Get the and worksheet objects.
        worksheet: Worksheet = writer.sheets[sheet_name]
        # Get the dimensions of the dataframe.
        (max_row, max_col) = df.shape
        # Create a list of column headers, to use in add_table().
        column_settings = [{"header": column} for column in df.columns]
        # Add the Excel table structure. Pandas will add the data.
        worksheet.add_table(
            0,
            0,
            max_row, max_col - 1,
            {
                "columns": column_settings,
                "style": "White, Table Style Light 15",
            },
        )
        # Make the columns wider for clarity.
        for i, col in enumerate(df.columns):
            width = df[col].astype(str).str.len().max()
            width = max([width, len(col)])
            width += 2
            if col == "catch_date":
                width += 6
            worksheet.set_column(i, i, width)

    def to_clean_excel(self, path=Path("./data/poke_genie_clean_2025-01-31.xlsx")):
        with pd.ExcelWriter(path, engine = 'xlsxwriter') as writer:
            self.to_excel_table(writer=writer, df=self, sheet_name='genie')
            for sheet_name, df in self.sheets.items():
                self.to_excel_table(writer=writer, df=df, sheet_name=sheet_name)

    def _build_form_enum(self) -> str:
        form: str
        code = [
            "class FormEnum(StrEnum):",
        ]
        df: pd.DataFrame
        forms = ["None"]
        for df in [self, *self.sheets.values()]:
            forms.extend(sorted([f for f in df["form"].unique() if not pd.isna(f)]))
        forms = sorted(list(set(forms)))
        snake_repls = {
            " ": "_",
            "-": "_",
            "'": "",
        }
        for form in forms:
            line = " " * 4
            snake = form.lower()
            for _old, _new in snake_repls.items():
                snake = snake.replace(_old, _new)
            line += f'{snake} = "{form}"'
            code.append(line)
        return "\n".join(code)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index.rename("index", inplace=True)
        self.rename(self.rename_map, axis="columns", inplace=True)
        self.fix_weight_height()
        self.fix_unicode()
        self["sha_pur"] = self["sha_pur"].apply(ShadowPurified.clean)
        self["gender"] = self["gender"].apply(Gender.clean)
        self["form"] = self["form"].apply(FormEnum.clean)
        _ = self.sheets


if __name__ == "__main__":
    df = Genie.from_excel()
