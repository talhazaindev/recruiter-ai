"""
tech_aliases_db.py

This file serves as a shared database of tech stack aliases, compound terms,
job title mappings, and title prefixes for use across different modules.
"""

# Configuration for matching
MIN_TECH_STACK_MATCH_PERCENTAGE = 30  # Minimum percentage of tech stack matches (0-100)
FUZZY_MATCH_THRESHOLD = 0.85  # Threshold for fuzzy matching (0.0 to 1.0)
JOB_TITLE_TOKEN_WEIGHT = 0.7  # Minimum token overlap ratio for partial matches

# Common prefixes to remove from job titles (in order of specificity)
JOB_TITLE_PREFIXES = [
    # Senior
    "senior ", "sr ", "sr. ", "snr ", "snr. ",
    
    # Junior
    "junior ", "jr ", "jr. ",
    
    # Entry Level
    "entry ", "entry level ", "entry-level ",
    "graduate ", "graduate trainee ", "trainee ",
    "intern ", "internship ", "apprentice ",
    
    # Mid Level
    "mid ", "mid level ", "mid-level ",
    "middle ", "intermediate ",
    
    # Associate
    "associate ", "assoc ", "assoc. ",
    "assistant ", "asst ", "asst. ",
    
    # Lead
    "lead ",
    "team lead ",
    "technical lead ",
    "tech lead ",
    "lead software ",
    "lead engineer ",
    "lead developer ",
    
    # Principal / Staff
    "principal ",
    "staff ",
    "distinguished ",
    "fellow ",
    
    # Consultant
    "consultant ",
    "technical consultant ",
    "technology consultant ",
    "it consultant ",
    "solution consultant ",
    "solutions consultant ",
    "functional consultant ",
    
    # Manager
    "manager ",
    "mgr ", "mgr. ",
    "senior manager ",
    "group manager ",
    "engineering manager ",
    "development manager ",
    "software manager ",
    "project manager ",
    "program manager ",
    "product manager ",
    "delivery manager ",
    
    # Director
    "director ",
    "dir ", "dir. ",
    "senior director ",
    "associate director ",
    "executive director ",
    "technical director ",
    "engineering director ",
    
    # Head
    "head ",
    "head of ",
    
    # Chief
    "chief ",
    "chief technology ",
    "chief technical ",
    "chief information ",
    "chief executive ",
    "chief operating ",
    "chief product ",
    "chief data ",
    "chief architect ",
    
    # Vice President
    "vice president ",
    "vice-president ",
    "vp ", "vp. ",
    "svp ", "svp. ",
    "evp ", "evp. ",
    "avp ", "avp. ",
    "assistant vice president ",
    "associate vice president ",
    
    # Executive
    "executive ",
    "executive officer ",
    
    # Other Common Prefixes
    "acting ",
    "deputy ",
    "interim ",
    "temporary ",
    "contract ",
    "contractor ",
    "freelance ",
    "independent ",
    "remote ",
    "onsite ",
    "on-site ",
    "hybrid ",
    "full time ",
    "full-time ",
    "part time ",
    "part-time ",
]

