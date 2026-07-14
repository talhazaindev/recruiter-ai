# skills_db.py
"""
Skills database containing comprehensive skill categories, variations, and aliases.
Supports technical, business, HR, business development, and other professional skills.
"""

from typing import Dict, List, Set


# ============================================================
# Comprehensive Skill Variations and Synonyms
# ============================================================

COMMON_VARIATIONS: Dict[str, List[str]] = {

    # =========================
    # Programming Languages
    # =========================
    'python': ['python', 'py', 'python3', 'python 3'],
    'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015'],
    'typescript': ['typescript', 'ts', 'typescriptlang'],
    'java': ['java', 'java 8', 'java 11', 'java 17', 'jdk'],
    'c': ['c language', 'ansi c', 'c', 'c99', 'c11'],
    'c++': ['c++', 'cpp', 'cplusplus', 'c++11', 'c++14', 'c++17', 'c++20'],
    'c#': ['c#', 'c sharp', 'csharp', 'c#.net'],
    'go': ['go', 'golang', 'golanglang'],
    'rust': ['rust', 'rustlang'],
    'kotlin': ['kotlin', 'kotlinlang'],
    'swift': ['swift', 'swiftlang'],
    'php': ['php', 'php7', 'php8', 'php hypertext preprocessor'],
    'ruby': ['ruby', 'ruby lang'],
    'scala': ['scala', 'scalalang'],
    'perl': ['perl', 'perl5'],
    'r': ['r', 'r language', 'r programming'],
    'matlab': ['matlab', 'matrix laboratory'],
    'dart': ['dart', 'dartlang'],
    'objective-c': ['objective c', 'objective-c', 'objc'],
    'bash': ['bash', 'shell scripting', 'shell', 'bash scripting', 'sh'],
    'powershell': ['powershell', 'ps', 'powershell scripting'],
    'assembly': ['assembly', 'asm', 'assembler'],

    # =========================
    # Frontend Frameworks & Libraries
    # =========================
    'html': ['html', 'html5', 'hypertext markup language'],
    'css': ['css', 'css3', 'cascading style sheets'],
    'sass': ['sass', 'scss', 'sassy css'],
    'less': ['less', 'less css'],
    'bootstrap': ['bootstrap', 'bootstrap4', 'bootstrap5', 'bs4', 'bs5'],
    'tailwind css': ['tailwind', 'tailwind css', 'tailwindcss', 'tw'],
    'material ui': ['material ui', 'mui', 'material design'],
    'ant design': ['ant design', 'antd', 'ant.design'],
    'chakra ui': ['chakra ui', 'chakra', 'chakra-ui'],
    'react': ['react', 'reactjs', 'react.js', 'react library'],
    'next.js': ['next.js', 'nextjs', 'next'],
    'vue': ['vue', 'vuejs', 'vue.js', 'vue2', 'vue3'],
    'nuxt.js': ['nuxt', 'nuxtjs', 'nuxt.js'],
    'angular': ['angular', 'angularjs', 'angular 2+', 'angular12', 'angular13', 'angular14', 'angular15'],
    'svelte': ['svelte', 'sveltejs', 'svelte.js'],
    'redux': ['redux', 'react redux', 'redux toolkit', 'rtk'],
    'mobx': ['mobx', 'mobx state'],
    'webpack': ['webpack', 'webpack5'],
    'vite': ['vite', 'vitejs'],
    'jquery': ['jquery', 'jquery library'],

    # =========================
    # Backend Frameworks
    # =========================
    'node.js': ['node', 'nodejs', 'node.js', 'node runtime'],
    'express.js': ['express', 'expressjs', 'express.js'],
    'nestjs': ['nestjs', 'nest.js', 'nest'],
    'django': ['django', 'django framework'],
    'flask': ['flask', 'flask framework'],
    'fastapi': ['fastapi', 'fast api'],
    'spring boot': ['spring boot', 'springboot', 'spring-boot'],
    'spring': ['spring', 'spring framework'],
    'asp.net': ['asp.net', 'asp net', 'aspnet'],
    '.net': ['.net', 'dotnet', '.net core', 'dotnet core', '.net 5', '.net 6', '.net 7', '.net 8'],
    'laravel': ['laravel', 'laravel framework'],
    'symfony': ['symfony', 'symfony framework'],
    'ruby on rails': ['ruby on rails', 'rails', 'ror', 'rails framework'],
    'gin': ['gin', 'gin-gonic', 'gin framework'],
    'echo': ['echo', 'echo framework'],

    # =========================
    # Mobile Development
    # =========================
    'android': ['android', 'android development', 'android sdk', 'android studio'],
    'ios': ['ios', 'ios development', 'ios sdk', 'xcode', 'swift ios'],
    'react native': ['react native', 'react-native', 'rn'],
    'flutter': ['flutter', 'flutter framework', 'flutter sdk'],
    'xamarin': ['xamarin', 'xamarin forms', 'xamarin.android', 'xamarin.ios'],
    'ionic': ['ionic', 'ionic framework'],
    'kotlin android': ['kotlin android', 'android kotlin'],
    'swift ios': ['swift ios', 'ios swift'],

    # =========================
    # Databases & Storage
    # =========================
    'sql': ['sql', 'structured query language', 'sql queries'],
    'mysql': ['mysql', 'mysql database', 'mysql server'],
    'postgresql': ['postgresql', 'postgres', 'pgsql'],
    'sqlite': ['sqlite', 'sqlite3', 'sqlite db'],
    'oracle': ['oracle', 'oracle db', 'oracle database'],
    'sql server': ['sql server', 'mssql', 'microsoft sql server', 'ms sql'],
    'mongodb': ['mongodb', 'mongo', 'mongo db', 'nosql mongo'],
    'redis': ['redis', 'redis cache', 'redis db'],
    'cassandra': ['cassandra', 'apache cassandra'],
    'dynamodb': ['dynamodb', 'aws dynamodb', 'dynamo db'],
    'firebase': ['firebase', 'firebase db', 'firebase realtime'],
    'elasticsearch': ['elasticsearch', 'elastic search', 'es', 'elastic'],
    'neo4j': ['neo4j', 'neo4j graph', 'graph database'],
    'influxdb': ['influxdb', 'influx db', 'time series db'],
    'couchdb': ['couchdb', 'couch db', 'apache couchdb'],
    'supabase': ['supabase', 'supabase db', 'supabase postgres'],

    # =========================
    # Cloud Platforms
    # =========================
    'aws': ['aws', 'amazon web services', 'aws cloud', 'ec2', 's3', 'lambda', 'rds', 'vpc', 'iam'],
    'azure': ['azure', 'microsoft azure', 'azure cloud', 'azure devops', 'aks'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform', 'gce', 'gke', 'gcs', 'cloud run'],
    'digitalocean': ['digitalocean', 'do', 'digital ocean'],
    'heroku': ['heroku', 'heroku cloud'],
    'vercel': ['vercel', 'vercel app', 'vercel deployment'],
    'netlify': ['netlify', 'netlify deployment'],
    'cloudflare': ['cloudflare', 'cloudflare workers', 'cf'],
    'alibaba cloud': ['alibaba cloud', 'alicloud', 'aliyun'],
    'oracle cloud': ['oracle cloud', 'oci', 'oracle cloud infrastructure'],

    # =========================
    # DevOps & CI/CD
    # =========================
    'docker': ['docker', 'docker containers', 'docker engine', 'docker-compose', 'dockerfile'],
    'kubernetes': ['kubernetes', 'k8s', 'kube', 'kubectl', 'aks', 'eks', 'gke'],
    'jenkins': ['jenkins', 'jenkins ci', 'jenkins pipeline'],
    'github actions': ['github actions', 'github ci', 'github workflows'],
    'gitlab ci': ['gitlab ci', 'gitlab ci/cd', 'gitlab pipelines'],
    'circleci': ['circleci', 'circle ci'],
    'travis ci': ['travis', 'travis ci', 'travis-ci'],
    'terraform': ['terraform', 'terraform iac', 'tf'],
    'ansible': ['ansible', 'ansible playbook', 'ansible automation'],
    'chef': ['chef', 'chef automation'],
    'puppet': ['puppet', 'puppet automation'],
    'argo': ['argo', 'argo cd', 'argo workflows'],
    'tekton': ['tekton', 'tekton pipelines'],

    # =========================
    # Version Control
    # =========================
    'git': ['git', 'git scm', 'git version control'],
    'github': ['github', 'github platform'],
    'gitlab': ['gitlab', 'gitlab platform'],
    'bitbucket': ['bitbucket', 'bitbucket pipeline'],

    # =========================
    # APIs & Integration
    # =========================
    'rest': ['rest', 'rest api', 'restful api', 'restful services'],
    'graphql': ['graphql', 'graphql api', 'gql'],
    'grpc': ['grpc', 'g rpc', 'grpc protocol'],
    'soap': ['soap', 'soap api', 'soap web services'],
    'webhooks': ['webhooks', 'webhook'],
    'openapi': ['openapi', 'swagger', 'openapi spec', 'api specification'],
    'postman': ['postman', 'postman api', 'postman testing'],

    # =========================
    # AI / Machine Learning
    # =========================
    'machine learning': ['machine learning', 'ml', 'ml models', 'supervised learning', 'unsupervised learning'],
    'deep learning': ['deep learning', 'dl', 'neural networks', 'cnn', 'rnn', 'lstm'],
    'artificial intelligence': ['artificial intelligence', 'ai', 'ai systems', 'intelligent systems'],
    'tensorflow': ['tensorflow', 'tf', 'tensorflow2'],
    'pytorch': ['pytorch', 'torch', 'pytorch framework'],
    'keras': ['keras', 'keras framework'],
    'scikit-learn': ['scikit learn', 'scikit-learn', 'sklearn', 'scikit'],
    'opencv': ['opencv', 'open cv', 'computer vision'],
    'hugging face': ['hugging face', 'huggingface', 'hf', 'transformers'],
    'langchain': ['langchain', 'lang chain', 'lc'],
    'llm': ['llm', 'large language model', 'foundation model', 'fm'],
    'rag': ['rag', 'retrieval augmented generation', 'rag system'],
    'prompt engineering': ['prompt engineering', 'prompting', 'prompt design'],
    'llama': ['llama', 'meta llama', 'llama 2', 'llama3'],
    'gpt': ['gpt', 'openai gpt', 'chatgpt', 'gpt-3', 'gpt-4', 'gpt-4o'],
    'bert': ['bert', 'bert model', 'google bert'],
    'computer vision': ['computer vision', 'cv', 'image recognition', 'object detection'],
    'nlp': ['nlp', 'natural language processing', 'text processing'],
    'data science': ['data science', 'data analytics', 'data analysis', 'data mining'],
    'big data': ['big data', 'large datasets', 'data engineering'],
    'spark': ['spark', 'apache spark', 'pyspark', 'spark sql'],
    'hadoop': ['hadoop', 'apache hadoop', 'hdfs', 'mapreduce'],
    'kafka': ['kafka', 'apache kafka', 'kafka streams'],
    'airflow': ['apache airflow', 'airflow', 'airflow dag'],
    'snowflake': ['snowflake', 'snowflake data', 'snowflake cloud'],
    'tableau': ['tableau', 'tableau visualization', 'tableau dashboard'],
    'power bi': ['power bi', 'microsoft power bi', 'powerbi', 'power bi dashboard'],
    'looker': ['looker', 'google looker', 'looker dashboard'],

    # =========================
    # Testing & Quality Assurance
    # =========================
    'junit': ['junit', 'junit4', 'junit5'],
    'pytest': ['pytest', 'py test'],
    'selenium': ['selenium', 'selenium webdriver'],
    'cypress': ['cypress', 'cypress testing'],
    'playwright': ['playwright', 'playwright testing'],
    'jest': ['jest', 'jest testing', 'react testing'],
    'mocha': ['mocha', 'mocha testing'],
    'chai': ['chai', 'chai assertion'],
    'testing library': ['testing library', 'react testing library', 'rtl'],
    'unit testing': ['unit testing', 'unit test', 'test driven development', 'tdd'],
    'integration testing': ['integration testing', 'integration test'],
    'e2e testing': ['e2e testing', 'end to end testing'],
    'performance testing': ['performance testing', 'load testing', 'stress testing'],
    'security testing': ['security testing', 'vulnerability testing', 'penetration testing'],
    'quality assurance': ['quality assurance', 'qa', 'qa testing', 'quality control'],
    'manual testing': ['manual testing', 'manual qa', 'functional testing'],
    'automation testing': ['automation testing', 'test automation', 'automation framework'],
    'api testing': ['api testing', 'api test', 'rest api testing'],
    'mobile testing': ['mobile testing', 'mobile app testing', 'android testing', 'ios testing'],
    'appium': ['appium', 'appium testing', 'appium mobile'],
    'testng': ['testng', 'testng framework'],

    # =========================
    # Security
    # =========================
    'oauth': ['oauth', 'oauth2', 'oauth 2.0', 'oauth protocol'],
    'jwt': ['jwt', 'json web token', 'jwt token'],
    'ssl': ['ssl', 'secure socket layer', 'ssl certificate'],
    'tls': ['tls', 'transport layer security'],
    'owasp': ['owasp', 'owasp top 10', 'owasp security'],
    'penetration testing': ['penetration testing', 'pen testing', 'pentest', 'ethical hacking'],
    'vulnerability assessment': ['vulnerability assessment', 'va', 'vulnerability scanning'],
    'security auditing': ['security auditing', 'security audit', 'audit'],
    'identity management': ['identity management', 'idm', 'access management', 'iam'],
    'security compliance': ['security compliance', 'compliance', 'gdpr', 'hipaa', 'pci dss'],
    'encryption': ['encryption', 'data encryption', 'cryptography'],
    'firewall': ['firewall', 'firewall management', 'network firewall'],
    'zero trust': ['zero trust', 'zero trust architecture', 'zero trust security'],
    'devsecops': ['devsecops', 'security devops'],

    # =========================
    # Architecture & Design Patterns
    # =========================
    'microservices': ['microservices', 'microservice architecture', 'microservices architecture'],
    'monolith': ['monolith', 'monolithic', 'monolithic architecture'],
    'serverless': ['serverless', 'serverless architecture', 'aws lambda'],
    'event driven architecture': ['event driven architecture', 'eda', 'event driven design'],
    'mvc': ['mvc', 'model view controller', 'mvc pattern'],
    'mvvm': ['mvvm', 'model view viewmodel'],
    'clean architecture': ['clean architecture', 'clean code', 'clean design'],
    'domain driven design': ['domain driven design', 'ddd', 'domain driven'],
    'solid': ['solid', 'solid principles', 'solid design'],
    'design patterns': ['design patterns', 'gang of four', 'gof patterns'],
    'restful design': ['restful design', 'rest api design', 'restful architecture'],
    'event sourcing': ['event sourcing', 'event sourcing architecture'],
    'cqrs': ['cqrs', 'command query responsibility segregation'],

    # =========================
    # Operating Systems
    # =========================
    'linux': ['linux', 'linux os', 'linux kernel', 'linux environment'],
    'ubuntu': ['ubuntu', 'ubuntu os', 'ubuntu linux'],
    'windows': ['windows', 'windows os', 'windows server'],
    'macos': ['macos', 'mac os', 'os x', 'macintosh'],
    'unix': ['unix', 'unix os', 'unix systems'],

    # =========================
    # Networking
    # =========================
    'tcp/ip': ['tcp/ip', 'tcp ip', 'tcp/ip protocol', 'ip networking'],
    'http': ['http', 'http protocol', 'https', 'http/2', 'http/3'],
    'dns': ['dns', 'domain name system', 'dns server'],
    'ftp': ['ftp', 'file transfer protocol', 'sftp'],
    'ssh': ['ssh', 'secure shell', 'ssh protocol'],
    'load balancing': ['load balancing', 'load balancer', 'lb'],
    'cdn': ['cdn', 'content delivery network', 'cloud cdn'],

    # =========================
    # Messaging & Queues
    # =========================
    'rabbitmq': ['rabbitmq', 'rabbit mq', 'rabbitmq broker'],
    'activemq': ['activemq', 'active mq', 'apache activemq'],
    'sqs': ['sqs', 'amazon sqs', 'aws sqs', 'simple queue service'],
    'sns': ['sns', 'amazon sns', 'aws sns', 'simple notification service'],
    'pubsub': ['pubsub', 'publish subscribe', 'google pubsub'],
    'kafka': ['kafka', 'apache kafka', 'kafka streaming'],

    # =========================
    # Monitoring & Observability
    # =========================
    'grafana': ['grafana', 'grafana dashboard'],
    'prometheus': ['prometheus', 'prometheus monitoring'],
    'elk stack': ['elk', 'elk stack', 'elasticsearch logstash kibana'],
    'splunk': ['splunk', 'splunk monitoring'],
    'datadog': ['datadog', 'ddog', 'datadog monitoring'],
    'new relic': ['new relic', 'newrelic', 'nr'],
    'cloudwatch': ['cloudwatch', 'aws cloudwatch', 'amazon cloudwatch'],
    'appdynamics': ['appdynamics', 'app dynamics'],
    'dynatrace': ['dynatrace', 'dt'],

    # =========================
    # Project Management & Tools
    # =========================
    'agile': ['agile', 'agile methodology', 'agile development'],
    'scrum': ['scrum', 'scrum master', 'scrum framework'],
    'kanban': ['kanban', 'kanban board', 'kanban methodology'],
    'jira': ['jira', 'jira software', 'atlassian jira'],
    'confluence': ['confluence', 'confluence wiki', 'atlassian confluence'],
    'trello': ['trello', 'trello board'],
    'asana': ['asana', 'asana project management'],
    'monday.com': ['monday', 'monday.com', 'monday platform'],
    'notion': ['notion', 'notion workspace'],
    'slack': ['slack', 'slack communication'],
    'microsoft teams': ['microsoft teams', 'msteams', 'teams'],
    'zoom': ['zoom', 'zoom meeting'],
    'smartsheet': ['smartsheet', 'smartsheet management'],
    'basecamp': ['basecamp', 'basecamp project'],

    # =========================
    # HR & Talent Management
    # =========================
    # Core HR
    'human resources': ['human resources', 'hr', 'human resource management', 'hrm', 'hr management'],
    'hr operations': ['hr operations', 'hr ops', 'hr administration'],
    'hr strategy': ['hr strategy', 'strategic hr', 'hr planning'],
    
    # Talent Acquisition & Recruitment
    'talent acquisition': ['talent acquisition', 'ta', 'recruitment', 'recruiting', 'talent sourcing', 'sourcing'],
    'full cycle recruiting': ['full cycle recruiting', 'end to end recruitment', '360 recruiting', 'full recruitment lifecycle'],
    'candidate sourcing': ['candidate sourcing', 'talent sourcing', 'source candidates', 'sourcing strategy'],
    'candidate screening': ['candidate screening', 'resume screening', 'application screening'],
    'candidate assessment': ['candidate assessment', 'candidate evaluation', 'assessment tools'],
    'interviewing': ['interviewing', 'interview techniques', 'behavioral interviewing', 'structured interviews'],
    'offer management': ['offer management', 'offer negotiation', 'offer letter', 'compensation negotiation'],
    'onboarding': ['onboarding', 'new hire onboarding', 'employee onboarding', 'orientation'],
    'recruitment marketing': ['recruitment marketing', 'employer branding', 'talent branding'],
    'applicant tracking system': ['applicant tracking system', 'ats', 'applicant tracking'],
    'workday': ['workday', 'workday hcm', 'workday recruitment', 'workday platform'],
    'greenhouse': ['greenhouse', 'greenhouse ats', 'greenhouse recruiting'],
    'lever': ['lever', 'lever ats', 'lever recruitment'],
    'recruiter': ['recruiter', 'linkedin recruiter', 'linkedin talent'],
    
    # Employee Relations & Engagement
    'employee relations': ['employee relations', 'er', 'employee engagement', 'employee satisfaction'],
    'employee engagement': ['employee engagement', 'engagement strategies', 'employee motivation'],
    'employee retention': ['employee retention', 'retention strategies', 'turnover reduction'],
    'employee experience': ['employee experience', 'ex', 'employee journey'],
    'employee wellness': ['employee wellness', 'wellness programs', 'wellbeing', 'work life balance'],
    'diversity and inclusion': ['diversity and inclusion', 'd&i', 'dei', 'diversity equity inclusion', 'belonging'],
    'workplace culture': ['workplace culture', 'company culture', 'organizational culture', 'culture building'],
    'organizational development': ['organizational development', 'od', 'org development', 'change management'],
    'change management': ['change management', 'organizational change', 'change implementation'],
    
    # Performance Management
    'performance management': ['performance management', 'performance review', 'appraisal', 'performance evaluation'],
    'performance appraisal': ['performance appraisal', 'appraisal system', 'review process'],
    'goal setting': ['goal setting', 'okr', 'kpi', 'objectives and key results', 'performance goals'],
    'performance improvement plan': ['performance improvement plan', 'pip', 'improvement plan'],
    'talent management': ['talent management', 'talent development', 'talent strategy'],
    'succession planning': ['succession planning', 'succession management', 'talent pipeline'],
    'career development': ['career development', 'career progression', 'career pathing'],
    'career counseling': ['career counseling', 'career advising', 'career guidance'],
    'mentoring': ['mentoring', 'mentorship', 'mentoring program'],
    'coaching': ['coaching', 'employee coaching', 'performance coaching'],
    
    # Learning & Development
    'learning and development': ['learning and development', 'l&d', 'learning development', 'training development'],
    'training': ['training', 'training programs', 'employee training', 'staff training'],
    'training delivery': ['training delivery', 'training facilitation', 'conducting training'],
    'training needs analysis': ['training needs analysis', 'tna', 'training gap analysis'],
    'learning management system': ['learning management system', 'lms', 'learning platform'],
    'elearning': ['elearning', 'online learning', 'digital learning', 'virtual training'],
    'instructional design': ['instructional design', 'curriculum design', 'training design'],
    'workshop facilitation': ['workshop facilitation', 'facilitation', 'workshop delivery'],
    'corporate training': ['corporate training', 'corporate learning', 'professional development'],
    
    # Compensation & Benefits
    'compensation': ['compensation', 'compensation management', 'salary administration', 'pay structure'],
    'compensation and benefits': ['compensation and benefits', 'c&b', 'total rewards', 'comp & ben'],
    'benefits administration': ['benefits administration', 'employee benefits', 'benefits management'],
    'salary benchmarking': ['salary benchmarking', 'salary surveys', 'market pricing'],
    'payroll': ['payroll', 'payroll management', 'payroll processing'],
    'incentive programs': ['incentive programs', 'bonus programs', 'performance incentives'],
    'stock options': ['stock options', 'equity compensation', 'employee stock'],
    
    # HR Compliance & Legal
    'hr compliance': ['hr compliance', 'compliance', 'employment compliance', 'regulatory compliance'],
    'labor law': ['labor law', 'employment law', 'labor legislation'],
    'hr policies': ['hr policies', 'hr policy development', 'employee policies'],
    'employee handbook': ['employee handbook', 'handbook development', 'policy manual'],
    'workplace safety': ['workplace safety', 'ohs', 'health and safety', 'occupational safety'],
    'data privacy': ['data privacy', 'gdpr compliance', 'privacy regulations', 'data protection'],
    'union relations': ['union relations', 'labor relations', 'collective bargaining'],
    
    # HRIS & Technology
    'hris': ['hris', 'hr information system', 'hr system', 'hr technology'],
    'hr analytics': ['hr analytics', 'people analytics', 'workforce analytics', 'hr data analysis'],
    'people analytics': ['people analytics', 'workforce analytics', 'talent analytics'],
    'human capital management': ['human capital management', 'hcm', 'human capital', 'hc'],
    'hr reporting': ['hr reporting', 'hr metrics', 'hr dashboards', 'workforce reporting'],
    'workforce planning': ['workforce planning', 'workforce management', 'staffing planning'],
    'headcount planning': ['headcount planning', 'resource planning', 'capacity planning'],

    # =========================
    # Business Development
    # =========================
    # Core Business Development
    'business development': ['business development', 'bd', 'new business', 'business growth'],
    'business strategy': ['business strategy', 'strategic planning', 'corporate strategy', 'business planning'],
    'market expansion': ['market expansion', 'market growth', 'territory expansion', 'geographic expansion'],
    'strategic partnerships': ['strategic partnerships', 'partnership development', 'strategic alliances'],
    'new market entry': ['new market entry', 'market entry strategy', 'market penetration'],
    'competitive analysis': ['competitive analysis', 'competitor analysis', 'market intelligence'],
    'market research': ['market research', 'market analysis', 'market study', 'industry research'],
    'market analysis': ['market analysis', 'market assessment', 'market evaluation'],
    'industry analysis': ['industry analysis', 'industry research', 'sector analysis'],
    'due diligence': ['due diligence', 'business due diligence', 'financial due diligence'],
    
    # Sales & Revenue
    'sales': ['sales', 'sales management', 'sales strategy', 'selling'],
    'sales strategy': ['sales strategy', 'sales planning', 'sales approach', 'sales methodology'],
    'revenue growth': ['revenue growth', 'revenue generation', 'revenue development', 'top line growth'],
    'sales pipeline': ['sales pipeline', 'pipeline management', 'deal pipeline'],
    'lead generation': ['lead generation', 'lead gen', 'new leads', 'prospecting'],
    'client acquisition': ['client acquisition', 'customer acquisition', 'new client development'],
    'account management': ['account management', 'client management', 'customer retention'],
    'key account management': ['key account management', 'kam', 'strategic accounts'],
    'sales operations': ['sales operations', 'sales ops', 'sales enablement'],
    'sales enablement': ['sales enablement', 'sales tools', 'sales support'],
    'cold calling': ['cold calling', 'cold outreach', 'sales calls'],
    'proposal writing': ['proposal writing', 'proposal development', 'rfp response', 'bid management'],
    'contract negotiation': ['contract negotiation', 'negotiation', 'deal negotiation', 'contract management'],
    'closing deals': ['closing deals', 'deal closing', 'sales closing', 'deal execution'],
    'sales forecasting': ['sales forecasting', 'forecasting', 'revenue forecasting'],
    'quote to cash': ['quote to cash', 'quote to cash process', 'q2c'],
    
    # Relationship Management
    'relationship building': ['relationship building', 'relationship management', 'client relationships', 'stakeholder management'],
    'stakeholder management': ['stakeholder management', 'stakeholder engagement', 'stakeholder communication'],
    'network development': ['network development', 'networking', 'business networking', 'professional networking'],
    'crm': ['crm', 'customer relationship management', 'salesforce crm', 'hubspot'],
    'salesforce': ['salesforce', 'salesforce crm', 'salesforce platform'],
    'hubspot': ['hubspot', 'hubspot crm', 'hubspot platform'],
    'pipeline management': ['pipeline management', 'sales pipeline management'],
    
    # Business Planning
    'business planning': ['business planning', 'business plan', 'strategic planning'],
    'go-to-market strategy': ['go-to-market strategy', 'gtm', 'go to market', 'market launch'],
    'business model': ['business model', 'business model innovation', 'business design'],
    'business case': ['business case', 'business justification', 'proposal development'],
    'investment analysis': ['investment analysis', 'investment evaluation', 'roi analysis'],
    'financial modeling': ['financial modeling', 'financial models', 'financial analysis'],
    'budgeting': ['budgeting', 'budget management', 'financial planning'],
    
    # Business Communication
    'executive presentations': ['executive presentations', 'executive summary', 'board presentations'],
    'pitch deck creation': ['pitch deck', 'investor pitch', 'pitch presentation', 'slide deck'],
    'public speaking': ['public speaking', 'presentations', 'speaking engagements'],
    'business writing': ['business writing', 'professional writing', 'business communication'],
    
    # Strategic Planning
    'strategic thinking': ['strategic thinking', 'strategic mindset', 'strategic approach'],
    'strategic planning': ['strategic planning', 'strategy development', 'strategy formulation'],
    'strategic initiatives': ['strategic initiatives', 'strategic projects', 'key initiatives'],
    'mergers and acquisitions': ['mergers and acquisitions', 'm&a', 'acquisitions', 'mergers'],
    'joint ventures': ['joint ventures', 'jv', 'strategic alliances', 'partnerships'],
    'license agreements': ['license agreements', 'licensing', 'ip licensing', 'technology licensing'],
    'venture capital': ['venture capital', 'vc', 'investment management', 'funding'],
    'fundraising': ['fundraising', 'funding', 'capital raising', 'investor relations'],
    
    # International Business
    'international business': ['international business', 'global business', 'cross-border', 'multinational'],
    'global strategy': ['global strategy', 'international strategy', 'global expansion'],
    'export': ['export', 'export management', 'international trade'],
    'import': ['import', 'import management', 'import/export'],
    'global supply chain': ['global supply chain', 'global sourcing', 'international logistics'],

    # =========================
    # Marketing (for BD support)
    # =========================
    'marketing': ['marketing', 'marketing strategy', 'marketing management'],
    'digital marketing': ['digital marketing', 'online marketing', 'internet marketing'],
    'content marketing': ['content marketing', 'content strategy', 'content creation'],
    'social media marketing': ['social media marketing', 'smm', 'social marketing'],
    'branding': ['branding', 'brand management', 'brand strategy'],
    'brand management': ['brand management', 'brand building', 'brand development'],
    'public relations': ['public relations', 'pr', 'media relations'],
    'communications': ['communications', 'corporate communications', 'strategic communications'],
    'email marketing': ['email marketing', 'email campaigns', 'mailchimp'],
    'seo': ['seo', 'search engine optimization', 'search marketing'],
    'sem': ['sem', 'search engine marketing', 'paid search'],
    'google analytics': ['google analytics', 'ga', 'analytics'],
    'product marketing': ['product marketing', 'product go to market'],
    'growth hacking': ['growth hacking', 'growth marketing', 'growth strategy'],

    # =========================
    # Leadership & Management
    # =========================
    'leadership': ['leadership', 'leadership skills', 'people leadership', 'team leadership'],
    'team leadership': ['team leadership', 'team lead', 'leading teams', 'team management'],
    'people management': ['people management', 'personnel management', 'staff management'],
    'project leadership': ['project leadership', 'project lead', 'leading projects'],
    'strategic leadership': ['strategic leadership', 'executive leadership', 'leadership strategy'],
    'mentorship': ['mentorship', 'mentoring', 'coaching', 'people development'],
    'team building': ['team building', 'building teams', 'team development'],
    'delegation': ['delegation', 'task delegation', 'work delegation'],
    'decision making': ['decision making', 'decision-making', 'strategic decisions'],
    'problem solving': ['problem solving', 'analytical problem solving', 'solution finding'],
    'critical thinking': ['critical thinking', 'critical analysis', 'analytical thinking'],
    'time management': ['time management', 'time optimization', 'prioritization'],
    'project management': ['project management', 'project delivery', 'project coordination'],
    'program management': ['program management', 'program delivery', 'program leadership'],
    'resource management': ['resource management', 'resource allocation', 'resource planning'],
    'stakeholder management': ['stakeholder management', 'stakeholder engagement'],
    'conflict resolution': ['conflict resolution', 'conflict management', 'mediation'],
    'negotiation': ['negotiation', 'negotiating', 'deal making'],
    'influencing': ['influencing', 'influence', 'persuasion', 'negotiation'],
    'cross-functional collaboration': ['cross-functional collaboration', 'cross-functional teams', 'cross team collaboration'],
    'remote team management': ['remote team management', 'distributed teams', 'virtual teams'],
    
    # =========================
    # Communication
    # =========================
    'communication': ['communication', 'excellent communication', 'strong communication', 'effective communication'],
    'verbal communication': ['verbal communication', 'spoken communication', 'oral communication'],
    'written communication': ['written communication', 'writing skills', 'written skills'],
    'presentation skills': ['presentation skills', 'presenting', 'public speaking'],
    'interpersonal skills': ['interpersonal skills', 'people skills', 'soft skills'],
    'active listening': ['active listening', 'listening skills', 'empathy'],
    'emotional intelligence': ['emotional intelligence', 'eq', 'emotional awareness'],
    'collaboration': ['collaboration', 'teamwork', 'collaborative', 'team player'],
    'negotiation': ['negotiation', 'negotiating', 'persuasion', 'influence'],

    # =========================
    # Financial Management
    # =========================
    'financial analysis': ['financial analysis', 'financial modeling', 'financial evaluation'],
    'financial management': ['financial management', 'finance management', 'financial planning'],
    'budget management': ['budget management', 'budgeting', 'cost management'],
    'cost analysis': ['cost analysis', 'cost benefit analysis', 'cba'],
    'forecasting': ['forecasting', 'financial forecasting', 'predictive modeling'],
    'risk assessment': ['risk assessment', 'risk analysis', 'risk evaluation'],
    'audit': ['audit', 'financial audit', 'internal audit', 'external audit'],
    'accounting': ['accounting', 'financial accounting', 'management accounting'],
    'accounts payable': ['accounts payable', 'ap', 'payables', 'vendor payments'],
    'accounts receivable': ['accounts receivable', 'ar', 'receivables', 'invoicing'],
    'tax compliance': ['tax compliance', 'taxation', 'tax management'],
    
    # =========================
    # Legal (for BD and HR)
    # =========================
    'contract law': ['contract law', 'contract management', 'contract review'],
    'corporate law': ['corporate law', 'business law', 'company law'],
    'intellectual property': ['intellectual property', 'ip', 'patents', 'trademarks', 'copyright'],
    'commercial law': ['commercial law', 'trade law', 'business regulations'],
    'regulatory compliance': ['regulatory compliance', 'compliance management', 'regulations'],
    'commercial contracts': ['commercial contracts', 'business contracts', 'contract negotiation'],
    'employment law': ['employment law', 'labor law', 'employee rights'],
    'data privacy': ['data privacy', 'gdpr', 'data protection', 'privacy compliance'],
    'compliance management': ['compliance management', 'regulatory compliance', 'compliance officer'],
    'legal research': ['legal research', 'legal analysis', 'case law research'],

    # =========================
    # Consulting
    # =========================
    'management consulting': ['management consulting', 'consulting', 'business consulting'],
    'strategy consulting': ['strategy consulting', 'strategic consulting'],
    'change management': ['change management', 'organizational change', 'transformation'],
    'process improvement': ['process improvement', 'business process improvement', 'bpi'],
    'business transformation': ['business transformation', 'transformation management'],
    'digital transformation': ['digital transformation', 'digital strategy'],
    'data driven decision making': ['data driven decision making', 'data driven decisions', 'dddm'],
    'analytics': ['analytics', 'data analytics', 'business analytics'],
    'kpi': ['kpi', 'key performance indicators', 'metrics', 'measurement'],
    'benchmarking': ['benchmarking', 'performance benchmarking', 'competitive benchmarking'],

    # =========================
    # Languages
    # =========================
    'english': ['english', 'fluent english', 'english language', 'native english'],
    'spanish': ['spanish', 'español', 'spanish language'],
    'french': ['french', 'français', 'french language'],
    'german': ['german', 'deutsch', 'german language'],
    'mandarin': ['mandarin', 'chinese', '普通话', 'mandarin chinese'],
    'arabic': ['arabic', 'العربية', 'arabic language'],
    'hindi': ['hindi', 'हिन्दी', 'hindi language'],
    'japanese': ['japanese', '日本語', 'japanese language'],

    # =========================
    # Additional Technical Skills
    # =========================
    'blockchain': ['blockchain', 'blockchain technology', 'distributed ledger', 'web3'],
    'ethereum': ['ethereum', 'eth', 'solidity'],
    'smart contracts': ['smart contracts', 'smart contract development'],
    'web3': ['web3', 'web3.0', 'web3 development'],
    'reactjs': ['reactjs', 'react', 'react.js'],
    'vuejs': ['vuejs', 'vue', 'vue.js'],
    'angularjs': ['angularjs', 'angular', 'angular.js'],
    'nodejs': ['nodejs', 'node', 'node.js'],
    'expressjs': ['expressjs', 'express', 'express.js'],
    'flask': ['flask', 'flask framework', 'python flask'],
    'django': ['django', 'django framework', 'python django'],
    'spring boot': ['spring boot', 'springboot', 'spring-boot'],
    'apache': ['apache', 'apache server', 'httpd'],
    'nginx': ['nginx', 'nginx server', 'nginx web server'],
    'tomcat': ['tomcat', 'apache tomcat'],
    'jboss': ['jboss', 'wildfly'],
    'weblogic': ['weblogic', 'oracle weblogic'],
    'websphere': ['websphere', 'ibm websphere'],
}

