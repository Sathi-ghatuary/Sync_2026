"""
CSV ingestion script to load titles into ChromaDB.
Handles multiple CSV formats and batch processing.
"""
import csv
import sys
from pathlib import Path
from ..db.manager import get_db_manager


def ingest_from_csv(csv_path: str, title_column: int = 0, delimiter: str = ','):
    """
    Ingest titles from a CSV file.
    
    Args:
        csv_path: Path to CSV file
        title_column: Column index containing titles (default 0)
        delimiter: CSV delimiter (default ',')
    
    Returns:
        Number of titles ingested
    """
    db_manager = get_db_manager()
    p = Path(csv_path)
    
    if not p.exists():
        print(f"Error: File {csv_path} not found")
        return 0
    
    titles = []
    skipped = 0
    
    print(f"Reading titles from {csv_path}...")
    
    with p.open('r', encoding='utf-8-sig') as fh:
        try:
            reader = csv.reader(fh, delimiter=delimiter)
            for i, row in enumerate(reader):
                if not row:
                    skipped += 1
                    continue
                try:
                    title = row[title_column].strip() if title_column < len(row) else None
                    if title and len(title) > 0:
                        titles.append(title)
                except (IndexError, AttributeError):
                    skipped += 1
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return 0
    
    print(f"Found {len(titles)} titles, skipped {skipped} rows")
    
    if not titles:
        print("No titles to ingest")
        return 0
    
    print(f"Ingesting titles in batches...")
    count = db_manager.batch_add_titles(titles, batch_size=512)
    print(f"Successfully ingested {count} titles")
    
    # Print stats
    stats = db_manager.get_stats()
    print(f"\nDatabase stats: {stats}")
    
    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.scripts.ingest <csv_path> [column_index] [delimiter]")
        print("Example: python -m app.scripts.ingest titles.csv 0 ,")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    col_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    delim = sys.argv[3] if len(sys.argv) > 3 else ','
    
    ingest_from_csv(csv_file, col_index, delim)
