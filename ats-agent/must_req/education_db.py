# education_db.py
"""
Education database containing degree levels, aliases, and discipline mappings
for education verification. Supports technical, business, management, HR, and 
other professional fields.
"""

from typing import Dict, List, Set


# ============================================================
# Degree Levels (ordered from low to high)
# ============================================================

DEGREE_LEVELS: Dict[str, int] = {
    "certificate": 0,
    "diploma": 0,
    "associate": 1,
    "bachelor": 2,
    "graduate_certificate": 2,  # Post-graduate certificate/diploma
    "graduate_diploma": 2,
    "master": 3,
    "professional_degree": 3,  # MD, JD, PharmD, etc.
    "phd": 4,
    "doctorate": 4,
}


# ============================================================
# Degree Aliases
# ============================================================

DEGREE_ALIASES: Dict[str, List[str]] = {
    "certificate": [
        "certificate", "certification", "professional certificate",
        "graduate certificate", "postgraduate certificate", "cert",
        "cert.", "certification program", "certificate program"
    ],
    "diploma": [
        "diploma", "graduate diploma", "postgraduate diploma",
        "dipl.", "advanced diploma", "professional diploma"
    ],
    "associate": [
        "associate", "associates", "associate degree", "aa", "as",
        "a.a.", "a.s.", "associate of arts", "associate of science",
        "associate of applied science", "associate degree in"
    ],
    "bachelor": [
        "bachelor", "bachelors", "bachelor of", "bs", "bsc", "ba",
        "beng", "btech", "bca", "bba", "b.b.a.", "b.a.", "b.s.",
        "b.sc.", "b.e.", "b.eng.", "b.tech.", "b.c.a.", "b.b.a.",
        "bachelor of arts", "bachelor of science", "bachelor of engineering",
        "bachelor of technology", "bachelor of business administration",
        "bachelor of commerce", "b.com", "bachelor of computer applications",
        "bachelor of information technology", "bachelor of laws", "llb",
        "bachelor of law", "bachelor of nursing", "bachelor of education",
        "bachelor of fine arts", "bachelor of architecture", "b.arch",
        "bachelor of design", "bachelor of pharmacy", "b.pharm",
        "bachelor of physiotherapy", "bachelor of occupational therapy",
        "bachelor of social work", "bachelor of psychology", 
        "bachelor of economics", "bachelor of finance", "bachelor of accounting",
        "bachelor of marketing", "bachelor of human resources", "b.hrm",
        "bachelor of international business", "bachelor of management studies",
        "bms", "bachelor of management", "bachelor of hospitality management"
    ],
    "graduate_certificate": [
        "graduate certificate", "postgraduate certificate", 
        "postgrad certificate", "grad cert", "p.g. cert.",
        "graduate certification"
    ],
    "graduate_diploma": [
        "graduate diploma", "postgraduate diploma", "grad dip",
        "p.g. dip.", "postgrad diploma"
    ],
    "master": [
        "master", "masters", "master of", "msc", "ms", "ma", "meng",
        "mtech", "mba", "mca", "m.s.", "m.sc.", "m.a.", "m.eng.",
        "m.tech.", "m.b.a.", "m.c.a.", "master of science",
        "master of arts", "master of engineering", "master of technology",
        "master of business administration", "master of commerce", "m.com",
        "master of computer applications", "master of information technology",
        "master of laws", "llm", "master of law", "master of nursing",
        "master of education", "master of fine arts", "master of architecture",
        "master of design", "master of pharmacy", "master of physiotherapy",
        "master of social work", "master of psychology", "master of economics",
        "master of finance", "master of accounting", "master of marketing",
        "master of human resources", "master of international business",
        "master of management", "master of hospitality management",
        "master of public administration", "mpa", "master of public health",
        "mph", "master of social sciences", "master of statistics",
        "master of applied science", "master of professional studies",
        "mps", "master of library science", "master of information science",
        "master of data science", "master of artificial intelligence",
        "master of cybersecurity", "master of it", "master of software engineering"
    ],
    "professional_degree": [
        "md", "doctor of medicine", "jd", "juris doctor", "doctor of law",
        "pharmd", "doctor of pharmacy", "dds", "doctor of dental surgery",
        "dmd", "doctor of dental medicine", "od", "doctor of optometry",
        "dc", "doctor of chiropractic", "nd", "doctor of naturopathy",
        "do", "doctor of osteopathic medicine", "dvm", "doctor of veterinary medicine",
        "professional degree", "first professional degree",
        "doctor of education", "edd", "doctor of psychology", "psyd",
        "doctor of nursing practice", "dnp"
    ],
    "phd": [
        "phd", "ph d", "doctorate", "doctoral", "doctor of philosophy",
        "dphil", "dsc", "d.sc.", "d.phil.", "ph.d.",
        "doctor of science", "doctor of engineering", "eng.d",
        "doctor of education", "doctor of psychology",
        "doctor of business administration", "dba",
        "doctor of public health", "drph",
        "doctor of social work", "dsw",
        "doctor of nursing", "phd in", "doctoral degree"
    ],
}


