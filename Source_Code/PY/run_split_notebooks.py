"""Eksekusi 5 file notebook secara berurutan pada kernel terpisah dan simpan output nyata."""
from datetime import datetime, timezone
import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

from create_split_notebooks import NAMES

ROOT = Path(__file__).resolve().parents[1]


def main():
    evidence = {
        'executed_utc': datetime.now(timezone.utc).isoformat(),
        'separate_kernels': True,
        'success': False,
        'notebooks': []
    }
    destination = ROOT / 'Dokumentasi/eksekusi_notebook_bertahap.json'
    try:
        for name in NAMES:
            path = ROOT / 'Source_Code/notebooks' / name
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            client = NotebookClient(
                notebook, timeout=300, kernel_name='python3',
                resources={'metadata': {'path': str(path.parent)}}
            )
            client.execute()
            nbformat.write(notebook, path)
            count = sum(cell.cell_type == 'code' for cell in notebook.cells)
            evidence['notebooks'].append({'file': name, 'code_cells_executed': count, 'success': True})
            print(f'PASS: {name} ({count} sel kode)', flush=True)
        evidence['success'] = True
    except Exception as error:
        evidence['error'] = str(error)
        raise
    finally:
        destination.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
