"""
Resume Embedding Generator
Generates embeddings for resume JSON files and stores them in resume_embeddings folder.

Usage:
    from resume_embedding_generator import process_resume_file
    embeddings = process_resume_file("resume.json")
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# ==================== CONFIGURATION ====================
# You can change this to any sentence-transformers model
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# Folder where embeddings will be stored
EMBEDDINGS_FOLDER = "resume_embeddings"

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


def get_resume_folder_path() -> Path:
    """
    Get the path to the Resumes-jsons folder.
    
    Returns:
        Path to Resumes-jsons folder
    """
    project_root = get_project_root()
    return project_root / "Resumes-jsons"


def get_resume_file_path(filename: str) -> Path:
    """
    Get the full path to a resume file in the Resumes-jsons folder.
    
    Args:
        filename: Name of the resume file
        
    Returns:
        Full path to the resume file
    """
    resume_folder = get_resume_folder_path()
    return resume_folder / filename


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a piece of text.
    
    Args:
        text: The text to convert to embedding
        
    Returns:
        List of numbers (embedding vector)
    """
    if not text or text.strip() == "":
        return [0.0] * 384
    
    if MODEL_AVAILABLE:
        try:
            embedding = model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return get_mock_embedding(text)
    else:
        return get_mock_embedding(text)