# ============================================================
# Disciplines and Their Aliases
# ============================================================

DISCIPLINE_ALIASES: Dict[str, List[str]] = {
    # ===== Technical Disciplines =====
    "computer science": [
        "computer science", "cs", "cse", "comp sci", "computer science and engineering",
        "computer science & engineering", "computing", "computational science"
    ],
    "software engineering": [
        "software engineering", "software development", "se", "swe",
        "software engineering and management", "software systems"
    ],
    "information technology": [
        "information technology", "it", "information systems", "info tech",
        "information technology and management", "it management"
    ],
    "data science": [
        "data science", "ds", "data analytics", "data analysis", "data science and analytics",
        "data engineering", "big data", "data science and machine learning"
    ],
    "artificial intelligence": [
        "artificial intelligence", "ai", "machine learning", "ml",
        "deep learning", "neural networks", "artificial intelligence and machine learning",
        "ai/ml", "intelligent systems"
    ],
    "cybersecurity": [
        "cybersecurity", "cyber security", "information security", "infosec",
        "network security", "computer security", "cyber defense"
    ],
    "computer engineering": [
        "computer engineering", "computer systems engineering", "cpe",
        "computer engineering and science", "computer hardware"
    ],
    "information science": [
        "information science", "informatics", "information studies",
        "information and communication technology", "ict"
    ],
    "computer networks": [
        "computer networks", "networking", "network engineering",
        "network security", "telecommunications"
    ],
    "database systems": [
        "database systems", "database management", "dbms", "database",
        "data management", "database administration"
    ],
    "cloud computing": [
        "cloud computing", "cloud technology", "cloud technologies",
        "aws", "azure", "gcp", "cloud architecture", "cloud solutions"
    ],
    "electrical engineering": [
        "electrical engineering", "electronics engineering", "ee", "ece",
        "electrical and electronics", "electronic engineering"
    ],
    "mechanical engineering": [
        "mechanical engineering", "me", "mechanical and manufacturing",
        "mechanical systems engineering"
    ],
    "civil engineering": [
        "civil engineering", "ce", "civil and environmental",
        "structural engineering", "construction engineering"
    ],
    
    # ===== Mathematical Sciences =====
    "mathematics": [
        "mathematics", "math", "maths", "applied mathematics",
        "mathematical sciences", "computational mathematics"
    ],
    "statistics": [
        "statistics", "statistical", "stats", "stat",
        "applied statistics", "mathematical statistics"
    ],
    
    # ===== Business and Management Disciplines =====
    "business administration": [
        "business administration", "business management", "business admin",
        "business administration and management", "business studies"
    ],
    "management": [
        "management", "management studies", "management science",
        "general management", "strategic management", "operations management"
    ],
    "human resources": [
        "human resources", "hr", "human resource management", "hrm",
        "human resources management", "personnel management",
        "human capital management", "talent management", "hr management"
    ],
    "organizational psychology": [
        "organizational psychology", "industrial psychology",
        "organizational behavior", "organizational development",
        "industrial and organizational psychology", "io psychology"
    ],
    "finance": [
        "finance", "financial management", "financial services",
        "corporate finance", "financial analysis"
    ],
    "accounting": [
        "accounting", "accountancy", "financial accounting",
        "auditing", "taxation", "accounting and finance"
    ],
    "marketing": [
        "marketing", "marketing management", "digital marketing",
        "marketing and communications", "brand management"
    ],
    "economics": [
        "economics", "economic", "econometrics", "applied economics",
        "business economics", "financial economics"
    ],
    "entrepreneurship": [
        "entrepreneurship", "entrepreneurial studies", "new venture management",
        "entrepreneurship and innovation"
    ],
    "international business": [
        "international business", "global business", "international management",
        "global management", "international business management"
    ],
    "hospitality management": [
        "hospitality management", "hotel management", "tourism management",
        "hospitality and tourism", "event management"
    ],
    "supply chain management": [
        "supply chain management", "logistics", "logistics management",
        "supply chain and logistics", "operations and supply chain",
        "procurement", "purchasing"
    ],
    "project management": [
        "project management", "project planning", "project leadership",
        "program management", "project management studies"
    ],
    "operations management": [
        "operations management", "operations research", "operational management",
        "production management", "operations planning"
    ],
    
    # ===== Legal and Public Administration =====
    "law": [
        "law", "legal studies", "jurisprudence", "law and business",
        "corporate law", "commercial law"
    ],
    "public administration": [
        "public administration", "public policy", "public management",
        "government administration", "administrative studies"
    ],
    "public policy": [
        "public policy", "policy studies", "policy analysis",
        "public policy and administration"
    ],
    
    # ===== Social Sciences =====
    "psychology": [
        "psychology", "psychological science", "applied psychology",
        "clinical psychology", "counseling psychology"
    ],
    "sociology": [
        "sociology", "social sciences", "sociological studies",
        "applied sociology"
    ],
    "communications": [
        "communications", "communication studies", "corporate communications",
        "strategic communications", "media and communications"
    ],
    
    # ===== Health Sciences =====
    "public health": [
        "public health", "community health", "global health",
        "health administration", "health management"
    ],
    "nursing": [
        "nursing", "registered nursing", "nursing science",
        "nursing administration", "clinical nursing"
    ],
    "pharmacy": [
        "pharmacy", "pharmaceutical sciences", "clinical pharmacy",
        "pharmacy administration"
    ],
    
    # ===== Other Professional Disciplines =====
    "education": [
        "education", "education studies", "educational psychology",
        "curriculum and instruction", "education administration"
    ],
    "architecture": [
        "architecture", "architectural design", "architectural engineering",
        "urban planning", "urban design"
    ],
    "design": [
        "design", "graphic design", "interaction design",
        "ux design", "user experience design", "ui design"
    ],
    "environmental science": [
        "environmental science", "environmental studies", "ecology",
        "environmental management", "sustainability"
    ],
    "agriculture": [
        "agriculture", "agricultural science", "agribusiness",
        "agricultural economics", "agronomy"
    ],
}