# Compound tech stack aliases (acronyms and their expanded forms)
COMPOUND_TECH_ALIASES = {
    # Full Stack Frameworks
    "mern": ["mongodb", "express.js", "react", "node.js", "mongodb express react node", "mern stack"],
    "mean": ["mongodb", "express.js", "angular", "node.js", "mongodb express angular node", "mean stack"],
    "mevn": ["mongodb", "express.js", "vue.js", "node.js", "mongodb express vue node", "mevn stack"],
    "lamp": ["linux", "apache", "mysql", "php", "linux apache mysql php", "lamp stack"],
    "lemp": ["linux", "nginx", "mysql", "php", "linux nginx mysql php", "lemp stack"],
    "wamp": ["windows", "apache", "mysql", "php", "windows apache mysql php", "wamp stack"],
    "xampp": ["apache", "mysql", "php", "perl", "apache mysql php perl", "xampp stack"],
    "pern": ["postgresql", "express.js", "react", "node.js", "postgresql express react node", "pern stack"],
    "jamstack": ["javascript", "apis", "markup", "jam stack", "javascript api markup"],
    
    # Cloud & DevOps
    "elk": ["elasticsearch", "logstash", "kibana", "elastic search logstash kibana", "elk stack"],
    "efk": ["elasticsearch", "fluentd", "kibana", "elasticsearch fluentd kibana", "efk stack"],
    "tick": ["telegraf", "influxdb", "chronograf", "kapacitor", "tick stack"],
    
    # Data & ML
    "hadoop": ["hadoop", "hdfs", "mapreduce", "yarn", "hadoop ecosystem"],
    "spark": ["apache spark", "spark core", "spark sql", "spark streaming", "pyspark"],
    "airflow": ["apache airflow", "airflow dag", "airflow scheduler", "airflow webserver"],
    
    # Web Development
    "jhipster": ["spring boot", "angular", "react", "vue", "jhipster stack"],
    "serverless": ["aws lambda", "api gateway", "dynamodb", "s3", "serverless framework"],
    
    # Testing
    "bdd": ["behavior driven development", "cucumber", "gherkin", "specflow"],
    "tdd": ["test driven development", "junit", "pytest", "testng"],
    "atdd": ["acceptance test driven development", "fit", "fitnesse"],
    
    # Mobile
    "ionic": ["ionic framework", "angular", "react", "vue", "cordova", "capacitor"],
    
    # DevOps
    "cicd": ["ci/cd", "continuous integration", "continuous delivery", "jenkins", "gitlab ci", "github actions"],
    "gitops": ["gitops", "argo cd", "flux", "git as source of truth"],
    "iac": ["infrastructure as code", "terraform", "cloudformation", "pulumi", "ansible"],
    
    # AI/ML
    "llm": ["large language model", "gpt", "claude", "gemini", "llama", "bert", "transformer"],
    "nlp": ["natural language processing", "spacy", "nltk", "huggingface", "bert", "gpt"],
    "cv": ["computer vision", "opencv", "yolo", "detectron", "pytorch vision"],
    "dl": ["deep learning", "neural networks", "tensorflow", "pytorch", "keras"],
    "ml": ["machine learning", "scikit-learn", "xgboost", "lightgbm", "catboost"],
    
    # Data Engineering
    "etl": ["extract transform load", "etl pipeline", "data pipeline", "airflow", "dbt"],
    "elt": ["extract load transform", "elt pipeline", "dbt", "data transformation"],
    
    # Security
    "owasp": ["owasp top 10", "web security", "penetration testing", "vulnerability assessment"],
    "devsecops": ["devsecops", "security as code", "sast", "dast", "container security"],
}