# ============================================================
# Skill Categories
# ============================================================

SKILL_CATEGORIES: Dict[str, Set[str]] = {
    # Technical Skills
    'programming_languages': {
        'python', 'javascript', 'typescript', 'java', 'c', 'c++', 'c#', 'go', 'rust',
        'kotlin', 'swift', 'php', 'ruby', 'scala', 'perl', 'r', 'matlab', 'dart',
        'objective-c', 'bash', 'powershell', 'assembly'
    },
    'frontend': {
        'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind css', 'material ui',
        'ant design', 'chakra ui', 'react', 'next.js', 'vue', 'nuxt.js', 'angular',
        'svelte', 'redux', 'mobx', 'webpack', 'vite', 'jquery'
    },
    'backend': {
        'node.js', 'express.js', 'nestjs', 'django', 'flask', 'fastapi',
        'spring boot', 'spring', 'asp.net', '.net', 'laravel', 'symfony',
        'ruby on rails', 'gin', 'echo'
    },
    'mobile': {
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
        'kotlin android', 'swift ios'
    },
    'databases': {
        'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server',
        'mongodb', 'redis', 'cassandra', 'dynamodb', 'firebase', 'elasticsearch',
        'neo4j', 'influxdb', 'couchdb', 'supabase'
    },
    'cloud': {
        'aws', 'azure', 'gcp', 'digitalocean', 'heroku', 'vercel', 'netlify',
        'cloudflare', 'alibaba cloud', 'oracle cloud'
    },
    'devops': {
        'docker', 'kubernetes', 'jenkins', 'github actions', 'gitlab ci',
        'circleci', 'travis ci', 'terraform', 'ansible', 'chef', 'puppet',
        'argo', 'tekton'
    },
    'version_control': {
        'git', 'github', 'gitlab', 'bitbucket'
    },
    'apis': {
        'rest', 'graphql', 'grpc', 'soap', 'webhooks', 'openapi', 'postman'
    },
    'ai_ml': {
        'machine learning', 'deep learning', 'artificial intelligence',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'opencv',
        'hugging face', 'langchain', 'llm', 'rag', 'prompt engineering',
        'llama', 'gpt', 'bert', 'computer vision', 'nlp', 'data science'
    },
    'big_data': {
        'big data', 'spark', 'hadoop', 'kafka', 'airflow', 'snowflake',
        'tableau', 'power bi', 'looker'
    },
    'testing': {
        'junit', 'pytest', 'selenium', 'cypress', 'playwright', 'jest',
        'mocha', 'chai', 'testing library', 'unit testing', 'integration testing',
        'e2e testing', 'performance testing', 'security testing',
        'quality assurance', 'manual testing', 'automation testing',
        'api testing', 'mobile testing', 'appium', 'testng'
    },
    'security': {
        'oauth', 'jwt', 'ssl', 'tls', 'owasp', 'penetration testing',
        'vulnerability assessment', 'security auditing', 'identity management',
        'security compliance', 'encryption', 'firewall', 'zero trust',
        'devsecops'
    },
    'architecture': {
        'microservices', 'monolith', 'serverless', 'event driven architecture',
        'mvc', 'mvvm', 'clean architecture', 'domain driven design', 'solid',
        'design patterns', 'restful design', 'event sourcing', 'cqrs'
    },
    'os': {
        'linux', 'ubuntu', 'windows', 'macos', 'unix'
    },
    'networking': {
        'tcp/ip', 'http', 'dns', 'ftp', 'ssh', 'load balancing', 'cdn'
    },
    'messaging': {
        'rabbitmq', 'activemq', 'sqs', 'sns', 'pubsub', 'kafka'
    },
    'monitoring': {
        'grafana', 'prometheus', 'elk stack', 'splunk', 'datadog',
        'new relic', 'cloudwatch', 'appdynamics', 'dynatrace'
    },
    
    # HR Skills
    'hr_core': {
        'human resources', 'hr operations', 'hr strategy'
    },
    'talent_acquisition': {
        'talent acquisition', 'full cycle recruiting', 'candidate sourcing',
        'candidate screening', 'candidate assessment', 'interviewing',
        'offer management', 'onboarding', 'recruitment marketing',
        'applicant tracking system', 'workday', 'greenhouse', 'lever', 'recruiter'
    },
    'employee_relations': {
        'employee relations', 'employee engagement', 'employee retention',
        'employee experience', 'employee wellness', 'diversity and inclusion',
        'workplace culture', 'organizational development', 'change management'
    },
    'performance_management': {
        'performance management', 'performance appraisal', 'goal setting',
        'performance improvement plan', 'talent management', 'succession planning',
        'career development', 'career counseling', 'mentoring', 'coaching'
    },
    'learning_development': {
        'learning and development', 'training', 'training delivery',
        'training needs analysis', 'learning management system', 'elearning',
        'instructional design', 'workshop facilitation', 'corporate training'
    },
    'compensation_benefits': {
        'compensation', 'compensation and benefits', 'benefits administration',
        'salary benchmarking', 'payroll', 'incentive programs', 'stock options'
    },
    'hr_compliance': {
        'hr compliance', 'labor law', 'hr policies', 'employee handbook',
        'workplace safety', 'data privacy', 'union relations'
    },
    'hris': {
        'hris', 'hr analytics', 'people analytics', 'human capital management',
        'hr reporting', 'workforce planning', 'headcount planning'
    },
    
    # Business Development Skills
    'business_development': {
        'business development', 'business strategy', 'market expansion',
        'strategic partnerships', 'new market entry', 'competitive analysis',
        'market research', 'market analysis', 'industry analysis', 'due diligence'
    },
    'sales': {
        'sales', 'sales strategy', 'revenue growth', 'sales pipeline',
        'lead generation', 'client acquisition', 'account management',
        'key account management', 'sales operations', 'sales enablement',
        'cold calling', 'proposal writing', 'contract negotiation',
        'closing deals', 'sales forecasting', 'quote to cash'
    },
    'relationship_management': {
        'relationship building', 'stakeholder management', 'network development',
        'crm', 'salesforce', 'hubspot', 'pipeline management'
    },
    'business_planning': {
        'business planning', 'go-to-market strategy', 'business model',
        'business case', 'investment analysis', 'financial modeling',
        'budgeting'
    },
    'business_communication': {
        'executive presentations', 'pitch deck creation', 'public speaking',
        'business writing'
    },
    'strategic_planning': {
        'strategic thinking', 'strategic planning', 'strategic initiatives',
        'mergers and acquisitions', 'joint ventures', 'license agreements',
        'venture capital', 'fundraising'
    },
    'international_business': {
        'international business', 'global strategy', 'export', 'import',
        'global supply chain'
    },
    
    # Marketing Skills
    'marketing': {
        'marketing', 'digital marketing', 'content marketing',
        'social media marketing', 'branding', 'brand management',
        'public relations', 'communications', 'email marketing',
        'seo', 'sem', 'google analytics', 'product marketing',
        'growth hacking'
    },
    
    # Leadership & Management
    'leadership': {
        'leadership', 'team leadership', 'people management', 'project leadership',
        'strategic leadership', 'mentorship', 'team building', 'delegation',
        'decision making', 'problem solving', 'critical thinking',
        'time management', 'project management', 'program management',
        'resource management', 'stakeholder management', 'conflict resolution',
        'negotiation', 'influencing', 'cross-functional collaboration',
        'remote team management'
    },
    'communication_skills': {
        'communication', 'verbal communication', 'written communication',
        'presentation skills', 'interpersonal skills', 'active listening',
        'emotional intelligence', 'collaboration', 'negotiation'
    },
    
    # Financial Skills
    'financial': {
        'financial analysis', 'financial management', 'budget management',
        'cost analysis', 'forecasting', 'risk assessment', 'audit',
        'accounting', 'accounts payable', 'accounts receivable', 'tax compliance'
    },
    
    # Legal Skills
    'legal': {
        'contract law', 'corporate law', 'intellectual property',
        'commercial law', 'regulatory compliance', 'commercial contracts',
        'employment law', 'data privacy', 'compliance management', 'legal research'
    },
    
    # Consulting Skills
    'consulting': {
        'management consulting', 'strategy consulting', 'change management',
        'process improvement', 'business transformation', 'digital transformation',
        'data driven decision making', 'analytics', 'kpi', 'benchmarking'
    },
    
    # Project Management Tools
    'project_tools': {
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'trello',
        'asana', 'monday.com', 'notion', 'slack', 'microsoft teams',
        'zoom', 'smartsheet', 'basecamp'
    },
    
    # Languages
    'languages': {
        'english', 'spanish', 'french', 'german', 'mandarin', 'arabic',
        'hindi', 'japanese'
    },
    
    # Additional
    'additional_tech': {
        'blockchain', 'ethereum', 'smart contracts', 'web3', 'reactjs',
        'vuejs', 'angularjs', 'nodejs', 'expressjs', 'flask', 'django',
        'spring boot', 'apache', 'nginx', 'tomcat', 'jboss', 'weblogic',
        'websphere'
    }
}