# ============================================================
# IT-Related Disciplines (for broad matching)
# ============================================================

IT_RELATED_DISCIPLINES: Set[str] = {
    "computer science",
    "software engineering",
    "information technology",
    "data science",
    "artificial intelligence",
    "cybersecurity",
    "computer engineering",
    "information science",
    "computer networks",
    "database systems",
    "cloud computing",
    "information security",
}


# ============================================================
# Business-Related Disciplines (for HR/BD professionals)
# ============================================================

BUSINESS_RELATED_DISCIPLINES: Set[str] = {
    "business administration",
    "management",
    "human resources",
    "organizational psychology",
    "finance",
    "accounting",
    "marketing",
    "economics",
    "entrepreneurship",
    "international business",
    "hospitality management",
    "supply chain management",
    "project management",
    "operations management",
    "public administration",
    "public policy",
    "law",
    "communications",
}


# ============================================================
# All Disciplines (for reference)
# ============================================================

ALL_DISCIPLINES: Set[str] = set(DISCIPLINE_ALIASES.keys())


# ============================================================
# Helper Functions
# ============================================================

def get_all_degree_aliases() -> Set[str]:
    """Return all degree aliases as a flat set."""
    all_aliases = set()
    for aliases in DEGREE_ALIASES.values():
        all_aliases.update(aliases)
    return all_aliases


def get_all_discipline_aliases() -> Set[str]:
    """Return all discipline aliases as a flat set."""
    all_aliases = set()
    for aliases in DISCIPLINE_ALIASES.values():
        all_aliases.update(aliases)
    return all_aliases


def is_business_discipline(discipline: str) -> bool:
    """Check if a discipline is business-related."""
    return discipline in BUSINESS_RELATED_DISCIPLINES


def is_it_discipline(discipline: str) -> bool:
    """Check if a discipline is IT-related."""
    return discipline in IT_RELATED_DISCIPLINES


def get_discipline_categories() -> Dict[str, Set[str]]:
    """Return discipline categories for grouping."""
    return {
        "technical": {
            "computer science", "software engineering", "information technology",
            "data science", "artificial intelligence", "cybersecurity",
            "computer engineering", "information science", "computer networks",
            "database systems", "cloud computing", "electrical engineering",
            "mechanical engineering", "civil engineering"
        },
        "mathematical": {
            "mathematics", "statistics"
        },
        "business": BUSINESS_RELATED_DISCIPLINES,
        "health": {
            "public health", "nursing", "pharmacy"
        },
        "social_sciences": {
            "psychology", "sociology", "communications"
        },
        "other": {
            "education", "architecture", "design", "environmental science",
            "agriculture", "law"
        }
    }


# ============================================================
# Pre-built Matching Patterns (for use in verify_education.py)
# ============================================================

# Common degree prefix patterns for compact form detection
DEGREE_PREFIXES: List[str] = [
    "phd", "msc", "mba", "mca", "mtech", "meng", "ms", "ma", "mcom",
    "bsc", "bs", "ba", "beng", "btech", "bca", "bba", "bcom",
    "associate", "diploma", "certificate"
]

# Discipline patterns for compact form detection
DISCIPLINE_PATTERNS: Dict[str, List[str]] = {
    "computer science": ["cs", "cse", "compsci"],
    "software engineering": ["se", "swe", "sweng"],
    "information technology": ["it", "infotech"],
    "data science": ["ds", "datasci"],
    "artificial intelligence": ["ai", "ml"],
    "cybersecurity": ["cybersec", "infosec"],
    "business administration": ["ba", "busadmin"],
    "human resources": ["hr", "hrm"],
    "organizational psychology": ["iopsych"],
    "supply chain management": ["scm"],
    "project management": ["pm"],
    "operations management": ["om"],
}