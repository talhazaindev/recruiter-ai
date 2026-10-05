MAX_SUBSECTIONS = 10

data = {
    "experience": {
        "LEAD SOFTWARE ENGINEER (AI, ML, DATA SCIENCE)": [
            "(Jan 2026 – Present)"
        ],
        "ARTILENCE": [
            "Lahore, PK · Full-time • Lead a team of 6 engineers to architect and ship AI-driven platforms spanning backend, frontend, data pipelines, and cloud infrastructure. • Architect Agentic AI workflows, multi-agent systems, RAG pipelines, and Computer Vision solutions translating complex business requirements into production-ready systems. • Drive technical strategy, mentor engineers, and align roadmap with business objectives across ML, Data Science, and AI domains."
        ],
        "Stack:": [
            "Python · LangChain · LangGraph · RAG · Agentic AI · Computer Vision · AWS · GCP · Docker · Leadership"
        ],
        "AI/ML ENGINEER": [
            "(Aug 2025 – Jan 2026)"
        ],
        "ARTILENCE_2": [
            "Lahore, PK · On-site • Contributed to cutting-edge projects in real-time data engineering and AI, focusing on business automation leveraging modern cloud technologies. • Designed scalable backend services with FastAPI and Django; integrated React/Next.js frontends and high-performance ETL pipelines for large-scale data processing. • Drove cloud-native deployments across AWS, Azure, GCP, and Digital Ocean with Terraform IaC, Docker containerization, and CI/CD automation."
        ],
        "Stack:_2": [
            "Python · FastAPI · Django · React · Next.js · TypeScript · AWS · Azure · GCP · Digital Ocean · Docker · Terraform"
        ],
        "SOFTWARE ENGINEER (FULLSTACK, AI/ML, CLOUD TECHNOLOGIES)": [
            "(Jul 2023 – Aug 2025)"
        ],
        "TECHBIT SYSTEMS": [
            "Ontario, Canada · Remote • Worked as AI/ML Engineer focused on building scalable Python-based backend systems and deploying AI-powered applications on AWS; designed and developed RESTful APIs. • Engineered an AI-powered voice cloning backend on AWS — covering API development, async processing, secure S3 file storage, Lambda functions, and API Gateway integration. • Containerized applications with Docker, deployed to AWS EC2/S3, and automated cloud resource management via Boto3 SDK for provisioning and data workflows. • Contributed to CI/CD pipeline design with GitHub Actions; led performance optimization, structured logging, and error-handling initiatives across production services."
        ],
        "Stack:_3": [
            "Python · FastAPI · AWS EC2/S3/Lambda · Docker · Boto3 · GitHub Actions · RESTful APIs"
        ],
        "ASSOCIATE SOFTWARE ENGINEER (FULLSTACK, AI/ML)": [
            "(Jul 2022 – Jul 2023)"
        ],
        "TECHBIT SYSTEMS_2": [
            "Ontario, Canada · Remote • Built and maintained scalable Python backend systems and RESTful APIs on AWS, prioritizing clean architecture, modularity, and high production reliability. • Contributed to full-stack development spanning Python backends and frontend integration; developed core AI/ML features and cloud-based automation workflows."
        ],
        "Stack:_4": [
            "Python · AWS · RESTful APIs · Full-stack Development · AI/ML"
        ],
        "SOFTWARE ENGINEER INTERN": [
            "(Apr 2022 – Jul 2022)"
        ],
        "TECHBIT SYSTEMS_3": [
            "Ontario, Canada · Remote • Assisted in backend development and API design; gained hands-on experience with Python, cloud deployments, and software engineering best practices."
        ],
        "Stack:_5": [
            "Python · REST APIs · Backend Development · AWS ◆ Digital Ocean ◆ Docker ◆ Terraform ◆ CI/CD ◆ GitHub Actions"
        ],
        "DATA ENGINEERING": [
            "◆ ETL Pipelines ◆ Pandas ◆ NumPy ◆ GeoPandas ◆ GDAL ◆ Rasterio ◆ Apache Spark"
        ],
        "DATABASES": [
            "◆ PostgreSQL ◆ MySQL ◆ DuckDB ◆ SQLite ◆ Neo4j ◆ Redis"
        ],
        "FIND ME ONLINE": [
            "◆ github.com/shanAweb"
        ],
        "Towards an Intelligent Automation Framework for Improving Supermarket Sales using Deep Learning and Computer Vision": [
            "Novel end-to-end pipeline leveraging Deep Learning, Computer Vision, and LLMs to enhance supermarket sales performance, with Digital Twins roadmap for future enhancement. researchgate.net/publication/398033265"
        ]
    },
    
    "education": {
        "FAST NUCES": {"xd"},
        
    }
}

def check_subsections(parsed_data: dict):
    """
    Detects sections that likely need LLM repair.
    """

    for section in ["experience", "education"]:
        value = parsed_data.get(section)

        if not isinstance(value, dict):
            continue

        # Case 1: Everything merged into one content key
        if len(value) == 1 and "content" in value:
            print(f"{section}: Only 'content' found. Send to LLM.")

        # Case 2: Too many subsection keys
        elif len(value) > MAX_SUBSECTIONS:
            print(f"{section}: {len(value)} subsection keys found. Send to LLM.")

check_subsections(data)