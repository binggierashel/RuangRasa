"""Runner otomatis untuk menjalankan seluruh pengujian unit testing proyek."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "Source_Code/tests"


def run():
    print("=" * 70)
    print("MENJALANKAN AUTOMATED UNIT TESTING PROYEK PREDIKSI DEPRESI")
    print("=" * 70)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TEST_DIR), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f"Total Pengujian  : {result.testsRun}")
    print(f"Pengujian Sukses : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Kegagalan        : {len(result.failures)}")
    print(f"Kesalahan        : {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print("HASIL AKHIR: 100% PENGUJIAN LOLOS (ALL TESTS PASSED)!")
        sys.exit(0)
    else:
        print("HASIL AKHIR: TERDAPAT PENGUJIAN GAGAL.")
        sys.exit(1)


if __name__ == "__main__":
    run()