# Very extensive dictionary of tech stack aliases and variations
TECH_STACK_ALIASES = {
    # Programming Languages
    "python": ["python", "py", "python3", "python 3", "cpython", "anaconda", "jupyter", "ipython"],
    "javascript": ["javascript", "js", "ecmascript", "es6", "es2015", "es2020", "vanilla js", "node", "nodejs"],
    "typescript": ["typescript", "ts", "typed javascript", "tsx"],
    "java": ["java", "j2se", "jdk", "jre", "core java", "advanced java", "java 8", "java 11", "java 17"],
    "c": ["c", "ansi c", "c99", "c11", "gcc", "clang"],
    "cpp": ["cpp", "c++", "c plus plus", "c++11", "c++14", "c++17", "c++20", "g++", "visual c++"],
    "csharp": ["csharp", "c#", "c-sharp", "dotnet", ".net", "asp.net"],
    "ruby": ["ruby", "rb", "ruby on rails", "rails", "jruby"],
    "php": ["php", "php7", "php8", "laravel", "symfony", "wordpress", "drupal", "magento"],
    "swift": ["swift", "swift5", "swift ui", "apple swift"],
    "kotlin": ["kotlin", "kt", "kotlin native", "kotlin multiplatform"],
    "go": ["go", "golang", "go lang", "go language"],
    "rust": ["rust", "rustlang", "rust lang"],
    "scala": ["scala", "scala lang"],
    "perl": ["perl", "perl5", "perl6"],
    "r": ["r", "r language", "r programming", "rstudio"],
    "shell": ["shell", "bash", "zsh", "sh", "ksh", "csh", "fish", "powershell"],
    "sql": ["sql", "structured query language", "pl/sql", "tsql", "transact-sql"],
    "html": ["html", "html5", "xhtml", "dhtml", "html5 canvas"],
    "css": ["css", "css3", "sass", "scss", "less", "stylus", "tailwind", "bootstrap"],
    
    # Web Frameworks & Libraries
    "react": ["react", "reactjs", "react.js", "react js", "react library", "next.js", "nextjs", "gatsby", "remix"],
    "angular": ["angular", "angularjs", "angular 2", "angular4", "angular5", "angular6", "angular7", "angular8", 
                "angular9", "angular10", "angular11", "angular12", "angular13", "angular14", "angular15", "angular16"],
    "vue": ["vue", "vuejs", "vue.js", "vue 2", "vue 3", "nuxt", "nuxtjs"],
    "django": ["django", "django framework", "django rest", "django rest framework", "drf"],
    "flask": ["flask", "flask framework", "flask restful"],
    "fastapi": ["fastapi", "fast api"],
    "spring": ["spring", "spring boot", "spring framework", "spring mvc", "spring cloud", "spring data", "spring security"],
    "express": ["express", "expressjs", "express.js", "express framework", "express server"],
    "node": ["node", "nodejs", "node.js", "node server", "node runtime"],
    "jquery": ["jquery", "jq", "jquery ui", "jquery mobile"],
    "bootstrap": ["bootstrap", "bootstrap 4", "bootstrap 5", "bootstrap framework"],
    "tailwind": ["tailwind", "tailwindcss", "tailwind css"],
    "material": ["material", "material ui", "mui", "material design", "angular material", "react material"],
    "webpack": ["webpack", "webpack module", "webpack bundler", "webpack config"],
    "vite": ["vite", "vitejs", "vite bundler", "vite build tool"],
    "redux": ["redux", "redux state", "redux toolkit", "react redux"],
    "mobx": ["mobx", "mobx state", "mobx react"],
    
    # Machine Learning & Data Science
    "tensorflow": ["tensorflow", "tf", "tensor flow", "keras", "tf.keras"],
    "pytorch": ["pytorch", "torch", "py torch", "torchvision", "torchaudio"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn", "scikit", "sk learn"],
    "pandas": ["pandas", "pd", "pandas library"],
    "numpy": ["numpy", "np", "numpy library"],
    "matplotlib": ["matplotlib", "plt", "matplot", "pyplot"],
    "seaborn": ["seaborn", "sns"],
    "jupyter": ["jupyter", "jupyter notebook", "jupyter lab", "ipython notebook"],
    "spark": ["spark", "apache spark", "pyspark", "spark sql", "spark streaming"],
    "kafka": ["kafka", "apache kafka", "confluent", "kafka streaming"],
    "airflow": ["airflow", "apache airflow", "airflow dag", "airflow pipeline"],
    "mlflow": ["mlflow", "ml flow"],
    "huggingface": ["huggingface", "hugging face", "transformers", "huggingface transformers"],
    "langchain": ["langchain", "lang chain", "langsmith"],
    "xgboost": ["xgboost", "xgb", "extreme gradient boosting"],
    "lightgbm": ["lightgbm", "light gbm", "lgbm"],
    "catboost": ["catboost", "cat boost"],
    
    # Databases
    "mysql": ["mysql", "my sql", "mysql server", "maria db"],
    "postgresql": ["postgresql", "postgres", "pg", "psql"],
    "mongodb": ["mongodb", "mongo", "mongo db", "mongoose"],
    "redis": ["redis", "redis cache", "redis server"],
    "elasticsearch": ["elasticsearch", "es", "elastic search", "elk"],
    "cassandra": ["cassandra", "apache cassandra"],
    "neo4j": ["neo4j", "neo4j graph", "graph database"],
    "firebase": ["firebase", "firebase realtime", "firestore", "firebase firestore"],
    "dynamodb": ["dynamodb", "aws dynamodb", "dynamo db"],
    "sqlite": ["sqlite", "sqlite3"],
    "snowflake": ["snowflake", "snowflake db", "snowflake data warehouse"],
    "redshift": ["redshift", "aws redshift", "redshift data warehouse"],
    "bigquery": ["bigquery", "big query", "google bigquery"],
    "oracle": ["oracle", "oracle db", "oracle database", "oracle sql"],
    
    # Cloud Platforms
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "rds", "dynamodb", "cloudfront", "route53", "vpc", "iam"],
    "azure": ["azure", "microsoft azure", "azure cloud", "azure devops", "azure functions", "azure sql"],
    "gcp": ["gcp", "google cloud", "google cloud platform", "gcloud", "kubernetes engine", "cloud run", "bigquery"],
    "heroku": ["heroku", "heroku cloud", "heroku platform"],
    "digitalocean": ["digitalocean", "digital ocean", "do cloud"],
    "cloudflare": ["cloudflare", "cf", "cloud flare"],
    
    # DevOps & Containerization
    "docker": ["docker", "docker container", "docker image", "dockerfile", "docker compose", "dockerhub"],
    "kubernetes": ["kubernetes", "k8s", "kube", "kubectl", "aks", "eks", "gke"],
    "jenkins": ["jenkins", "jenkins ci", "jenkins pipeline", "jenkins server"],
    "git": ["git", "git version control", "git bash", "git cli"],
    "github": ["github", "github actions", "github ci", "gh"],
    "gitlab": ["gitlab", "gitlab ci", "gitlab runner"],
    "bitbucket": ["bitbucket", "bitbucket pipelines"],
    "ansible": ["ansible", "ansible playbook", "ansible tower"],
    "terraform": ["terraform", "tf", "terraform cloud", "terraform modules"],
    "puppet": ["puppet", "puppet enterprise", "puppet master"],
    "chef": ["chef", "chef server", "chef cookbook"],
    "prometheus": ["prometheus", "promql", "prometheus metrics"],
    "grafana": ["grafana", "grafana dashboard", "grafana cloud"],
    "argo": ["argo", "argo cd", "argo workflows", "argo rollouts"],
    "istio": ["istio", "service mesh", "istio service mesh"],
    
    # Testing
    "junit": ["junit", "junit4", "junit5", "unit testing"],
    "pytest": ["pytest", "py test", "python testing"],
    "selenium": ["selenium", "selenium webdriver", "selenium grid"],
    "cypress": ["cypress", "cypress io", "end to end testing"],
    "jest": ["jest", "jest testing", "react testing"],
    "mocha": ["mocha", "mocha testing", "mocha js"],
    "chai": ["chai", "chai testing", "chai expect"],
    "testng": ["testng", "test ng", "test framework"],
    "cucumber": ["cucumber", "cucumber bdd", "cucumber tests"],
    "playwright": ["playwright", "playwright testing", "playwright automation"],
    "puppeteer": ["puppeteer", "puppeteer testing", "headless chrome"],
    
    # APIs & Communication
    "rest": ["rest", "restful", "rest api", "restful api", "rest endpoints"],
    "graphql": ["graphql", "graph ql", "apollo", "apollo client", "apollo server"],
    "grpc": ["grpc", "grpc", "protobuf", "protocol buffers"],
    "websocket": ["websocket", "ws", "socket.io", "websocket protocol"],
    "soap": ["soap", "soap api", "soap web service"],
    
    # Message Queues
    "rabbitmq": ["rabbitmq", "rabbit mq", "rabbit"],
    "kafka": ["kafka", "apache kafka", "confluent kafka"],
    "redis": ["redis", "redis pubsub", "redis queue"],
    "sqs": ["sqs", "aws sqs", "amazon sqs", "simple queue service"],
    "sns": ["sns", "aws sns", "amazon sns", "simple notification service"],
    
    # Monitoring & Logging
    "elk": ["elk", "elasticsearch", "logstash", "kibana", "elastic stack"],
    "splunk": ["splunk", "splunk enterprise", "splunk cloud"],
    "datadog": ["datadog", "dd", "datadog monitoring"],
    "newrelic": ["newrelic", "new relic", "nr"],
}

