"""
JD Embedding Retriever
Retrieves embeddings from the jd_embeddings folder.

Usage:
    from retrieve_jd_embeddings import get_embeddings
    embeddings = get_embeddings("sample_jd.json")
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# ==================== CONFIGURATION ====================
EMBEDDINGS_FOLDER = "jd_embeddings"
# ======================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_embeddings(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve embeddings for a JD file from the jd_embeddings folder.
    
    Args:
        file_path: Path to the JD JSON file (e.g., "sample_jd.json")
        
    Returns:
        Dictionary containing the embeddings, or None if not found
        
    Example:
        embeddings = get_embeddings("sample_jd.json")
    """
    try:
        # Get filename
        filename = Path(file_path).name
        base_name = Path(filename).stem
        embedding_filename = f"{base_name}_embeddings.json"
        embedding_path = Path(EMBEDDINGS_FOLDER) / embedding_filename
        
        # Check if file exists
        if not embedding_path.exists():
            logger.warning(f"Embeddings not found for {filename}")
            return None
        
        # Read and return embeddings
        with open(embedding_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Error: {e}")
        return None


# ==================== EXAMPLE USAGE ====================
if __name__ == "__main__":
    embeddings = get_embeddings("samples_jd.json")
    if embeddings:
        print("✅ Embeddings retrieved successfully!")
        print(embeddings)
    else:
        print("❌ Failed to retrieve embeddings")