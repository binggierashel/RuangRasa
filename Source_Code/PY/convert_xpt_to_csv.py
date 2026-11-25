"""Script konversi batch file SAS XPORT (.xpt) CDC NHANES menjadi CSV."""
import argparse
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "Dataset" / "Data_XPT"
DEFAULT_OUTPUT_DIR = ROOT / "Dataset" / "Data_XPT_CSV"


def decode_bytes_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Mendekode nama kolom dan isi teks yang terbaca sebagai bytes dari format SAS XPORT."""
    df.columns = [
        col.decode("utf-8", errors="replace") if isinstance(col, bytes) else str(col)
        for col in df.columns
    ]
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda v: v.decode("utf-8", errors="replace").strip() if isinstance(v, bytes) else v
        )
    return df


def convert_all_xpt(input_dir: Path, output_dir: Path) -> tuple[int, int]:
    """Mengonversi seluruh file .xpt/.XPT secara rekursif sambil mempertahankan struktur subfolder."""
    xpt_files = sorted(input_dir.rglob("*.[xX][pP][tT]"))
    if not xpt_files:
        print(f"[!] Tidak ada file .xpt ditemukan di: {input_dir}")
        return 0, 0

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Ditemukan {len(xpt_files)} file .xpt di {input_dir}")
    print(f"[*] Output CSV akan disimpan ke {output_dir}\n")

    sukses = 0
    gagal = 0

    for idx, xpt_path in enumerate(xpt_files, start=1):
        rel_path = xpt_path.relative_to(input_dir)
        csv_path = (output_dir / rel_path).with_suffix(".csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            df = pd.read_sas(xpt_path, format="xport")
            df = decode_bytes_columns(df)

            if "SEQN" in df.columns:
                df["SEQN"] = df["SEQN"].astype("Int64")

            df.to_csv(csv_path, index=False)
            display_dest = csv_path.relative_to(ROOT) if csv_path.is_relative_to(ROOT) else csv_path
            print(f"[{idx:02d}/{len(xpt_files):02d}] OK: {rel_path} -> {display_dest} ({len(df):,} baris, {df.shape[1]} kolom)")
            sukses += 1
        except Exception as exc:
            print(f"[{idx:02d}/{len(xpt_files):02d}] GAGAL: {rel_path} ({exc})")
            gagal += 1

    print("\n" + "=" * 60)
    print(f"Konversi selesai: {sukses} berhasil, {gagal} gagal.")
    print("=" * 60)
    return sukses, gagal


def main():
    parser = argparse.ArgumentParser(description="Konversi batch file .xpt CDC NHANES ke .csv")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Direktori sumber file .xpt (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Direktori tujuan file .csv (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()
    convert_all_xpt(args.input.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