# Dictionary of job title mappings (canonical -> list of variations/aliases)
JOB_TITLE_MAPPINGS = {
    # ---------------- Software Engineering ----------------
    "associate_software_engineer": [
        "associate software engineer", "associate software developer",
        "associate developer", "ase"
    ],
    "software_engineer": [
        "software engineer", "software developer",
        "application developer", "application engineer",
        "programmer", "developer", "software consultant",
        "software development engineer", "sde"
    ],
    "backend_engineer": [
        "backend engineer", "backend developer",
        "back-end engineer", "back-end developer",
        "server side engineer", "server-side engineer",
        "server side developer", "server-side developer",
        "api developer", "api engineer",
        "services engineer", "microservices engineer"
    ],
    "python_backend_engineer": [
        "python developer", "python engineer",
        "django developer", "django engineer",
        "fastapi developer", "fastapi engineer",
        "flask developer", "flask engineer"
    ],
    "java_backend_engineer": [
        "java developer", "java engineer",
        "spring developer", "spring boot developer",
        "spring engineer", "j2ee developer"
    ],
    "dotnet_backend_engineer": [
        ".net developer", "dotnet developer",
        "dot net developer", "c# developer",
        "asp.net developer"
    ],
    "frontend_engineer": [
        "frontend developer", "frontend engineer",
        "front-end developer", "front-end engineer",
        "web developer", "web engineer",
        "client-side developer"
    ],
    "react_developer": [
        "react developer", "react engineer",
        "reactjs developer", "react.js developer"
    ],
    "angular_developer": [
        "angular developer", "angular engineer"
    ],
    "vue_developer": [
        "vue developer", "vuejs developer",
        "vue.js developer"
    ],
    "fullstack_engineer": [
        "full stack developer", "full stack engineer",
        "fullstack developer", "fullstack engineer",
        "full stack software engineer"
    ],
    
    # ---------------- Mobile ----------------
    "mobile_developer": [
        "mobile developer", "mobile engineer"
    ],
    "android_developer": [
        "android developer", "android engineer"
    ],
    "ios_developer": [
        "ios developer", "iphone developer",
        "swift developer"
    ],
    "flutter_developer": [
        "flutter developer", "flutter engineer"
    ],
    "react_native_developer": [
        "react native developer",
        "react native engineer"
    ],
    
    # ---------------- AI / ML ----------------
    "machine_learning_engineer": [
        "machine learning engineer", "machine learning developer",
        "ml engineer", "ml developer", "machine learning specialist"
    ],
    "ai_engineer": [
        "ai engineer", "artificial intelligence engineer",
        "artificial intelligence developer", "ai developer",
        "ai specialist", "generative ai engineer", "gen ai engineer",
        "llm engineer", "llm developer", "foundation model engineer",
        "prompt engineer", "ai application engineer",
        "ai/ml engineer", "ml/ai engineer",
        "artificial intelligence/machine learning engineer"
    ],
    "deep_learning_engineer": [
        "deep learning engineer", "deep learning developer",
        "computer vision engineer", "vision engineer",
        "nlp engineer", "speech engineer"
    ],
    "data_scientist": [
        "data scientist", "applied scientist",
        "research scientist", "decision scientist",
        "ai/ml scientist"
    ],
    "data_analyst": [
        "data analyst", "analytics analyst",
        "business intelligence analyst", "bi analyst"
    ],
    "data_engineer": [
        "data engineer", "etl developer",
        "etl engineer", "big data engineer",
        "big data developer", "pipeline engineer"
    ],
    "analytics_engineer": [
        "analytics engineer", "bi engineer"
    ],
    "mlops_engineer": [
        "mlops engineer", "machine learning operations engineer",
        "ai platform engineer", "model deployment engineer"
    ],
    
    # ---------------- Cloud / DevOps ----------------
    "devops_engineer": [
        "devops engineer", "devops developer", "platform engineer"
    ],
    "site_reliability_engineer": [
        "site reliability engineer", "sre"
    ],
    "cloud_engineer": [
        "cloud engineer", "aws engineer",
        "azure engineer", "gcp engineer"
    ],
    "cloud_architect": [
        "cloud architect", "aws architect",
        "azure architect", "gcp architect"
    ],
    
    # ---------------- QA ----------------
    "qa_engineer": [
        "qa engineer", "quality assurance engineer",
        "software tester", "test engineer", "qa analyst"
    ],
    "automation_engineer": [
        "automation engineer", "test automation engineer",
        "qa automation engineer", "selenium engineer"
    ],
    
    # ---------------- Security ----------------
    "security_engineer": [
        "security engineer", "cybersecurity engineer",
        "cyber security engineer", "information security engineer",
        "application security engineer", "security analyst"
    ],
    
    # ---------------- Infrastructure ----------------
    "system_administrator": [
        "system administrator", "systems administrator", "sysadmin"
    ],
    "network_engineer": [
        "network engineer", "network administrator"
    ],
    "database_administrator": [
        "database administrator", "dba", "sql dba", "oracle dba"
    ],
    
    # ---------------- Architecture ----------------
    "solution_architect": [
        "solution architect", "solutions architect", "technical architect"
    ],
    "enterprise_architect": [
        "enterprise architect"
    ],
    
    # ---------------- Management ----------------
    "engineering_manager": [
        "engineering manager", "software engineering manager"
    ],
    "project_manager": [
        "project manager", "delivery manager", "program manager"
    ],
    "product_manager": [
        "product manager", "product owner"
    ],
    "scrum_master": [
        "scrum master", "agile coach"
    ],
    
    # ---------------- Design ----------------
    "ui_designer": [
        "ui designer", "user interface designer"
    ],
    "ux_designer": [
        "ux designer", "user experience designer"
    ],
    "ui_ux_designer": [
        "ui ux designer", "ux ui designer", "product designer"
    ],
    "graphic_designer": [
        "graphic designer", "visual designer"
    ],
    
    # ---------------- Business ----------------
    "business_analyst": [
        "business analyst", "systems analyst", "ba"
    ],
    "consultant": [
        "consultant", "technology consultant", "it consultant"
    ],
    "technical_writer": [
        "technical writer", "documentation specialist"
    ]
}