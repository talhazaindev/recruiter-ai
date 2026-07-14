"""
JD Embedding Generator
A simple tool to generate embeddings for Job Description JSON files.

Usage:
    from jd_embedding_generator import process_jd_file
    result = process_jd_file("job_description.json")
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# ==================== CONFIGURATION ====================
# You can change this to any sentence-transformers model
# Popular options: 'all-MiniLM-L6-v2', 'all-mpnet-base-v2', 'bert-base-nli-mean-tokens'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# Folder where embeddings will be stored
EMBEDDINGS_FOLDER = "jd_embeddings"

# ======================================================

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    logger.info("Model loaded successfully!")
except ImportError:
    MODEL_AVAILABLE = False
    logger.warning("sentence-transformers not installed. Using mock embeddings.")
    logger.warning("Install it with: pip install sentence-transformers")
except Exception as e:
    MODEL_AVAILABLE = False
    logger.warning(f"Failed to load model: {e}. Using mock embeddings.")


def get_project_root() -> Path:
    """
    Get the project root directory (parent of the current script's directory).
    
    Returns:
        Path to project root
    """
    current_dir = Path(__file__).parent.parent
    return current_dir.parent


def get_jd_folder_path() -> Path:
    """
    Get the path to the JD-jsons folder.
    
    Returns:
        Path to JD-jsons folder
    """
    project_root = get_project_root()
    return project_root / "JD-jsons"


def get_jd_file_path(filename: str) -> Path:
    """
    Get the full path to a JD file in the JD-jsons folder.
    
    Args:
        filename: Name of the JD file
        
    Returns:
        Full path to the JD file
    """
    jd_folder = get_jd_folder_path()
    return jd_folder / filename


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a piece of text.
    This is the main function that creates the embeddings.
    
    Args:
        text: The text to convert to embedding
        
    Returns:
        List of numbers (embedding vector)
        
    Example:
        embedding = get_embedding("Python Developer")
        print(len(embedding))  # 384 for all-MiniLM-L6-v2
    """
    if not text or text.strip() == "":
        # Return zeros for empty text
        return [0.0] * 384  # 384 is the size of all-MiniLM-L6-v2 embeddings
    
    if MODEL_AVAILABLE:
        try:
            # Generate real embedding using the model
            embedding = model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return get_mock_embedding(text)
    else:
        # Use mock embedding if model is not available
        return get_mock_embedding(text)


def get_mock_embedding(text: str, size: int = 384) -> List[float]:
    """
    Generate a simple mock embedding for testing.
    This is used when sentence-transformers is not installed.
    
    Args:
        text: The text to generate mock embedding for
        size: Size of the embedding vector
        
    Returns:
        List of numbers (mock embedding)
    """
    import hashlib
    import math
    
    if not text:
        return [0.0] * size
    
    # Create a deterministic hash from the text
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    
    # Convert hash to numbers
    embedding = []
    for i in range(size):
        idx = i % len(hash_bytes)
        # Convert byte to float between -1 and 1
        val = hash_bytes[idx]
        embedding.append((val / 127.5) - 1.0)
    
    # Normalize the vector (make it length 1)
    norm = math.sqrt(sum(x * x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]
    
    return embedding


def create_embeddings_folder():
    """Create the embeddings folder if it doesn't exist."""
    try:
        # Create embeddings folder in the current directory (where the script is)
        Path(EMBEDDINGS_FOLDER).mkdir(exist_ok=True)
        logger.info(f"📁 Embeddings folder: {EMBEDDINGS_FOLDER}")
    except Exception as e:
        logger.error(f"❌ Failed to create folder: {e}")
        raise


def get_embedding_filename(input_filename: str) -> str:
    """
    Generate the name for the embedding file.
    
    Args:
        input_filename: Name of the input JD file
        
    Returns:
        Name of the embedding file
    """
    base_name = Path(input_filename).stem
    return f"{base_name}_embeddings.json"


def check_if_embeddings_exist(embedding_filename: str) -> bool:
    """
    Check if embeddings already exist for a file.
    
    Args:
        embedding_filename: Name of the embedding file
        
    Returns:
        True if embeddings exist, False otherwise
    """
    embedding_path = Path(EMBEDDINGS_FOLDER) / embedding_filename
    return embedding_path.exists()


def extract_required_data(jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only the fields we need for embedding generation.
    
    Args:
        jd_data: The full JD JSON data
        
    Returns:
        Extracted data with only required fields
    """
    # Start with empty structure
    extracted = {
        "job_title": "",
        "job_summary": "",
        "key_responsibilities": [],
        "nice_to_have": {
            "certifications": []
        }
    }
    
    # Extract job_title
    if "job_title" in jd_data and jd_data["job_title"]:
        extracted["job_title"] = jd_data["job_title"]
    
    # Extract job_summary
    if "job_summary" in jd_data and jd_data["job_summary"]:
        extracted["job_summary"] = jd_data["job_summary"]
    
    # Extract key_responsibilities (make sure it's a list)
    if "key_responsibilities" in jd_data:
        if isinstance(jd_data["key_responsibilities"], list):
            extracted["key_responsibilities"] = jd_data["key_responsibilities"]
        else:
            logger.warning("key_responsibilities should be a list, using empty list")
    
    # Extract certifications from nice_to_have
    if "nice_to_have" in jd_data:
        if isinstance(jd_data["nice_to_have"], dict):
            if "certifications" in jd_data["nice_to_have"]:
                if isinstance(jd_data["nice_to_have"]["certifications"], list):
                    extracted["nice_to_have"]["certifications"] = jd_data["nice_to_have"]["certifications"]
    
    return extracted


def generate_embeddings_for_text(text: str) -> List[float]:
    """
    Generate embeddings for a single text string.
    Wrapper around get_embedding for consistency.
    
    Args:
        text: The text to embed
        
    Returns:
        Embedding vector
    """
    return get_embedding(text)


def create_embedding_structure(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create the final embedding structure with text and embeddings.
    
    Args:
        extracted_data: The extracted JD data
        
    Returns:
        Complete embedding structure ready to save
    """
    logger.info("🔄 Generating embeddings...")
    
    # Create the structure
    embedding_structure = {
        "job_title": {
            "text": extracted_data["job_title"],
            "embedding": generate_embeddings_for_text(extracted_data["job_title"])
        },
        "job_summary": {
            "text": extracted_data["job_summary"],
            "embedding": generate_embeddings_for_text(extracted_data["job_summary"])
        },
        "key_responsibilities": [],
        "nice_to_have": {
            "certifications": []
        }
    }
    
    # Add embeddings for each responsibility
    for resp in extracted_data["key_responsibilities"]:
        embedding_structure["key_responsibilities"].append({
            "text": resp,
            "embedding": generate_embeddings_for_text(resp)
        })
    
    # Add embeddings for each certification
    for cert in extracted_data["nice_to_have"]["certifications"]:
        embedding_structure["nice_to_have"]["certifications"].append({
            "text": cert,
            "embedding": generate_embeddings_for_text(cert)
        })
    
    logger.info("✅ Embeddings generated successfully!")
    return embedding_structure


def save_embeddings(embedding_structure: Dict[str, Any], filename: str) -> str:
    """
    Save the embedding structure to a JSON file.
    
    Args:
        embedding_structure: The embedding data to save
        filename: Name of the file to save
        
    Returns:
        Path where the file was saved
    """
    embedding_filename = get_embedding_filename(filename)
    embedding_path = Path(EMBEDDINGS_FOLDER) / embedding_filename
    
    try:
        with open(embedding_path, 'w', encoding='utf-8') as f:
            json.dump(embedding_structure, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Embeddings saved to: {embedding_path}")
        return str(embedding_path)
    except Exception as e:
        logger.error(f"❌ Failed to save embeddings: {e}")
        raise


def process_jd_file(filename: str) -> str:
    """
    Main function to process a JD file and generate embeddings.
    This is the function you'll call from other files.
    
    Args:
        filename: Name of the JD file (e.g., "Backend_Developer_JD.json")
                 The file should be in the JD-jsons folder (parent directory)
        
    Returns:
        Status message explaining what happened
        
    Example:
        >>> result = process_jd_file("Backend_Developer_JD.json")
        >>> print(result)
        "✅ Embeddings saved to: jd_embeddings/Backend_Developer_JD_embeddings.json"
    """
    try:
        # Step 1: Get the full path to the JD file
        file_path = get_jd_file_path(filename)
        
        # Step 2: Check if file exists
        if not file_path.exists():
            msg = f"❌ File not found: {file_path}"
            logger.error(msg)
            return msg
        
        # Step 3: Read the JD file
        logger.info(f"📖 Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        # Step 4: Get the filename
        embedding_filename = get_embedding_filename(filename)
        
        # Step 5: Check if embeddings already exist
        create_embeddings_folder()
        if check_if_embeddings_exist(embedding_filename):
            msg = f"ℹ️  Embeddings already exist for {filename}"
            logger.info(msg)
            return msg
        
        # Step 6: Extract required data
        logger.info("📋 Extracting required data...")
        extracted_data = extract_required_data(jd_data)
        
        # Step 7: Generate embeddings
        embedding_structure = create_embedding_structure(extracted_data)
        
        # Step 8: Save embeddings
        save_path = save_embeddings(embedding_structure, filename)
        
        return f"✅ Embeddings saved to: {save_path}"
        
    except FileNotFoundError:
        msg = f"❌ File not found: {file_path}"
        logger.error(msg)
        return msg
    except json.JSONDecodeError as e:
        msg = f"❌ Invalid JSON in file {filename}: {e}"
        logger.error(msg)
        return msg
    except Exception as e:
        msg = f"❌ Unexpected error: {e}"
        logger.error(msg)
        return msg


# ==================== HELPERS FOR BEGINNERS ====================

def check_embedding_model():
    """
    Helper function to check if the embedding model is working.
    Useful for debugging.
    
    Example:
        >>> check_embedding_model()
        Model: all-MiniLM-L6-v2
        Status: ✅ Working
        Example embedding for 'test': [0.123, -0.456, ...]
    """
    print(f"\n{'='*50}")
    print(f"🔍 Embedding Model Check")
    print(f"{'='*50}")
    print(f"Model: {EMBEDDING_MODEL}")
    
    if MODEL_AVAILABLE:
        print("Status: ✅ Working")
        test_text = "Hello, this is a test"
        embedding = get_embedding(test_text)
        print(f"Test text: '{test_text}'")
        print(f"Embedding size: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
    else:
        print("Status: ⚠️  Using mock embeddings (sentence-transformers not installed)")
        print("Install with: pip install sentence-transformers")
    print(f"{'='*50}\n")


def list_available_models():
    """
    List some popular sentence-transformers models you can try.
    """
    print("\n📚 Popular Embedding Models:")
    print("-" * 40)
    print("1. all-MiniLM-L6-v2     (384 dims, fast, good for most tasks)")
    print("2. all-mpnet-base-v2     (768 dims, better quality, slower)")
    print("3. bert-base-nli-mean-tokens (768 dims, good for semantic search)")
    print("4. paraphrase-MiniLM-L3-v2 (384 dims, very fast, lower quality)")
    print("5. multi-qa-MiniLM-L6-cos-v1 (384 dims, good for question answering)")
    print("\n💡 To change model, edit EMBEDDING_MODEL at the top of this file")


def list_jd_files():
    """
    List all JD files available in the JD-jsons folder.
    """
    jd_folder = get_jd_folder_path()
    
    if not jd_folder.exists():
        print(f"❌ JD-jsons folder not found at: {jd_folder}")
        return
    
    jd_files = list(jd_folder.glob("*.json"))
    
    if not jd_files:
        print(f"📁 No JSON files found in: {jd_folder}")
        return
    
    print(f"\n📁 JD files found in {jd_folder}:")
    print("-" * 50)
    for i, file in enumerate(jd_files, 1):
        print(f"{i}. {file.name}")


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Show available models
    list_available_models()
    
    # Check if embedding model is working
    check_embedding_model()
    
    # List all JD files in the JD-jsons folder
    list_jd_files()
    
    # Example: Process a specific JD file from the JD-jsons folder
    # Change this to the name of your JD file
    sample_file = "Backend_Developer_JD.json"  # This should exist in JD-jsons folder
    
    print(f"\n🔄 Processing JD: {sample_file}")
    result = process_jd_file(sample_file)
    print(result)
    
    # Process again to show "already exists" message
    print("\n🔄 Processing again...")
    result2 = process_jd_file(sample_file)
    print(result2)