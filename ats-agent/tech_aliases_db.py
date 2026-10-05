"""
tech_aliases_db.py

This file serves as a shared database of tech stack aliases, compound terms,
job title mappings, and title prefixes for use across different modules.
"""

# Configuration for matching
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
    "head of ",
    "head ",
    
    "B2B ", "B2C ", "B2B2C ", "B2G ", "B2E ", "B2B SaaS ", "B2C SaaS ","b2b ", "b2c ", "b2b2c ", "b2g ", "b2e ", "b2b saas ", "b2c saas ",
    
    
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

TECH_STACK_ALIASES = {
    # ============================================================
    # 1. PROGRAMMING LANGUAGES
    # ============================================================
    "python": [
        "python", "py", "python3", "python 3", "cpython", 
        "anaconda", "jupyter", "ipython", "python2", "python 2",
        "python 3.7", "python 3.8", "python 3.9", "python 3.10",
        "python 3.11", "python 3.12", "python 3.13", "pypy", "micropython",
        "django", "flask", "fastapi", "requests", "beautifulsoup",
        "selenium", "scrapy", "pandas", "numpy", "scipy",
        "matplotlib", "seaborn", "plotly", "bokeh", "altair",
        "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras",
        "jax", "huggingface", "transformers", "langchain", "llama_index",
        "mlflow", "wandb", "pytest", "unittest", "airflow",
        "celery", "redis-py", "sqlalchemy", "psycopg2", "pymongo",
        "async", "asyncio", "conda", "pip", "poetry", "venv",
        "flask-restful", "django-rest", "fastapi", "streamlit", "gradio",
        "opencv-python", "pillow", "scikit-image", "nltk", "spacy",
        "gensim", "transformers", "datasets", "tokenizers", "accelerate",
        "peft", "trl", "xformers", "flash-attention", "deepspeed",
        "fairscale", "torchvision", "torchaudio", "torchtext",
        "tensorboard", "wandb", "comet-ml", "neptune", "optuna",
        "hyperopt", "bayesian-optimization", "scikit-optimize"
    ],
    
    "javascript": [
        "javascript", "js", "ecmascript", "es5", "es6", "es2015", 
        "es2016", "es2017", "es2018", "es2019", "es2020", "es2021",
        "es2022", "es2023", "es2024", "vanilla js", "node", "nodejs", 
        "node.js", "browser js", "client-side js", "server-side js",
        "react", "angular", "vue", "jquery", "express", "next.js",
        "nestjs", "nuxtjs", "gatsby", "remix", "svelte", "solidjs",
        "ember", "backbone", "underscore", "lodash", "axios",
        "fetch-api", "promises", "async-await", "event-loop", "dom",
        "webpack", "vite", "rollup", "parcel", "babel", "typescript",
        "eslint", "prettier", "jest", "mocha", "chai", "cypress",
        "playwright", "puppeteer", "web3", "ethers", "d3", "chart.js",
        "three.js", "phaser", "socket.io", "ws", "graphql", "apollo"
    ],
    
    "typescript": [
        "typescript", "ts", "typed javascript", "tsx", "typescript 4",
        "typescript 5", "typescript 5.0", "typescript 5.1", "typescript 5.2",
        "typescript 5.3", "typescript 5.4", "typescript 5.5",
        "angular", "react", "vue", "next.js", "nestjs", "express",
        "typeorm", "prisma", "type-graphql", "graphql-ts", "node-ts",
        "deno", "bun", "ts-node", "ts-jest", "typedoc", "types",
        "interfaces", "generics", "decorators", "enums", "tuples",
        "union-types", "intersection-types", "conditional-types"
    ],
    
    "java": [
        "java", "j2se", "jdk", "jre", "core java", "advanced java",
        "java 7", "java 8", "java 9", "java 10", "java 11", "java 12",
        "java 13", "java 14", "java 15", "java 16", "java 17", "java 18",
        "java 19", "java 20", "java 21", "java 22", "openjdk", "oracle jdk",
        "spring", "spring-boot", "spring-mvc", "spring-data", "spring-security",
        "spring-cloud", "spring-batch", "spring-web", "hibernate", "jpa",
        "maven", "gradle", "junit", "mockito", "testng", "powermock",
        "tomcat", "jetty", "jboss", "weblogic", "websphere", "wildfly",
        "servlets", "jsp", "jsf", "struts", "play-framework", "dropwizard",
        "vertx", "quarkus", "micronaut", "helidon", "graalvm", "kotlin",
        "scala", "clojure", "groovy", "android", "hadoop", "spark",
        "elasticsearch", "cassandra", "neo4j", "ehcache", "hazelcast"
    ],
    
    "cpp": [
        "cpp", "c++", "c plus plus", "c++03", "c++11", "c++14",
        "c++17", "c++20", "c++23", "c++26", "g++", "clang++",
        "msvc", "visual c++", "c++ standard library", "stl",
        "boost", "qt", "wxwidgets", "gtkmm", "fltk", "openframeworks",
        "cinder", "juice", "unreal engine", "cocos2d-x", "godot",
        "opengl", "vulkan", "directx", "metal", "cuda", "opencl",
        "sycl", "oneapi", "tensorflow c++", "pytorch c++", "opencv",
        "poco", "cpprestsdk", "grpc", "protobuf", "capnproto",
        "zmq", "nanomsg", "asio", "boost-asio", "cpp-httplib",
        "nlohmann-json", "rapidjson", "simd", "avx", "sse"
    ],
    
    "csharp": [
        "csharp", "c#", "c-sharp", "dotnet", ".net", ".net core",
        ".net 5", ".net 6", ".net 7", ".net 8", ".net 9",
        "asp.net", "asp.net core", "entity-framework", "ef-core",
        "linq", "xunit", "nunit", "mstest", "moq", "fluentassertions",
        "serilog", "nlog", "log4net", "automapper", "fluentvalidation",
        "mediatr", "mass-transit", "rabbitmq", "azure-sdk", "aws-sdk",
        "signalr", "blazor", "xamarin", "maui", "unity", "monogame",
        "wpf", "winforms", "avalonia", "uno-platform", "telerik",
        "devexpress", "syncfusion", "identityserver", "openiddict",
        "hotchocolate", "graphql-dotnet", "odata", "grpc-dotnet",
        "dapper", "nhibernate", "mongodb-driver", "cosmos-sdk"
    ],
    
    "ruby": [
        "ruby", "rb", "ruby 2", "ruby 3", "jruby", "mruby",
        "ruby on rails", "rails", "rails 5", "rails 6", "rails 7",
        "sinatra", "rack", "haml", "slim", "erb", "sass",
        "rspec", "cucumber", "capybara", "factory-bot", "faker",
        "puma", "unicorn", "passenger", "sidekiq", "delayed-job",
        "resque", "redis", "elasticsearch", "active-record", "activemodel",
        "action-pack", "action-view", "action-mailer", "active-job",
        "active-storage", "action-cable", "webpacker", "turbo", "stimulus",
        "hotwire", "devise", "cancan", "paperclip", "carrierwave",
        "shrine", "active-storage", "ransack", "kaminari", "will-paginate"
    ],
    
    "php": [
        "php", "php4", "php5", "php7", "php8", "php 7.4", "php 8.0",
        "php 8.1", "php 8.2", "php 8.3", "php 8.4", "hhvm", "zend",
        "laravel", "laravel 8", "laravel 9", "laravel 10", "laravel 11",
        "symfony", "symfony 4", "symfony 5", "symfony 6", "symfony 7",
        "wordpress", "wordpress plugin", "wordpress theme", "wp",
        "drupal", "drupal 8", "drupal 9", "drupal 10", "magento",
        "codeigniter", "codeigniter 3", "codeigniter 4", "cakephp",
        "yii", "yii2", "phalcon", "slim", "lumen", "mezzio",
        "composer", "packagist", "phpunit", "psr", "psr-7", "psr-15",
        "doctrine", "eloquent", "orm", "mysql", "postgresql", "mongodb",
        "redis", "memcached", "nginx", "apache", "php-fpm", "swoole",
        "roadrunner", "openswoole", "reactphp", "amphp", "guzzle"
    ],
    
    "swift": [
        "swift", "swift 5", "swift 5.5", "swift 5.7", "swift 5.9",
        "swift 6", "swiftui", "uikit", "cocoa", "cocoatouch",
        "xcode", "xcode 14", "xcode 15", "xcode 16",
        "ios", "ios app", "iphone", "ipad", "macos", "watchos", "tvos",
        "apple", "apple developer", "app store", "testflight",
        "combine", "swift-concurrency", "async-await", "actors",
        "protocols", "extensions", "generics", "optionals", "closures",
        "core-data", "core-animation", "core-graphics", "core-text",
        "swift-package-manager", "spm", "cocoapods", "carthage",
        "xctest", "ui-testing", "snapshot-testing", "swiftlint",
        "swiftformat", "vapor", "kitura", "perfect", "swift-nio",
        "grpc-swift", "aws-sdk-swift", "firebase-ios", "realm"
    ],
    
    "kotlin": [
        "kotlin", "kt", "kotlin 1.5", "kotlin 1.6", "kotlin 1.7",
        "kotlin 1.8", "kotlin 1.9", "kotlin 2.0", "kotlin native",
        "kotlin multiplatform", "kotlin js", "kotlin android",
        "android", "android development", "android studio",
        "jetpack", "jetpack compose", "compose", "androidx",
        "coroutines", "kotlinx-coroutines", "flow", "channels",
        "ktor", "ktor-server", "ktor-client", "ktor-websockets",
        "kotlin-spring", "spring-boot-kotlin", "exposed", "ktorm",
        "kmongo", "ktor-auth", "kotlin-serialization", "kotlinx-serialization",
        "ktor-koin", "ktor-ktorfit", "ktor-jsoup", "ktor-websocket",
        "mockk", "kotest", "spek", "koin", "dagger", "hilt"
    ],
    
    "go": [
        "go", "golang", "go lang", "go language", "go 1.18",
        "go 1.19", "go 1.20", "go 1.21", "go 1.22", "go 1.23",
        "gopher", "golang.org", "google go", "goroutines", "channels",
        "net/http", "gin", "echo", "fiber", "gorilla", "gorilla-mux",
        "gorilla-websocket", "cobra", "viper", "gorm", "sqlx", "pgx",
        "mongo-go", "redis-go", "sarama", "kafka-go", "nats",
        "grpc-go", "protobuf", "wire", "fx", "dig", "uber-fx",
        "zap", "logrus", "zerolog", "slog", "prometheus", "opentelemetry",
        "jwt-go", "oauth2", "casbin", "auth0", "go-zero", "go-micro",
        "micro", "go-kit", "go-clean-arch", "ddd", "cqrs", "event-sourcing"
    ],
    
    "rust": [
        "rust", "rustlang", "rust 2021", "rust 2024", "cargo",
        "rust stable", "rust nightly", "rust beta", "rust-analyzer",
        "tokio", "async-std", "smol", "actix", "rocket", "warp",
        "axum", "poem", "salvo", "serde", "serde_json", "serde_yaml",
        "clap", "structopt", "thiserror", "anyhow", "regex", "rayon",
        "diesel", "sqlx", "sea-orm", "mongodb", "redis-rs",
        "reqwest", "ureq", "isahc", "hyper", "tonic", "prost",
        "rust-crypto", "ring", "rustls", "webpki", "oauth2",
        "loom", "tracing", "log", "env_logger", "criterion",
        "cargo-toml", "cargo-watch", "cargo-audit", "cargo-deny",
        "cargo-license", "rustfmt", "clippy", "rustdoc", "mdbook"
    ],
    
    "scala": [
        "scala", "scala 2", "scala 3", "scala lang", "sbt",
        "akka", "akka-http", "akka-stream", "akka-cluster", "akka-persistence",
        "play", "play-framework", "play-json", "play-slick",
        "spark", "apache-spark", "pyspark", "spark-sql", "spark-streaming",
        "kafka", "apache-kafka", "kafka-streams", "kafka-connect",
        "lagom", "pekko", "zio", "cats", "cats-effect", "fs2",
        "circe", "json4s", "circe-yaml", "doobie", "slick", "quill",
        "scalatest", "specs2", "scalacheck", "scalaz", "shapeless",
        "akka-http-cors", "akka-http-jwt", "akka-http-session",
        "play-silhouette", "play-auth", "play-reactivemongo"
    ],
    
    "perl": [
        "perl", "perl5", "perl6", "raku", "cpan", "perlbrew",
        "catalyst", "mason", "template-toolkit", "moose", "mojolicious",
        "dancer", "dancer2", "plack", "psgi", "mi6", "perl-mongodb",
        "dbix-class", "sql-abstract", "ddl", "convert-asn1", "crypt",
        "net-ssleay", "io-socket-ssl", "lwp", "plack-middleware"
    ],
    
    "r": [
        "r", "r language", "r programming", "rstudio", "r 4.0",
        "r 4.1", "r 4.2", "r 4.3", "r 4.4", "r shiny", "shiny",
        "ggplot2", "dplyr", "tidyr", "tidyverse", "caret", "randomforest",
        "rpart", "xgboost", "glmnet", "ranger", "neuralnet", "nnet",
        "plotly-r", "leaflet", "highcharter", "dbplot", "shinydashboard",
        "rmarkdown", "knitr", "r-data-table", "data-table", "pander",
        "rvest", "xml2", "jsonlite", "httr", "aws.s3", "bigrquery",
        "RPostgres", "RMySQL", "odbc", "DBI", "pool", "sparklyr",
        "tidytext", "text2vec", "wordcloud", "topicmodels", "lda"
    ],
    
    "shell": [
        "shell", "bash", "zsh", "sh", "ksh", "csh", "fish",
        "powershell", "powershell core", "pwsh", "posix shell",
        "bourne shell", "ash", "dash", "shell scripting", "shell script",
        "awk", "sed", "grep", "find", "xargs", "jq", "yq",
        "cut", "sort", "uniq", "head", "tail", "wc", "tr",
        "sed stream", "awk pattern", "bash completion", "zsh-completions",
        "shellcheck", "shfmt", "bash-it", "oh-my-zsh", "prezto",
        "tmux", "screen", "ssh", "scp", "rsync", "wget", "curl"
    ],
    
    "sql": [
        "sql", "structured query language", "pl/sql", "tsql",
        "transact-sql", "sql server", "mysql", "postgresql",
        "oracle sql", "ansi sql", "sql-92", "sql-99", "sql-2003",
        "sql-2006", "sql-2008", "sql-2011", "sql-2016", "sql-2019",
        "query", "select", "insert", "update", "delete", "join",
        "inner join", "outer join", "left join", "right join", "full join",
        "subquery", "cte", "common table expression", "window function",
        "group by", "having", "order by", "distinct", "limit", "offset",
        "index", "view", "materialized view", "stored procedure", "function",
        "trigger", "event", "transaction", "acid", "isolation level",
        "optimization", "query plan", "explain", "analyze", "vacuum",
        "database design", "normalization", "denormalization", "schema"
    ],
    
    "html": [
        "html", "html5", "xhtml", "dhtml", "html 5.1", "html 5.2",
        "html5 canvas", "html5 svg", "html5 semantic", "semantic html",
        "html5 video", "html5 audio", "html5 geolocation", "localstorage",
        "sessionstorage", "webworkers", "websockets", "push-api",
        "notification-api", "drag-and-drop", "history-api", "fetch",
        "doctype", "meta tags", "title", "head", "body", "div", "span",
        "section", "article", "header", "footer", "nav", "main", "aside",
        "figure", "figcaption", "mark", "time", "details", "summary",
        "progress", "meter", "input", "button", "form", "table", "ul", "ol",
        "a", "img", "picture", "source", "video", "audio", "iframe",
        "accessibility", "wai-aria", "semantic web", "microdata", "json-ld"
    ],
    
    "css": [
        "css", "css3", "css 3", "css 4", "css modules", "css-in-js",
        "sass", "scss", "less", "stylus", "tailwind", "tailwindcss",
        "bootstrap", "foundation", "materialize", "bulma", "semantic ui",
        "css grid", "grid layout", "flexbox", "flex layout", "box model",
        "positioning", "z-index", "floats", "clearing", "overflow",
        "css variables", "custom properties", "css animations",
        "css transitions", "transforms", "transitions", "keyframes",
        "media queries", "responsive design", "rwd", "mobile-first",
        "css preprocessors", "postcss", "autoprefixer", "cssnano",
        "styled-components", "emotion", "react-css", "vue-css",
        "pseudo-classes", "pseudo-elements", "selectors", "specificity",
        "css reset", "normalize.css", "ui-framework", "component-library"
    ],
    
    
    "agentic_ai": [
    # Core Naming
    "agentic ai", "agentic", "ai agent", "autonomous agent",
    "agent-based ai", "agentic workflow", "agentic system",
    "intelligent agent", "software agent", "autonomous system",
    
    # Agent Types
    "llm agent", "language agent", "multi-modal agent",
    "conversational agent", "task-oriented agent",
    "goal-oriented agent", "utility agent", "learning agent",
    "reflex agent", "deliberative agent", "hybrid agent",
    "reactive agent", "proactive agent", "social agent",
    "interface agent", "mobile agent", "information agent",
    
    # Multi-Agent Systems
    "multi-agent", "multi-agent system", "mas",
    "multi-agent framework", "agent team", "agent swarm",
    "multi-agent orchestration", "agent coordination",
    "agent communication", "agent negotiation", "agent collaboration",
    "distributed agents", "swarm intelligence", "collective intelligence",
    "agent-based modeling", "abm", "agent simulation",
    
    # Agent Architecture
    "agent architecture", "agent design", "agent memory",
    "working memory", "long-term memory", "episodic memory",
    "semantic memory", "memory management", "memory retrieval",
    "agent state", "agent context", "agent reasoning",
    "planning", "decision making", "action selection",
    "tool use", "tool calling", "function calling",
    "agent loop", "agent cycle", "perception-action cycle",
    
    # Agent Frameworks
    "langchain", "langgraph", "langsmith", "langserve",
    "llama_index", "agentic", "crewai", "autogen", 
    "taskweaver", "assistants api", "openai assistants",
    "agentforce", "azure ai agent", "amazon bedrock agents",
    "vertex ai agent", "google agents", "langflow",
    "flowise", "n8n agent", "wordware", "agentgpt",
    "babyagi", "auto-gpt", "agentops", "haystack",
    "rag", "retrieval augmented generation", "agentic rag",
    
    # Agent Capabilities
    "tool use", "tool execution", "plugin system",
    "function calling", "action execution", "step execution",
    "task decomposition", "subtask", "plan execution",
    "self-reflection", "self-correction", "self-improvement",
    "reasoning", "chain-of-thought", "cot",
    "tree-of-thought", "tot", "self-consistency",
    "re-act", "reasoning action", "reflection",
    "planning", "re-planning", "adaptive planning",
    
    # Agent Interactions
    "human-agent interaction", "hai", "human feedback",
    "human-in-the-loop", "supervised agent", "agent oversight",
    "agent collaboration", "agent cooperation", "agent competition",
    "agent communication", "agent language", "agent protocol",
    "agent negotiation", "agent persuasion", "agent mediation",
    "agent delegation", "task delegation", "handoff",
    
    # Agent Evaluation
    "agent evaluation", "agent benchmarking", "agent metrics",
    "task success rate", "completion rate", "efficiency",
    "cost per task", "token usage", "latency",
    "agent robustness", "agent reliability", "agent safety",
    "alignment", "value alignment", "security",
    "agent monitoring", "agent observability", "agent tracing",
    
    # Agent Applications
    "chatbot", "virtual assistant", "digital assistant",
    "copilot", "personal assistant", "task assistant",
    "automation agent", "workflow agent", "process agent",
    "research agent", "analysis agent", "data agent",
    "coding agent", "software agent", "devops agent",
    "customer support agent", "sales agent", "marketing agent",
    "hr agent", "recruiting agent", "onboarding agent",
    "educational agent", "tutoring agent", "learning agent",
    
    # Agent Concepts
    "autonomous", "self-directed", "self-governing",
    "proactive", "initiative", "self-starting",
    "adaptive", "flexible", "autonomous decision making",
    "agent-based automation", "intelligent automation",
    "cognitive automation", "autonomous workflows",
    "agent orchestration", "workflow orchestration",
    "dynamic execution", "adaptive execution",
    
    # Related AI Concepts
    "agi", "artificial general intelligence",
    "autonomous ai", "self-improving ai", "self-evolving ai",
    "ai automation", "intelligent automation", "cognitive computing",
    "ai orchestration", "smart agents", "autonomous systems"
],
    
    # ============================================================
# VECTOR DATABASES - COMPREHENSIVE SECTION
# ============================================================

"vector_database": [
    # Core Naming
    "vector database", "vector db", "vector search", "vector index",
    "vector store", "embedding database", "embedding store",
    "similarity search", "semantic search", "nearest neighbor",
    "ann", "approximate nearest neighbor", "knn search",
    
    # Vector DB Providers
    "pinecone", "pinecone db", "pinecone vector",
    "weaviate", "weaviate db", "weaviate vector",
    "qdrant", "qdrant db", "qdrant vector",
    "milvus", "milvus db", "milvus vector", "zilliz",
    "chroma", "chromadb", "chroma db", "chroma vector",
    "faiss", "facebook faiss", "faiss vector",
    "lancedb", "lance db", "lancedb vector",
    "pgvector", "postgres vector", "postgresql vector",
    "elasticsearch vector", "es vector", "elastic vector",
    "opensearch vector", "opensearch knn",
    "redis vector", "redis search", "redis vecsim",
    "mongodb vector", "mongo vector", "atlas vector",
    "cassandra vector", "astra vector", "datastax vector",
    "vertex ai vector", "google vector", "cloud vector",
    "azure cognitive vector", "azure vector", "azure search",
    "aws vector", "amazon vector", "opensearch serverless",
    
    # Vector Operations
    "embedding", "embeddings", "text embedding", "image embedding",
    "multimodal embedding", "vector embedding", "embedding model",
    "embedding generation", "embedding pipeline",
    "vectorization", "vectorize", "vectorization pipeline",
    "embedding creation", "embedding storage",
    "vector indexing", "vector index", "vector index creation",
    "vector search", "similarity search", "semantic search",
    "cosine similarity", "euclidean distance", "dot product",
    "inner product", "l2 distance", "angular distance",
    "hybrid search", "dense retrieval", "sparse retrieval",
    
    # Vector DB Features
    "metadata filtering", "metadata search", "pre-filtering",
    "post-filtering", "metadata indexing", "payload indexing",
    "partitioning", "sharding", "replication", "scaling",
    "vector compression", "product quantization", "pq",
    "scalar quantization", "sq", "binary quantization",
    "hierarchical navigable small world", "hnsw",
    "inverted file", "ivf", "ivf flat", "ivf pq",
    "gpu acceleration", "cuda vector", "gpu search",
    
    # RAG & Vector DB Integration
    "rag", "retrieval augmented generation",
    "retrieval", "retriever", "retriever pipeline",
    "vector retriever", "dense retriever", "hybrid retriever",
    "retrieval chain", "retrieval qa", "retrieval agent",
    "document retriever", "context retrieval", "memory retrieval",
    "semantic retrieval", "neural retrieval", "neural search",
    
    # Vector DB Libraries & APIs
    "langchain vector", "langchain vectorstore",
    "llama_index vector", "llama index vector",
    "haystack vector", "haystack retriever",
    "openai embeddings", "ada-002", "text-embedding-ada",
    "openai ada", "gpt embeddings",
    "cohere embeddings", "cohere vector", "cohere search",
    "huggingface embeddings", "hf embeddings", "sentence-transformers",
    "all-mpnet-base-v2", "all-MiniLM-L6-v2", "bge-embeddings",
    "e5-embeddings", "instructor-embeddings",
    
    # Vector DB Concepts
    "embedding model", "embedding size", "embedding dimension",
    "vector dimension", "dimension reduction",
    "index build", "index rebuild", "index optimization",
    "vector cache", "embedding cache", "search latency",
    "query throughput", "qps", "recall", "precision",
    "mrr", "mean reciprocal rank", "hit rate",
    "recall@10", "recall@100", "search accuracy",
    
    # Vector DB Applications
    "semantic search", "neural search", "ai search",
    "recommendation system", "recsys", "recommender",
    "similarity matching", "clustering", "classification",
    "anomaly detection", "outlier detection",
    "image search", "multimodal search", "video search",
    "chatbot memory", "conversation memory", "knowledge base",
    "document retrieval", "pdf retrieval", "text retrieval",
    
    # Vector DB Management
    "vector database management", "vector monitoring",
    "vector backup", "vector restore", "vector migration",
    "vector performance tuning", "vector optimization",
    "vector schema design", "vector data modeling",
    "vector data pipeline", "embedding pipeline"
],
    
    
    
    # ============================================================
    # 2. MACHINE LEARNING & AI DOMAINS
    # ============================================================
    
    "machine_learning": [
        "ml", "machine learning", "predictive modeling", "pattern recognition",
        "supervised learning", "unsupervised learning", "reinforcement learning",
        "semi-supervised learning", "self-supervised learning",
        "classification", "regression", "clustering", "dimensionality reduction",
        "ensemble methods", "bagging", "boosting", "stacking", "voting",
        "random forest", "xgboost", "lightgbm", "catboost", "decision tree",
        "svm", "support vector machine", "knn", "k-nearest neighbors",
        "linear regression", "logistic regression", "ridge regression",
        "lasso regression", "elastic net", "naive bayes", "lda", "qda",
        "gradient descent", "stochastic gradient descent", "batch gradient descent",
        "mini-batch gradient descent", "adam", "rmsprop", "adagrad", "sgd",
        "feature engineering", "feature selection", "feature extraction",
        "hyperparameter tuning", "grid search", "random search", "bayesian optimization",
        "cross validation", "k-fold", "stratified k-fold", "leave-one-out",
        "model evaluation", "accuracy", "precision", "recall", "f1-score",
        "confusion matrix", "roc curve", "auc", "auc-roc", "precision-recall",
        "model deployment", "model serving", "model monitoring", "model drift",
        "mlflow", "wandb", "neptune", "comet", "model registry",
        "experiment tracking", "model versioning", "model governance",
        "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "jax",
        "model training", "model inference", "prediction", "forecasting",
        "exploratory data analysis", "eda", "data exploration", "data visualization",
        "feature importance", "shap", "shapley", "lime", "interpretability",
        "explainable ai", "xai", "fairness", "bias", "ethics ai"
    ],
    
    "deep_learning": [
        "deep learning", "dl", "deep neural networks", "dnn",
        "neural network", "artificial neural network", "ann",
        "cnn", "convolutional neural network", "convolutional network",
        "rnn", "recurrent neural network", "recurrent network",
        "lstm", "long short-term memory", "bi-lstm", "bidirectional lstm",
        "gru", "gated recurrent unit", "transformer", "attention mechanism",
        "multi-head attention", "self-attention", "positional encoding",
        "bert", "gpt", "llama", "t5", "bart", "roberta", "electra", "deberta",
        "resnet", "vgg", "inception", "efficientnet", "mobilenet", "densenet",
        "yolo", "you only look once", "faster r-cnn", "mask r-cnn", "retinanet",
        "unet", "segnet", "deeplab", "gan", "generative adversarial network",
        "variational autoencoder", "vae", "diffusion model", "stable diffusion",
        "dalle", "midjourney", "clip", "contrastive learning", "simclr",
        "moco", "byol", "simsiam", "vit", "vision transformer",
        "swin transformer", "detr", "segformer", "maskformer",
        "backpropagation", "gradient descent", "optimizer", "adam",
        "learning rate", "scheduler", "batch size", "epochs", "iterations",
        "activation function", "relu", "sigmoid", "tanh", "softmax",
        "dropout", "batch normalization", "layer normalization", "weight decay",
        "regularization", "l1 regularization", "l2 regularization",
        "transfer learning", "fine-tuning", "pre-trained model", "foundation model",
        "gradient checkpointing", "mixed precision", "fp16", "fp32", "bf16",
        "cuda", "cudnn", "tensorrt", "onnx", "onnx runtime", "tvm",
        "distributed training", "data parallelism", "model parallelism",
        "pipeline parallelism", "fsdp", "deepspeed", "fairscale", "horovod",
        "autograd", "tensorboard", "torchvision", "torchaudio", "torchtext"
    ],
    
    "nlp": [
        "nlp", "natural language processing", "text mining", "text analytics",
        "computational linguistics", "language processing", "text analysis",
        "text classification", "document classification", "text categorization",
        "sentiment analysis", "opinion mining", "emotion detection", "sentiment classification",
        "named entity recognition", "ner", "entity extraction", "entity recognition",
        "relationship extraction", "event extraction", "information extraction",
        "machine translation", "mt", "neural translation", "language translation",
        "question answering", "qa", "extractive qa", "generative qa",
        "reading comprehension", "text generation", "text synthesis", "content generation",
        "text summarization", "document summarization", "abstractive summarization",
        "extractive summarization", "language modeling", "language model",
        "tokenization", "word tokenization", "sentence tokenization",
        "lemmatization", "stemming", "pos tagging", "part-of-speech tagging",
        "dependency parsing", "constituency parsing", "syntactic parsing",
        "word embedding", "word2vec", "glove", "fasttext", "elmo",
        "contextual embedding", "bert embedding", "transformer",
        "spacy", "nltk", "huggingface", "transformers", "tokenizers",
        "datasets", "accelerate", "peft", "lora", "prefix-tuning",
        "prompt engineering", "few-shot learning", "zero-shot learning",
        "large language model", "llm", "gpt", "claude", "gemini", "llama",
        "fine-tuning", "instruction tuning", "rlhf", "constitutional ai",
        "chatbot", "conversational ai", "dialogue system", "virtual assistant",
        "speech recognition", "asr", "automatic speech recognition", "speech-to-text",
        "text-to-speech", "tts", "speech synthesis", "voice synthesis"
    ],
    
    "computer_vision": [
        "computer vision", "cv", "image understanding", "visual recognition",
        "image recognition", "object recognition", "pattern recognition",
        "image classification", "object classification", "scene classification",
        "object detection", "object localization", "bounding boxes",
        "object tracking", "multi-object tracking", "mot", "tracking",
        "image segmentation", "semantic segmentation", "instance segmentation",
        "panoptic segmentation", "image generation", "image synthesis",
        "face recognition", "facial recognition", "face verification", "face detection",
        "pose estimation", "keypoint detection", "skeleton tracking",
        "optical character recognition", "ocr", "text recognition",
        "document scanning", "image enhancement", "image restoration",
        "super-resolution", "image denoising", "image deblurring",
        "edge detection", "feature detection", "sift", "surf", "orb",
        "optical flow", "motion estimation", "video analytics",
        "surveillance", "security camera", "autonomous vehicles", "self-driving",
        "medical imaging", "mri analysis", "ct scan", "x-ray", "ultrasound",
        "augmented reality", "ar", "virtual reality", "vr", "mixed reality",
        "3d reconstruction", "structure from motion", "sfm", "stereo vision",
        "depth estimation", "point cloud", "lidar", "radar", "sonar",
        "opencv", "cv2", "pillow", "pil", "scikit-image",
        "yolo", "you only look once", "detectron", "detectron2", "mmdetection",
        "pytorch vision", "torchvision", "tensorflow vision", "tf.image",
        "caffe", "caffe2", "darknet", "kitti", "coco", "imagenet",
        "transfer learning", "image augmentation", "data augmentation"
    ],
    
    "reinforcement_learning": [
        "reinforcement learning", "rl", "rl agent", "reinforcement learning agent",
        "q-learning", "dqn", "deep q-network", "double dqn", "dueling dqn",
        "policy gradient", "reinforce", "actor-critic", "a2c", "a3c",
        "ppo", "proximal policy optimization", "trpo", "trust region policy optimization",
        "sac", "soft actor-critic", "td3", "twin delayed ddpg",
        "ddpg", "deep deterministic policy gradient", "d4pg",
        "distributional rl", "c51", "quantile", "iqn", "fqf",
        "multi-agent rl", "marl", "centralized training", "decentralized execution",
        "imitation learning", "behavior cloning", "inverse rl",
        "apprenticeship learning", "rl for robotics", "rl for games",
        "openai gym", "gymnasium", "atari", "ale", "mujoco", "pybullet",
        "env", "environment", "episode", "trajectory", "rollout",
        "exploration", "exploitation", "epsilon-greedy", "softmax",
        "markov decision process", "mdp", "partially observable mdp", "pomdp",
        "reward function", "reward shaping", "discount factor", "gamma",
        "advantage", "td-error", "temporal difference", "monte carlo",
        "deepmind", "openai", "rlhf", "reinforcement learning from human feedback"
    ],
    
    "nlp": [
        "nlp", "natural language processing", "text mining", "text analytics",
        "computational linguistics", "language processing", "text analysis",
        "text classification", "document classification", "text categorization",
        "sentiment analysis", "opinion mining", "emotion detection", "sentiment classification",
        "named entity recognition", "ner", "entity extraction", "entity recognition",
        "relationship extraction", "event extraction", "information extraction",
        "machine translation", "mt", "neural translation", "language translation",
        "question answering", "qa", "extractive qa", "generative qa",
        "reading comprehension", "text generation", "text synthesis", "content generation",
        "text summarization", "document summarization", "abstractive summarization",
        "extractive summarization", "language modeling", "language model",
        "tokenization", "word tokenization", "sentence tokenization",
        "lemmatization", "stemming", "pos tagging", "part-of-speech tagging",
        "dependency parsing", "constituency parsing", "syntactic parsing",
        "word embedding", "word2vec", "glove", "fasttext", "elmo",
        "contextual embedding", "bert embedding", "transformer",
        "spacy", "nltk", "huggingface", "transformers", "tokenizers",
        "datasets", "accelerate", "peft", "lora", "prefix-tuning",
        "prompt engineering", "few-shot learning", "zero-shot learning",
        "large language model", "llm", "gpt", "claude", "gemini", "llama",
        "fine-tuning", "instruction tuning", "rlhf", "constitutional ai",
        "chatbot", "conversational ai", "dialogue system", "virtual assistant",
        "speech recognition", "asr", "automatic speech recognition", "speech-to-text",
        "text-to-speech", "tts", "speech synthesis", "voice synthesis"
    ],
    
    # ============================================================
    # 3. DATA SCIENCE & ANALYTICS
    # ============================================================
    
    "data_science": [
        "data science", "ds", "data analytics", "analytics",
        "business analytics", "predictive analytics", "prescriptive analytics",
        "descriptive analytics", "diagnostic analytics", "data mining",
        "exploratory data analysis", "eda", "data exploration", "data profiling",
        "statistical analysis", "statistics", "descriptive statistics", "inferential statistics",
        "hypothesis testing", "a/b testing", "experimentation", "t-test", "chi-square",
        "anova", "manova", "correlation", "causation", "regression analysis",
        "data visualization", "visualization", "dashboards", "reporting",
        "feature engineering", "feature creation", "feature extraction", "feature transformation",
        "feature selection", "feature importance", "variable selection", "attribute selection",
        "data cleaning", "data preprocessing", "data wrangling", "data munging",
        "data transformation", "data normalization", "data scaling", "standardization",
        "data modeling", "model building", "model training", "model evaluation",
        "cross validation", "model validation", "model selection", "model testing",
        "business intelligence", "bi", "data driven", "data informed",
        "decision making", "insights", "data storytelling", "presentation",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "tableau", "power bi", "looker", "metabase", "superset", "qlik",
        "d3", "highcharts", "amcharts", "chart.js", "plotly-dash",
        "jupyter", "rstudio", "colab", "databricks", "hex", "deepnote"
    ],
    
    "data_engineering": [
        "data engineering", "de", "data infrastructure", "data platform",
        "data pipeline", "etl", "extract transform load", "elt", "extract load transform",
        "data ingestion", "data collection", "data acquisition", "data integration",
        "data processing", "batch processing", "stream processing", "real-time processing",
        "data transformation", "data loading", "data warehouse", "data warehousing",
        "data lake", "data lakehouse", "lakehouse", "data mesh", "data fabric",
        "data quality", "data validation", "data cleansing", "data enrichment",
        "data governance", "data lineage", "data catalog", "data dictionary",
        "data orchestration", "workflow orchestration", "dag", "workflow management",
        "airflow", "prefect", "dbt", "data build tool", "meltano", "dagster",
        "apache spark", "pyspark", "spark sql", "spark streaming", "spark core",
        "apache kafka", "kafka streaming", "kafka connect", "kafka producer", "kafka consumer",
        "apache flink", "flink streaming", "flink batch", "flink sql",
        "apache beam", "beam pipeline", "beam dataflow", "beam portable",
        "hadoop", "hdfs", "hive", "hbase", "pig", "sqoop", "flume", "zookeeper",
        "cassandra", "elasticsearch", "mongodb", "redis", "dynamodb",
        "snowflake", "redshift", "bigquery", "databricks", "synapse",
        "delta lake", "delta table", "iceberg", "hudi", "parquet", "orc", "avro",
        "data infrastructure", "data ops", "data observability", "data reliability"
    ],
    
    # ============================================================
    # 4. WEB DEVELOPMENT FRAMEWORKS
    # ============================================================
    
    "react": [
        "react", "reactjs", "react.js", "react js", "react framework",
        "react 16", "react 17", "react 18", "react 19", "react hooks",
        "react components", "react component", "jsx", "virtual dom",
        "react state", "react props", "react lifecycle", "useState", "useEffect",
        "useContext", "useReducer", "useCallback", "useMemo", "useRef",
        "react context", "react redux", "react router", "react-query",
        "react-hook-form", "react-table", "react-window", "react-virtualized",
        "react-spring", "framer-motion", "react-helmet", "react-i18next",
        "react-testing-library", "enzyme", "jest", "react-native",
        "next.js", "nextjs", "gatsby", "remix", "react-scripts",
        "create-react-app", "vite", "webpack", "babel", "tailwind",
        "material-ui", "mui", "antd", "chakra-ui", "semantic-ui",
        "bootstrap", "shadcn", "radix-ui", "headless-ui", "react-aria",
        "react-component", "single page application", "spa", "component-based"
    ],
    
    "angular": [
        "angular", "angularjs", "angular 2", "angular 2+", "angular 4",
        "angular 5", "angular 6", "angular 7", "angular 8", "angular 9",
        "angular 10", "angular 11", "angular 12", "angular 13", "angular 14",
        "angular 15", "angular 16", "angular 17", "angular 18", "angular 19",
        "typescript", "rxjs", "observables", "subjects", "behavior-subject",
        "dependency injection", "di", "injectable", "providers",
        "components", "directives", "pipes", "services", "modules",
        "angular material", "material design", "cdk", "angular cdk",
        "ngrx", "ngxs", "angular-redux", "angular-forms", "reactive-forms",
        "template-driven", "angular router", "route guards", "resolvers",
        "interceptors", "http-client", "angular-cli", "ng", "angular cli",
        "single page application", "spa", "progressive web app", "pwa",
        "angular universal", "ssr", "server-side rendering", "angular i18n",
        "angular animations", "angular testing", "jasmine", "karma",
        "protractor", "jest", "cypress", "nx", "angular-monorepo"
    ],
    
    "vue": [
        "vue", "vuejs", "vue.js", "vue 2", "vue 3", "vue framework",
        "composition api", "options api", "vue reactivity", "ref", "reactive",
        "computed", "watch", "watchEffect", "vue lifecycle", "vue hooks",
        "vue directives", "vue components", "single file component", "sfc",
        "vue router", "vuex", "pinia", "vue state", "vue store",
        "vue 3 setup", "vue 3 script setup", "vue 3 suspense", "vue 3 teleport",
        "vue 3 fragments", "vue 3 emits", "vue 3 provides", "vue 3 inject",
        "vue test-utils", "vitest", "jest", "cypress", "vue-cli",
        "vue cli", "vite", "vite-vue", "nuxt", "nuxtjs", "nuxt 2", "nuxt 3",
        "nuxt 4", "vue-i18n", "vue-axios", "vuetify", "bootstrap-vue",
        "element-ui", "ant-design-vue", "tailwind-vue", "quasar",
        "vuepress", "vitepress", "gridsome", "storybook", "playwright"
    ],
    
    "svelte": [
        "svelte", "sveltejs", "svelte.js", "svelte 3", "svelte 4", "svelte 5",
        "svelte reactivity", "svelte stores", "svelte components", "svelte props",
        "svelte bindings", "svelte lifecycle", "svelte actions", "svelte transitions",
        "svelte animations", "svelte slots", "svelte context", "svelte events",
        "svelte kit", "sveltekit", "svelte adapter", "svelte preprocessor",
        "svelte compiler", "rollup", "vite", "svelte-testing", "vitest",
        "svelte-tailwind", "svelte-material", "svelte-fragment", "svelte-query"
    ],
    
    "django": [
        "django", "django framework", "django 3", "django 4", "django 5",
        "django rest framework", "drf", "django rest", "django-rest",
        "django orm", "django models", "django forms", "django views",
        "django templates", "django admin", "django middleware",
        "django signals", "django authentication", "django sessions",
        "django migrations", "django management", "django commands",
        "django celery", "django channels", "django websockets",
        "django debug toolbar", "django cors", "django jwt",
        "django allauth", "django rest auth", "django oauth",
        "django mptt", "django polymorphic", "django taggit",
        "django filter", "django rest swagger", "django spectacular",
        "django test", "django unittest", "pytest-django", "django factory",
        "django fixtures", "django seed", "django env", "django dotenv",
        "django secret", "django security", "django deployment",
        "django docker", "django kubernetes", "django aws", "django heroku",
        "django postgres", "django mysql", "django mongodb", "django redis"
    ],
    
    "flask": [
        "flask", "flask framework", "flask microframework", "flask app",
        "flask routes", "flask views", "flask templates", "flask jinja2",
        "flask sqlalchemy", "flask orm", "flask migrate", "flask shell",
        "flask forms", "flask wtforms", "flask validation", "flask login",
        "flask security", "flask auth", "flask jwt", "flask oauth",
        "flask rest", "flask restful", "flask restx", "flask api",
        "flask socket", "flask socketio", "flask websocket", "flask realtime",
        "flask cors", "flask caching", "flask redis", "flask session",
        "flask mail", "flask mailgun", "flask sendgrid", "flask email",
        "flask celery", "flask background", "flask async", "flask asyncio",
        "flask testing", "flask unittest", "pytest-flask", "flask debug",
        "flask debugger", "flask dashboard", "flask admin", "flask adminlte",
        "flask bootstrap", "flask tailwind", "flask docker", "flask deploy",
        "flask gunicorn", "flask uwsgi", "flask nginx", "flask heroku"
    ],
    
    "fastapi": [
        "fastapi", "fast api", "fastapi framework", "fastapi 0.100", "fastapi 0.115",
        "fastapi async", "fastapi asyncio", "fastapi endpoints", "fastapi routes",
        "fastapi dependency injection", "fastapi di", "fastapi middleware",
        "fastapi exceptions", "fastapi validation", "fastapi pydantic",
        "fastapi models", "fastapi schemas", "fastapi database", "fastapi sqlalchemy",
        "fastapi mongodb", "fastapi postgres", "fastapi redis", "fastapi cache",
        "fastapi jwt", "fastapi auth", "fastapi oauth2", "fastapi security",
        "fastapi websockets", "fastapi socket", "fastapi realtime",
        "fastapi background", "fastapi background tasks", "fastapi celery",
        "fastapi testing", "pytest-fastapi", "fastapi test client",
        "fastapi documentation", "fastapi swagger", "fastapi openapi",
        "fastapi redoc", "fastapi generation", "fastapi openapi",
        "fastapi deployment", "fastapi docker", "fastapi kubernetes",
        "fastapi aws", "fastapi lambda", "fastapi serverless", "fastapi gcp",
        "fastapi azure", "fastapi gunicorn", "fastapi uvicorn", "fastapi hypercorn",
        "fastapi asyncpg", "fastapi databases", "fastapi tortoise-orm",
        "fastapi alembic", "fastapi migrations", "fastapi logging"
    ],
    
    "spring": [
        "spring", "spring framework", "spring boot", "spring boot 2", "spring boot 3",
        "spring mvc", "spring web", "spring webflux", "spring reactive",
        "spring data", "spring data jpa", "spring data mongodb", "spring data redis",
        "spring security", "spring oauth2", "spring jwt", "spring authentication",
        "spring cloud", "spring cloud aws", "spring cloud gcp", "spring cloud azure",
        "spring cloud kubernetes", "spring cloud gateway", "spring cloud config",
        "spring cloud stream", "spring cloud bus", "spring cloud netflix",
        "spring cloud hystrix", "spring cloud feign", "spring cloud ribbon",
        "spring batch", "spring integration", "spring scheduling",
        "spring transactions", "spring caching", "spring cache",
        "spring messaging", "spring jms", "spring rabbitmq", "spring kafka",
        "spring actuator", "spring micrometer", "spring metrics", "spring prometheus",
        "spring test", "spring junit", "spring mockito", "spring testcontainers",
        "spring container", "spring ioc", "spring dependency injection",
        "spring beans", "spring configuration", "spring properties",
        "spring profiles", "spring validation", "spring exceptions",
        "spring internationalization", "spring i18n", "spring restdocs",
        "spring swagger", "spring openapi", "spring doc", "spring data rest",
        "spring hateoas", "spring graphql", "spring graphql api",
        "spring native", "spring graalvm", "spring native image",
        "spring lifecycle", "spring events", "spring asynchronous"
    ],
    
    "express": [
        "express", "expressjs", "express.js", "express framework", "express server",
        "express routing", "express routes", "express middleware", "express app",
        "express request", "express response", "express next", "express error",
        "express error handling", "express async", "express promises",
        "express validation", "express express-validator", "express joi",
        "express authentication", "express jwt", "express passport",
        "express session", "express cookie", "express cors", "express helmet",
        "express compression", "express static", "express template",
        "express ejs", "express pug", "express handlebars", "express hbs",
        "express api", "express rest", "express restful", "express endpoints",
        "express websocket", "express socket.io", "express realtime",
        "express database", "express mysql", "express postgres", "express mongodb",
        "express sequelize", "express typeorm", "express mongoose",
        "express testing", "express jest", "express mocha", "express chai",
        "express supertest", "express docker", "express deploy",
        "express aws", "express lambda", "express serverless", "express vercel",
        "express heroku", "express digitalocean", "express nginx", "express pm2",
        "express clustering", "express cluster", "express security"
    ],
    
    "node": [
        "node", "nodejs", "node.js", "node server", "node runtime",
        "node 14", "node 16", "node 18", "node 20", "node 21", "node 22",
        "node core", "node modules", "node packages", "npm", "yarn", "pnpm",
        "node event loop", "node async", "node promises", "node callback",
        "node streams", "node buffer", "node file system", "node fs",
        "node http", "node https", "node websocket", "node socket",
        "node child_process", "node cluster", "node worker_threads",
        "node crypto", "node security", "node authentication",
        "node database", "node mysql", "node postgres", "node mongodb",
        "node redis", "node cache", "node session", "node cookies",
        "node testing", "node jest", "node mocha", "node chai", "node assert",
        "node debugging", "node inspector", "node devtools", "node performance",
        "node profiling", "node monitoring", "node logging", "node winston",
        "node pino", "node bunyan", "node express", "node nestjs", "node fastify",
        "node koa", "node hapi", "node restify", "node graphql", "node apollo",
        "node docker", "node kubernetes", "node aws", "node lambda",
        "node azure", "node gcp", "node deploy", "node heroku", "node vercel"
    ],
    
    # ============================================================
    # 5. DATABASES
    # ============================================================
    
    "postgresql": [
        "postgresql", "postgres", "pg", "psql", "postgresql 13",
        "postgresql 14", "postgresql 15", "postgresql 16", "postgresql 17",
        "postgis", "postgresql orm", "pgadmin", "pgcli", "psql cli",
        "postgresql database", "rds postgres", "aws rds postgres",
        "azure postgres", "google cloud sql postgres", "heroku postgres",
        "postgresql replication", "postgresql streaming", "postgresql logical",
        "postgresql high availability", "postgresql clustering",
        "postgresql backup", "postgresql restore", "postgresql dump",
        "postgresql indexes", "postgresql performance", "postgresql tuning",
        "postgresql partitioning", "postgresql sharding", "postgresql distributed",
        "postgresql transactions", "postgresql acid", "postgresql isolation",
        "postgresql json", "postgresql jsonb", "postgresql hstore",
        "postgresql array", "postgresql full text", "postgresql full-text search",
        "postgresql trigrams", "postgresql similarity", "postgresql fuzzy search",
        "postgresql foreign data", "postgresql foreign data wrapper", "fdw"
    ],
    
    "mysql": [
        "mysql", "my sql", "mysql server", "mariadb", "percona",
        "mysql 5.7", "mysql 8.0", "mysql 8.4", "mysql 9.0",
        "mysql workbench", "mysql cli", "mysqladmin", "mysqldump",
        "mysql replication", "mysql master-slave", "mysql group replication",
        "mysql innodb", "myisam", "mysql storage", "mysql engine",
        "mysql transactions", "mysql acid", "mysql isolation levels",
        "mysql indexes", "mysql performance", "mysql query optimization",
        "mysql explain", "mysql slow query", "mysql profiling",
        "mysql partitioning", "mysql sharding", "mysql cluster",
        "mysql backup", "mysql restore", "mysql binary log",
        "mysql replication lag", "mysql high availability",
        "mysql connector", "mysql python connector", "mysql jdbc",
        "mysql nodejs", "mysql php", "mysql pdo", "mysql orm",
        "mysql full text", "mysql json", "mysql spatial", "mysql gis",
        "mysql foreign key", "mysql constraints", "mysql triggers",
        "mysql stored procedures", "mysql functions", "mysql views"
    ],
    
    "mongodb": [
        "mongodb", "mongo", "mongo db", "mongodb atlas", "mongodb enterprise",
        "mongodb 5.0", "mongodb 6.0", "mongodb 7.0", "mongodb 8.0",
        "mongodb compass", "mongodb shell", "mongo shell",
        "mongodb documents", "mongodb collections", "mongodb database",
        "mongodb query", "mongodb aggregation", "mongodb pipeline",
        "mongodb indexing", "mongodb performance", "mongodb optimization",
        "mongodb sharding", "mongodb cluster", "mongodb replica set",
        "mongodb high availability", "mongodb backup", "mongodb restore",
        "mongodb transactions", "mongodb acid", "mongodb multi-document",
        "mongodb mongoose", "mongodb driver", "mongodb python", "mongodb nodejs",
        "mongodb java", "mongodb go", "mongodb ruby", "mongodb php",
        "mongodb atlas search", "mongodb search", "mongodb full-text",
        "mongodb geospatial", "mongodb gis", "mongodb time series",
        "mongodb change streams", "mongodb triggers", "mongodb realm",
        "mongodb stitch", "mongodb charts", "mongodb bi", "mongodb connector"
    ],
    
    "redis": [
        "redis", "redis cache", "redis server", "redis enterprise", "redis cluster",
        "redis 5", "redis 6", "redis 7", "redis 7.2", "redis 7.4",
        "redis data types", "redis strings", "redis hashes", "redis lists",
        "redis sets", "redis sorted sets", "redis streams", "redis geospatial",
        "redis pubsub", "redis publish subscribe", "redis messaging",
        "redis queue", "redis task queue", "redis job queue", "redis bull",
        "redis celery", "redis sidekiq", "redis resque", "redis delayed",
        "redis caching", "redis cache strategy", "redis invalidation",
        "redis session", "redis session store", "redis authentication",
        "redis rate limiting", "redis throttling", "redis counter",
        "redis leaderboard", "redis ranking", "redis real-time",
        "redis persistence", "redis rdb", "redis aof", "redis snapshot",
        "redis replication", "redis replica", "redis sentinel",
        "redis cluster mode", "redis sharding", "redis partitioning",
        "redis lua scripting", "redis transactions", "redis atomic",
        "redis performance", "redis monitoring", "redis metrics",
        "redis commander", "redis insight", "redis-cli", "redis benchmark",
        "python redis", "redis-py", "node redis", "ioredis", "jedis", "lettuce"
    ],
    
    "elasticsearch": [
        "elasticsearch", "es", "elastic search", "elasticsearch 7", "elasticsearch 8",
        "elasticsearch cluster", "elasticsearch node", "elasticsearch index",
        "elasticsearch shard", "elasticsearch replica", "elasticsearch mapping",
        "elasticsearch document", "elasticsearch query", "elasticsearch dsl",
        "elasticsearch bool", "elasticsearch match", "elasticsearch term",
        "elasticsearch range", "elasticsearch aggregate", "elasticsearch aggregation",
        "elasticsearch metrics", "elasticsearch bucket", "elasticsearch pipeline",
        "elasticsearch sort", "elasticsearch scoring", "elasticsearch relevance",
        "elasticsearch fuzzy", "elasticsearch suggest", "elasticsearch autocomplete",
        "elasticsearch geo", "elasticsearch geospatial", "elasticsearch distance",
        "elasticsearch highlight", "elasticsearch source", "elasticsearch scripting",
        "elasticsearch painless", "elasticsearch ingest", "elasticsearch pipeline",
        "elasticsearch logstash", "elasticsearch kibana", "elk", "elk stack",
        "elasticsearch beats", "filebeat", "metricbeat", "heartbeat", "auditbeat",
        "elasticsearch security", "elasticsearch authentication", "elasticsearch ssl",
        "elasticsearch performance", "elasticsearch tuning", "elasticsearch monitoring",
        "elasticsearch cloud", "elastic cloud", "aws elasticsearch", "opensearch",
        "elasticsearch python", "elasticsearch-py", "elasticsearch.js", "elasticsearch go"
    ],
    
    "cassandra": [
        "cassandra", "apache cassandra", "cassandra db", "cassandra 3", "cassandra 4",
        "cassandra 5", "cassandra cluster", "cassandra node", "cassandra rack",
        "cassandra datacenter", "cassandra ring", "cassandra token", "cassandra partition",
        "cassandra keyspace", "cassandra table", "cassandra column family",
        "cassandra cql", "cassandra query", "cassandra select", "cassandra insert",
        "cassandra update", "cassandra delete", "cassandra cqlsh", "cql shell",
        "cassandra replication", "cassandra replication factor", "cassandra consistency",
        "cassandra eventual consistency", "cassandra quorum", "cassandra read",
        "cassandra write", "cassandra batch", "cassandra lightweight",
        "cassandra paxos", "cassandra gossip", "cassandra snitch",
        "cassandra compaction", "cassandra streaming", "cassandra repair",
        "cassandra backup", "cassandra restore", "cassandra nodetool",
        "cassandra monitoring", "cassandra metrics", "cassandra performance",
        "cassandra tuning", "cassandra driver", "cassandra python", "cassandra java",
        "cassandra nodejs", "cassandra go", "cassandra cql3", "cassandra scylla",
        "cassandra dse", "cassandra opscenter", "cassandra datastax"
    ],
    
    "dynamodb": [
        "dynamodb", "aws dynamodb", "dynamo db", "amazon dynamodb",
        "dynamodb table", "dynamodb item", "dynamodb document", "dynamodb key",
        "dynamodb partition key", "dynamodb sort key", "dynamodb primary key",
        "dynamodb secondary index", "dynamodb gsi", "dynamodb lsi",
        "dynamodb global table", "dynamodb on-demand", "dynamodb provisioned",
        "dynamodb read capacity", "dynamodb write capacity", "dynamodb throughput",
        "dynamodb auto-scaling", "dynamodb transaction", "dynamodb acid",
        "dynamodb batch", "dynamodb query", "dynamodb scan", "dynamodb filter",
        "dynamodb expression", "dynamodb projection", "dynamodb condition",
        "dynamodb atomic", "dynamodb counter", "dynamodb consistent",
        "dynamodb eventual consistency", "dynamodb streams", "dynamodb change data",
        "dynamodb triggers", "dynamodb lambda", "dynamodb incremental",
        "dynamodb sdk", "aws-sdk-dynamodb", "python dynamodb", "boto3 dynamodb",
        "nodejs dynamodb", "dynamoose", "dynamodb-local", "dynamodb emulator",
        "dynamodb backup", "dynamodb point-in-time", "dynamodb restore",
        "dynamodb export", "dynamodb import", "dynamodb data pipeline"
    ],
    
    "sqlite": [
        "sqlite", "sqlite3", "sqlite database", "sqlite 3.35", "sqlite 3.40",
        "sqlite 3.45", "sqlite 3.46", "sqlite embedded", "sqlite local",
        "sqlite temp", "sqlite memory", "sqlite in-memory", "sqlite file",
        "sqlite query", "sqlite select", "sqlite insert", "sqlite update", "sqlite delete",
        "sqlite join", "sqlite inner", "sqlite left", "sqlite outer",
        "sqlite index", "sqlite view", "sqlite trigger", "sqlite transaction",
        "sqlite acid", "sqlite rolling", "sqlite wal", "sqlite journal",
        "sqlite pragma", "sqlite optimize", "sqlite vacuum", "sqlite analyze",
        "sqlite backup", "sqlite restore", "sqlite dump", "sqlite import",
        "sqlite export", "sqlite csv", "sqlite json", "sqlite full text",
        "sqlite fts", "sqlite fts5", "sqlite virtual", "sqlite vfs",
        "sqlite extension", "sqlite python", "sqlite3 python", "sqlite nodejs",
        "sqlite java", "sqlite go", "sqlite c", "sqlite cpp", "sqlite gui",
        "sqlite browser", "sqlite studio", "sqlite admin", "dbeaver",
        "sqlite backup", "sqlite recovery", "sqlite corruption"
    ],
    
    "oracle": [
        "oracle", "oracle db", "oracle database", "oracle sql", "oracle 19c",
        "oracle 21c", "oracle 23c", "oracle 23ai", "oracle enterprise",
        "oracle standard", "oracle express", "oracle xe", "oracle cloud",
        "oracle autonomous", "oracle aws", "oracle azure", "oracle gcp",
        "oracle pl/sql", "oracle procedural", "oracle packages",
        "oracle stored procedure", "oracle function", "oracle trigger",
        "oracle view", "oracle materialized view", "oracle partition",
        "oracle index", "oracle bitmap", "oracle function-based",
        "oracle cluster", "oracle hash", "oracle range", "oracle list",
        "oracle transaction", "oracle acid", "oracle locking",
        "oracle sqlplus", "oracle sql developer", "oracle sqldeveloper",
        "oracle toad", "oracle data pump", "oracle impdp", "oracle expdp",
        "oracle rman", "oracle backup", "oracle restore", "oracle recovery",
        "oracle dataguard", "oracle rac", "oracle grid", "oracle asm",
        "oracle performance", "oracle tuning", "oracle explain plan",
        "oracle awr", "oracle statspack", "oracle oem", "oracle cloud control"
    ],
    
    "mssql": [
        "mssql", "sql server", "microsoft sql", "ms sql", "sql server 2016",
        "sql server 2017", "sql server 2019", "sql server 2022", "azure sql",
        "sql server management studio", "ssms", "sql server agent",
        "sql server integration services", "ssis", "sql server analysis services",
        "ssas", "sql server reporting services", "ssrs", "sql server replication",
        "sql server alwayson", "sql server availability", "sql server cluster",
        "sql server backup", "sql server restore", "sql server recovery",
        "sql server performance", "sql server tuning", "sql server index",
        "sql server columnstore", "sql server memory", "sql server in-memory",
        "sql server query store", "sql server plan", "sql server optimization",
        "sql server deadlock", "sql server blocking", "sql server troubleshooting",
        "sql server transact-sql", "t-sql", "stored procedure", "function",
        "sql server triggers", "sql server views", "sql server partitioning",
        "sql server sharding", "sql server linked server", "sql server polybase",
        "sql server power bi", "sql server analysis", "sql server dw", "sql server etl",
        "sql server containerdb", "sql server docker", "sql server linux"
    ],
    
    "firebase": [
        "firebase", "firebase realtime", "firestore", "firebase firestore",
        "firebase auth", "firebase authentication", "firebase email/password",
        "firebase google", "firebase facebook", "firebase twitter", "firebase github",
        "firebase anonymous", "firebase custom token", "firebase security",
        "firebase rules", "firebase storage", "firebase file storage",
        "firebase hosting", "firebase deploy", "firebase site",
        "firebase functions", "firebase cloud functions", "firebase serverless",
        "firebase triggers", "firebase events", "firebase analytics",
        "firebase crashlytics", "firebase crash reporting", "firebase performance",
        "firebase monitoring", "firebase realtime database", "rtdb",
        "firebase query", "firebase filters", "firebase sorting",
        "firebase listen", "firebase realtime listener", "firebase offline",
        "firebase sdk", "firebase web sdk", "firebase android", "firebase ios",
        "firebase unity", "firebase admin", "firebase admin sdk",
        "firebase config", "firebase remote config", "firebase ab testing",
        "firebase notifications", "firebase cloud messaging", "fcm",
        "firebase in-app messaging", "firebase dynamic links",
        "firebase authentication", "firebase token", "firebase uid"
    ],
    
    "neo4j": [
        "neo4j", "neo4j graph", "graph database", "neo4j 4", "neo4j 5",
        "neo4j enterprise", "neo4j community", "neo4j aura", "neo4j cloud",
        "neo4j cypher", "cypher query", "neo4j query", "neo4j match",
        "neo4j create", "neo4j update", "neo4j delete", "neo4j merge",
        "neo4j optional match", "neo4j where", "neo4j order by",
        "neo4j limit", "neo4j skip", "neo4j return", "neo4j with",
        "neo4j unwind", "neo4j collect", "neo4j count", "neo4j sum",
        "neo4j avg", "neo4j min", "neo4j max", "neo4j distinct",
        "neo4j node", "neo4j relationship", "neo4j property",
        "neo4j label", "neo4j index", "neo4j constraint",
        "neo4j transaction", "neo4j acid", "neo4j backup", "neo4j restore",
        "neo4j driver", "neo4j python", "neo4j java", "neo4j nodejs",
        "neo4j go", "neo4j spring", "neo4j bolt", "neo4j http",
        "neo4j bloom", "neo4j graphql", "neo4j recommendations",
        "neo4j social graph", "neo4j fraud detection", "neo4j knowledge graph"
    ],
    
    # ============================================================
    # 6. CLOUD PLATFORMS
    # ============================================================
    
    "aws": [
        "aws", "amazon web services", "aws cloud", "aws platform",
        "ec2", "elastic compute cloud", "s3", "simple storage service",
        "lambda", "aws lambda", "serverless", "aws serverless",
        "rds", "relational database service", "dynamodb", "cloudfront",
        "route53", "vpc", "virtual private cloud", "iam", "identity access management",
        "cloudformation", "cloudwatch", "sns", "simple notification service",
        "sqs", "simple queue service", "kinesis", "glue", "emr", "elastic mapreduce",
        "athena", "quicksight", "sagemaker", "redshift", "elasticache",
        "opensearch", "aws amplify", "app runner", "ecs", "elastic container service",
        "eks", "elastic kubernetes service", "fargate", "api gateway",
        "aws batch", "step functions", "elastic beanstalk", "lightsail",
        "outposts", "snowball", "snowmobile", "directory service",
        "cognito", "amplify", "appsync", "serverless app", "sam",
        "aws cdk", "cloud development kit", "aws cli", "aws sdk",
        "boto3", "aws python", "aws java", "aws nodejs", "aws go", "aws rust",
        "well-architected", "aws certification", "aws solutions architect"
    ],
    
    "azure": [
        "azure", "microsoft azure", "azure cloud", "azure platform",
        "azure functions", "azure app service", "azure sql", "azure sql database",
        "azure cosmos db", "azure blob storage", "azure file storage",
        "azure kubernetes", "aks", "azure container", "azure container instances",
        "azure devops", "azure pipelines", "azure repos", "azure boards",
        "azure test plans", "azure artifacts", "azure data factory",
        "azure databricks", "azure synapse", "azure ml", "azure machine learning",
        "azure cognitive services", "azure openai", "azure speech",
        "azure vision", "azure language", "azure translator", "azure ad",
        "azure active directory", "azure b2c", "azure b2b", "azure iam",
        "azure virtual machines", "azure scale sets", "azure load balancer",
        "azure application gateway", "azure cdn", "azure front door",
        "azure traffic manager", "azure dns", "azure cosmos", "azure table storage",
        "azure queue storage", "azure service bus", "azure event grid",
        "azure event hub", "azure iot hub", "azure iot central",
        "azure logic apps", "azure automation", "azure backup", "azure site recovery",
        "azure monitor", "azure log analytics", "azure application insights",
        "azure sentinel", "azure defender", "azure key vault", "azure storage account"
    ],
    
    "gcp": [
        "gcp", "google cloud", "google cloud platform", "gcloud",
        "compute engine", "gce", "cloud run", "cloud functions",
        "app engine", "cloud storage", "persistent disk", "cloud sql",
        "cloud spanner", "cloud firestore", "cloud bigtable", "cloud datastore",
        "bigquery", "big query", "pub/sub", "dataflow", "dataproc",
        "cloud composer", "airflow", "vertex ai", "ai platform",
        "automl", "vision api", "speech api", "language api", "translation api",
        "dialogflow", "dialogflow cx", "natural language", "recommendations ai",
        "kubernetes engine", "gke", "anthos", "cloud shell", "cloud console",
        "cloud iam", "cloud identity", "cloud armor", "cloud cdn",
        "cloud load balancing", "cloud networking", "vpc", "cloud vpn",
        "cloud interconnect", "cloud endpoints", "api gateway",
        "cloud scheduler", "cloud tasks", "cloud workflows", "cloud functions",
        "cloud logging", "cloud monitoring", "cloud trace", "cloud profiler",
        "cloud debugger", "cloud error reporting", "cloud alerting",
        "cloud deployment manager", "terraform", "gcloud cli", "google cloud sdk",
        "python gcp", "nodejs gcp", "java gcp", "go gcp", "rust gcp"
    ],
    
    # ============================================================
    # 7. DEVOPS & CONTAINERIZATION
    # ============================================================
    
    "docker": [
        "docker", "docker container", "docker image", "dockerfile",
        "docker compose", "docker compose", "docker-compose", "dockerhub",
        "docker hub", "docker registry", "docker engine", "docker desktop",
        "docker swarm", "docker swarm mode", "docker stack",
        "docker build", "docker run", "docker push", "docker pull",
        "docker ps", "docker stop", "docker start", "docker restart",
        "docker rm", "docker rmi", "docker exec", "docker logs",
        "docker inspect", "docker stats", "docker network",
        "docker volume", "docker bind", "docker overlay", "docker bridge",
        "docker host", "docker daemon", "docker cli", "docker api",
        "docker registry", "docker private registry", "docker ecr",
        "docker acr", "docker gcr", "docker caching", "docker multi-stage",
        "docker optimization", "docker security", "docker scan",
        "docker buildkit", "docker buildx", "docker rootless",
        "containerization", "container runtime", "oci", "open container",
        "containerd", "cri-o", "podman", "buildah", "skopeo"
    ],
    
    "kubernetes": [
        "kubernetes", "k8s", "kube", "kubectl", "kubelet",
        "aks", "azure kubernetes", "eks", "aws kubernetes", "gke", "google kubernetes",
        "k3s", "minikube", "kind", "kubefed", "kubeadm", "kubeconfig",
        "kubernetes cluster", "kubernetes node", "kubernetes pod",
        "kubernetes service", "kubernetes deployment", "kubernetes statefulset",
        "kubernetes daemonset", "kubernetes job", "kubernetes cronjob",
        "kubernetes configmap", "kubernetes secret", "kubernetes volume",
        "kubernetes persistent volume", "kubernetes pv", "kubernetes pvc",
        "kubernetes storage class", "kubernetes ingress", "kubernetes ingress controller",
        "kubernetes load balancer", "kubernetes service mesh", "kubernetes istio",
        "kubernetes envoy", "kubernetes gateway", "kubernetes api",
        "kubernetes controller", "kubernetes operator", "kubernetes helm",
        "kubernetes charts", "kubernetes repo", "kubernetes rancher",
        "kubernetes monitoring", "kubernetes metrics", "kubernetes prometheus",
        "kubernetes grafana", "kubernetes logging", "kubernetes elk",
        "kubernetes security", "kubernetes rbac", "kubernetes authentication",
        "kubernetes authorization", "kubernetes admission", "kubernetes webhook",
        "container orchestration", "cluster management", "orchestration tool"
    ],
    
    "jenkins": [
        "jenkins", "jenkins ci", "jenkins pipeline", "jenkins server",
        "jenkins master", "jenkins slave", "jenkins agent", "jenkins node",
        "jenkinsfile", "jenkins groovy", "jenkins plugins", "jenkins configuration",
        "jenkins build", "jenkins job", "jenkins stages", "jenkins steps",
        "jenkins triggers", "jenkins schedule", "jenkins hooks", "jenkins webhooks",
        "jenkins integration", "jenkins github", "jenkins gitlab", "jenkins bitbucket",
        "jenkins docker", "jenkins kubernetes", "jenkins agents",
        "jenkins declarative", "jenkins scripted", "jenkins shared library",
        "jenkins blue ocean", "jenkins blueocean", "jenkins monitoring",
        "jenkins backup", "jenkins restore", "jenkins security", "jenkins authentication",
        "jenkins authorization", "jenkins plugins", "jenkins pipeline as code",
        "jenkins multibranch", "jenkins folder", "jenkins organization",
        "ci/cd", "continuous integration", "continuous delivery",
        "continuous deployment", "build automation", "ci pipeline"
    ],
    
    "git": [
        "git", "git version control", "git scm", "git cli",
        "git bash", "git init", "git clone", "git add", "git commit",
        "git push", "git pull", "git fetch", "git remote", "git branch",
        "git checkout", "git merge", "git rebase", "git cherry-pick",
        "git revert", "git reset", "git stash", "git tag", "git log",
        "git diff", "git status", "git show", "git grep", "git blame",
        "git bisect", "git worktree", "git submodule", "git-lfs",
        "git flow", "git hooks", "git attributes", "git config",
        "git lfs", "git credential", "git ssh", "git https", "git protocol",
        "git fetch", "git rebase interactive", "git squash",
        "git fast-forward", "git merge conflict", "git diff merge",
        "git pre-commit", "git pre-push", "git post-commit",
        "git workflow", "github", "gitlab", "bitbucket", "git hosting"
    ],
    
    "github": [
        "github", "github actions", "gh", "github ci",
        "github enterprise", "github cloud", "github repository",
        "github repo", "github clone", "github fork", "github pull request",
        "github pr", "github issues", "github discussions", "github wiki",
        "github pages", "github pages site", "github codespaces",
        "github packages", "github registry", "github container registry",
        "github npm", "github maven", "github docker", "github actions workflow",
        "github actions yaml", "github actions matrix", "github actions cache",
        "github actions artifact", "github actions secret", "github actions env",
        "github actions self-hosted", "github actions runner", "github apps",
        "github oauth", "github api", "github graphql api", "github rest api",
        "github webhook", "github cli", "github desktop", "github mobile",
        "github copilot", "github copilot chat", "github spark", "github gist",
        "github security", "github dependabot", "github codeql",
        "github secret scanning", "github vulnerability", "github advisories"
    ],
    
    "gitlab": [
        "gitlab", "gitlab ci", "gitlab runner", "gitlab pipeline",
        "gitlab devops", "gitlab cloud", "gitlab self-hosted",
        "gitlab repository", "gitlab repo", "gitlab merge request",
        "gitlab mr", "gitlab issues", "gitlab epics", "gitlab boards",
        "gitlab milestones", "gitlab labels", "gitlab wiki", "gitlab snippets",
        "gitlab pages", "gitlab registry", "gitlab container registry",
        "gitlab npm", "gitlab docker", "gitlab ci job", "gitlab ci stages",
        "gitlab ci yaml", "gitlab ci templates", "gitlab ci cache",
        "gitlab ci artifacts", "gitlab ci variables", "gitlab ci secrets",
        "gitlab ci environment", "gitlab ci review app", "gitlab ci canary",
        "gitlab ci feature flags", "gitlab ci auto-devops", "gitlab ci kubernetes",
        "gitlab ci aws", "gitlab ci azure", "gitlab ci gcp", "gitlab api",
        "gitlab graphql", "gitlab rest api", "gitlab webhook", "gitlab cli",
        "gitlab terraform", "gitlab security", "gitlab vulnerability",
        "gitlab dependency scanning", "gitlab container scanning",
        "gitlab secret detection", "gitlab compliance", "gitlab audit"
    ],
    
    "terraform": [
        "terraform", "tf", "terraform cloud", "terraform enterprise",
        "terraform cli", "terraform init", "terraform plan", "terraform apply",
        "terraform destroy", "terraform refresh", "terraform state", "terraform import",
        "terraform output", "terraform module", "terraform provider",
        "terraform aws provider", "terraform azure", "terraform gcp",
        "terraform kubernetes", "terraform docker", "terraform github",
        "terraform gitlab", "terraform vault", "terraform hcl", "terraform language",
        "terraform variables", "terraform outputs", "terraform resources",
        "terraform data sources", "terraform locals", "terraform modules",
        "terraform remote state", "terraform backend", "terraform s3",
        "terraform dynamodb", "terraform workspaces", "terraform environment",
        "terraform lock", "terraform version", "terraform upgrade",
        "terraform validate", "terraform fmt", "terraform graph",
        "terraform apply plan", "terraform automated", "terraform pipeline",
        "terraform ci/cd", "terraform best practices", "terraform patterns",
        "terraform iac", "infrastructure as code", "iac", "infrastructure automation"
    ],
    
    "ansible": [
        "ansible", "ansible playbook", "ansible tower", "ansible automation",
        "ansible roles", "ansible inventory", "ansible galaxy", "ansible hub",
        "ansible modules", "ansible tasks", "ansible handlers", "ansible vars",
        "ansible facts", "ansible templates", "ansible jinja2", "ansible yaml",
        "ansible playbook run", "ansible ad-hoc", "ansible command",
        "ansible shell", "ansible copy", "ansible file", "ansible git",
        "ansible docker", "ansible kubernetes", "ansible aws", "ansible azure",
        "ansible gcp", "ansible vmware", "ansible windows", "ansible linux",
        "ansible networking", "ansible cisco", "ansible juniper", "ansible arista",
        "ansible cloud", "ansible configuration", "ansible deployment",
        "ansible orchestration", "ansible idempotency", "ansible testing",
        "ansible molecule", "ansible lint", "ansible syntax-check",
        "ansible vault", "ansible encryption", "ansible secrets",
        "ansible tags", "ansible limit", "ansible become", "ansible user",
        "ansible prompt", "ansible retry", "ansible diff", "ansible check-mode"
    ],
    
    "prometheus": [
        "prometheus", "promql", "prometheus metrics", "prometheus monitoring",
        "prometheus exporter", "prometheus node exporter", "prometheus blackbox exporter",
        "prometheus mysql exporter", "prometheus postgres exporter", "prometheus redis exporter",
        "prometheus mongodb exporter", "prometheus rabbitmq exporter", "prometheus nginx exporter",
        "prometheus docker exporter", "prometheus kubernetes exporter", "prometheus cAdvisor",
        "prometheus alertmanager", "prometheus alert", "prometheus rules",
        "prometheus recording", "prometheus federation", "prometheus remote",
        "prometheus storage", "prometheus tsdb", "prometheus retention",
        "prometheus scrape", "prometheus target", "prometheus endpoint",
        "prometheus job", "prometheus instance", "prometheus relabel",
        "prometheus service discovery", "prometheus kubernetes sd",
        "prometheus ec2 discovery", "prometheus gce discovery", "prometheus azure discovery",
        "prometheus consul", "prometheus etcd", "prometheus kube-state-metrics",
        "prometheus metrics endpoint", "prometheus health", "prometheus performance",
        "prometheus high availability", "prometheus replication", "prometheus sharding",
        "prometheus thanos", "prometheus cortex", "prometheus mimir", "prometheus victoriametrics",
        "observability", "monitoring", "metrics", "timeseries", "alerting"
    ],
    
    "grafana": [
        "grafana", "grafana dashboard", "grafana cloud", "grafana enterprise",
        "grafana panels", "grafana graphs", "grafana tables", "grafana stats",
        "grafana metrics", "grafana logging", "grafana tracing", "grafana observability",
        "grafana prometheus", "grafana prometheus datasource", "grafana promql",
        "grafana loki", "grafana log aggregation", "grafana logql",
        "grafana tempo", "grafana tracing", "grafana pyroscope", "grafana profiling",
        "grafana plugins", "grafana alerts", "grafana notifications",
        "grafana annotations", "grafana variables", "grafana templating",
        "grafana teams", "grafana folders", "grafana users", "grafana permissions",
        "grafana api", "grafana provisioning", "grafana docker", "grafana kubernetes",
        "grafana datasource", "grafana mysql", "grafana postgres", "grafana elasticsearch",
        "grafana graphql", "grafana infinity", "grafana bigquery", "grafana snowflake",
        "grafana analytics", "grafana monitoring", "grafana alertmanager",
        "grafana grafana-labs", "grafana dashboard as code", "grafana helm",
        "observability", "visualization", "dashboards", "monitoring"
    ],
    
    "argo": [
        "argo", "argo cd", "argo workflows", "argo rollouts",
        "argo events", "argo cd app", "argo cd application",
        "argo cd sync", "argo cd deployment", "argo cd rollback",
        "argo cd repo", "argo cd repository", "argo cd git",
        "argo cd manifest", "argo cd yaml", "argo cd webhook",
        "argo cd cluster", "argo cd server", "argo cd ui",
        "argo cd cli", "argo cd api", "argo cd notifications",
        "argo cd alerts", "argo cd monitoring", "argo cd prometheus",
        "argo workflow dag", "argo workflow steps", "argo workflow template",
        "argo workflow archive", "argo workflow ui", "argo workflow logging",
        "argo rollouts blue-green", "argo rollouts canary", "argo rollouts analysis",
        "argo rollouts progressive", "argo rollouts traffic", "argo rollouts istio",
        "argo events webhook", "argo events trigger", "argo events sensor",
        "argo events gateway", "argo events bus", "argo events event-source",
        "argo cd decapod", "argo cd sealed-secrets", "argo cd kustomize",
        "argo cd helm", "argo cd jsonnet", "argo cd plugin", "gitops",
        "continuous deployment", "cd", "progressive delivery"
    ],
    
    # ============================================================
    # 8. MESSAGE QUEUES & STREAMING
    # ============================================================
    
    "kafka": [
        "kafka", "apache kafka", "confluent", "confluent kafka",
        "kafka streaming", "kafka stream", "kafka connect", "kafka connector",
        "kafka producer", "kafka consumer", "kafka broker", "kafka cluster",
        "kafka topics", "kafka partition", "kafka offset", "kafka consumer group",
        "kafka replication", "kafka lag", "kafka monitor", "kafka manager",
        "kafka schema registry", "kafka avro", "kafka protobuf", "kafka json",
        "kafka rest proxy", "kafka admin", "kafka operations", "kafka zookeeper",
        "kafka kraft", "kafka native", "kafka eos", "kafka exactly-once",
        "kafka transactions", "kafka idempotent", "kafka compression",
        "kafka security", "kafka ssl", "kafka sasl", "kafka auth", "kafka acl",
        "kafka connect source", "kafka connect sink", "kafka jdbc",
        "kafka elasticsearch", "kafka s3", "kafka bigquery", "kafka redshift",
        "kafka snowflake", "kafka mongodb", "kafka cassandra", "kafka postgres",
        "kafka debezium", "kafka cdc", "kafka event streaming", "event-driven"
    ],
    
    "rabbitmq": [
        "rabbitmq", "rabbit mq", "rabbit", "rabbitmq broker",
        "rabbitmq queue", "rabbitmq exchange", "rabbitmq binding",
        "rabbitmq producer", "rabbitmq consumer", "rabbitmq publisher",
        "rabbitmq subscriber", "rabbitmq channel", "rabbitmq connection",
        "rabbitmq vhost", "rabbitmq virtual host", "rabbitmq user",
        "rabbitmq permissions", "rabbitmq management", "rabbitmq ui",
        "rabbitmq api", "rabbitmq clustering", "rabbitmq mirror",
        "rabbitmq ha", "rabbitmq high availability", "rabbitmq quorum",
        "rabbitmq stream", "rabbitmq plugin", "rabbitmq shovel",
        "rabbitmq federation", "rabbitmq upstream", "rabbitmq downstream",
        "rabbitmq dead letter", "rabbitmq ttl", "rabbitmq delay",
        "rabbitmq scheduled", "rabbitmq priority", "rabbitmq persistent",
        "rabbitmq durable", "rabbitmq exclusive", "rabbitmq auto-delete",
        "rabbitmq confirm", "rabbitmq ack", "rabbitmq nack", "rabbitmq reject",
        "rabbitmq prefetch", "rabbitmq qos", "rabbitmq monitoring",
        "rabbitmq metrics", "rabbitmq prometheus", "rabbitmq grafana",
        "amqp", "amqp 0-9-1", "amqp 1.0", "message queue", "mq"
    ],
    
    # ============================================================
    # 9. TESTING FRAMEWORKS
    # ============================================================
    
    "junit": [
        "junit", "junit4", "junit5", "jupiter", "junit vintage",
        "junit assertions", "junit test", "junit test runner",
        "junit suite", "junit category", "junit tags", "junit params",
        "junit parameterized", "junit dynamic test", "junit test factory",
        "junit mocks", "mockito", "powermock", "jmockit",
        "junit hamcrest", "assertj", "testng", "spring test",
        "spring boot test", "integration test", "unit test",
        "test coverage", "jacoco", "cobertura", "sonarqube",
        "junit reporting", "junit xml", "junit html", "junit console",
        "junit ci", "junit jenkins", "junit gradle", "junit maven"
    ],
    
    "pytest": [
        "pytest", "py test", "python testing", "pytest framework",
        "pytest fixtures", "pytest markers", "pytest parametrize",
        "pytest skip", "pytest xfail", "pytest timeout", "pytest coverage",
        "pytest mock", "pytest monkeypatch", "pytest tmpdir", "pytest capsys",
        "pytest capfd", "pytest requests", "pytest flask", "pytest django",
        "pytest fastapi", "pytest asyncio", "pytest async", "pytest aiohttp",
        "pytest selenium", "pytest playwright", "pytest api", "pytest integration",
        "pytest unit", "pytest functional", "pytest regression",
        "pytest html", "pytest xml", "pytest junit", "pytest ci",
        "pytest github", "pytest gitlab", "pytest jenkins", "pytest caching",
        "pytest parallel", "pytest xdist", "pytest rerun", "pytest flaky",
        "unittest", "doctest", "tox", "coverage.py", "pytest-cov"
    ],
    
    "selenium": [
        "selenium", "selenium webdriver", "selenium grid", "selenium ide",
        "selenium java", "selenium python", "selenium csharp", "selenium ruby",
        "selenium javascript", "selenium nodejs", "selenium php", "selenium go",
        "selenium chrome", "selenium chromedriver", "selenium firefox",
        "selenium geckodriver", "selenium edge", "selenium safari",
        "selenium remote", "selenium server", "selenium standalone",
        "selenium hub", "selenium node", "selenium scale",
        "selenium docker", "selenium grid distributed", "selenium parallel",
        "selenium cross-browser", "selenium testing", "selenium automation",
        "selenium click", "selenium find", "selenium wait", "selenium implicit",
        "selenium explicit", "selenium fluent", "selenium page object",
        "selenium page factory", "selenium actions", "selenium js executor",
        "selenium alerts", "selenium windows", "selenium frames", "selenium iframes",
        "selenium screenshots", "selenium headless", "selenium proxy",
        "webdriver", "browser automation", "ui testing", "e2e testing"
    ],
    
    "cypress": [
        "cypress", "cypress io", "cypress testing", "cypress framework",
        "cypress e2e", "cypress component", "cypress integration",
        "cypress unit", "cypress api", "cypress custom",
        "cypress mocha", "cypress chai", "cypress assertions",
        "cypress hooks", "cypress describe", "cypress it", "cypress before",
        "cypress after", "cypress beforeEach", "cypress afterEach",
        "cypress commands", "cypress custom commands", "cypress fixtures",
        "cypress utils", "cypress plugins", "cypress tasks",
        "cypress retry", "cypress screenshot", "cypress video",
        "cypress parallel", "cypress ci", "cypress github",
        "cypress gitlab", "cypress jenkins", "cypress docker",
        "cypress kubernetes", "cypress dashboard", "cypress cloud",
        "cypress run", "cypress open", "cypress headless", "cypress intercept",
        "cypress mock", "cypress stub", "cypress spy", "cypress clock",
        "cypress network", "cypress requests", "cypress cookies",
        "cypress localstorage", "cypress session", "cypress coverage"
    ],
    
    "jest": [
        "jest", "jest testing", "jest framework", "jest runner",
        "jest dom", "jest assertions", "jest matchers", "jest snapshots",
        "jest coverage", "jest watch", "jest config", "jest cli",
        "jest babel", "jest typescript", "jest esm", "jest module",
        "jest mock", "jest spy", "jest fake", "jest timer",
        "jest describe", "jest it", "jest test", "jest expect",
        "jest toBe", "jest toEqual", "jest toMatch", "jest toThrow",
        "jest async", "jest promises", "jest callback", "jest done",
        "jest before", "jest after", "jest beforeEach", "jest afterEach",
        "jest beforeAll", "jest afterAll", "jest timeout", "jest skip",
        "jest only", "jest retry", "jest reporter", "jest html",
        "jest junit", "jest github", "jest gitlab", "jest jenkins",
        "react jest", "vue jest", "angular jest", "node jest"
    ],
    
    "playwright": [
        "playwright", "playwright testing", "playwright automation",
        "playwright framework", "playwright e2e", "playwright component",
        "playwright browser", "playwright chromium", "playwright firefox",
        "playwright webkit", "playwright devices", "playwright mobile",
        "playwright emulation", "playwright network", "playwright intercept",
        "playwright mock", "playwright stub", "playwright spy",
        "playwright assertions", "playwright expect", "playwright matchers",
        "playwright toHave", "playwright toBe", "playwright wait",
        "playwright selector", "playwright locator", "playwright page",
        "playwright context", "playwright browserContext", "playwright frame",
        "playwright screenshot", "playwright video", "playwright trace",
        "playwright report", "playwright html", "playwright json",
        "playwright junit", "playwright ci", "playwright github",
        "playwright gitlab", "playwright jenkins", "playwright docker",
        "playwright kubernetes", "playwright parallel", "playwright sharding",
        "playwright retry", "playwright flaky", "playwright test-runner",
        "playwright codegen", "playwright inspector", "playwright debug"
    ],
    
    # ============================================================
    # 10. WEB & API TECHNOLOGIES
    # ============================================================
    
    "rest": [
        "rest", "restful", "rest api", "restful api", "restful web service",
        "rest endpoints", "rest resource", "rest methods", "rest verbs",
        "get", "post", "put", "patch", "delete", "head", "options",
        "rest status codes", "http 200", "http 201", "http 204", "http 400",
        "http 401", "http 403", "http 404", "http 422", "http 500",
        "rest versioning", "rest authentication", "rest authorization",
        "rest security", "rest cors", "rest json", "rest xml",
        "rest request", "rest response", "rest body", "rest query",
        "rest path", "rest header", "rest cookie", "rest session",
        "rest token", "rest jwt", "rest oauth", "rest api gateway",
        "rest documentation", "rest swagger", "rest openapi", "rest postman",
        "rest client", "rest server", "rest middleware", "rest controller",
        "rest service", "restful design", "rest principles", "rest constraints"
    ],
    
    "graphql": [
        "graphql", "graph ql", "graphql api", "graphql server",
        "graphql client", "graphql query", "graphql mutation",
        "graphql subscription", "graphql subscription",
        "graphql schema", "graphql type", "graphql object", "graphql input",
        "graphql enum", "graphql union", "graphql interface",
        "graphql scalar", "graphql custom", "graphql directive",
        "graphql resolver", "graphql context", "graphql middleware",
        "graphql authorization", "graphql authentication", "graphql security",
        "graphql caching", "graphql persisted", "graphql batching",
        "graphql federation", "graphql federation 2", "apollo",
        "apollo client", "apollo server", "apollo graphql",
        "apollo federation", "apollo gateway", "apollo studio",
        "relay", "relay graphql", "graphql-js", "graphql-python",
        "graphql-java", "graphql-go", "graphql-ruby", "graphql-php",
        "graphql-csharp", "graphql-dotnet", "graphql-schema",
        "graphql playground", "graphql explorer", "graphiql",
        "hasura", "graphql-engine", "postgraphile", "prisma graphql"
    ],
    
    "grpc": [
        "grpc", "gRPC", "grpc framework", "grpc service",
        "grpc client", "grpc server", "grpc stub", "grpc channel",
        "grpc streaming", "grpc server streaming", "grpc client streaming",
        "grpc bidirectional", "grpc unary", "grpc call", "grpc context",
        "grpc deadline", "grpc timeout", "grpc cancellation",
        "grpc interceptor", "grpc middleware", "grpc auth", "grpc security",
        "grpc tls", "grpc ssl", "grpc compression", "grpc encoding",
        "grpc reflection", "grpc health", "grpc load balancing",
        "grpc service mesh", "grpc envoy", "grpc nginx",
        "grpc gateway", "grpc rest", "grpc web", "grpc node",
        "grpc python", "grpc java", "grpc go", "grpc cpp", "grpc csharp",
        "grpc ruby", "grpc php", "grpc swift", "grpc objc",
        "protobuf", "protocol buffers", "proto3", "protoc",
        "grpc gateway", "grpc streaming", "grpc async", "grpc blocking"
    ],
    
    "websocket": [
        "websocket", "ws", "websocket protocol", "websocket server",
        "websocket client", "websocket connection", "websocket handshake",
        "websocket upgrade", "websocket frame", "websocket message",
        "websocket text", "websocket binary", "websocket ping", "websocket pong",
        "websocket close", "websocket error", "websocket event",
        "websocket onopen", "websocket onmessage", "websocket onerror",
        "websocket onclose", "websocket send", "websocket receive",
        "socket.io", "socketio", "socket.io server", "socket.io client",
        "socket.io room", "socket.io namespace", "socket.io event",
        "socket.io broadcast", "socket.io emit", "socket.io on",
        "websocket secure", "wss", "websocket tls", "websocket ssl",
        "websocket loadbalancing", "websocket cluster", "websocket scaling",
        "websocket debugging", "websocket testing", "websocket tools",
        "real-time", "realtime", "live updates", "push notifications"
    ],
    
    # ============================================================
    # 11. SECURITY
    # ============================================================
    
    "cybersecurity": [
        "cybersecurity", "cyber security", "information security", "infosec",
        "security engineering", "security architecture", "security operations",
        "network security", "application security", "appsec", "cloud security",
        "data security", "endpoint security", "identity security",
        "security monitoring", "incident response", "threat hunting",
        "vulnerability management", "risk assessment", "compliance",
        "audit", "security audit", "penetration testing", "pen test",
        "ethical hacking", "security assessment", "security review",
        "security control", "security framework", "nist", "iso 27001",
        "soc2", "hipaa", "gdpr", "pci", "pci dss", "fedramp",
        "zero trust", "zero-trust", "defense in depth", "least privilege",
        "security training", "security awareness", "phishing", "social engineering",
        "malware", "ransomware", "phishing", "ddos", "protection",
        "firewall", "ids", "ips", "waf", "web application firewall"
    ],
    
    "oauth": [
        "oauth", "oauth2", "oauth2.0", "oauth1", "oauth1.0",
        "oauth authorization", "oauth authentication", "oauth flow",
        "oauth grant", "authorization code", "authorization code flow",
        "implicit flow", "client credentials", "password grant",
        "refresh token", "access token", "id token", "jwt",
        "openid", "openid connect", "oidc", "saml", "sso",
        "single sign-on", "identity provider", "idp", "service provider",
        "sp", "auth0", "auth0 authentication", "okta", "keycloak",
        "identityserver", "oauth server", "oauth client", "oauth scopes",
        "oauth redirect", "oauth callback", "oauth consent", "oauth endpoint",
        "oauth bearer", "oauth mac", "oauth pkce", "oauth proof key",
        "oauth confidentiality", "oauth jws", "oauth jwe",
        "oauth client authentication", "oauth client secret"
    ],
    
    "jwt": [
        "jwt", "json web token", "jwt token", "jwt authentication",
        "jwt authorization", "jwt claims", "jwt header", "jwt payload",
        "jwt signature", "jwt algorithm", "jwt hs256", "jwt rs256",
        "jwt es256", "jwt ps256", "jwt secret", "jwt key",
        "jwt private key", "jwt public key", "jwt verify", "jwt decode",
        "jwt encode", "jwt sign", "jwt expire", "jwt expiration",
        "jwt iat", "jwt nbf", "jwt aud", "jwt iss", "jwt sub",
        "jwt scopes", "jwt permission", "jwt roles", "jwt session",
        "jwt stateless", "jwt refresh", "jwt rotate", "jwt revoke",
        "jwt blacklist", "jwt white list", "jwt version", "jwt security",
        "jwt best practices", "jwt validation", "jwt interceptor",
        "jwt middleware", "jwt filter", "jwt spring security",
        "jsonwebtoken", "jwt-io", "jwt python", "jwt nodejs"
    ],
    
    # ============================================================
    # 12. PROJECT MANAGEMENT & METHODOLOGIES
    # ============================================================
    
    "agile": [
        "agile", "agile methodology", "agile development", "agile framework",
        "agile manifesto", "agile principles", "agile values", "agile practices",
        "scrum", "scrum master", "scrum framework", "scrum team",
        "scrum ceremony", "sprint", "sprint planning", "daily scrum",
        "sprint review", "sprint retrospective", "sprint backlog",
        "product backlog", "user stories", "story points", "velocity",
        "burn-down chart", "burnup chart", "kanban", "kanban board",
        "kanban methodology", "wip", "work in progress", "lean",
        "lean development", "lean startup", "xp", "extreme programming",
        "pair programming", "tdd", "test driven development", "bdd",
        "behavior driven development", "continuous delivery", "continuous deployment",
        "pivotal tracker", "jira", "trello", "asana", "monday.com",
        "linear", "notion", "clickup", "sprint management", "backlog grooming"
    ],
    
    # ============================================================
    # 13. MONITORING & OBSERVABILITY
    # ============================================================
    
    "monitoring": [
        "monitoring", "observability", "observability stack",
        "metrics", "logs", "traces", "distributed tracing",
        "prometheus", "grafana", "datadog", "newrelic", "dynatrace",
        "appdynamics", "instana", "splunk", "elastic", "elasticsearch",
        "logstash", "kibana", "elk", "elastic stack", "sumologic",
        "loggly", "papertrail", "logz.io", "sentinel", "azure monitor",
        "cloudwatch", "aws cloudwatch", "stackdriver", "google cloud monitoring",
        "azure monitor", "opentelemetry", "otel", "jaeger", "zipkin",
        "tempo", "loki", "fluentd", "fluentbit", "vector", "telegraf",
        "statsd", "graphite", "influxdb", "telegraf", "chronograf",
        "kapacitor", "tick stack", "promql", "logql", "traceql"
    ],
    
    "logging": [
        "logging", "log management", "log aggregation", "log analysis",
        "log collection", "log processing", "log storage", "log retention",
        "log rotation", "log compression", "log shipping", "log parsing",
        "log structured", "json logging", "log levels", "debug",
        "info", "warn", "error", "fatal", "trace", "audit log",
        "access log", "error log", "system log", "application log",
        "security log", "transaction log", "slow query log", "binary log",
        "elb log", "cloudfront log", "s3 log", "github log", "jenkins log",
        "kafka log", "elasticsearch log", "postgres log", "mysql log",
        "nginx log", "apache log", "docker log", "kubernetes log",
        "log4j", "logback", "log4net", "log4php", "log4javascript",
        "winston", "pino", "bunyan", "logrus", "zap", "zerolog",
        "serilog", "nlog", "logback", "fluentd", "logstash", "vector"
    ],
    
    # ============================================================
    # 14. COMPOUND & MISCELLANEOUS
    # ============================================================
    
    "full_stack": [
        "full stack", "fullstack", "full-stack", "full stack developer",
        "fullstack developer", "full-stack developer", "full stack engineer",
        "frontend", "backend", "database", "devops", "api", "ui/ux",
        "end-to-end", "e2e", "front-end", "back-end", "server-side",
        "client-side", "web development", "app development",
        "frontend development", "backend development", "full stack engineering"
    ],
    
    "microservices": [
        "microservices", "microservice", "micro service", "microservices architecture",
        "microservices development", "microservices design", "service oriented architecture",
        "soa", "service mesh", "distributed systems", "distributed architecture",
        "api gateway", "circuit breaker", "service discovery", "load balancing",
        "event-driven architecture", "eda", "choreography", "orchestration",
        "resilience", "fault tolerance", "retry", "timeout", "rate limiting",
        "bulkhead", "health check", "liveness", "readiness", "monitoring",
        "tracing", "distributed logging", "docker", "kubernetes", "spring cloud",
        "netflix oss", "eureka", "ribbon", "feign", "hystrix", "zuul"
    ],
    
    "serverless": [
        "serverless", "serverless architecture", "serverless computing",
        "faas", "function as a service", "aws lambda", "azure functions",
        "google cloud functions", "cloudflare workers", "vercel", "netlify",
        "apigateway", "event-driven", "pay-per-use", "auto-scaling",
        "cold start", "warm start", "timeout", "memory", "concurrency",
        "iam", "vpc", "environment variables", "layers", "extensions",
        "dependency injection", "serverless framework", "serverless.yml",
        "sam", "serverless application model", "cdk", "pulumi",
        "event bridge", "kinesis", "s3 events", "api gateway",
        "webhook", "cron", "schedule", "queue", "stream", "database",
        "nosql", "firestore", "dynamodb", "mongodb atlas", "rds"
    ],
    
    "ci_cd": [
        "ci/cd", "ci", "cd", "continuous integration", "continuous delivery",
        "continuous deployment", "build automation", "release automation",
        "pipeline", "pipeline as code", "jenkins", "gitlab ci", "github actions",
        "bitbucket pipelines", "circleci", "travis ci", "teamcity",
        "bamboo", "buildkite", "azure pipelines", "aws codepipeline",
        "google cloud build", "drone", "argo", "flux", "spinnaker",
        "automated testing", "unit tests", "integration tests", "e2e tests",
        "code coverage", "sonarqube", "quality gates", "security scanning",
        "dependency scanning", "container scanning", "deployment automation",
        "rollback", "canary", "blue/green", "a/b testing", "feature flag",
        "release management", "versioning", "branching", "tagging", "artifacts"
    ],
    
    "api_gateway": [
        "api gateway", "aws api gateway", "azure api management",
        "google api gateway", "kong", "nginx", "envoy", "traefik",
        "ambassador", "gloo", "tyk", "gravitee", "krakenD", "oracle api gateway",
        "route", "proxy", "reverse proxy", "load balancer", "rate limiting",
        "authentication", "authorization", "jwt", "oauth2", "api key",
        "monitoring", "logging", "analytics", "caching", "error handling",
        "timeout", "retry", "circuit breaker", "api versioning", "canary",
        "blue/green", "ssl", "tls", "certificate", "security", "web firewall"
    ],
    
    "blockchain": [
        "blockchain", "blockchain technology", "distributed ledger",
        "ethereum", "eth", "smart contract", "solidity", "web3",
        "web3.js", "ethers.js", "bitcoin", "btc", "hyperledger",
        "fabric", "corda", "quorum", "polygon", "matic", "bsc",
        "binance smart chain", "solana", "avalanche", "near",
        "cosmos", "polkadot", "cardano", "tezos", "algorand",
        "consensus", "pow", "proof of work", "pos", "proof of stake",
        "dapps", "decentralized", "defi", "nft", "crypto", "wallet",
        "metamask", "trust wallet", "rainbow", "coinbase", "truffle",
        "hardhat", "foundry", "remix", "ganache", "etherscan"
    ],
    
    "data_viz": [
        "data visualization", "data viz", "visualization",
        "dashboard", "reporting", "charts", "graphs", "plots",
        "tableau", "power bi", "looker", "looker studio", "google data studio",
        "metabase", "superset", "apache superset", "qlik", "qlik sense",
        "qlikview", "d3", "d3.js", "plotly", "chart.js", "highcharts",
        "amcharts", "apexcharts", "chartist", "echarts", "graphana",
        "grafana", "kibana", "redash", "preset", "mode", "hex",
        "deepnote", "observable", "observablehq", "vega", "vega-lite",
        "altair", "ggplot2", "matplotlib", "seaborn", "bokeh", "plotly dash",
        "dashboarding", "data storytelling", "visual analytics", "bi dashboards",
        "reporting tools", "data exploration", "interactive dashboards"
    ],
    
    
    
    # ============================================================
    # FRONTEND BACKEND & FULL STACK SKILLS START
    # ============================================================
    
    
    "html": [
    "html",
    "html5",
    "hypertext markup language",
    "xhtml"
  ],
  "css": [
    "css",
    "css3",
    "cascading style sheets",
    "css preprocessors"
  ],
  "sass": [
    "sass",
    "scss",
    "syntactically awesome stylesheets"
  ],
  "less": [
    "less",
    "less css"
  ],
  "tailwind_css": [
    "tailwind",
    "tailwind css",
    "tailwindcss"
  ],
  "bootstrap": [
    "bootstrap",
    "bootstrap 4",
    "bootstrap 5",
    "twitter bootstrap"
  ],
  "material_ui": [
    "material ui",
    "mui",
    "material design"
  ],
  "chakra_ui": [
    "chakra ui",
    "chakra"
  ],
  "ant_design": [
    "ant design",
    "antd"
  ],
  "bulma": [
    "bulma"
  ],
  "foundation": [
    "foundation",
    "zurb foundation"
  ],
  "semantic_ui": [
    "semantic ui",
    "semantic"
  ],
  "javascript": [
    "javascript",
    "js",
    "vanilla js",
    "es5",
    "es6",
    "ecmascript",
    "ecmascript 6",
    "es2015",
    "es2016",
    "es2017",
    "es2018",
    "es2019",
    "es2020",
    "es2021",
    "es2022",
    "es2023"
  ],
  "typescript": [
    "typescript",
    "ts"
  ],
  "react": [
    "react",
    "react js",
    "reactjs",
    "react.js"
  ],
  "react_native": [
    "react native",
    "rn"
  ],
  "next_js": [
    "next.js",
    "nextjs",
    "next"
  ],
  "gatsby": [
    "gatsby",
    "gatsby js"
  ],
  "vue": [
    "vue.js",
    "vuejs",
    "vue",
    "vue 2",
    "vue 3"
  ],
  "nuxt": [
    "nuxt.js",
    "nuxtjs",
    "nuxt"
  ],
  "angular": [
    "angular",
    "angular 2",
    "angular 4",
    "angular 5",
    "angular 6",
    "angular 7",
    "angular 8",
    "angular 9",
    "angular 10",
    "angular 11",
    "angular 12",
    "angular 13",
    "angular 14",
    "angular 15",
    "angular 16",
    "angular 17"
  ],
  "angularjs": [
    "angularjs",
    "angular 1",
    "angular 1.x"
  ],
  "svelte": [
    "svelte",
    "svelte js"
  ],
  "sveltekit": [
    "sveltekit",
    "svelte kit"
  ],
  "solid_js": [
    "solidjs",
    "solid js",
    "solid"
  ],
  "qwik": [
    "qwik",
    "qwik js"
  ],
  "ember": [
    "ember.js",
    "emberjs",
    "ember"
  ],
  "backbone": [
    "backbone.js",
    "backbonejs",
    "backbone"
  ],
  "jquery": [
    "jquery",
    "jquery ui",
    "jquery mobile"
  ],
  "node_js": [
    "node.js",
    "nodejs",
    "node",
    "node runtime"
  ],
  "express": [
    "express",
    "express.js",
    "expressjs",
    "express framework"
  ],
  "nestjs": [
    "nestjs",
    "nest js",
    "nest"
  ],
  "fastify": [
    "fastify",
    "fastify js"
  ],
  "koa": [
    "koa",
    "koa.js",
    "koajs"
  ],
  "meteor": [
    "meteor",
    "meteor js",
    "meteor framework"
  ],
  "adonis": [
    "adonis",
    "adonis js",
    "adonisjs"
  ],
  "loopback": [
    "loopback",
    "loopback js"
  ],
  "python": [
    "python",
    "python 3",
    "python2"
  ],
  "django": [
    "django",
    "django framework"
  ],
  "flask": [
    "flask",
    "flask python"
  ],
  "fastapi": [
    "fastapi",
    "fast api"
  ],
  "pyramid": [
    "pyramid",
    "pyramid framework"
  ],
  "tornado": [
    "tornado",
    "tornado python"
  ],
  "java": [
    "java",
    "java 8",
    "java 11",
    "java 17",
    "java 21"
  ],
  "spring_boot": [
    "spring boot",
    "springboot",
    "spring framework"
  ],
  "spring_mvc": [
    "spring mvc",
    "spring web"
  ],
  "hibernate": [
    "hibernate",
    "hibernate orm"
  ],
  "jpa": [
    "jpa",
    "java persistence api"
  ],
  "java_ee": [
    "java ee",
    "jakarta ee",
    "j2ee"
  ],
  "csharp": [
    "c#",
    "csharp",
    "c sharp"
  ],
  "dotnet": [
    "dotnet",
    ".net",
    ".net core",
    "asp.net",
    "asp.net core",
    "dotnet core"
  ],
  "php": [
    "php",
    "php 7",
    "php 8",
    "php 8.1",
    "php 8.2",
    "php 8.3"
  ],
  "laravel": [
    "laravel",
    "laravel framework"
  ],
  "symfony": [
    "symfony",
    "symfony framework"
  ],
  "codeigniter": [
    "codeigniter",
    "code igniter"
  ],
  "cakephp": [
    "cakephp",
    "cake php"
  ],
  "yii": [
    "yii",
    "yii2",
    "yii framework"
  ],
  "zend": [
    "zend",
    "zend framework",
    "laminas"
  ],
  "ruby": [
    "ruby",
    "ruby programming"
  ],
  "rails": [
    "rails",
    "ruby on rails",
    "ror"
  ],
  "sinatra": [
    "sinatra",
    "sinatra ruby"
  ],
  "golang": [
    "go",
    "golang",
    "go language"
  ],
  "rust": [
    "rust",
    "rust language"
  ],
  "cplusplus": [
    "c++",
    "cpp",
    "c plus plus"
  ],
  "c": [
    "c",
    "c programming"
  ],
  "elixir": [
    "elixir",
    "elixir language"
  ],
  "phoenix": [
    "phoenix",
    "phoenix framework"
  ],
  "kotlin": [
    "kotlin",
    "kotlin language"
  ],
  "kotlin_spring": [
    "kotlin spring",
    "spring with kotlin"
  ],
  "scala": [
    "scala",
    "scala language"
  ],
  "play_framework": [
    "play",
    "play framework"
  ],
  "perl": [
    "perl",
    "perl language"
  ],
  "swift": [
    "swift",
    "swift language"
  ],
  "vapor": [
    "vapor",
    "vapor swift"
  ],
  "graphql": [
    "graphql",
    "graph ql",
    "gql"
  ],
  "apollo_graphql": [
    "apollo",
    "apollo graphql",
    "apollo client",
    "apollo server"
  ],
  "relay": [
    "relay",
    "relay graphql"
  ],
  "rest_api": [
    "rest",
    "rest api",
    "restful",
    "restful api",
    "restful web services"
  ],
  "soap": [
    "soap",
    "soap api",
    "soap web services"
  ],
  "websocket": [
    "websocket",
    "websockets",
    "ws protocol"
  ],
  "socket_io": [
    "socket.io",
    "socketio",
    "socket"
  ],
  "web_rtc": [
    "webrtc",
    "web rtc",
    "rtc"
  ],
  "json": [
    "json",
    "javascript object notation"
  ],
  "xml": [
    "xml",
    "extensible markup language"
  ],
  "yaml": [
    "yaml",
    "yml"
  ],
  "toml": [
    "toml",
    "toml configuration"
  ],
  "postgresql": [
    "postgresql",
    "postgres",
    "pg",
    "pgsql"
  ],
  "mysql": [
    "mysql",
    "my sql",
    "mariadb",
    "maria db"
  ],
  "mongodb": [
    "mongodb",
    "mongo",
    "mongo db"
  ],
  "redis": [
    "redis",
    "redis cache"
  ],
  "elasticsearch": [
    "elasticsearch",
    "elastic search",
    "es"
  ],
  "cassandra": [
    "cassandra",
    "apache cassandra"
  ],
  "dynamodb": [
    "dynamodb",
    "aws dynamodb",
    "dynamo db"
  ],
  "couchdb": [
    "couchdb",
    "couch db"
  ],
  "neo4j": [
    "neo4j",
    "neo4j graph"
  ],
  "sqlite": [
    "sqlite",
    "sql lite"
  ],
  "firebase_firestore": [
    "firestore",
    "firebase firestore",
    "cloud firestore"
  ],
  "firebase_realtime": [
    "firebase realtime",
    "realtime database",
    "firebase rtbd"
  ],
  "sqlalchemy": [
    "sqlalchemy",
    "sql alchemy"
  ],
  "sequelize": [
    "sequelize",
    "sequelize orm"
  ],
  "mongoose": [
    "mongoose",
    "mongoose odm"
  ],
  "typeorm": [
    "typeorm",
    "type orm"
  ],
  "prisma": [
    "prisma",
    "prisma orm"
  ],
  "drizzle": [
    "drizzle",
    "drizzle orm"
  ],
  "knex": [
    "knex",
    "knex js"
  ],
  "redis_cache": [
    "redis cache",
    "caching with redis"
  ],
  "memcached": [
    "memcached",
    "mem cache"
  ],
  "rabbitmq": [
    "rabbitmq",
    "rabbit mq"
  ],
  "kafka": [
    "kafka",
    "apache kafka"
  ],
  "aws_sqs": [
    "sqs",
    "aws sqs",
    "simple queue service"
  ],
  "celery": [
    "celery",
    "celery python"
  ],
  "bull": [
    "bull",
    "bull queue",
    "bullmq"
  ],
  "docker": [
    "docker",
    "docker container",
    "docker engine"
  ],
  "kubernetes": [
    "kubernetes",
    "k8s",
    "kube"
  ],
  "helm": [
    "helm",
    "helm charts"
  ],
  "jenkins": [
    "jenkins",
    "jenkins ci",
    "jenkins pipeline"
  ],
  "gitlab_ci": [
    "gitlab ci",
    "gitlab pipeline"
  ],
  "github_actions": [
    "github actions",
    "gh actions"
  ],
  "circleci": [
    "circleci",
    "circle ci"
  ],
  "travis_ci": [
    "travis",
    "travis ci"
  ],
  "argocd": [
    "argocd",
    "argo cd"
  ],
  "terraform": [
    "terraform",
    "tf"
  ],
  "ansible": [
    "ansible",
    "ansible automation"
  ],
  "prometheus": [
    "prometheus",
    "prometheus monitoring"
  ],
  "grafana": [
    "grafana",
    "grafana dashboards"
  ],
  "datadog": [
    "datadog",
    "data dog"
  ],
  "newrelic": [
    "newrelic",
    "new relic"
  ],
  "sentry": [
    "sentry",
    "sentry error tracking"
  ],
  "aws": [
    "aws",
    "amazon web services"
  ],
  "ec2": [
    "ec2",
    "aws ec2",
    "elastic compute cloud"
  ],
  "s3": [
    "s3",
    "aws s3",
    "simple storage service"
  ],
  "lambda": [
    "lambda",
    "aws lambda",
    "serverless function"
  ],
  "api_gateway": [
    "api gateway",
    "aws api gateway"
  ],
  "rds": [
    "rds",
    "aws rds",
    "relational database service"
  ],
  "ecs": [
    "ecs",
    "aws ecs",
    "elastic container service"
  ],
  "eks": [
    "eks",
    "aws eks",
    "elastic kubernetes service"
  ],
  "cloudfront": [
    "cloudfront",
    "aws cloudfront",
    "cdn"
  ],
  "route53": [
    "route53",
    "aws route 53"
  ],
  "iam": [
    "iam",
    "aws iam",
    "identity and access management"
  ],
  "cloudformation": [
    "cloudformation",
    "aws cloudformation"
  ],
  "azure": [
    "azure",
    "microsoft azure",
    "azure cloud"
  ],
  "azure_devops": [
    "azure devops",
    "azure pipelines"
  ],
  "gcp": [
    "gcp",
    "google cloud platform",
    "google cloud"
  ],
  "gce": [
    "gce",
    "google compute engine"
  ],
  "gke": [
    "gke",
    "google kubernetes engine"
  ],
  "cloud_run": [
    "cloud run",
    "google cloud run"
  ],
  "firebase": [
    "firebase",
    "firebase platform"
  ],
  "heroku": [
    "heroku",
    "heroku platform"
  ],
  "netlify": [
    "netlify",
    "netlify hosting"
  ],
  "vercel": [
    "vercel",
    "vercel hosting"
  ],
  "render": [
    "render",
    "render hosting"
  ],
  "digitalocean": [
    "digitalocean",
    "digital ocean",
    "do"
  ],
  "nginx": [
    "nginx",
    "nginx server"
  ],
  "apache": [
    "apache",
    "apache server",
    "httpd"
  ],
  "traefik": [
    "traefik",
    "traefik proxy"
  ],
  "haproxy": [
    "haproxy",
    "ha proxy"
  ],
  "linux": [
    "linux",
    "linux os",
    "ubuntu",
    "centos",
    "redhat",
    "debian",
    "fedora"
  ],
  "windows_server": [
    "windows server",
    "windows os",
    "iis"
  ],
  "git": [
    "git",
    "git version control"
  ],
  "github": [
    "github",
    "gh"
  ],
  "gitlab": [
    "gitlab",
    "git lab"
  ],
  "bitbucket": [
    "bitbucket",
    "bit bucket"
  ],
  "webpack": [
    "webpack",
    "webpack bundler"
  ],
  "vite": [
    "vite",
    "vite bundler"
  ],
  "rollup": [
    "rollup",
    "rollup.js"
  ],
  "parcel": [
    "parcel",
    "parcel bundler"
  ],
  "babel": [
    "babel",
    "babeljs"
  ],
  "eslint": [
    "eslint",
    "es lint"
  ],
  "prettier": [
    "prettier",
    "prettier code formatter"
  ],
  "jest": [
    "jest",
    "jest testing"
  ],
  "mocha": [
    "mocha",
    "mocha js"
  ],
  "chai": [
    "chai",
    "chai assertion"
  ],
  "jasmine": [
    "jasmine",
    "jasmine testing"
  ],
  "cypress": [
    "cypress",
    "cypress testing"
  ],
  "playwright": [
    "playwright",
    "playwright testing"
  ],
  "puppeteer": [
    "puppeteer",
    "puppeteer testing"
  ],
  "selenium": [
    "selenium",
    "selenium webdriver"
  ],
  "storybook": [
    "storybook",
    "storybook js"
  ],
  "redux": [
    "redux",
    "redux state",
    "react redux"
  ],
  "mobx": [
    "mobx",
    "mobx state"
  ],
  "zustand": [
    "zustand",
    "zustand state"
  ],
  "jotai": [
    "jotai",
    "jotai state"
  ],
  "recoil": [
    "recoil",
    "recoil state"
  ],
  "context_api": [
    "context api",
    "react context"
  ],
  "react_query": [
    "react query",
    "tanstack query"
  ],
  "swr": [
    "swr",
    "swr react"
  ],
  "axios": [
    "axios",
    "axios http"
  ],
  "fetch_api": [
    "fetch",
    "fetch api",
    "window.fetch"
  ],
  "react_hook_form": [
    "react hook form",
    "rhf"
  ],
  "formik": [
    "formik",
    "formik forms"
  ],
  "react_router": [
    "react router",
    "react-router"
  ],
  "vue_router": [
    "vue router",
    "vue-router"
  ],
  "react_navigation": [
    "react navigation",
    "react-navigation"
  ],
  "next_router": [
    "next router",
    "app router",
    "pages router"
  ],
  "react_i18n": [
    "react i18n",
    "i18next"
  ],
  "dayjs": [
    "dayjs",
    "day.js"
  ],
  "moment": [
    "moment",
    "moment.js"
  ],
  "date_fns": [
    "date fns",
    "date-fns"
  ],
  "lodash": [
    "lodash",
    "lodash library"
  ],
  "underscore": [
    "underscore",
    "underscore.js"
  ],
  "ramda": [
    "ramda",
    "ramda js"
  ],
  "swagger": [
    "swagger",
    "openapi",
    "swagger ui",
    "swagger docs"
  ],
  "postman": [
    "postman",
    "postman api"
  ],
  "insomnia": [
    "insomnia",
    "insomnia api"
  ],
  "conventional_commits": [
    "conventional commits",
    "semantic commits"
  ],
  "jwt": [
    "jwt",
    "json web token",
    "jsonwebtoken"
  ],
  "oauth": [
    "oauth",
    "oauth2",
    "oauth 2.0"
  ],
  "openid_connect": [
    "openid",
    "openid connect",
    "oidc"
  ],
  "saml": [
    "saml",
    "saml 2.0"
  ],
  "bcrypt": [
    "bcrypt",
    "bcrypt hashing"
  ],
  "argon2": [
    "argon2",
    "argon2 hashing"
  ],
  "passport": [
    "passport",
    "passport.js"
  ],
  "next_auth": [
    "nextauth",
    "next auth",
    "auth.js"
  ],
  "auth0": [
    "auth0",
    "auth0 authentication"
  ],
  "firebase_auth": [
    "firebase auth",
    "firebase authentication"
  ],
  "supabase": [
    "supabase",
    "supabase platform"
  ],
  "pocketbase": [
    "pocketbase",
    "pocket base"
  ],
  "deno": [
    "deno",
    "deno runtime"
  ],
  "bun": [
    "bun",
    "bun runtime"
  ],
  "npm": [
    "npm",
    "node package manager"
  ],
  "yarn": [
    "yarn",
    "yarn package manager"
  ],
  "pnpm": [
    "pnpm",
    "pnpm package manager"
  ],
  "junit": [
    "junit",
    "junit testing"
  ],
  "pytest": [
    "pytest",
    "py test"
  ],
  "unittest": [
    "unittest",
    "python unittest"
  ],
  "xunit": [
    "xunit",
    "xunit testing"
  ],
  "nunit": [
    "nunit",
    "nunit testing"
  ],
  "codeceptjs": [
    "codeceptjs",
    "codecept js"
  ],
  "testcafe": [
    "testcafe",
    "test cafe"
  ],
  "react_testing_library": [
    "react testing library",
    "testing library"
  ],
  "vitest": [
    "vitest",
    "vite test"
  ],
  "jwt_auth": [
    "jwt auth",
    "token based auth"
  ],
  "session_auth": [
    "session auth",
    "cookie based auth"
  ],
  "microservices": [
    "microservices",
    "microservice architecture"
  ],
  "monolithic": [
    "monolithic",
    "monolith architecture"
  ],
  "serverless": [
    "serverless",
    "serverless architecture"
  ],
  "event_driven": [
    "event driven",
    "event driven architecture"
  ],
  "tdd": [
    "tdd",
    "test driven development"
  ],
  "bdd": [
    "bdd",
    "behavior driven development"
  ],
  "ddd": [
    "ddd",
    "domain driven design"
  ],
  "clean_code": [
    "clean code",
    "clean architecture"
  ],
  "solid": [
    "solid",
    "solid principles",
    "solid design"
  ],
  "design_patterns": [
    "design patterns",
    "software design patterns",
    "gang of four"
  ],
  "caching": [
    "caching",
    "cache strategy"
  ],
  "message_queue": [
    "message queue",
    "mq",
    "message broker"
  ],
  "api_design": [
    "api design",
    "rest api design",
    "api architecture"
  ],
  "load_balancing": [
    "load balancing",
    "load balancer"
  ],
  "distributed_systems": [
    "distributed systems",
    "distributed computing"
  ],
  "monitoring": [
    "monitoring",
    "system monitoring",
    "application monitoring"
  ],
  "logging": [
    "logging",
    "application logging",
    "log management"
  ],
  "debugging": [
    "debugging",
    "debugger",
    "chrome devtools"
  ],
  "testing": [
    "testing",
    "unit testing",
    "integration testing",
    "e2e testing",
    "end to end testing"
  ],
  "ci_cd": [
    "ci/cd",
    "continuous integration",
    "continuous delivery",
    "continuous deployment",
    "cicd"
  ],
  "performance_optimization": [
    "performance",
    "performance optimization",
    "web performance",
    "app performance",
    "perf"
  ],
  "seo": [
    "seo",
    "search engine optimization"
  ],
  "a11y": [
    "a11y",
    "accessibility",
    "web accessibility"
  ],
  "responsive_design": [
    "responsive design",
    "responsive web design",
    "mobile first",
    "rwd"
  ],
  "cross_browser": [
    "cross browser",
    "cross browser compatibility"
  ],
  "code_review": [
    "code review",
    "code review process"
  ],
  "collaboration": [
    "collaboration",
    "team collaboration"
  ],
  "agile": [
    "agile",
    "agile methodology",
    "agile development"
  ],
  "scrum": [
    "scrum",
    "scrum framework"
  ],
  "kanban": [
    "kanban",
    "kanban methodology"
  ],
  "jira_tracking": [
    "jira tracking",
    "jira software",
    "atlassian jira"
  ],
  "confluence_docs": [
    "confluence docs",
    "atlassian confluence"
  ],
  "linear": [
    "linear",
    "linear app"
  ],
  "github_projects": [
    "github projects",
    "projects"
  ],
  "notion_docs": [
    "notion docs",
    "notion project management"
  ],
  
    # ============================================================
    # FRONTEND BACKEND & FULL STACK SKILLS END
    # ============================================================
    
    # ============================================================
    # UI/UX Skills Start
    # ============================================================
    
    
    "ui_design": [
    "ui design",
    "user interface design",
    "interface design"
  ],
  "ux_design": [
    "ux design",
    "user experience design",
    "experience design"
  ],
  "ui_ux_design": [
    "ui/ux design",
    "ui ux",
    "ui ux design",
    "product design"
  ],
  "user_research": [
    "user research",
    "ux research",
    "user experience research",
    "design research",
    "qualitative research",
    "quantitative research"
  ],
  "usability_testing": [
    "usability testing",
    "user testing",
    "ux testing",
    "usability study"
  ],
  "user_personas": [
    "user personas",
    "personas",
    "buyer personas",
    "customer personas"
  ],
  "user_journey": [
    "user journey",
    "journey mapping",
    "customer journey map",
    "user journey map",
    "experience mapping"
  ],
  "user_flows": [
    "user flows",
    "user flow diagrams",
    "flowcharts",
    "task flows"
  ],
  "wireframing": [
    "wireframing",
    "wireframes",
    "wireframe design",
    "low fidelity wireframes"
  ],
  "prototyping": [
    "prototyping",
    "prototypes",
    "interactive prototypes",
    "high fidelity prototypes",
    "clickable prototypes"
  ],
  "mockups": [
    "mockups",
    "ui mockups",
    "visual mockups",
    "design mockups"
  ],
  "visual_design": [
    "visual design",
    "visual communication",
    "graphic design",
    "visual hierarchy"
  ],
  "interaction_design": [
    "interaction design",
    "ixd",
    "interaction design",
    "microinteractions"
  ],
  "information_architecture": [
    "information architecture",
    "ia",
    "information design",
    "content architecture"
  ],
  "design_systems": [
    "design systems",
    "design system",
    "component library",
    "ui kit",
    "pattern library"
  ],
  "design_tokens": [
    "design tokens",
    "design system tokens",
    "style tokens"
  ],
  "atomic_design": [
    "atomic design",
    "atomic methodology",
    "atoms molecules organisms"
  ],
  "material_design": [
    "material design",
    "google material design",
    "material guidelines"
  ],
  "human_interface_guidelines": [
    "human interface guidelines",
    "hgi",
    "apple design guidelines"
  ],
  "gestalt_principles": [
    "gestalt",
    "gestalt principles",
    "gestalt laws"
  ],
  "typography": [
    "typography",
    "font design",
    "typeface",
    "typography design"
  ],
  "color_theory": [
    "color theory",
    "color palette",
    "color scheme",
    "color psychology"
  ],
  "branding": [
    "branding",
    "brand identity",
    "brand design",
    "visual identity"
  ],
  "logo_design": [
    "logo design",
    "logo creation",
    "brand marks"
  ],
  "illustration": [
    "illustration",
    "digital illustration",
    "vector illustration",
    "custom illustration"
  ],
  "iconography": [
    "iconography",
    "icon design",
    "icons",
    "icon system"
  ],
  "animation": [
    "animation",
    "ui animation",
    "motion design",
    "micro animations",
    "transitions"
  ],
  "motion_design": [
    "motion design",
    "motion graphics",
    "ui motion",
    "interaction animation"
  ],
  "responsive_design": [
    "responsive design",
    "responsive ui",
    "adaptive design",
    "multi-device design",
    "mobile first design"
  ],
  "accessibility_design": [
    "accessibility",
    "a11y design",
    "inclusive design",
    "accessible design",
    "wcag"
  ],
  "figma": [
    "figma",
    "figma design",
    "figma tool"
  ],
  "adobe_xd": [
    "adobe xd",
    "adobe experience design",
    "xd"
  ],
  "sketch": [
    "sketch",
    "sketch app",
    "sketch design"
  ],
  "framer": [
    "framer",
    "framer design",
    "framer prototyping"
  ],
  "invision": [
    "invision",
    "invision studio",
    "invision app"
  ],
  "marvel": [
    "marvel",
    "marvel app",
    "marvel prototyping"
  ],
  "zeplin": [
    "zeplin",
    "zeplin design"
  ],
  "abstract": [
    "abstract",
    "abstract design"
  ],
  "balsamiq": [
    "balsamiq",
    "balsamiq wireframes"
  ],
  "axure": [
    "axure",
    "axure rp",
    "axure prototyping"
  ],
  "proto_pie": [
    "proto pie",
    "protopie",
    "proto pie design"
  ],
  "principle": [
    "principle",
    "principle app",
    "principle animation"
  ],
  "after_effects": [
    "after effects",
    "adobe after effects",
    "ae"
  ],
  "photoshop": [
    "photoshop",
    "adobe photoshop",
    "ps"
  ],
  "illustrator": [
    "illustrator",
    "adobe illustrator",
    "ai"
  ],
  "indesign": [
    "indesign",
    "adobe indesign",
    "id"
  ],
  "figjam": [
    "figjam",
    "figjam whiteboard",
    "figma jam"
  ],
  "miro": [
    "miro",
    "miro whiteboard",
    "miro board"
  ],
  "mural": [
    "mural",
    "mural whiteboard"
  ],
  "whimsical": [
    "whimsical",
    "whimsical design"
  ],
  "ux_research_tools": [
    "user research tools",
    "usability hub",
    "userzoom",
    "lookback",
    "optimal workshop",
    "dovetail",
    "userinterviews"
  ],
  "hotjar_ux": [
    "hotjar",
    "hotjar analytics",
    "user recordings",
    "heatmaps"
  ],
  "crazyegg_ux": [
    "crazyegg",
    "crazy egg heatmaps"
  ],
  "fullstory_ux": [
    "fullstory",
    "fullstory analytics"
  ],
  "usabilityhub": [
    "usabilityhub",
    "usability hub"
  ],
  "userbrain": [
    "userbrain",
    "userbrain testing"
  ],
  "lookback": [
    "lookback",
    "lookback research"
  ],
  "userzoom": [
    "userzoom",
    "user zoom"
  ],
  "dovetail": [
    "dovetail",
    "dovetail research"
  ],
  "userinterviews": [
    "userinterviews",
    "user interviews"
  ],
  "optimal_workshop": [
    "optimal workshop",
    "optimalworkshop"
  ],
  "customer_journey": [
    "customer journey",
    "customer journey mapping",
    "user journey"
  ],
  "service_design": [
    "service design",
    "service blueprint",
    "blueprinting"
  ],
  "empathy_maps": [
    "empathy maps",
    "empathy mapping"
  ],
  "sitemaps": [
    "sitemaps",
    "site maps",
    "website sitemap"
  ],
  "storyboarding": [
    "storyboarding",
    "storyboard design",
    "user storyboards"
  ],
  "heuristic_evaluation": [
    "heuristic evaluation",
    "heuristic analysis",
    "usability heuristics"
  ],
  "a_b_testing_design": [
    "a/b testing",
    "ab testing design",
    "split testing design"
  ],
  "card_sorting": [
    "card sorting",
    "card sort",
    "information architecture sorting"
  ],
  "tree_testing": [
    "tree testing",
    "tree test",
    "information architecture testing"
  ],
  "surveys": [
    "surveys",
    "user surveys",
    "survey design",
    "questionnaire design"
  ],
  "interviews": [
    "interviews",
    "user interviews",
    "stakeholder interviews",
    "one-on-one interviews"
  ],
  "focus_groups": [
    "focus groups",
    "focus group research"
  ],
  "design_thinking": [
    "design thinking",
    "design thinking methodology",
    "human centered design"
  ],
  "lean_ux": [
    "lean ux",
    "lean user experience"
  ],
  "agile_ux": [
    "agile ux",
    "agile user experience"
  ],
  "ui_patterns": [
    "ui patterns",
    "user interface patterns",
    "design patterns ui"
  ],
  "ux_writing": [
    "ux writing",
    "microcopy",
    "copywriting",
    "ui copy",
    "content design"
  ],
  "content_strategy": [
    "content strategy",
    "content design",
    "content planning"
  ],
  "data_visualization": [
    "data visualization",
    "data viz",
    "dashboard design",
    "infographics"
  ],
  "dashboard_design": [
    "dashboard design",
    "admin dashboard ui",
    "data dashboard"
  ],
  "mobile_app_design": [
    "mobile design",
    "app design",
    "ios design",
    "android design",
    "mobile ui"
  ],
  "web_design": [
    "web design",
    "website design",
    "web ui design",
    "landing page design"
  ],
  "ecommerce_design": [
    "ecommerce design",
    "e-commerce ui",
    "store design",
    "product page design"
  ],
  "saas_design": [
    "saas design",
    "saas ui",
    "software as a service design"
  ],
  "design_handoff": [
    "design handoff",
    "handoff to development",
    "design to code"
  ],
  "developer_handoff": [
    "developer handoff",
    "design to dev",
    "dev handoff"
  ],
  "design_specs": [
    "design specs",
    "specifications",
    "design documentation"
  ],
  "style_guides": [
    "style guides",
    "styleguide",
    "brand style guide"
  ],
  "prototyping_tools": [
    "prototyping tools",
    "prototype tools",
    "interactive design"
  ],
  "ux_strategy": [
    "ux strategy",
    "user experience strategy",
    "design strategy"
  ],
  "product_management": [
    "product management",
    "product strategy",
    "product owner"
  ],
  "stakeholder_management": [
    "stakeholder management",
    "stakeholder communication"
  ],
  "user_centric_design": [
    "user centered design",
    "human centered design",
    "ucd"
  ],
  "conversational_design": [
    "conversational design",
    "chatbot design",
    "voice ux",
    "voice interface"
  ],
  "vr_ar_design": [
    "vr design",
    "ar design",
    "virtual reality design",
    "augmented reality design",
    "spatial design"
  ],
  "game_ui": [
    "game ui",
    "game interface design",
    "video game ui"
  ],
  "design_leadership": [
    "design leadership",
    "lead designer",
    "design director"
  ],
  "mentoring": [
    "mentoring",
    "design mentoring",
    "coaching design"
  ],
  "design_sprint": [
    "design sprint",
    "google design sprint",
    "sprint methodology"
  ],
  "workshop_facilitation": [
    "workshop facilitation",
    "design workshops",
    "facilitation"
  ],
  "jira_design": [
    "jira",
    "jira for design",
    "atlassian jira"
  ],
  "trello_design": [
    "trello",
    "trello boards"
  ],
  "asana_design": [
    "asana",
    "asana project management"
  ],
  "clickup_design": [
    "clickup",
    "click up tasks"
  ],
  "notion_design": [
    "notion",
    "notion for design"
  ],
  "confluence_design": [
    "confluence",
    "confluence documentation"
  ],
  "slack_design": [
    "slack",
    "slack communication"
  ],
  "teams_design": [
    "teams",
    "microsoft teams"
  ],
  "zoom_design": [
    "zoom",
    "zoom meetings"
  ],
  "google_meet_design": [
    "google meet",
    "meet"
  ],
  "google_drive_design": [
    "google drive",
    "drive storage"
  ],
  "dropbox_design": [
    "dropbox",
    "dropbox storage"
  ],
  "portfolio_design": [
    "portfolio design",
    "design portfolio"
  ],
  "case_studies": [
    "case studies",
    "design case studies",
    "project cases"
  ],
  "creative_cloud": [
    "creative cloud",
    "adobe creative cloud",
    "adobe cc"
  ],
  "creative_direction": [
    "creative direction",
    "creative director"
  ],
  "art_direction": [
    "art direction",
    "art director"
  ],
  "ux_audit": [
    "ux audit",
    "user experience audit",
    "design audit"
  ],
  "ux_analytics": [
    "ux analytics",
    "user analytics",
    "behavior analytics"
  ],
  "user_metrics": [
    "user metrics",
    "ux metrics",
    "key performance indicators",
    "kpis"
  ],
        
        
    # ============================================================
    # UI/UX skills END
    # ============================================================    
    
    # ============================================================
    # Business Developer START
    # ============================================================
    
    
    "sales": [
    "sales", "selling", "sold", "salesmanship", "sales experience", "sales background", "sales work", 
    "sales activities", "sales function", "sales role", "sales job", "sales career", "sales profession",
    "merchandising", "merchandise", "retail sales", "wholesale sales", "direct sales", "indirect sales",
    "field sales", "inside sales", "outside sales", "territory sales", "regional sales", "national sales",
    "global sales", "international sales", "domestic sales", "local sales", "consumer sales", "b2b sales",
    "b2c sales", "business to business sales", "business to consumer sales", "b2g sales", "government sales",
    "institutional sales", "corporate sales", "commercial sales", "enterprise sales", "sme sales",
    "mid-market sales", "key account sales", "strategic sales", "solution sales", "product sales",
    "service sales", "consultative sales", "hard sales", "soft sales", "face to face sales", "f2f sales",
    "phone sales", "telephone sales", "telemarketing", "telesales", "door to door sales", "d2d sales",
    "car sales", "automotive sales", "real estate sales", "property sales", "insurance sales",
    "financial sales", "banking sales", "tech sales", "software sales", "saas sales", "it sales",
    "pharma sales", "pharmaceutical sales", "medical sales", "equipment sales", "machinery sales",
    "industrial sales", "manufacturing sales", "fmcg sales", "fast moving consumer goods sales",
    "cpg sales", "consumer packaged goods sales", "retail sales associate", "sales assistant",
    "sales officer", "sales executive", "sales manager", "sales director", "sales head", "sales lead",
    "sales specialist", "sales professional", "sales guru", "sales ninja", "sales rockstar",
    "sales warrior", "sales hunter", "sales closer", "deal closer", "closer"
  ],

  "negotiation": [
    "negotiation", "negotiating", "negotiate", "negotiated", "negotiator", "negotiations",
    "commercial negotiation", "contract negotiation", "deal negotiation", "price negotiation",
    "pricing negotiation", "terms negotiation", "procurement negotiation", "vendor negotiation",
    "supplier negotiation", "buyer negotiation", "sales negotiation", "strategic negotiation",
    "complex negotiation", "high-stakes negotiation", "win-win negotiation", "negotiation skills",
    "negotiation tactics", "negotiation techniques", "negotiation strategy", "negotiation expertise",
    "negotiation experience", "negotiation mastery", "negotiation professional", "negotiation lead",
    "bargaining", "bargain", "haggle", "haggling", "mediation", "conciliation", "arbitration",
    "conflict resolution", "dispute resolution", "compromise", "trade-off", "concession",
    "deal-making", "dealmaking", "deal maker", "deal broker", "barter", "trade negotiation",
    "price negotiation", "cost negotiation", "rate negotiation", "fee negotiation", "salary negotiation",
    "contract discussion", "terms discussion", "agreement negotiation"
  ],

  "lead_generation": [
    "lead generation", "lead gen", "leadgeneration", "leadg gen", "leads generation",
    "generating leads", "generate leads", "lead sourcing", "lead acquisition", "lead accumulation",
    "lead building", "lead creation", "lead development", "lead identification", "lead mining",
    "lead prospecting", "lead qualification", "lead research", "lead discovery", "lead outreach",
    "cold lead generation", "warm lead generation", "hot lead generation", "inbound lead generation",
    "outbound lead generation", "b2b lead generation", "b2c lead generation", "digital lead generation",
    "online lead generation", "offline lead generation", "marketing qualified leads", "mql",
    "sales qualified leads", "sql", "product qualified leads", "pql", "service qualified leads",
    "lead scoring", "lead nurturing", "lead conversion", "lead pipeline", "lead funnel",
    "lead management", "lead tracking", "lead follow-up", "lead response", "lead capture",
    "lead magnet", "lead bait", "lead list", "lead database", "lead enrichment", "lead verification",
    "prospecting", "prospect generation", "prospecting calls", "prospecting emails", "cold outreach",
    "cold calling", "cold emailing", "cold mailing", "cold messaging", "cold dming", "cold linkedin",
    "warm outreach", "warm calling", "referral generation", "referral leads", "network leads",
    "conference leads", "exhibition leads", "trade show leads", "event leads", "webinar leads",
    "landing page leads", "ppc leads", "seo leads", "social media leads", "content leads",
    "inbound marketing", "outbound marketing", "demand generation", "demand gen"
  ],

  "pipeline": [
    "pipeline", "sales pipeline", "pipelining", "pipeline development", "pipeline generation",
    "pipeline management", "pipeline building", "pipeline creation", "pipeline growth",
    "pipeline acceleration", "pipeline expansion", "pipeline forecasting", "pipeline analysis",
    "pipeline review", "pipeline hygiene", "pipeline health", "pipeline coverage", "pipeline velocity",
    "opportunity pipeline", "deal pipeline", "revenue pipeline", "lead pipeline", "prospect pipeline",
    "pipeline stage", "pipeline progression", "pipeline conversion", "pipeline drop-off",
    "pipeline leak", "pipeline plug", "pipeline report", "pipeline dashboard", "pipeline crm",
    "pipe", "sales pipe", "deal flow", "dealflow", "opportunity flow", "lead flow", "inquiry flow"
  ],

  "client_relationship": [
    "client relationship", "customer relationship", "relationship management",
    "relationship building", "relationship cultivation", "relationship development",
    "relationship maintenance", "relationship retention", "relationship expansion",
    "client management", "customer management", "account management", "key account management",
    "strategic account management", "global account management", "regional account management",
    "client servicing", "customer servicing", "client handling", "customer handling",
    "client interaction", "customer interaction", "client communication", "customer communication",
    "client engagement", "customer engagement", "client retention", "customer retention",
    "client loyalty", "customer loyalty", "client satisfaction", "customer satisfaction",
    "csat", "net promoter score", "nps", "client success", "customer success", "client advocacy",
    "customer advocacy", "client reference", "customer reference", "client testimonials",
    "case studies", "client partnership", "customer partnership", "stakeholder management",
    "stakeholder engagement", "stakeholder relationship", "client facing", "customer facing",
    "frontline", "relationship officer", "relationship manager", "rm", "customer relationship officer",
    "cro", "client relationship executive", "relationship executive", "client success manager",
    "csm", "customer success manager"
  ],

  "strategic_planning": [
    "strategic planning", "strategy planning", "strategy development", "strategy formulation",
    "strategic development", "strategic thinking", "strategic analysis", "strategic execution",
    "strategic implementation", "strategic management", "strategic direction", "strategic vision",
    "strategic roadmap", "roadmap creation", "roadmap development", "go-to-market strategy",
    "gtm strategy", "gtm plan", "market entry strategy", "market expansion strategy",
    "growth strategy", "business strategy", "commercial strategy", "sales strategy",
    "revenue strategy", "pricing strategy", "product strategy", "channel strategy",
    "partnership strategy", "alliance strategy", "global strategy", "regional strategy",
    "local strategy", "competitive strategy", "differentiation strategy", "cost leadership",
    "focus strategy", "blue ocean strategy", "market penetration", "market development",
    "product development", "diversification", "strategic initiatives", "strategic projects",
    "strategic programs", "strategic portfolio", "strategy consulting", "strategic advisory"
  ],

  "partnership": [
    "partnership", "partnerships", "partnering", "partner", "partnered", "partners",
    "strategic partnerships", "strategic partners", "strategic partnering", "alliances",
    "strategic alliances", "alliance management", "alliance building", "alliance development",
    "partner ecosystem", "partner network", "partner relationship", "partner management",
    "partner enablement", "partner success", "channel partnerships", "channel partners",
    "channel management", "channel sales", "channel development", "indirect sales",
    "reseller partnerships", "reseller management", "distributor partnerships",
    "distributor management", "dealer partnerships", "dealer network", "franchise partnerships",
    "franchise development", "licensing partnerships", "licensing agreements", "oem partnerships",
    "original equipment manufacturer", "system integrator", "si partnerships", "value-added reseller",
    "var", "technology partnerships", "technology alliances", "co-marketing partnerships",
    "co-branding partnerships", "joint ventures", "jv", "jv partnerships", "strategic cooperation",
    "collaboration", "collaborative partnerships", "industry partnerships", "government partnerships",
    "ngo partnerships", "academic partnerships", "research partnerships", "innovation partnerships",
    "equity partnerships", "profit-sharing partnerships", "referral partnerships", "affiliate partnerships"
  ],

  "proposal": [
    "proposal", "proposals", "proposal writing", "proposal creation", "proposal development",
    "proposal management", "proposal coordination", "proposal submission", "proposal response",
    "rfp response", "rfp submission", "request for proposal", "rfq response", "request for quotation",
    "rfi response", "request for information", "bid management", "bid writing", "bid preparation",
    "bid submission", "tender management", "tender response", "tender submission", "tender writing",
    "public tender", "government tender", "private tender", "commercial proposal", "technical proposal",
    "financial proposal", "combined proposal", "solicited proposal", "unsolicited proposal",
    "proposal pitch", "proposal presentation", "proposal defense", "bid defense", "tender defense",
    "contract proposal", "project proposal", "service proposal", "product proposal", "solution proposal",
    "proposal drafting", "proposal template", "proposal content", "proposal strategy", "bid strategy",
    "bid pricing", "bid winning", "win strategy", "win theme", "competitive bidding", "e-tendering",
    "electronic tendering", "ppra", "public procurement", "procurement proposal"
  ],

  "networking": [
    "networking", "network", "networked", "networking skills", "professional networking",
    "business networking", "social networking", "online networking", "offline networking",
    "digital networking", "in-person networking", "virtual networking", "linkedin networking",
    "linkedin outreach", "linkedin connection", "linkedin networking", "event networking",
    "conference networking", "trade show networking", "exhibition networking", "seminar networking",
    "webinar networking", "alumni networking", "referral networking", "introduction networking",
    "relationship building", "connection building", "business connections", "professional connections",
    "industry connections", "network expansion", "network development", "network cultivation",
    "network leverage", "network utilization", "network growth", "network mapping", "contact building",
    "contacts development", "rolodex", "address book", "database building", "contact list",
    "warm introductions", "cold introductions", "referral generation", "word of mouth",
    "personal branding", "professional branding", "visibility", "thought leadership",
    "community building", "community engagement", "community networking", "council membership",
    "board membership", "committee participation", "chamber of commerce", "trade association",
    "industry body", "professional body", "pakistan chamber", "karachi chamber", "lahore chamber",
    "islamabad chamber", "fpcci", "pasha", "pseb", "tdap"
  ],

  "market_research": [
    "market research", "market analysis", "market assessment", "market evaluation",
    "market study", "market survey", "market intelligence", "competitive intelligence",
    "competitor analysis", "competitor research", "industry research", "industry analysis",
    "sector analysis", "trend analysis", "trend spotting", "market trends", "market dynamics",
    "market sizing", "tam analysis", "total addressable market", "sam analysis",
    "serviceable addressable market", "som analysis", "serviceable obtainable market",
    "market segmentation", "segment analysis", "target market", "target audience",
    "customer research", "buyer research", "buyer persona", "customer profiling",
    "client profiling", "demographic analysis", "psychographic analysis", "behavioral analysis",
    "swot analysis", "strengths weaknesses opportunities threats", "pestel analysis",
    "political economic social technological legal environmental", "porter's five forces",
    "porter five forces", "gap analysis", "needs analysis", "requirements gathering",
    "data gathering", "data collection", "primary research", "secondary research",
    "qualitative research", "quantitative research", "focus groups", "surveys", "questionnaires",
    "interviews", "field research", "desk research", "online research", "google trends",
    "keyword research", "seo research", "analytics research", "consumer insights",
    "customer insights", "voice of customer", "voc", "feedback analysis", "sentiment analysis"
  ],

  "closing": [
    "closing", "close deals", "closing deals", "closed deals", "closer", "deal closer",
    "closing skills", "closing techniques", "closing strategies", "closing tactics",
    "closing ability", "closing expertise", "closing experience", "closing ratio",
    "closing rate", "closing percentage", "win rate", "conversion rate", "conversion skills",
    "conversion optimization", "deal completion", "deal finalization", "deal sealing",
    "signing deals", "agreement signing", "contract execution", "deal closure", "deal sign-off",
    "commitment closing", "decision closing", "objection handling", "objection resolution",
    "overcoming objections", "stall prevention", "procrastination handling", "hurdle removal",
    "last mile closing", "trial close", "assumptive close", "alternative close",
    "urgency close", "scarcity close", "summary close", "question close", "benefit close",
    "now or never close", "soft close", "hard close", "close rate", "win-loss ratio",
    "successful closing", "effective closing", "closing performance", "closing achievements"
  ],

  "crm": [
    "crm", "customer relationship management", "client relationship management",
    "crm software", "crm platform", "crm tool", "crm system", "crm solution",
    "salesforce", "salesforce crm", "sfdc", "sales cloud", "hubspot", "hubspot crm",
    "zoho", "zoho crm", "pipedrive", "pipedrive crm", "freshsales", "freshworks",
    "close crm", "close", "copper crm", "copper", "nimble", "nimble crm", "insightly",
    "monday crm", "monday.com", "dynamics", "microsoft dynamics", "dynamics 365",
    "oracle crm", "netsuite", "sugarcrm", "keap", "infusionsoft", "activecampaign",
    "capsule crm", "capsule", "folk", "streak", "streak crm", "salesflare", "bigin",
    "less annoying crm", "crm administration", "crm management", "crm implementation",
    "crm customization", "crm data", "crm reporting", "crm dashboards", "crm analytics",
    "crm migration", "crm integration", "crm automation", "crm adoption", "crm training",
    "crm user", "crm superuser", "crm champion", "crm specialist", "crm administrator",
    "crm consultant", "crm strategist", "crm manager", "salesforce administrator",
    "salesforce admin", "hubspot admin", "zoho admin", "pipedrive admin"
  ],

  "forecasting": [
    "forecasting", "forecast", "forecasts", "forecasted", "sales forecasting",
    "sales forecast", "revenue forecasting", "revenue forecast", "pipeline forecasting",
    "pipeline forecast", "opportunity forecasting", "demand forecasting", "demand forecast",
    "financial forecasting", "financial forecast", "budget forecasting", "budget forecast",
    "projection", "projections", "projected", "predictive analytics", "prediction",
    "predictions", "trend analysis", "trend forecasting", "market forecasting",
    "quarterly forecast", "monthly forecast", "annual forecast", "rolling forecast",
    "top-down forecast", "bottom-up forecast", "statistical forecast", "data-driven forecast",
    "accuracy", "forecast accuracy", "forecast precision", "forecast reliability",
    "forecast confidence", "forecast review", "forecast update", "forecast adjustment",
    "forecast variance", "forecast gap", "forecast methodology", "forecast model",
    "forecast tool", "forecast dashboard", "forecast reporting", "forecast meeting",
    "sales projection", "revenue projection", "growth projection", "target projection",
    "goal projection", "outlook", "business outlook", "market outlook", "economic outlook"
  ],

  "revenue": [
    "revenue", "revenues", "revenue growth", "revenue generation", "revenue development",
    "revenue expansion", "revenue acceleration", "revenue optimization", "revenue management",
    "revenue strategy", "revenue planning", "revenue forecasting", "revenue reporting",
    "revenue analysis", "revenue performance", "revenue targets", "revenue goals",
    "revenue metrics", "revenue kpis", "revenue pipeline", "revenue funnel", "revenue streams",
    "revenue diversification", "revenue maximization", "topline growth", "top-line growth",
    "topline", "top line", "sales revenue", "service revenue", "product revenue",
    "subscription revenue", "recurring revenue", "mrr", "monthly recurring revenue",
    "arr", "annual recurring revenue", "acv", "annual contract value", "tcv",
    "total contract value", "new revenue", "net new revenue", "expansion revenue",
    "retention revenue", "renewal revenue", "upsell revenue", "cross-sell revenue",
    "gross revenue", "net revenue", "adjusted revenue", "deferred revenue",
    "unearned revenue", "revenue recognition", "revenue realization", "revenue assurance",
    "revenue protection", "recovery", "collection", "accounts receivable", "ar",
    "invoice", "invoicing", "billing", "payment collection", "payment terms"
  ],

  "contract": [
    "contract", "contracts", "contracting", "contract management", "contract administration",
    "contract negotiation", "contract execution", "contract signing", "contract finalization",
    "contract review", "contract analysis", "contract drafting", "contract preparation",
    "contract renewal", "contract extension", "contract amendment", "contract modification",
    "contract termination", "contract closeout", "master agreement", "service agreement",
    "service contract", "product agreement", "supply agreement", "purchase agreement",
    "sales agreement", "distribution agreement", "licensing agreement", "franchise agreement",
    "joint venture agreement", "partnership agreement", "alliance agreement", "nda",
    "non-disclosure agreement", "confidentiality agreement", "mou", "memorandum of understanding",
    "moa", "memorandum of agreement", "letter of intent", "loi", "term sheet", "statement of work",
    "sow", "scope of work", "sla", "service level agreement", "kpi agreement", "performance agreement",
    "employment contract", "consultancy agreement", "vendor contract", "supplier contract",
    "subcontract", "prime contract", "government contract", "public contract", "private contract",
    "commercial contract", "legal agreement", "binding agreement", "enforceable contract",
    "contract lifecycle", "contract compliance", "contract governance", "contract risk"
  ],

  "account_management": [
    "account management", "account manager", "strategic account management",
    "key account management", "global account management", "national account management",
    "regional account management", "major account management", "enterprise account management",
    "corporate account management", "sme account management", "mid-market account management",
    "account planning", "account strategy", "account growth", "account expansion",
    "account retention", "account renewal", "account profitability", "account revenue",
    "account penetration", "account coverage", "account mapping", "account organization",
    "account team", "account leadership", "account coordinator", "account specialist",
    "account executive", "account director", "account lead", "account owner",
    "account stewardship", "account advocacy", "account health", "account score",
    "account analysis", "account review", "account qbr", "quarterly business review",
    "annual account review", "client account", "customer account", "accounts receivable",
    "credit management", "collections", "account reconciliation", "account auditing"
  ],

  "presentation": [
    "presentation", "presentations", "presenting", "presenter", "presentation skills",
    "public speaking", "speaking", "speaker", "keynote", "keynote speaker", "panelist",
    "moderator", "host", "facilitator", "presentation creation", "presentation development",
    "presentation design", "slide deck", "slide creation", "powerpoint", "ppt", "google slides",
    "slides", "canva", "prezi", "visual aids", "data visualization", "chart creation",
    "graph creation", "infographics", "storytelling", "narrative", "pitch deck", "investor deck",
    "board presentation", "executive presentation", "client presentation", "sales presentation",
    "product presentation", "service presentation", "proposal presentation", "bid presentation",
    "team presentation", "training presentation", "workshop presentation", "conference presentation",
    "webinar presentation", "virtual presentation", "remote presentation", "stand-up presentation",
    "formal presentation", "informal presentation", "impromptu presentation", "extemporaneous",
    "persuasive presentation", "informative presentation", "demonstration", "demo", "product demo",
    "live demo", "recorded demo", "screen share", "walkthrough", "showcase"
  ],

  "communication": [
    "communication", "communicating", "communicator", "verbal communication",
    "written communication", "oral communication", "interpersonal communication",
    "business communication", "professional communication", "client communication",
    "customer communication", "internal communication", "external communication",
    "upward communication", "downward communication", "lateral communication",
    "formal communication", "informal communication", "email communication",
    "phone communication", "video communication", "face-to-face communication",
    "virtual communication", "remote communication", "cross-cultural communication",
    "multilingual communication", "persuasive communication", "influential communication",
    "clear communication", "concise communication", "effective communication",
    "active listening", "listening skills", "questioning skills", "probing",
    "clarification", "summarizing", "paraphrasing", "feedback", "constructive feedback",
    "report writing", "business writing", "technical writing", "proposal writing",
    "reporting", "briefing", "debriefing", "collaboration", "team communication",
    "cross-functional communication", "stakeholder communication", "board communication",
    "executive communication", "c-suite communication", "correspondence", "memo",
    "email drafting", "letter writing", "message crafting", "social media communication",
    "linkedin communication", "networking communication"
  ],

  "team_leadership": [
    "team leadership", "leadership", "leading teams", "team management", "people management",
    "staff management", "employee management", "team development", "team building",
    "team culture", "team motivation", "team inspiration", "team direction", "team vision",
    "team strategy", "team operations", "team performance", "team kpis", "team goals",
    "team targets", "team review", "team feedback", "team coaching", "team mentoring",
    "talent development", "career development", "skill development", "training", "onboarding",
    "team onboarding", "cross-training", "upskilling", "reskilling", "succession planning",
    "performance management", "performance reviews", "performance improvement", "pip",
    "conflict resolution", "team conflict", "mediating", "team harmony", "employee retention",
    "retention strategy", "employee engagement", "culture building", "inclusive culture",
    "diversity", "inclusion", "remote team", "distributed team", "hybrid team", "virtual team",
    "team meetings", "stand-ups", "sprint planning", "retrospectives", "team building activities",
    "offsite", "team retreat", "recognition", "team rewards", "delegation", "empowerment",
    "trust building", "accountability", "ownership", "responsibility", "decision making"
  ],

  "problem_solving": [
    "problem solving", "problem solver", "problem-solving", "problem analysis", "issue resolution",
    "issue management", "challenge solving", "complex problem solving", "analytical problem solving",
    "creative problem solving", "structured problem solving", "root cause analysis", "rca",
    "diagnosis", "troubleshooting", "resolution", "solution development", "solution architecture",
    "solution designing", "solution implementation", "critical thinking", "analytical thinking",
    "logic", "reasoning", "deduction", "induction", "abduction", "hypothesis testing",
    "data analysis", "data interpretation", "evidence-based decisions", "decision making",
    "sound judgment", "strategic thinking", "systems thinking", "lateral thinking", "out-of-box thinking",
    "innovation", "resourcefulness", "adaptability", "flexibility", "resilience", "persistence",
    "compromise", "negotiation", "mediation", "facilitation", "brainstorming", "ideation",
    "synthesis", "prioritization", "trade-off analysis", "cost-benefit analysis", "risk analysis",
    "risk mitigation", "contingency planning", "what-if analysis", "scenario planning"
  ],

  "time_management": [
    "time management", "time management skills", "managing time", "priority setting",
    "prioritization", "task management", "task prioritization", "task organization",
    "workload management", "workload balancing", "multitasking", "focus", "attention",
    "deadline management", "deadline achievement", "meeting deadlines", "on-time delivery",
    "punctuality", "reliability", "dependability", "scheduling", "schedule management",
    "calendar management", "calendar planning", "agenda setting", "planning", "forethought",
    "organization", "organized", "systematic", "methodical", "structured", "efficient",
    "productivity", "productive", "effective", "goal setting", "goal orientation",
    "target setting", "milestone achievement", "progress tracking", "progress monitoring",
    "time tracking", "timesheet", "task automation", "delegation", "outsourcing",
    "resource allocation", "resource management", "utilization", "optimization",
    "efficiency improvement", "process improvement", "lean", "agile", "scrum", "kanban"
  ],

  "financial_acumen": [
    "financial acumen", "financial literacy", "financial understanding", "financial skills",
    "budget management", "budgeting", "budget planning", "budget development", "budget control",
    "cost management", "cost control", "cost optimization", "cost reduction", "expense management",
    "expense tracking", "p&l management", "profit and loss", "p&l", "income statement",
    "balance sheet", "cash flow", "cash flow management", "financial modeling", "financial projection",
    "financial forecasting", "financial analysis", "financial reporting", "financial review",
    "roi analysis", "return on investment", "irr", "internal rate of return", "npv",
    "net present value", "payback period", "break-even analysis", "break even", "ebitda",
    "earnings before interest taxes depreciation amortization", "gross margin", "net margin",
    "profit margin", "operating margin", "contribution margin", "unit economics", "customer lifetime value",
    "clv", "customer acquisition cost", "cac", "clv:cac ratio", "payback", "payback period",
    "value-based pricing", "cost-plus pricing", "competitive pricing", "price elasticity",
    "discounting", "volume discount", "tiered pricing", "bundling", "upsell", "cross-sell"
  ],

  "business_development": [
    "business development", "bd", "biz dev", "business dev", "new business development",
    "new biz dev", "business growth", "growth development", "market development",
    "opportunity development", "opportunity creation", "opportunity identification",
    "opportunity pipeline", "deal sourcing", "deal origination", "deal flow", "inorganic growth",
    "organic growth", "expansion", "market expansion", "geographic expansion", "global expansion",
    "international expansion", "regional expansion", "local expansion", "sector expansion",
    "product expansion", "service expansion", "innovation", "growth hacking", "growth strategy",
    "scalability", "scale-up", "startup growth", "sme growth", "enterprise growth",
    "corporate development", "corp dev", "m&a", "mergers and acquisitions", "joint ventures",
    "strategic investments", "equity investments", "minority stake", "majority stake",
    "holding company", "subsidiary", "spin-off", "divestiture", "asset acquisition", "talent acquisition",
    "white space", "white space analysis", "untapped market", "greenfield", "brownfield"
  ],

  "sales_operations": [
    "sales operations", "sales ops", "sales administration", "sales support", "sales enablement",
    "sales excellence", "sales optimization", "sales efficiency", "sales effectiveness",
    "sales transformation", "sales process improvement", "sales workflow", "sales automation",
    "sales technology", "sales tools", "sales stack", "sales analytics", "sales insights",
    "sales reporting", "sales dashboards", "sales metrics", "sales kpis", "sales scoring",
    "sales territory planning", "territory alignment", "sales quota", "quota management",
    "sales compensation", "sales incentives", "sales commission", "spiff", "sales bonus",
    "sales performance", "sales productivity", "sales capacity planning", "sales coverage",
    "sales routing", "sales cadence", "sales playbook", "sales script", "sales talk track",
    "sales objection handling", "sales training", "sales coaching", "sales onboarding",
    "sales certification", "sales methodology", "sales best practices", "sales standard",
    "sales compliance", "sales audit", "sales quality", "sales governance", "sales policy"
  ],

  "marketing": [
    "marketing", "digital marketing", "online marketing", "offline marketing", "traditional marketing",
    "inbound marketing", "outbound marketing", "content marketing", "social media marketing",
    "email marketing", "sms marketing", "mobile marketing", "video marketing", "seo", "search engine optimization",
    "sem", "search engine marketing", "ppc", "pay per click", "google ads", "meta ads", "facebook ads",
    "instagram ads", "linkedin ads", "twitter ads", "tiktok ads", "display ads", "banner ads",
    "affiliate marketing", "influencer marketing", "brand marketing", "product marketing",
    "service marketing", "b2b marketing", "b2c marketing", "b2g marketing", "growth marketing",
    "performance marketing", "guerrilla marketing", "viral marketing", "word of mouth",
    "referral marketing", "event marketing", "trade show marketing", "conference marketing",
    "webinar marketing", "podcast marketing", "public relations", "pr", "brand awareness",
    "brand positioning", "brand management", "brand strategy", "brand storytelling",
    "brand identity", "brand equity", "brand loyalty", "brand advocacy", "market positioning",
    "unique selling proposition", "usp", "value proposition", "differentiation", "messaging",
    "copywriting", "content creation", "blogging", "thought leadership", "whitepaper",
    "case study", "e-book", "infographic", "newsletter", "campaign management", "campaign strategy"
  ],

  "analytics": [
    "analytics", "analysis", "data analysis", "business analytics", "sales analytics",
    "marketing analytics", "financial analytics", "predictive analytics", "descriptive analytics",
    "diagnostic analytics", "prescriptive analytics", "data interpretation", "data synthesis",
    "data visualization", "reporting", "dashboards", "scorecards", "kpi tracking", "metric analysis",
    "trend analysis", "pattern recognition", "correlation", "causation", "regression", "cohort analysis",
    "funnel analysis", "conversion analysis", "retention analysis", "churn analysis", "lifetime value",
    "attribution", "multi-touch attribution", "a/b testing", "split testing", "multivariate testing",
    "optimization", "experimentation", "data-driven decisions", "evidence-based", "business intelligence",
    "bi", "tableau", "power bi", "looker", "metabase", "google analytics", "ga4", "amplitude",
    "mixpanel", "heap", "pendo", "fullstory", "hotjar", "crazyegg", "semrush", "ahrefs", "similarweb"
  ],

  "software": [
    "software", "saas", "software as a service", "crm", "sales software", "marketing software",
    "outreach", "salesloft", "apollo", "zoominfo", "lusha", "clearbit", "hunter", "snov", "lemlist",
    "reply", "mailshake", "woodpecker", "instantly", "smartlead", "yesware", "mixmax", "gmass",
    "salesforce", "hubspot", "zoho", "pipedrive", "dynamics", "slack", "teams", "zoom", "google meet",
    "calendly", "notion", "trello", "asana", "clickup", "jira", "monday", "airtable", "excel", "sheets",
    "powerpoint", "word", "docs", "pandadoc", "docusign", "hellosign", "zapier", "make", "chatgpt",
    "gemini", "claude", "copilot", "perplexity", "wordpress", "shopify", "sales navigator", 
    "linkedin recruiter", "crunchbase", "pitchbook", "owler", "g2", "clutch", "capterra"
  ],

  "export": [
    "export", "exports", "exporting", "export management", "export development", "international trade",
    "cross-border trade", "global trade", "foreign trade", "trade facilitation", "trade compliance",
    "customs", "customs clearance", "customs brokerage", "shipping", "international shipping",
    "logistics", "supply chain", "freight", "freight forwarding", "cargo", "air freight", "sea freight",
    "land freight", "courier", "dhl", "fedex", "ups", "tnt", "aramex", "pakistan exports",
    "textile export", "garment export", "leather export", "sports goods export", "surgical goods export",
    "rice export", "basmati export", "mango export", "fruit export", "vegetable export", "pharma export",
    "chemical export", "steel export", "cement export", "marble export", "carpet export", "handicraft export",
    "export to usa", "export to eu", "export to uk", "export to uae", "export to saudi", "export to gcc",
    "export to china", "export to japan", "export to korea", "export to africa", "export to central asia",
    "export documentation", "export license", "export permit", "exporter", "export house",
    "export oriented", "export incentives", "export subsidies", "duty drawback", "export processing zone",
    "epz", "special economic zone", "sez", "free trade agreement", "fta", "gsp", "generalized system of preferences",
    "certificate of origin", "bill of lading", "letter of credit", "lc", "export finance", "export credit"
  ],
    
    "linkedin": [
    "linkedin",
    "linked in",
    "linkedin sales navigator",
    "sales navigator",
    "linkedin recruiter",
    "linkedin premium",
    "linkedin jobs",
    "linkedin talent solutions",
    "linkedin learning",
    "linkedin live",
    "linkedin ads",
    "linkedin marketing solutions",
    "linkedin sales insights",
    "sales insights",
    "linkedin service marketplace",
    "linkedin pages"
  ],
  "upwork": [
    "upwork",
    "up work"
  ],
  "fiverr": [
    "fiverr",
    "fiveer",
    "fiverr pro"
  ],
  "peopleperhour": [
    "peopleperhour",
    "people per hour",
    "pph"
  ],
  "freelancer": [
    "freelancer",
    "freelancer.com"
  ],
  "guru": [
    "guru",
    "guru.com"
  ],
  "toptal": [
    "toptal"
  ],
  "contra": [
    "contra"
  ],
  "truelancer": [
    "truelancer"
  ],
  "workana": [
    "workana"
  ],
  "outsourcely": [
    "outsourcely",
    "outsourcely.com"
  ],
  "remoteok": [
    "remoteok",
    "remote ok"
  ],
  "wellfound": [
    "wellfound",
    "angellist",
    "angel list",
    "angel.co",
    "well found"
  ],
  "arc.dev": [
    "arc.dev",
    "arc"
  ],
  "codementor": [
    "codementor"
  ],
  "hireable": [
    "hireable"
  ],
  "working_nomads": [
    "working nomads"
  ],
  "flexjobs": [
    "flexjobs",
    "flex jobs"
  ],
  "simplyhired": [
    "simplyhired",
    "simply hired"
  ],
  "kwork": [
    "kwork"
  ],
  "envato_studio": [
    "envato studio"
  ],
  "fivesquid": [
    "fivesquid"
  ],
  "twine": [
    "twine"
  ],
  "kolabtree": [
    "kolabtree"
  ],
  "clutch": [
    "clutch",
    "clutch.co"
  ],
  "goodfirms": [
    "goodfirms",
    "good firms"
  ],
  "designrush": [
    "designrush",
    "design rush"
  ],
  "g2": [
    "g2",
    "g2.com"
  ],
  "capterra": [
    "capterra"
  ],
  "software_advice": [
    "software advice"
  ],
  "sourceforge": [
    "sourceforge"
  ],
  "trustpilot": [
    "trustpilot",
    "trust pilot"
  ],
  "glassdoor": [
    "glassdoor"
  ],
  "yelp": [
    "yelp",
    "yelp for business"
  ],
  "yellow_pages": [
    "yellow pages",
    "yp",
    "yp.com"
  ],
  "manta": [
    "manta"
  ],
  "angi": [
    "angie's list",
    "angi"
  ],
  "bbb": [
    "better business bureau",
    "bbb"
  ],
  "sitejabber": [
    "sitejabber"
  ],
  "producthunt": [
    "product hunt",
    "producthunt"
  ],
  "betalist": [
    "betalist",
    "betalist.com"
  ],
  "saasworthy": [
    "saasworthy",
    "saas worthy"
  ],
  "getapp": [
    "getapp",
    "get app"
  ],
  "financesonline": [
    "financesonline"
  ],
  "crozdesk": [
    "crozdesk"
  ],
  "salesforce_appexchange": [
    "appexchange",
    "salesforce appexchange"
  ],
  "zapier_marketplace": [
    "zapier marketplace"
  ],
  "make_marketplace": [
    "make marketplace"
  ],
  "apollo": [
    "apollo",
    "apollo.io",
    "apollo io"
  ],
  "zoominfo": [
    "zoominfo",
    "zoom info",
    "zoominfo salesos"
  ],
  "lusha": [
    "lusha"
  ],
  "rocketreach": [
    "rocketreach",
    "rocket reach"
  ],
  "leadiq": [
    "leadiq",
    "lead iq"
  ],
  "cognism": [
    "cognism"
  ],
  "seamless.ai": [
    "seamless.ai",
    "seamless ai",
    "seamless"
  ],
  "hunter": [
    "hunter",
    "hunter.io",
    "email hunter",
    "hunter campaigns"
  ],
  "snov": [
    "snov",
    "snov.io",
    "snov campaigns"
  ],
  "kaspr": [
    "kaspr"
  ],
  "adapt": [
    "adapt",
    "adapt.io"
  ],
  "uplead": [
    "uplead",
    "up lead"
  ],
  "salesintel": [
    "salesintel",
    "sales intel"
  ],
  "clearbit": [
    "clearbit"
  ],
  "contactout": [
    "contactout",
    "contact out"
  ],
  "datanyze": [
    "datanyze"
  ],
  "echobot": [
    "echobot"
  ],
  "convince_convert": [
    "convince & convert"
  ],
  "skrapp": [
    "skrapp",
    "skrapp.io"
  ],
  "aero_leads": [
    "aero leads"
  ],
  "leadsift": [
    "leadsift"
  ],
  "truelane": [
    "truelane"
  ],
  "bound": [
    "bound",
    "bound.io"
  ],
  "salesgenie": [
    "salesgenie"
  ],
  "infousa": [
    "infousa"
  ],
  "discoverorg": [
    "discoverorg"
  ],
  "teckler": [
    "teckler"
  ],
  "prospect.io": [
    "prospect.io",
    "prospect"
  ],
  "signalhire": [
    "signalhire",
    "signal hire"
  ],
  "connectifier": [
    "connectifier"
  ],
  "snapbird": [
    "snapbird"
  ],
  "leadfeeder": [
    "leadfeeder",
    "lead feeder"
  ],
  "dealfront": [
    "dealfront",
    "front lead"
  ],
  "nymeria": [
    "nymeria"
  ],
  "anymail_finder": [
    "anymail finder"
  ],
  "dropcontact": [
    "dropcontact",
    "drop contact"
  ],
  "tomba": [
    "tomba.io",
    "tomba"
  ],
  "verifalia": [
    "verifalia"
  ],
  "email_verifier": [
    "email verifier"
  ],
  "neverbounce": [
    "neverbounce"
  ],
  "zero_bounce": [
    "zero bounce"
  ],
  "kickbox": [
    "kickbox"
  ],
  "bulkemailchecker": [
    "bulkemailchecker"
  ],
  "crunchbase": [
    "crunchbase",
    "crunch base"
  ],
  "pitchbook": [
    "pitchbook",
    "pitch book"
  ],
  "owler": [
    "owler"
  ],
  "cb_insights": [
    "cb insights",
    "cbinsights"
  ],
  "dealroom": [
    "dealroom",
    "deal room"
  ],
  "bloomberg": [
    "bloomberg"
  ],
  "reuters": [
    "reuters"
  ],
  "yahoo_finance": [
    "yahoo finance"
  ],
  "google_finance": [
    "google finance"
  ],
  "sec_edgar": [
    "sec edgar",
    "edgar"
  ],
  "hoovers": [
    "hoovers"
  ],
  "dun_bradstreet": [
    "dun & bradstreet",
    "dnb"
  ],
  "moodys": [
    "moody's"
  ],
  "sp_global": [
    "s&p global"
  ],
  "capital_iq": [
    "capital iq"
  ],
  "factiva": [
    "factiva"
  ],
  "lexisnexis": [
    "lexisnexis",
    "lexis nexis"
  ],
  "marketline": [
    "marketline"
  ],
  "statista": [
    "statista"
  ],
  "ibisworld": [
    "ibisworld"
  ],
  "garter": [
    "garter"
  ],
  "forrester": [
    "forrester"
  ],
  "pwc": [
    "pwc"
  ],
  "deloitte_insights": [
    "deloitte insights"
  ],
  "kpmg": [
    "kpmg"
  ],
  "ey": [
    "ey"
  ],
  "mckinsey": [
    "mckinsey"
  ],
  "bcg": [
    "bcg"
  ],
  "bain": [
    "bain"
  ],
  "glassnode": [
    "glassnode"
  ],
  "coinmarketcap": [
    "coinmarketcap"
  ],
  "coingecko": [
    "coingecko"
  ],
  "salesforce": [
    "salesforce",
    "sfdc",
    "sales cloud",
    "salesforce cpq"
  ],
  "hubspot": [
    "hubspot",
    "hub spot",
    "hubspot sales hub"
  ],
  "zoho_crm": [
    "zoho crm",
    "zoho",
    "zoho bigin"
  ],
  "pipedrive": [
    "pipedrive",
    "pipe drive"
  ],
  "freshsales": [
    "freshsales",
    "fresh sales"
  ],
  "close_crm": [
    "close",
    "close crm"
  ],
  "copper": [
    "copper",
    "copper crm"
  ],
  "nimble": [
    "nimble",
    "nimble crm"
  ],
  "insightly": [
    "insightly"
  ],
  "monday_crm": [
    "monday crm",
    "monday.com",
    "monday"
  ],
  "nocrm": [
    "no crm",
    "nocrm"
  ],
  "microsoft_dynamics": [
    "microsoft dynamics",
    "dynamics 365",
    "ms dynamics"
  ],
  "oracle_crm": [
    "oracle crm",
    "oracle netsuite",
    "netsuite"
  ],
  "sugarcrm": [
    "sugarcrm",
    "sugar crm"
  ],
  "salesloft": [
    "salesloft",
    "sales loft"
  ],
  "keap": [
    "keap"
  ],
  "infusionsoft": [
    "infusionsoft"
  ],
  "activecampaign": [
    "activecampaign",
    "active campaign"
  ],
  "crm_generic": [
    "crm"
  ],
  "less_annoying_crm": [
    "less annoying crm"
  ],
  "capsule": [
    "capsule",
    "capsule crm"
  ],
  "bigin": [
    "bigin"
  ],
  "freshworks": [
    "freshworks"
  ],
  "folk": [
    "folk",
    "folk crm"
  ],
  "streak": [
    "streak",
    "streak crm"
  ],
  "salesflare": [
    "salesflare"
  ],
  "net_hunt": [
    "net hunt"
  ],
  "outreach": [
    "outreach",
    "outreach.io"
  ],
  "reply": [
    "reply.io",
    "reply"
  ],
  "lemlist": [
    "lemlist"
  ],
  "mailshake": [
    "mailshake"
  ],
  "woodpecker": [
    "woodpecker",
    "woodpecker.co"
  ],
  "instantly": [
    "instantly",
    "instantly.ai"
  ],
  "smartlead": [
    "smartlead",
    "smartlead.ai"
  ],
  "yesware": [
    "yesware"
  ],
  "mixmax": [
    "mixmax"
  ],
  "gmass": [
    "gmass",
    "gmass.io"
  ],
  "warmbox": [
    "warmbox"
  ],
  "warm_up": [
    "warm up"
  ],
  "quickmail": [
    "quickmail",
    "quick mail"
  ],
  "autoklose": [
    "autoklose"
  ],
  "groove": [
    "groove",
    "groove.co"
  ],
  "xant": [
    "xant"
  ],
  "cirrus_insight": [
    "cirrus insight"
  ],
  "ebsta": [
    "ebsta"
  ],
  "vanillasoft": [
    "vanillasoft"
  ],
  "leadfwd": [
    "leadfwd"
  ],
  "saleshandy": [
    "saleshandy",
    "sales handy"
  ],
  "briefly": [
    "briefly"
  ],
  "outfunnel": [
    "outfunnel"
  ],
  "amocrm": [
    "amocrm",
    "amo crm"
  ],
  "mailchimp": [
    "mailchimp",
    "mail chimp"
  ],
  "brevo": [
    "brevo",
    "sendinblue",
    "send in blue"
  ],
  "constant_contact": [
    "constant contact"
  ],
  "convertkit": [
    "convertkit",
    "kit"
  ],
  "mailerlite": [
    "mailerlite",
    "mailer lite"
  ],
  "getresponse": [
    "getresponse",
    "get response"
  ],
  "aweber": [
    "aweber",
    "awber"
  ],
  "campaign_monitor": [
    "campaign monitor"
  ],
  "drip": [
    "drip",
    "drip email"
  ],
  "klaviyo": [
    "klaviyo"
  ],
  "omnisend": [
    "omnisend"
  ],
  "moosend": [
    "moosend"
  ],
  "mailjet": [
    "mailjet"
  ],
  "sendgrid": [
    "sendgrid",
    "twilio sendgrid"
  ],
  "postmark": [
    "postmark"
  ],
  "resend": [
    "resend"
  ],
  "beehiiv": [
    "beehiiv"
  ],
  "substack": [
    "substack"
  ],
  "medium": [
    "medium"
  ],
  "ghost": [
    "ghost"
  ],
  "buttondown": [
    "buttondown"
  ],
  "letterhead": [
    "letterhead"
  ],
  "systeme": [
    "systeme.io",
    "systeme"
  ],
  "gmail": [
    "gmail",
    "google workspace",
    "google mail"
  ],
  "outlook": [
    "outlook",
    "microsoft outlook",
    "office365",
    "office 365"
  ],
  "slack": [
    "slack",
    "slack communities"
  ],
  "discord": [
    "discord",
    "discord servers"
  ],
  "microsoft_teams": [
    "microsoft teams",
    "ms teams",
    "teams"
  ],
  "zoom": [
    "zoom"
  ],
  "google_meet": [
    "google meet",
    "meet",
    "gmeet"
  ],
  "calendly": [
    "calendly"
  ],
  "cal.com": [
    "cal.com",
    "cal"
  ],
  "savvycal": [
    "savvycal",
    "savvy"
  ],
  "acuity": [
    "acuity scheduling",
    "acuity"
  ],
  "vocus": [
    "vocus"
  ],
  "gotomeeting": [
    "gotomeeting",
    "go to meeting"
  ],
  "webex": [
    "webex",
    "cisco webex"
  ],
  "whereby": [
    "whereby"
  ],
  "jitsi": [
    "jitsi"
  ],
  "telegram": [
    "telegram"
  ],
  "signal": [
    "signal"
  ],
  "whatsapp": [
    "whatsapp",
    "whatsapp business"
  ],
  "wechat": [
    "wechat"
  ],
  "line": [
    "line"
  ],
  "skype": [
    "skype",
    "microsoft skype"
  ],
  "notion": [
    "notion"
  ],
  "trello": [
    "trello"
  ],
  "asana": [
    "asana"
  ],
  "clickup": [
    "clickup",
    "click up"
  ],
  "jira": [
    "jira"
  ],
  "airtable": [
    "airtable",
    "air table"
  ],
  "wrike": [
    "wrike"
  ],
  "basecamp": [
    "basecamp"
  ],
  "smartsheet": [
    "smartsheet",
    "smart sheet"
  ],
  "teamwork": [
    "teamwork",
    "teamwork.com"
  ],
  "confluence": [
    "confluence"
  ],
  "milanote": [
    "milanote"
  ],
  "coda": [
    "coda",
    "coda.io"
  ],
  "fibery": [
    "fibery"
  ],
  "anytype": [
    "anytype"
  ],
  "obsidian": [
    "obsidian"
  ],
  "roam_research": [
    "roam research",
    "roam"
  ],
  "workflowy": [
    "workflowy"
  ],
  "google_docs": [
    "google docs",
    "docs"
  ],
  "google_sheets": [
    "google sheets",
    "sheets"
  ],
  "microsoft_excel": [
    "microsoft excel",
    "ms excel",
    "excel"
  ],
  "microsoft_word": [
    "microsoft word",
    "ms word",
    "word"
  ],
  "powerpoint": [
    "powerpoint",
    "microsoft powerpoint"
  ],
  "google_drive": [
    "google drive",
    "drive"
  ],
  "dropbox": [
    "dropbox",
    "dropbox sign"
  ],
  "onedrive": [
    "onedrive",
    "one drive"
  ],
  "box": [
    "box",
    "box.com"
  ],
  "google_slides": [
    "google slides",
    "slides"
  ],
  "google_forms": [
    "google forms",
    "forms"
  ],
  "evernote": [
    "evernote"
  ],
  "bear_notes": [
    "bear notes"
  ],
  "apple_notes": [
    "apple notes"
  ],
  "findings": [
    "findings"
  ],
  "pandadoc": [
    "pandadoc",
    "panda doc"
  ],
  "docusign": [
    "docusign",
    "docu sign"
  ],
  "hellosign": [
    "hellosign",
    "hello sign"
  ],
  "proposify": [
    "proposify"
  ],
  "better_proposals": [
    "better proposals"
  ],
  "qwilr": [
    "qwilr"
  ],
  "bidsketch": [
    "bidsketch"
  ],
  "panda": [
    "panda"
  ],
  "concord": [
    "concord"
  ],
  "congasign": [
    "congasign"
  ],
  "esignlive": [
    "esignlive"
  ],
  "adobe_sign": [
    "adobe sign",
    "adobe acrobat sign"
  ],
  "signnow": [
    "signnow",
    "sign now"
  ],
  "getaccept": [
    "getaccept"
  ],
  "dealhub": [
    "dealhub"
  ],
  "quote_roller": [
    "quote roller"
  ],
  "conga_composer": [
    "conga composer"
  ],
  "catalyst": [
    "catalyst"
  ],
  "x": [
    "x",
    "twitter"
  ],
  "facebook": [
    "facebook",
    "meta",
    "facebook groups"
  ],
  "instagram": [
    "instagram"
  ],
  "youtube": [
    "youtube"
  ],
  "reddit": [
    "reddit",
    "reddit communities"
  ],
  "quora": [
    "quora"
  ],
  "tiktok": [
    "tiktok"
  ],
  "pinterest": [
    "pinterest"
  ],
  "snapchat": [
    "snapchat"
  ],
  "weibo": [
    "weibo"
  ],
  "vkontakte": [
    "vkontakte",
    "vk"
  ],
  "tumblr": [
    "tumblr"
  ],
  "twitch": [
    "twitch"
  ],
  "flickr": [
    "flickr"
  ],
  "behance": [
    "behance"
  ],
  "dribbble": [
    "dribbble"
  ],
  "clubhouse": [
    "clubhouse"
  ],
  "mastodon": [
    "mastodon"
  ],
  "bluesky": [
    "bluesky"
  ],
  "threads": [
    "threads"
  ],
  "indeed": [
    "indeed"
  ],
  "ziprecruiter": [
    "ziprecruiter",
    "zip recruiter"
  ],
  "monster": [
    "monster",
    "monster jobs"
  ],
  "dice": [
    "dice"
  ],
  "we_work_remotely": [
    "we work remotely"
  ],
  "himalayas": [
    "himalayas"
  ],
  "otta": [
    "otta"
  ],
  "y_combinator": [
    "y combinator",
    "y combinator jobs",
    "yc"
  ],
  "startup.jobs": [
    "startup.jobs",
    "startup jobs"
  ],
  "recruiter_generic": [
    "recruiter"
  ],
  "talentlyft": [
    "talentlyft"
  ],
  "lever": [
    "lever"
  ],
  "greenhouse": [
    "greenhouse"
  ],
  "ashby": [
    "ashby"
  ],
  "bamboohr": [
    "bamboohr"
  ],
  "hiring_cafe": [
    "hiring.cafe"
  ],
  "nodesk": [
    "nodesk"
  ],
  "eon": [
    "eon"
  ],
  "shopify": [
    "shopify",
    "shopify plus"
  ],
  "woocommerce": [
    "woocommerce"
  ],
  "amazon_seller": [
    "amazon seller central"
  ],
  "etsy": [
    "etsy"
  ],
  "ebay": [
    "ebay"
  ],
  "alibaba": [
    "alibaba"
  ],
  "aliexpress": [
    "aliexpress"
  ],
  "walmart_marketplace": [
    "walmart marketplace"
  ],
  "target_plus": [
    "target plus"
  ],
  "best_buy": [
    "best buy"
  ],
  "wayfair": [
    "wayfair"
  ],
  "magento": [
    "magento",
    "adobe commerce"
  ],
  "bigcommerce": [
    "bigcommerce",
    "big commerce"
  ],
  "square": [
    "square"
  ],
  "squarespace": [
    "squarespace"
  ],
  "wix": [
    "wix"
  ],
  "stripe": [
    "stripe"
  ],
  "paypal": [
    "paypal"
  ],
  "braintree": [
    "braintree"
  ],
  "recurly": [
    "recurly"
  ],
  "chargebee": [
    "chargebee"
  ],
  "paddle": [
    "paddle"
  ],
  "gumroad": [
    "gumroad"
  ],
  "google_business_profile": [
    "google business profile",
    "google my business",
    "gmb"
  ],
  "bing_places": [
    "bing places"
  ],
  "foursquare": [
    "foursquare"
  ],
  "citysearch": [
    "citysearch"
  ],
  "mapquest": [
    "mapquest"
  ],
  "apple_maps": [
    "apple maps"
  ],
  "here_we_go": [
    "here we go"
  ],
  "tripadvisor": [
    "tripadvisor"
  ],
  "google_local_services": [
    "google local services"
  ],
  "thumbtack": [
    "thumbtack"
  ],
  "homeadvisor": [
    "homeadvisor"
  ],
  "porch": [
    "porch"
  ],
  "zapier": [
    "zapier"
  ],
  "make": [
    "make",
    "make.com",
    "integromat"
  ],
  "n8n": [
    "n8n"
  ],
  "pipedream": [
    "pipedream"
  ],
  "tray": [
    "tray.io",
    "tray"
  ],
  "workato": [
    "workato"
  ],
  "celigo": [
    "celigo"
  ],
  "tines": [
    "tines"
  ],
  "automate.io": [
    "automate.io"
  ],
  "power_automate": [
    "power automate",
    "microsoft power automate"
  ],
  "ifttt": [
    "ifttt",
    "if this then that"
  ],
  "appsmith": [
    "appsmith"
  ],
  "retool": [
    "retool"
  ],
  "airbyte": [
    "airbyte"
  ],
  "fivetran": [
    "fivetran"
  ],
  "estuary": [
    "estuary"
  ],
  "super.ai": [
    "super.ai"
  ],
  "relevance_ai": [
    "relevance ai"
  ],
  "chatgpt": [
    "chatgpt"
  ],
  "claude": [
    "claude"
  ],
  "gemini": [
    "gemini"
  ],
  "copilot": [
    "copilot"
  ],
  "perplexity": [
    "perplexity"
  ],
  "midjourney": [
    "midjourney"
  ],
  "stable_diffusion": [
    "stable diffusion"
  ],
  "runway_ml": [
    "runway ml"
  ],
  "hugging_face": [
    "hugging face"
  ],
  "openai": [
    "openai"
  ],
  "anthropic": [
    "anthropic"
  ],
  "mistral": [
    "mistral"
  ],
  "llama": [
    "llama"
  ],
  "groq": [
    "groq"
  ],
  "lamaindex": [
    "lamaindex"
  ],
  "langchain": [
    "langchain"
  ],
  "google_analytics": [
    "google analytics",
    "ga4",
    "universal analytics"
  ],
  "hotjar": [
    "hotjar"
  ],
  "semrush": [
    "semrush"
  ],
  "ahrefs": [
    "ahrefs"
  ],
  "similarweb": [
    "similarweb",
    "similar web"
  ],
  "moz": [
    "moz"
  ],
  "spyfu": [
    "spyfu"
  ],
  "serpstat": [
    "serpstat"
  ],
  "majestic": [
    "majestic"
  ],
  "surfer_seo": [
    "surfer seo",
    "surferseo"
  ],
  "keyword_planner": [
    "keyword planner",
    "google keyword planner"
  ],
  "search_console": [
    "search console",
    "google search console"
  ],
  "google_trends": [
    "google trends",
    "trends"
  ],
  "amplitude": [
    "amplitude"
  ],
  "mixpanel": [
    "mixpanel"
  ],
  "heap": [
    "heap"
  ],
  "pendo": [
    "pendo"
  ],
  "fullstory": [
    "fullstory"
  ],
  "clarity": [
    "clarity",
    "microsoft clarity"
  ],
  "logrocket": [
    "logrocket"
  ],
  "crazy_egg": [
    "crazy egg",
    "crazyegg"
  ],
  "optimizely": [
    "optimizely"
  ],
  "vwo": [
    "vwo",
    "visual website optimizer"
  ],
  "google_optimize": [
    "google optimize"
  ],
  "ab_tasty": [
    "ab tasty"
  ]
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
    "agentic_ai_engineer": [
        "agentic ai engineer", "agentic ai developer",
        "agentic ai specialist", "agentic ai researcher",
        "agentic ai architect", "agentic ai consultant"
    ],
    "gen_ai_engineer": [
        "generative ai engineer", "generative ai developer",
        "gen ai engineer", "gen ai developer",
        "gen ai specialist", "gen ai researcher",
        "gen ai architect", "gen ai consultant","genai engineer", "genai developer",
        "genai specialist", "genai researcher",
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
    ],
    "business_development": [
        "business development", "bd", "sales engineer", "pre-sales engineer", "business development executive", "bd executive", "sales executive",
        "business development representative", "bd representative", "sales representative", "business development manager", "bd manager", "sales manager",
        "sales and marketing", "sales & marketing", "marketing and sales", "sales specialist", "marketing specialist", "sales associate", "marketing associate",
        "sales consultant", "marketing consultant", "sales coordinator", "marketing coordinator", "sales director", "marketing director", "sales lead", "marketing lead", "sales strategist", "marketing strategist",
        "sales strategist", "marketing strategist", "sales analyst", "marketing analyst", "sales executive", "marketing executive", "sales representative", "marketing representative",
        "upwork growth specialist", "upwork growth manager", "upwork growth consultant", "upwork growth coordinator", "upwork growth director", "upwork growth lead",
        "upwork growth strategist", "upwork growth analyst", "upwork growth associate", "upwork growth specialist",
        "upwork growth manager", "upwork growth consultant", "upwork growth coordinator", "upwork growth director",
        "upwork growth lead", "upwork growth strategist", "upwork growth analyst", "business development specialist", "business development manager", "business development consultant", "business development coordinator", "business development director", "business development lead", "business development strategist", "business development analyst"
        "upwork", "upwork specialist", "upwork manager", "upwork consultant", "upwork coordinator", "upwork director", "upwork lead", "upwork strategist", "upwork analyst",
        "lead generation", "lead generation specialist", "lead generation manager", "lead generation consultant", "lead generation coordinator", "lead generation director", "lead generation lead",
        "lead generation strategist", "lead generation analyst", "account executive", "account manager", "account coordinator", "account director", "account lead", "account strategist", "account analyst",
        "sales development representative", "sales development specialist", "sales development manager", "sales development consultant", "sales development coordinator", "sales development director", "sales development lead", "sales development strategist", "sales development analyst",
        "upwork account executive", "upwork account manager", "upwork account coordinator", "upwork account director", "upwork account lead", "upwork account strategist", "upwork account analyst", "upwork account operator",
        "upwork profile operator", "upwork profile specialist", "upwork profile manager", "upwork profile consultant", "upwork profile coordinator", "upwork profile director", "upwork profile lead",
        "upwork profile strategist", "upwork profile analyst"
    ],
    

    
    
}