
import logging
from pathlib import Path
from datetime import datetime, timedelta
import json
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cleanup_conversations(storage_dir: str, max_age_days: int = 30, dry_run: bool = False):
    """Cleanup old conversations and validate conversation files."""
    storage_path = Path(storage_dir)
    if not storage_path.exists():
        logging.error(f"Storage directory {storage_dir} does not exist")
        return

    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    deleted_count = 0
    corrupted_count = 0
    total_count = 0

    for filepath in storage_path.glob("*.json"):
        total_count += 1
        try:
            # Check if file is too old
            mod_time = datetime.fromtimestamp(filepath.stat().st_mtime)
            is_old = mod_time < cutoff_date

            # Validate file contents
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Basic validation
                    assert 'conversation_id' in data
                    assert 'timestamp' in data
                    assert 'messages' in data
                    assert isinstance(data['messages'], list)
            except (json.JSONDecodeError, AssertionError):
                logging.warning(f"Corrupted conversation file: {filepath}")
                if not dry_run:
                    filepath.unlink()
                corrupted_count += 1
                continue

            # Delete if too old
            if is_old:
                if not dry_run:
                    filepath.unlink()
                deleted_count += 1
                logging.info(f"Deleted old conversation: {filepath}")

        except Exception as e:
            logging.error(f"Error processing {filepath}: {e}")

    return {
        'total': total_count,
        'deleted': deleted_count,
        'corrupted': corrupted_count
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup old and corrupted conversation files")
    parser.add_argument("--storage-dir", default="conversation_history",
                      help="Directory containing conversation files")
    parser.add_argument("--max-age-days", type=int, default=30,
                      help="Maximum age of conversations in days")
    parser.add_argument("--dry-run", action="store_true",
                      help="Don't actually delete files, just show what would be done")
    
    args = parser.parse_args()
    
    logging.info(f"Starting cleanup{'(dry run)' if args.dry_run else ''}")
    results = cleanup_conversations(args.storage_dir, args.max_age_days, args.dry_run)
    logging.info(
        f"Cleanup complete: {results['total']} total files, "
        f"{results['deleted']} deleted, {results['corrupted']} corrupted"
    )
