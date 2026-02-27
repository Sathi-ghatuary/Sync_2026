import csv
from ..db.chroma_client import get_collection
from pathlib import Path


def ingest_csv(path: str, id_column: str = None, text_column: str = 0, batch_size: int = 512):
    collection = get_collection()
    p = Path(path)
    docs = []
    metas = []
    ids = []
    with p.open('r', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        for i, row in enumerate(reader):
            try:
                if isinstance(text_column, int):
                    title = row[text_column]
                else:
                    title = row[text_column]
            except Exception:
                continue
            docs.append(title)
            metas.append({"text": title})
            ids.append(str(i))
            if len(docs) >= batch_size:
                collection.add(documents=docs, metadatas=metas, ids=ids)
                docs = []
                metas = []
                ids = []
        if docs:
            collection.add(documents=docs, metadatas=metas, ids=ids)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m app.scripts.ingest <csv_path>")
        sys.exit(1)
    ingest_csv(sys.argv[1])