def get_mock_embedding(text: str, size: int = 384) -> List[float]:
    """Generate a mock embedding for testing."""
    import hashlib
    import math
    
    if not text:
        return [0.0] * size
    
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    
    embedding = []
    for i in range(size):
        idx = i % len(hash_bytes)
        val = hash_bytes[idx]
        embedding.append((val / 127.5) - 1.0)
    
    norm = math.sqrt(sum(x * x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]
    
    return embedding


def create_embeddings_folder():
    """Create the embeddings folder if it doesn't exist."""
    try:
        Path(EMBEDDINGS_FOLDER).mkdir(exist_ok=True)
        logger.info(f"📁 Embeddings folder: {EMBEDDINGS_FOLDER}")
    except Exception as e:
        logger.error(f"❌ Failed to create folder: {e}")
        raise


def get_embedding_filename(input_filename: str) -> str:
    """
    Generate the name for the embedding file.
    
    Args:
        input_filename: Name of the input resume file
        
    Returns:
        Name of the embedding file
    """
    base_name = Path(input_filename).stem
    return f"{base_name}_embeddings.json"


def load_existing_embeddings(embedding_filename: str) -> Optional[Dict[str, Any]]:
    """
    Load existing embeddings from file.
    
    Args:
        embedding_filename: Name of the embedding file
        
    Returns:
        Embeddings dictionary if exists, None otherwise
    """
    embedding_path = Path(EMBEDDINGS_FOLDER) / embedding_filename
    if embedding_path.exists():
        try:
            with open(embedding_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load embeddings: {e}")
            return None
    return None


def extract_required_data(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only the fields needed for embedding generation.
    
    Args:
        resume_data: The full resume JSON data
        
    Returns:
        Extracted data with only required fields
    """
    extracted = {
        "professional_summary": "",
        "experience": [],
        "projects": [],
        "certifications": []
    }
    
    # Extract professional_summary
    if "professional_summary" in resume_data and resume_data["professional_summary"]:
        extracted["professional_summary"] = resume_data["professional_summary"]
    
    # Extract experience with designation and description
    if "experience" in resume_data and isinstance(resume_data["experience"], list):
        for exp in resume_data["experience"]:
            if isinstance(exp, dict):
                exp_data = {}
                if "designation" in exp and exp["designation"]:
                    exp_data["designation"] = exp["designation"]
                if "description" in exp and exp["description"]:
                    exp_data["description"] = exp["description"]
                if exp_data:
                    extracted["experience"].append(exp_data)
    
    # Extract projects
    if "projects" in resume_data and isinstance(resume_data["projects"], list):
        extracted["projects"] = resume_data["projects"]
    
    # Extract certifications
    if "certifications" in resume_data and isinstance(resume_data["certifications"], list):
        extracted["certifications"] = resume_data["certifications"]
    
    return extracted


def create_embedding_structure(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create the final embedding structure with text and embeddings.
    
    Args:
        extracted_data: The extracted resume data
        
    Returns:
        Complete embedding structure ready to save
    """
    logger.info("🔄 Generating embeddings...")
    
    # Build embedding structure
    embedding_structure = {
        "professional_summary": {
            "text": extracted_data["professional_summary"],
            "embedding": get_embedding(extracted_data["professional_summary"])
        },
        "experience": [],
        "projects": [],
        "certifications": []
    }
    
    # Generate embeddings for each experience (designation + description)
    for exp in extracted_data["experience"]:
        exp_data = {}
        
        designation = exp.get("designation", "")
        exp_data["designation"] = designation
        exp_data["designation_embedding"] = get_embedding(designation)
        
        description = exp.get("description", "")
        exp_data["description"] = description
        exp_data["description_embedding"] = get_embedding(description)
        
        embedding_structure["experience"].append(exp_data)
    
    # Generate embeddings for each project
    for project in extracted_data["projects"]:
        text = project if isinstance(project, str) else str(project)
        embedding_structure["projects"].append({
            "text": text,
            "embedding": get_embedding(text)
        })
    
    # Generate embeddings for each certification
    for cert in extracted_data["certifications"]:
        text = cert if isinstance(cert, str) else str(cert)
        embedding_structure["certifications"].append({
            "text": text,
            "embedding": get_embedding(text)
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


def process_resume_file(filename: str) -> Optional[Dict[str, Any]]:
    """
    Main function to process a resume file and return embeddings.
    If embeddings already exist, returns them from folder.
    Otherwise, generates new embeddings, saves them, and returns them.
    
    Args:
        filename: Name of the resume file (e.g., "resume.json")
                 The file should be in the Resumes-jsons folder (parent directory)
        
    Returns:
        Embeddings dictionary if successful, None otherwise
        
    Example:
        >>> embeddings = process_resume_file("resume.json")
        >>> if embeddings:
        >>>     print(embeddings["professional_summary"]["text"])
    """
    try:
        # Step 1: Get the full path to the resume file
        file_path = get_resume_file_path(filename)
        
        # Step 2: Check if file exists
        if not file_path.exists():
            logger.error(f"❌ File not found: {file_path}")
            return None
        
        # Step 3: Get the embedding filename
        embedding_filename = get_embedding_filename(filename)
        
        # Step 4: Check if embeddings already exist
        create_embeddings_folder()
        existing_embeddings = load_existing_embeddings(embedding_filename)
        
        if existing_embeddings:
            logger.info(f"ℹ️  Loading existing embeddings for {filename}")
            return existing_embeddings
        
        # Step 5: Read the resume file
        logger.info(f"📖 Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        # Step 6: Extract required data
        logger.info("📋 Extracting required data...")
        extracted_data = extract_required_data(resume_data)
        
        # Step 7: Generate embeddings
        embedding_structure = create_embedding_structure(extracted_data)
        
        # Step 8: Save embeddings
        save_embeddings(embedding_structure, filename)
        
        return embedding_structure
        
    except FileNotFoundError:
        logger.error(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in file {filename}: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return None


# ==================== HELPERS ====================

def list_resume_files():
    """
    List all resume files available in the Resumes-jsons folder.
    """
    resume_folder = get_resume_folder_path()
    
    if not resume_folder.exists():
        print(f"❌ Resumes-jsons folder not found at: {resume_folder}")
        return
    
    resume_files = list(resume_folder.glob("*.json"))
    
    if not resume_files:
        print(f"📁 No JSON files found in: {resume_folder}")
        return
    
    print(f"\n📁 Resume files found in {resume_folder}:")
    print("-" * 50)
    for i, file in enumerate(resume_files, 1):
        print(f"{i}. {file.name}")


def check_embedding_model():
    """
    Helper function to check if the embedding model is working.
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


# ==================== EXAMPLE USAGE ====================
# ==================== EXAMPLE USAGE ====================
if __name__ == "__main__":
    # Check if embedding model is working
    check_embedding_model()
    
    # List all resume files in the Resumes-jsons folder
    list_resume_files()
    
    # Process a specific resume file from the Resumes-jsons folder
    sample_file = "r1_best_maatch.json"
    
    print(f"\n🔄 Processing Resume: {sample_file}")
    embeddings = process_resume_file(sample_file)
    
    if embeddings:
        print("\n" + "="*60)
        print("📊 Resume Embedding Results")
        print("="*60)
        
        # Professional Summary
        print(f"\n📝 Professional Summary:")
        summary_text = embeddings['professional_summary']['text']
        print(f"  Text: {summary_text[:100]}..." if len(summary_text) > 100 else f"  Text: {summary_text}")
        print(f"  Embedding size: {len(embeddings['professional_summary']['embedding'])}")
        
        # Experience
        print(f"\n💼 Experience: {len(embeddings['experience'])} items")
        for i, exp in enumerate(embeddings['experience'], 1):
            print(f"\n  Experience #{i}:")
            print(f"    Designation: {exp['designation']}")
            print(f"    Designation Embedding size: {len(exp['designation_embedding'])}")
            desc = exp['description']
            print(f"    Description: {desc[:80]}..." if len(desc) > 80 else f"    Description: {desc}")
            print(f"    Description Embedding size: {len(exp['description_embedding'])}")
        
        # Projects
        print(f"\n📁 Projects: {len(embeddings['projects'])} items")
        for i, proj in enumerate(embeddings['projects'], 1):
            text = proj['text']
            print(f"  {i}. {text[:60]}..." if len(text) > 60 else f"  {i}. {text}")
            print(f"     Embedding size: {len(proj['embedding'])}")
        
        # Certifications
        print(f"\n🎓 Certifications: {len(embeddings['certifications'])} items")
        for i, cert in enumerate(embeddings['certifications'], 1):
            print(f"  {i}. {cert['text']}")
            print(f"     Embedding size: {len(cert['embedding'])}")
        
        print("\n" + "="*60)
        print("✅ Resume embeddings generated successfully!")
        print(f"📁 Embeddings saved in: resume_embeddings/{sample_file.replace('.json', '_embeddings.json')}")
        print("="*60)
        
        # Optional: Save embeddings to a variable for further use
        # You can use this embeddings dictionary in other functions
        resume_embeddings = embeddings
        
    else:
        print(f"\n❌ Failed to process resume: {sample_file}")
        print("Please make sure the file exists in the Resumes-jsons folder")