# ============================================================
# Helper Functions
# ============================================================

def get_all_skills() -> Set[str]:
    """Return all skill names as a set."""
    return set(COMMON_VARIATIONS.keys())


def get_all_skill_variations() -> Set[str]:
    """Return all skill variations as a flat set."""
    all_variations = set()
    for variations in COMMON_VARIATIONS.values():
        all_variations.update(variations)
    return all_variations


def get_skill_variations(skill: str) -> List[str]:
    """Get all variations for a specific skill."""
    return COMMON_VARIATIONS.get(skill, [])


def get_skills_by_category(category: str) -> Set[str]:
    """Get all skills in a specific category."""
    return SKILL_CATEGORIES.get(category, set())


def get_category_for_skill(skill: str) -> List[str]:
    """Find which category(ies) a skill belongs to."""
    categories = []
    for category, skills in SKILL_CATEGORIES.items():
        if skill in skills:
            categories.append(category)
    return categories


def is_hr_skill(skill: str) -> bool:
    """Check if a skill is HR-related."""
    hr_categories = {
        'hr_core', 'talent_acquisition', 'employee_relations',
        'performance_management', 'learning_development',
        'compensation_benefits', 'hr_compliance', 'hris'
    }
    for category in get_category_for_skill(skill):
        if category in hr_categories:
            return True
    return False


def is_business_skill(skill: str) -> bool:
    """Check if a skill is business-related."""
    business_categories = {
        'business_development', 'sales', 'relationship_management',
        'business_planning', 'business_communication', 'strategic_planning',
        'international_business', 'marketing'
    }
    for category in get_category_for_skill(skill):
        if category in business_categories:
            return True
    return False


def is_management_skill(skill: str) -> bool:
    """Check if a skill is management-related."""
    management_categories = {
        'leadership', 'project_tools', 'consulting', 'financial'
    }
    for category in get_category_for_skill(skill):
        if category in management_categories:
            return True
    return False


def is_technical_skill(skill: str) -> bool:
    """Check if a skill is technical."""
    tech_categories = {
        'programming_languages', 'frontend', 'backend', 'mobile',
        'databases', 'cloud', 'devops', 'version_control', 'apis',
        'ai_ml', 'big_data', 'testing', 'security', 'architecture',
        'os', 'networking', 'messaging', 'monitoring', 'additional_tech'
    }
    for category in get_category_for_skill(skill):
        if category in tech_categories:
            return True
    return False