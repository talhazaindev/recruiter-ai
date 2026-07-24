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
    # Programming Languages (Extended)
    # =========================
    'python': ['python', 'py', 'python3', 'python 3', 'python2', 'python 2', 'cpython', 'pypy', 'anaconda python', 'jupyter python', 'python programming', 'python development', 'python scripting', 'python automation', 'python data science'],
    'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015', 'es2020', 'es2021', 'es2022', 'es2023', 'vanilla js', 'node js', 'javascript programming', 'javascript development', 'jsx', 'ecmascript 6'],
    'typescript': ['typescript', 'ts', 'typescriptlang', 'tslang', 'typed javascript', 'tsx', 'typescript programming', 'typescript development'],
    'java': ['java', 'java 8', 'java 11', 'java 17', 'java 21', 'jdk', 'jre', 'openjdk', 'oracle java', 'spring java', 'java enterprise', 'java development', 'core java', 'advanced java'],
    'c': ['c language', 'ansi c', 'c', 'c99', 'c11', 'c17', 'c23', 'c programming', 'gnu c', 'c development', 'system programming', 'embedded c'],
    'c++': ['c++', 'cpp', 'cplusplus', 'c++11', 'c++14', 'c++17', 'c++20', 'c++23', 'modern cpp', 'stl', 'c++ development', 'cpp programming', 'c++ boost'],
    'c#': ['c#', 'c sharp', 'csharp', 'c#.net', 'dotnet c#', 'csharp .net', 'c# programming', 'c# development', 'c# unity'],
    'go': ['go', 'golang', 'golanglang', 'golang programming', 'golang development', 'go-lang', 'gopher', 'go language'],
    'rust': ['rust', 'rustlang', 'rust programming', 'cargo', 'rustc', 'rust development', 'rust systems programming'],
    'kotlin': ['kotlin', 'kotlinlang', 'kotlin programming', 'kotlin multiplatform', 'kotlin android', 'kotlin development'],
    'swift': ['swift', 'swiftlang', 'swift programming', 'apple swift', 'swift ios', 'swift macos', 'swift development'],
    'php': ['php', 'php7', 'php8', 'php hypertext preprocessor', 'php5', 'php8.1', 'php8.2', 'php8.3', 'php programming', 'php development', 'laravel php'],
    'ruby': ['ruby', 'ruby lang', 'ruby programming', 'ruby on rails', 'ruby gem', 'ruby development', 'jruby', 'ruby scripting'],
    'scala': ['scala', 'scalalang', 'scala programming', 'akka scala', 'spark scala', 'scala development'],
    'perl': ['perl', 'perl5', 'perl programming', 'perl script', 'perl6', 'raku', 'perl development'],
    'r': ['r', 'r language', 'r programming', 'rstudio', 'r statistical', 'r shiny', 'cran', 'tidyverse', 'r data science'],
    'matlab': ['matlab', 'matrix laboratory', 'matlab programming', 'simulink', 'octave', 'matlab development'],
    'dart': ['dart', 'dartlang', 'dart programming', 'dart flutter', 'dart development'],
    'objective-c': ['objective c', 'objective-c', 'objc', 'obj-c', 'objective c programming', 'apple objective-c'],
    'bash': ['bash', 'shell scripting', 'shell', 'bash scripting', 'sh', 'bourne shell', 'zsh', 'ksh', 'shell programming', 'bash automation'],
    'powershell': ['powershell', 'ps', 'powershell scripting', 'pwsh', 'powershell core', 'powershell automation', 'powershell development'],
    'assembly': ['assembly', 'asm', 'assembler', 'assembly language', 'x86 assembly', 'arm assembly', 'masm', 'nasm', 'assembly programming'],
    'julia': ['julia', 'julialang', 'julia programming', 'julia development', 'julia data science'],
    'zig': ['zig', 'ziglang', 'zig programming', 'zig development'],
    'crystal': ['crystal', 'crystal lang', 'crystal programming', 'crystal development'],
    'elixir': ['elixir', 'elixir lang', 'elixir programming', 'phoenix framework', 'elixir development'],
    'erlang': ['erlang', 'erlang programming', 'erlang development', 'otp'],
    'haskell': ['haskell', 'haskell programming', 'haskell development', 'haskell functional'],
    'lua': ['lua', 'lua programming', 'lua scripting', 'lua development', 'luajit'],
    'clojure': ['clojure', 'clojure programming', 'clojure development', 'clojurescript'],
    'groovy': ['groovy', 'groovy programming', 'groovy development', 'spock groovy'],
    'f#': ['f#', 'fsharp', 'f# programming', 'fsharp development', 'functional programming'],
    'vb.net': ['vb.net', 'vb net', 'visual basic .net', 'vb dotnet'],
    'delphi': ['delphi', 'delphi programming', 'delphi development', 'object pascal'],
    'ada': ['ada', 'ada programming', 'ada development', 'ada language'],
    'fortran': ['fortran', 'fortran programming', 'fortran development', 'fortran 90'],
    'cobol': ['cobol', 'cobol programming', 'cobol development', 'cobol mainframe'],
    'pl/sql': ['pl/sql', 'plsql', 'oracle pl/sql', 'sql procedural', 'oracle programming'],
    't-sql': ['t-sql', 'tsql', 'sql server t-sql', 'mssql programming'],

    # =========================
    # Frontend Frameworks & Libraries (Extended)
    # =========================
    'html': ['html', 'html5', 'hypertext markup language', 'html semantic', 'html5 semantic', 'xhtml', 'html markup', 'accessibility html', 'aria html'],
    'css': ['css', 'css3', 'cascading style sheets', 'css flexbox', 'css grid', 'css animations', 'css transitions', 'css variables', 'css custom properties', 'responsive css'],
    'sass': ['sass', 'scss', 'sassy css', 'sass/scss', 'sass css', 'scss styles', 'sass compilation'],
    'less': ['less', 'less css', 'less styles', 'leaner css'],
    'bootstrap': ['bootstrap', 'bootstrap4', 'bootstrap5', 'bs4', 'bs5', 'bootstrap css', 'bootstrap framework', 'bootstrap grid', 'bootstrap components'],
    'tailwind css': ['tailwind', 'tailwind css', 'tailwindcss', 'tw', 'tailwind framework', 'tailwind ui', 'tailwind config', 'tailwind utility classes'],
    'material ui': ['material ui', 'mui', 'material design', 'material design components', 'mui react', 'material ui components', 'material icons'],
    'ant design': ['ant design', 'antd', 'ant.design', 'ant design react', 'ant design components', 'ant design system', 'ant design pro'],
    'chakra ui': ['chakra ui', 'chakra', 'chakra-ui', 'chakra components', 'chakra framework', 'chakra react'],
    'react': ['react', 'reactjs', 'react.js', 'react library', 'react framework', 'react dom', 'react hooks', 'react 18', 'react development', 'react components', 'react state'],
    'next.js': ['next.js', 'nextjs', 'next', 'nextjs framework', 'next 13', 'next 14', 'next app router', 'next pages router', 'next server components', 'next static generation', 'next server side rendering'],
    'vue': ['vue', 'vuejs', 'vue.js', 'vue2', 'vue3', 'vue framework', 'vue composition api', 'vue options api', 'vue components', 'vue directives', 'vuex'],
    'nuxt.js': ['nuxt', 'nuxtjs', 'nuxt.js', 'nuxt3', 'nuxt framework', 'nuxt app', 'nuxt static generation', 'nuxt server side rendering'],
    'angular': ['angular', 'angularjs', 'angular 2+', 'angular12', 'angular13', 'angular14', 'angular15', 'angular16', 'angular17', 'angular18', 'angular framework', 'angular components', 'angular modules', 'angular routing', 'angular forms', 'angular material'],
    'svelte': ['svelte', 'sveltejs', 'svelte.js', 'sveltekit', 'svelte framework', 'svelte components', 'svelte stores', 'svelte reactivity'],
    'redux': ['redux', 'react redux', 'redux toolkit', 'rtk', 'redux saga', 'redux thunk', 'redux state management', 'redux actions', 'redux reducers'],
    'mobx': ['mobx', 'mobx state', 'mobx state management', 'mobx react', 'mobx observables', 'mobx actions'],
    'webpack': ['webpack', 'webpack5', 'webpack config', 'webpack bundle', 'webpack loader', 'webpack plugin', 'webpack optimization', 'webpack dev server'],
    'vite': ['vite', 'vitejs', 'vite build', 'vite dev', 'vite tool', 'vite bundler'],
    'jquery': ['jquery', 'jquery library', 'jquery ui', 'jquery plugins', 'jquery ajax', 'jquery dom manipulation'],
    'styled-components': ['styled components', 'styled-components', 'styled', 'styled react', 'css-in-js', 'styled components react'],
    'emotion': ['emotion', 'emotion css', 'emotion styled', 'emotion library', 'emotion react'],
    'framer motion': ['framer motion', 'framer', 'motion library', 'react animation', 'framer animations'],
    'react router': ['react router', 'react-router', 'react-router-dom', 'routing react', 'router dom', 'react navigation'],
    'react query': ['react query', 'tanstack query', 'react-query', 'query management', 'server state react'],
    'react native': ['react native', 'react-native', 'rn', 'react native mobile', 'expo', 'react native apps', 'react native framework'],
    'nextjs': ['nextjs', 'next.js', 'next js', 'next framework'],
    'gatsby': ['gatsby', 'gatsbyjs', 'gatsby.js', 'gatsby framework', 'gatsby static site'],
    'remix': ['remix', 'remix.run', 'remix framework', 'remix react'],
    'astro': ['astro', 'astro.js', 'astro framework', 'astro build'],
    'solidjs': ['solidjs', 'solid', 'solid.js', 'solid framework', 'solid reactivity'],
    'qwik': ['qwik', 'qwik.js', 'qwik framework', 'qwik optimization'],
    'preact': ['preact', 'preact.js', 'preact framework', 'preact components'],
    'lit': ['lit', 'lit.js', 'lit framework', 'lit-html', 'lit-element'],
    'alpinejs': ['alpinejs', 'alpine.js', 'alpine', 'alpine framework', 'alpine components'],
    'htmx': ['htmx', 'htmx.js', 'htmx framework', 'html extensions'],

    # =========================
    # UI/UX Design (Extended)
    # =========================
    'ui design': ['ui design', 'user interface design', 'ui', 'interface design', 'ui/ux', 'digital design', 'screen design', 'app design', 'web design'],
    'ux design': ['ux design', 'user experience design', 'ux', 'experience design', 'user experience', 'ux research'],
    'ux research': ['ux research', 'user research', 'user testing', 'usability testing', 'ux testing', 'a/b testing', 'user interviews', 'user surveys'],
    'interaction design': ['interaction design', 'ixd', 'interaction design', 'motion design', 'micro-interactions', 'user interaction'],
    'information architecture': ['information architecture', 'ia', 'content structure', 'sitemap', 'navigation design', 'user flow', 'wireframing'],
    'wireframing': ['wireframing', 'wireframes', 'wireframe design', 'low-fidelity design', 'lo-fi mockups'],
    'prototyping': ['prototyping', 'prototype design', 'interactive prototype', 'high-fidelity prototype', 'figma prototyping'],
    'visual design': ['visual design', 'visual communication', 'graphic design', 'visual identity', 'brand visual design'],
    'user personas': ['user personas', 'personas', 'user archetypes', 'customer personas', 'buyer personas'],
    'user journey mapping': ['user journey mapping', 'user journey', 'journey mapping', 'customer journey', 'user flow mapping'],
    'accessibility': ['accessibility', 'a11y', 'web accessibility', 'wcag', 'accessible design', 'inclusive design'],
    'design thinking': ['design thinking', 'human-centered design', 'design process', 'design strategy'],
    'product design': ['product design', 'digital product design', 'product experience', 'product ux'],
    'service design': ['service design', 'service blueprint', 'service experience'],
    'design systems': ['design systems', 'design system', 'component library', 'pattern library', 'design tokens'],
    'figma': ['figma', 'figma design', 'figma prototyping', 'figma collaboration', 'figma components'],
    'sketch': ['sketch', 'sketch app', 'sketch design', 'sketch prototyping'],
    'adobe xd': ['adobe xd', 'adobe experience design', 'xd', 'adobe prototyping', 'xd design'],
    'invision': ['invision', 'invision studio', 'invision prototyping', 'invision collaboration'],
    'zeplin': ['zeplin', 'zeplin design', 'design collaboration', 'design handoff'],
    'abstract': ['abstract', 'abstract design', 'design version control'],
    'framer': ['framer', 'framer design', 'framer prototyping', 'framer web design'],
    'webflow': ['webflow', 'webflow design', 'webflow development', 'webflow cms'],
    'balsamiq': ['balsamiq', 'balsamiq mockups', 'balsamiq wireframes'],
    'ux writing': ['ux writing', 'microcopy', 'content design', 'user copy', 'interface writing'],
    'user testing': ['user testing', 'usertesting', 'remote testing', 'user validation'],
    'conversion optimization': ['conversion optimization', 'cro', 'conversion rate optimization', 'conversion design'],
    'a/b testing': ['ab testing', 'a/b testing', 'split testing', 'a/b experimentation'],

    # =========================
    # Backend Frameworks (Extended)
    # =========================
    'node.js': ['node', 'nodejs', 'node.js', 'node runtime', 'nodejs runtime', 'node environment', 'node server', 'node backend'],
    'express.js': ['express', 'expressjs', 'express.js', 'express server', 'express framework', 'express routing', 'express middleware'],
    'nestjs': ['nestjs', 'nest.js', 'nest', 'nest framework', 'nestjs architecture', 'nestjs graphql', 'nestjs microservices'],
    'django': ['django', 'django framework', 'django rest', 'django rest framework', 'drf', 'django orm', 'django admin', 'django views'],
    'flask': ['flask', 'flask framework', 'python flask', 'flask microframework', 'flask api', 'flask extensions'],
    'fastapi': ['fastapi', 'fast api', 'fastapi framework', 'async fastapi', 'fastapi python', 'fastapi rest'],
    'spring boot': ['spring boot', 'springboot', 'spring-boot', 'spring boot framework', 'spring boot microservices', 'spring boot rest'],
    'spring': ['spring', 'spring framework', 'spring mvc', 'spring ioc', 'spring di', 'spring security', 'spring data', 'spring cloud'],
    'asp.net': ['asp.net', 'asp net', 'aspnet', 'asp.net core', 'asp.net mvc', 'asp.net web api', 'asp.net razor'],
    '.net': ['.net', 'dotnet', '.net core', 'dotnet core', '.net 5', '.net 6', '.net 7', '.net 8', '.net framework', 'dotnet development'],
    'laravel': ['laravel', 'laravel framework', 'laravel php', 'laravel eloquent', 'laravel blade', 'laravel api', 'laravel livewire'],
    'symfony': ['symfony', 'symfony framework', 'symfony php', 'symfony components', 'symfony bundles', 'symfony doctrine'],
    'ruby on rails': ['ruby on rails', 'rails', 'ror', 'rails framework', 'rails mvc', 'rails api', 'rails active record'],
    'gin': ['gin', 'gin-gonic', 'gin framework', 'gin golang', 'gin web framework', 'gin rest'],
    'echo': ['echo', 'echo framework', 'echo golang', 'echo web framework', 'echo rest'],
    'actix': ['actix', 'actix-web', 'actix web framework', 'rust actix', 'actix framework'],
    'rocket': ['rocket', 'rocket framework', 'rust rocket', 'rocket web framework'],
    'tornado': ['tornado', 'tornado python', 'tornado web', 'tornado framework'],
    'falcon': ['falcon', 'falcon framework', 'python falcon', 'falcon api'],
    'hapi': ['hapi', 'hapi.js', 'hapi framework', 'hapi node'],
    'koa': ['koa', 'koa.js', 'koa framework', 'koa node', 'koa middleware'],
    'meteor': ['meteor', 'meteor.js', 'meteor framework', 'meteor fullstack'],
    'adonis': ['adonis', 'adonisjs', 'adonis framework', 'adonis node'],
    'sails': ['sails', 'sails.js', 'sails framework', 'sails node'],
    'loopback': ['loopback', 'loopback.js', 'loopback framework', 'loopback node'],
    'strapi': ['strapi', 'strapi cms', 'strapi headless', 'strapi api'],
    'directus': ['directus', 'directus cms', 'directus headless', 'directus api'],
    'graphql': ['graphql', 'graphql api', 'gql', 'graphql schema', 'graphql resolvers', 'apollo graphql'],
    'grpc': ['grpc', 'g rpc', 'grpc protocol', 'grpc api', 'grpc service', 'protobuf'],
    'rest api': ['rest api', 'restful api', 'restful services', 'rest endpoints', 'restful web services', 'api rest'],

    # =========================
    # Mobile Development (Extended)
    # =========================
    'android': ['android', 'android development', 'android sdk', 'android studio', 'android app', 'android kotlin', 'android java', 'android native', 'android framework'],
    'ios': ['ios', 'ios development', 'ios sdk', 'xcode', 'swift ios', 'objective-c ios', 'ios app', 'ios native', 'ios framework'],
    'react native': ['react native', 'react-native', 'rn', 'react native mobile', 'expo', 'react native apps', 'react native framework', 'react native cli'],
    'flutter': ['flutter', 'flutter framework', 'flutter sdk', 'flutter app', 'dart flutter', 'flutter mobile', 'flutter cross-platform', 'flutter widgets'],
    'xamarin': ['xamarin', 'xamarin forms', 'xamarin.android', 'xamarin.ios', 'xamarin development', 'xamarin mobile'],
    'ionic': ['ionic', 'ionic framework', 'ionic mobile', 'ionic angular', 'ionic react', 'ionic vue', 'ionic capacitor'],
    'kotlin android': ['kotlin android', 'android kotlin', 'kotlin android development', 'android kotlin coroutines'],
    'swift ios': ['swift ios', 'ios swift', 'swift development ios'],
    'cordova': ['cordova', 'apache cordova', 'phonegap', 'cordova mobile', 'cordova hybrid'],
    'capacitor': ['capacitor', 'capacitor.js', 'capacitor mobile', 'ionic capacitor'],
    'nativescript': ['nativescript', 'nativescript mobile', 'nativescript angular', 'nativescript vue'],
    'react native expo': ['expo', 'expo react native', 'expo framework', 'expo app'],
    'android jetpack': ['jetpack', 'android jetpack', 'jetpack compose', 'android compose', 'compose ui'],
    'swiftui': ['swiftui', 'swift ui', 'swiftui ios', 'apple swiftui'],
    'uikit': ['uikit', 'uikit ios', 'apple uikit', 'ios uikit'],
    'android xml': ['android xml', 'xml layouts', 'android layout'],
    'android material': ['material android', 'android material design', 'material design android'],
    'flutter widgets': ['flutter widgets', 'widgets flutter', 'flutter ui'],
    'react native navigation': ['react navigation', 'navigation react native', 'react native router'],
    'android permissions': ['android permissions', 'permissions android', 'android runtime permissions'],
    'ios permissions': ['ios permissions', 'permissions ios', 'ios privacy'],

    # =========================
    # AI / Machine Learning (Extended - Agentic AI, LLMs, Computer Vision)
    # =========================
    
    # Agentic AI
    'agentic ai': ['agentic ai', 'ai agents', 'autonomous agents', 'intelligent agents', 'agent-based ai', 'multi-agent systems', 'agentic systems'],
    'ai agents': ['ai agents', 'llm agents', 'autonomous agents', 'agent frameworks', 'agentic workflow'],
    'langchain': ['langchain', 'lang chain', 'lc', 'langchain framework', 'llm orchestration', 'chain of thought', 'langchain agents', 'langchain tools'],
    'langgraph': ['langgraph', 'langraph', 'graph-based agents', 'langchain graphs'],
    'autogen': ['autogen', 'microsoft autogen', 'agentic framework', 'multi-agent systems', 'ai agent framework'],
    'crewai': ['crewai', 'crew ai', 'crew framework', 'agentic crew', 'ai teams'],
    'llamaindex': ['llamaindex', 'llama index', 'llamaindex framework', 'rag index', 'data framework'],
    'semantic kernel': ['semantic kernel', 'microsoft semantic', 'agentic kernel', 'ai orchestration'],
    'vector database': ['vector db', 'vector database', 'vector search', 'embeddings database', 'pinecone', 'weaviate', 'qdrant', 'milvus', 'chromadb', 'faiss'],
    'embedding': ['embeddings', 'embedding models', 'vector embeddings', 'text embeddings', 'image embeddings', 'openai embeddings'],
    
    # LLMs & Foundation Models
    'large language model': ['llm', 'large language model', 'foundation model', 'fm', 'llm models', 'language model', 'transformer model'],
    'gpt': ['gpt', 'openai gpt', 'chatgpt', 'gpt-3', 'gpt-4', 'gpt-4o', 'gpt-turbo', 'gpt-instruct', 'gpt-4 turbo', 'gpt-4 vision'],
    'llama': ['llama', 'meta llama', 'llama 2', 'llama3', 'meta llama2', 'llama model', 'llama.cpp', 'ollama llama'],
    'claude': ['claude', 'anthropic claude', 'claude 3', 'claude opus', 'claude sonnet', 'claude haiku'],
    'gemini': ['gemini', 'google gemini', 'gemini pro', 'gemini ultra', 'gemini advanced', 'bard gemini'],
    'mistral': ['mistral', 'mistral ai', 'mistral 7b', 'mistral large', 'mistral model'],
    'falcon': ['falcon', 'falcon llm', 'falcon model', 'tii falcon'],
    'bert': ['bert', 'bert model', 'google bert', 'bert embeddings', 'bert pretrained', 'bert-large', 'bert-base'],
    't5': ['t5', 't5 model', 'google t5', 'text-to-text', 't5-large'],
    'roberta': ['roberta', 'roberta model', 'facebook roberta', 'roberta-base'],
    'xlm-roberta': ['xlm-roberta', 'xlm roberta', 'multilingual bert', 'cross-lingual'],
    'electra': ['electra', 'electra model', 'google electra'],
    'deberta': ['deberta', 'deberta model', 'microsoft deberta'],
    'phi': ['phi', 'microsoft phi', 'phi-2', 'phi-3', 'small llm'],
    'mixtral': ['mixtral', 'mixtral 8x7b', 'mixtral model', 'moe model'],
    'command': ['command', 'cohere command', 'command model', 'cohere llm'],
    'dbrx': ['dbrx', 'databricks dbrx', 'dbrx model', 'databricks llm'],
    'grok': ['grok', 'xai grok', 'grok model', 'elon ai'],
    'palm': ['palm', 'google palm', 'palm 2', 'pathways model'],
    'bloom': ['bloom', 'bloom model', 'bigscience bloom', 'open source llm'],
    'opt': ['opt', 'meta opt', 'opt model', 'open pre-trained'],
    
    # RAG & Knowledge Retrieval
    'rag': ['rag', 'retrieval augmented generation', 'rag system', 'knowledge retrieval', 'document qna', 'rag architecture'],
    'retrieval': ['retrieval', 'information retrieval', 'document retrieval', 'knowledge retrieval', 'retrieval system'],
    'knowledge graph': ['knowledge graph', 'knowledge base', 'graph database', 'entity resolution', 'knowledge representation'],
    'semantic search': ['semantic search', 'vector search', 'neural search', 'similarity search', 'embedding search'],
    'hybrid search': ['hybrid search', 'full-text search', 'vector + keyword', 'combine search'],
    'reranking': ['reranking', 'rerank', 'cross-encoder', 'retrieval rerank'],
    'chunking': ['chunking', 'text chunking', 'document splitting', 'semantic chunking', 'recursive chunking'],
    
    # Prompt Engineering
    'prompt engineering': ['prompt engineering', 'prompting', 'prompt design', 'prompt tuning', 'few-shot prompting', 'chain-of-thought', 'cot', 'zero-shot', 'few-shot', 'prompt engineering techniques'],
    'chain of thought': ['chain of thought', 'cot', 'thought chain', 'reasoning chain', 'cognitive chain'],
    'tree of thoughts': ['tree of thoughts', 'tot', 'thought tree', 'reasoning tree'],
    'react': ['react prompting', 'reasoning + acting', 'react agent', 'react framework', 'reasoning acting'],
    'self-consistency': ['self-consistency', 'self consistency', 'multiple reasoning', 'ensemble reasoning'],
    'constitutional ai': ['constitutional ai', 'constitutional prompting', 'ai safety', 'aligned ai'],
    'instruction tuning': ['instruction tuning', 'instruction following', 'instruction dataset', 'finetuning instructions'],
    
    # Computer Vision
    'computer vision': ['computer vision', 'cv', 'image recognition', 'object detection', 'image segmentation', 'face detection', 'vision ai'],
    'object detection': ['object detection', 'object recognition', 'detection model', 'yolo', 'detectron', 'object localization'],
    'image classification': ['image classification', 'image recognition', 'classification model', 'cnn classification', 'vision classification'],
    'image segmentation': ['image segmentation', 'semantic segmentation', 'instance segmentation', 'panoptic segmentation', 'segmentation model'],
    'object tracking': ['object tracking', 'visual tracking', 'target tracking', 'video tracking', 'tracking algorithm'],
    'face recognition': ['face recognition', 'facial recognition', 'face detection', 'face verification', 'face identification'],
    'pose estimation': ['pose estimation', 'human pose', 'keypoint detection', 'skeleton tracking', 'pose detection'],
    'optical flow': ['optical flow', 'motion estimation', 'video flow', 'scene flow'],
    'depth estimation': ['depth estimation', 'depth prediction', 'monocular depth', 'depth map'],
    '3d reconstruction': ['3d reconstruction', '3d modeling', 'neural radiance fields', 'nerf', 'structure from motion', 'sfm'],
    'cnn': ['cnn', 'convolutional neural network', 'convnet', 'convolutional network', 'vision cnn'],
    'resnet': ['resnet', 'residual network', 'resnet50', 'resnet101', 'resnet152'],
    'efficientnet': ['efficientnet', 'efficientnet-b0', 'efficientnet-b7', 'efficient net'],
    'vgg': ['vgg', 'vgg16', 'vgg19', 'visual geometry group'],
    'inception': ['inception', 'inceptionv3', 'inceptionv4', 'googlenet'],
    'mobilenet': ['mobilenet', 'mobile net', 'mobilenetv2', 'mobilenetv3', 'lightweight cnn'],
    'yolo': ['yolo', 'you only look once', 'yolov3', 'yolov4', 'yolov5', 'yolov8', 'yolov9', 'yolo model'],
    'detectron': ['detectron', 'detectron2', 'facebook detectron', 'object detection'],
    'mask r-cnn': ['mask r-cnn', 'maskrcnn', 'instance segmentation', 'rcnn'],
    'faster r-cnn': ['faster r-cnn', 'fasterrcnn', 'region cnn'],
    'retinanet': ['retinanet', 'retina net', 'focal loss'],
    'ssd': ['ssd', 'single shot detector', 'object detection ssd'],
    'vision transformer': ['vit', 'vision transformer', 'transformer vision', 'image transformer'],
    'dino': ['dino', 'dino model', 'self-supervised vision', 'facebook dino'],
    'clip': ['clip', 'clip model', 'openai clip', 'vision-language', 'multimodal clip'],
    'sam': ['sam', 'segment anything', 'meta sam', 'segmentation model', 'sam model'],
    'stable diffusion': ['stable diffusion', 'sd', 'stability ai', 'diffusion model', 'image generation'],
    'dalle': ['dalle', 'dall-e', 'openai dalle', 'dalle-2', 'dalle-3', 'image generation'],
    'midjourney': ['midjourney', 'midjourney ai', 'image generation', 'ai art'],
    'imagen': ['imagen', 'google imagen', 'imagen ai', 'text to image'],
    'controlnet': ['controlnet', 'control net', 'diffusion control', 'guided generation'],
    'gan': ['gan', 'generative adversarial network', 'generative network', 'gan model'],
    'dcgan': ['dcgan', 'deep convolutional gan', 'gan image'],
    'stylegan': ['stylegan', 'style gan', 'nvidea stylegan', 'image generation'],
    'cyclegan': ['cyclegan', 'cycle gan', 'image translation'],
    'pix2pix': ['pix2pix', 'pix2pix gan', 'image-to-image translation'],
    
    # NLP & Text Processing
    'nlp': ['nlp', 'natural language processing', 'text processing', 'language processing', 'computational linguistics'],
    'text classification': ['text classification', 'document classification', 'sentiment analysis', 'topic labeling'],
    'ner': ['ner', 'named entity recognition', 'entity extraction', 'entity recognition', 'name entity'],
    'tokenization': ['tokenization', 'tokenizer', 'word tokens', 'subword tokenization', 'byte-pair encoding', 'bpe'],
    'sentiment analysis': ['sentiment analysis', 'sentiment detection', 'emotion analysis', 'opinion mining'],
    'text summarization': ['text summarization', 'summarization', 'abstractive summarization', 'extractive summarization'],
    'machine translation': ['machine translation', 'mt', 'neural machine translation', 'nmt', 'language translation'],
    'question answering': ['question answering', 'qa', 'qa system', 'document qa', 'knowledge qa'],
    'text generation': ['text generation', 'generation', 'language generation', 'story generation'],
    'topic modeling': ['topic modeling', 'topic model', 'lda', 'latent dirichlet allocation'],
    'word embeddings': ['word embeddings', 'embedding', 'word2vec', 'glove', 'fasttext'],
    'transformer': ['transformer', 'transformer model', 'attention mechanism', 'self-attention', 'multi-head attention'],
    'attention': ['attention', 'attention mechanism', 'self-attention', 'cross-attention', 'multi-head attention'],
    'encoder-decoder': ['encoder-decoder', 'seq2seq', 'sequence-to-sequence', 'transformer encoder decoder'],
    'fine-tuning': ['fine-tuning', 'finetuning', 'model tuning', 'parameter efficient tuning', 'pet'],
    'prompt tuning': ['prompt tuning', 'prompt engineering', 'soft prompts', 'prefix tuning'],
    'qlora': ['qlora', 'quantized lora', 'efficient fine-tuning', 'parameter efficient'],
    'lora': ['lora', 'low-rank adaptation', 'parameter efficient', 'lora fine-tuning'],
    'peft': ['peft', 'parameter efficient fine-tuning', 'efficient tuning', 'peft library'],
    
    # ML Operations & Tools
    'mlflow': ['mlflow', 'ml flow', 'ml tracking', 'model registry'],
    'weights & biases': ['weights & biases', 'wandb', 'experiment tracking', 'wandb.ai'],
    'tensorboard': ['tensorboard', 'tb', 'visualization tensorflow'],
    'model registry': ['model registry', 'model versioning', 'model store'],
    'feature store': ['feature store', 'feature engineering', 'feature pipeline'],
    'model monitoring': ['model monitoring', 'model drift', 'concept drift', 'data drift', 'monitoring ml'],
    'model deployment': ['model deployment', 'model serving', 'deploy model', 'ml deployment'],
    'model serving': ['model serving', 'serving model', 'tensorflow serving', 'torchserve', 'onnx runtime'],
    'onnx': ['onnx', 'open neural network exchange', 'onnx runtime', 'model conversion'],
    
    # ML Libraries
    'tensorflow': ['tensorflow', 'tf', 'tensorflow2', 'tf2', 'tensorflow lite', 'tf-serving', 'tensorflow keras'],
    'pytorch': ['pytorch', 'torch', 'pytorch framework', 'torchvision', 'torchaudio', 'pytorch lightning'],
    'keras': ['keras', 'keras framework', 'tensorflow keras', 'keras api', 'keras tuner'],
    'scikit-learn': ['scikit learn', 'scikit-learn', 'sklearn', 'scikit', 'sklearn python'],
    'opencv': ['opencv', 'open cv', 'computer vision', 'opencv python', 'image processing'],
    'hugging face': ['hugging face', 'huggingface', 'hf', 'transformers', 'huggingface transformers', 'huggingface pipeline'],
    'jax': ['jax', 'jaxlib', 'google jax', 'accelerated computing'],
    'numpy': ['numpy', 'np', 'numeric python', 'array operations'],
    'pandas': ['pandas', 'pd', 'dataframe', 'data manipulation'],
    'matplotlib': ['matplotlib', 'matplotlib python', 'mpl', 'data visualization'],
    'seaborn': ['seaborn', 'sns', 'statistical visualization', 'seaborn plots'],
    'plotly': ['plotly', 'plotly python', 'interactive plots', 'dash plotly'],
    'scipy': ['scipy', 'scientific python', 'scientific computing'],
    'statsmodels': ['statsmodels', 'statistical models', 'regression analysis'],
    'gradio': ['gradio', 'gradio interface', 'ml demo', 'model app'],
    'streamlit': ['streamlit', 'streamlit app', 'ml dashboard', 'data app'],
    'fastai': ['fastai', 'fast ai', 'fastai library', 'pytorch fastai'],
    'lightgbm': ['lightgbm', 'light gbm', 'gradient boosting', 'gbm'],
    'xgboost': ['xgboost', 'xgb', 'extreme gradient boosting', 'xgb model'],
    'catboost': ['catboost', 'cat boost', 'gradient boosting catboost'],
    
    # AI Safety & Ethics
    'ai ethics': ['ai ethics', 'ethical ai', 'responsible ai', 'fairness', 'bias detection'],
    'ai safety': ['ai safety', 'safe ai', 'alignment', 'ai alignment', 'secure ai'],
    'bias detection': ['bias detection', 'algorithmic bias', 'model bias', 'fairness metrics'],
    'interpretability': ['interpretability', 'model interpretation', 'shap', 'lime', 'explainable ai', 'xai'],
    'explainable ai': ['explainable ai', 'xai', 'explainable models', 'interpretable ml'],
    'model fairness': ['model fairness', 'fairness', 'fair ml', 'equalized odds'],
    'privacy preserving ml': ['privacy preserving', 'differential privacy', 'private ml', 'fed learning'],

    # =========================
    # Databases & Storage (Extended)
    # =========================
    'sql': ['sql', 'structured query language', 'sql queries', 'sql programming', 'sql database', 'pl/sql', 'tsql', 'sqlite sql'],
    'mysql': ['mysql', 'mysql database', 'mysql server', 'mysql workbench', 'mysql queries', 'mysql admin', 'mysql replication'],
    'postgresql': ['postgresql', 'postgres', 'pgsql', 'postgres db', 'psql', 'postgres server', 'postgres advanced'],
    'sqlite': ['sqlite', 'sqlite3', 'sqlite db', 'sqlite database', 'sqlite embedded'],
    'oracle': ['oracle', 'oracle db', 'oracle database', 'oracle sql', 'pl/sql oracle', 'oracle server'],
    'sql server': ['sql server', 'mssql', 'microsoft sql server', 'ms sql', 'sql server management', 'ssms'],
    'mongodb': ['mongodb', 'mongo', 'mongo db', 'nosql mongo', 'mongodb atlas', 'mongodb compass', 'mongoose'],
    'redis': ['redis', 'redis cache', 'redis db', 'redis server', 'redis caching', 'redis cluster'],
    'cassandra': ['cassandra', 'apache cassandra', 'cassandra db', 'nosql cassandra', 'cassandra cluster'],
    'dynamodb': ['dynamodb', 'aws dynamodb', 'dynamo db', 'amazon dynamodb', 'nosql dynamodb'],
    'firebase': ['firebase', 'firebase db', 'firebase realtime', 'firebase firestore', 'firebase auth', 'firebase hosting'],
    'elasticsearch': ['elasticsearch', 'elastic search', 'es', 'elastic', 'elk elasticsearch', 'elasticsearch cluster'],
    'neo4j': ['neo4j', 'neo4j graph', 'graph database', 'neo4j cypher', 'nosql neo4j'],
    'influxdb': ['influxdb', 'influx db', 'time series db', 'influxdb telegraf'],
    'couchdb': ['couchdb', 'couch db', 'apache couchdb', 'nosql couchdb'],
    'supabase': ['supabase', 'supabase db', 'supabase postgres', 'firebase alternative', 'supabase auth'],
    'arangodb': ['arangodb', 'arangodb graph', 'arangodb nosql', 'multi-model database'],
    'clickhouse': ['clickhouse', 'clickhouse db', 'clickhouse analytics', 'columnar database'],
    'cockroachdb': ['cockroachdb', 'cockroach db', 'distributed sql', 'crdb'],
    'planetscale': ['planetscale', 'vitess', 'mysql compatible', 'scalable database'],
    'hasura': ['hasura', 'hasura graphql', 'hasura engine', 'instant graphql'],
    'singleStore': ['singleStore', 'singlestore', 'memsql', 'distributed database'],
    'data lake': ['data lake', 'data lakehouse', 'lakehouse', 'delta lake'],
    'delta lake': ['delta lake', 'delta table', 'lakehouse format', 'databricks delta'],
    'iceberg': ['iceberg', 'apache iceberg', 'table format', 'data lake table'],
    'hudi': ['hudi', 'apache hudi', 'incremental processing', 'data lake'],
    
    # =========================
    # Cloud Platforms (Extended)
    # =========================
    'aws': ['aws', 'amazon web services', 'aws cloud', 'ec2', 's3', 'lambda', 'rds', 'vpc', 'iam', 'aws ec2', 'aws lambda', 'aws s3', 'aws rds', 'aws vpc', 'aws iam', 'aws dynamodb', 'aws sagemaker'],
    'azure': ['azure', 'microsoft azure', 'azure cloud', 'azure devops', 'aks', 'azure functions', 'azure storage', 'azure sql', 'azure ad', 'azure ai'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform', 'gce', 'gke', 'gcs', 'cloud run', 'google cloud functions', 'bigquery'],
    'digitalocean': ['digitalocean', 'do', 'digital ocean', 'digital ocean droplets', 'do cloud'],
    'heroku': ['heroku', 'heroku cloud', 'heroku platform', 'heroku deployment'],
    'vercel': ['vercel', 'vercel app', 'vercel deployment', 'vercel hosting', 'vercel platform'],
    'netlify': ['netlify', 'netlify deployment', 'netlify hosting', 'netlify platform'],
    'cloudflare': ['cloudflare', 'cloudflare workers', 'cf', 'cloudflare pages', 'cloudflare cdn'],
    'alibaba cloud': ['alibaba cloud', 'alicloud', 'aliyun', 'alibaba ecs', 'alibaba container'],
    'oracle cloud': ['oracle cloud', 'oci', 'oracle cloud infrastructure', 'oracle cloud applications'],
    'aws devops': ['aws devops', 'aws codebuild', 'aws codedeploy', 'aws codepipeline', 'aws codecommit'],
    'azure devops': ['azure devops', 'azure pipelines', 'azure repos', 'azure boards', 'azure artifacts'],
    'google cloud run': ['cloud run', 'google cloud run', 'fully managed serverless'],
    'google kubernetes': ['gke', 'google kubernetes engine', 'kubernetes gcp'],
    'aws ecs': ['ecs', 'amazon ecs', 'ecs fargate', 'container service'],
    'aws eks': ['eks', 'amazon eks', 'kubernetes aws', 'elastic kubernetes'],
    'azure aks': ['aks', 'azure kubernetes', 'aks cluster', 'managed kubernetes'],
    'linode': ['linode', 'akamai linode', 'cloud hosting'],
    'openstack': ['openstack', 'openstack cloud', 'openstack infrastructure'],
    
    # =========================
    # DevOps & CI/CD (Extended)
    # =========================
    'docker': ['docker', 'docker containers', 'docker engine', 'docker-compose', 'dockerfile', 'docker swarm', 'docker registry', 'dockerhub'],
    'kubernetes': ['kubernetes', 'k8s', 'kube', 'kubectl', 'aks', 'eks', 'gke', 'kubernetes cluster', 'k8s cluster', 'kubernetes pods', 'kubernetes services'],
    'jenkins': ['jenkins', 'jenkins ci', 'jenkins pipeline', 'jenkinsfile', 'jenkins declarative', 'jenkins scripted'],
    'github actions': ['github actions', 'github ci', 'github workflows', 'github actions yaml', 'github automation'],
    'gitlab ci': ['gitlab ci', 'gitlab ci/cd', 'gitlab pipelines', 'gitlab runners', 'gitlab yaml'],
    'circleci': ['circleci', 'circle ci', 'circleci config', 'circleci pipeline'],
    'travis ci': ['travis', 'travis ci', 'travis-ci', 'travis pipeline'],
    'terraform': ['terraform', 'terraform iac', 'tf', 'terraform cloud', 'terraform modules', 'terraform aws', 'hcl'],
    'ansible': ['ansible', 'ansible playbook', 'ansible automation', 'ansible tower', 'ansible awx'],
    'chef': ['chef', 'chef automation', 'chef cookbooks', 'chef recipes'],
    'puppet': ['puppet', 'puppet automation', 'puppet manifests', 'puppet modules'],
    'argo': ['argo', 'argo cd', 'argo workflows', 'argo rollouts', 'argo events'],
    'tekton': ['tekton', 'tekton pipelines', 'tekton triggers', 'kubernetes ci/cd'],
    'spinnaker': ['spinnaker', 'spinnaker pipeline', 'spinnaker deployment'],
    'flux': ['flux', 'fluxcd', 'gitops', 'flux controller'],
    'crossplane': ['crossplane', 'crossplane.io', 'kubernetes control plane'],
    'packer': ['packer', 'packer image', 'packer build', 'image builder'],
    'vagrant': ['vagrant', 'vagrant vm', 'vagrant box', 'vagrant development'],
    'istio': ['istio', 'istio service mesh', 'service mesh', 'istio networking'],
    'linkerd': ['linkerd', 'linkerd service mesh', 'linkerd mesh'],
    'consul': ['consul', 'hashicorp consul', 'service mesh consul', 'service discovery'],
    'vault': ['vault', 'hashicorp vault', 'secrets management', 'vault secrets'],
    'nomad': ['nomad', 'hashicorp nomad', 'orchestration', 'scheduler'],
    'helm': ['helm', 'helm charts', 'kubernetes package', 'helm template'],
    'kustomize': ['kustomize', 'kustomize k8s', 'kubernetes config'],
    'prometheus': ['prometheus', 'prometheus monitoring', 'prometheus metrics', 'prometheus query'],
    'grafana': ['grafana', 'grafana dashboard', 'grafana visualization', 'grafana cloud'],
    'elk stack': ['elk', 'elk stack', 'elasticsearch logstash kibana', 'elastic stack', 'elasticsearch'],
    'splunk': ['splunk', 'splunk monitoring', 'splunk search', 'splunk dashboard'],
    'datadog': ['datadog', 'ddog', 'datadog monitoring', 'datadog agent'],
    'new relic': ['new relic', 'newrelic', 'nr', 'new relic monitoring'],
    
    # =========================
    # Testing & Quality Assurance (Extended)
    # =========================
    'junit': ['junit', 'junit4', 'junit5', 'jupiter', 'junit testing'],
    'pytest': ['pytest', 'py test', 'pytest fixtures', 'pytest parametrize', 'python testing'],
    'selenium': ['selenium', 'selenium webdriver', 'selenium grid', 'selenium automation', 'webdriver'],
    'cypress': ['cypress', 'cypress testing', 'cypress io', 'cypress e2e', 'cypress integration'],
    'playwright': ['playwright', 'playwright testing', 'playwright automation', 'playwright framework'],
    'jest': ['jest', 'jest testing', 'react testing', 'jest framework', 'jest unit test'],
    'mocha': ['mocha', 'mocha testing', 'mocha framework', 'mocha describe'],
    'chai': ['chai', 'chai assertion', 'chai expect', 'chai should'],
    'testing library': ['testing library', 'react testing library', 'rtl', 'dom testing library'],
    'unit testing': ['unit testing', 'unit test', 'test driven development', 'tdd', 'unit test framework'],
    'integration testing': ['integration testing', 'integration test', 'integration test suite'],
    'e2e testing': ['e2e testing', 'end to end testing', 'e2e test automation'],
    'performance testing': ['performance testing', 'load testing', 'stress testing', 'jmeter', 'gatling'],
    'security testing': ['security testing', 'vulnerability testing', 'penetration testing', 'pentesting'],
    'quality assurance': ['quality assurance', 'qa', 'qa testing', 'quality control', 'qa engineer'],
    'manual testing': ['manual testing', 'manual qa', 'functional testing', 'smoke testing', 'sanity testing'],
    'automation testing': ['automation testing', 'test automation', 'automation framework', 'automation suite'],
    'api testing': ['api testing', 'api test', 'rest api testing', 'postman testing', 'soapui'],
    'mobile testing': ['mobile testing', 'mobile app testing', 'android testing', 'ios testing', 'app testing'],
    'appium': ['appium', 'appium testing', 'appium mobile', 'appium automation'],
    'testng': ['testng', 'testng framework', 'testng annotations'],
    'cucumber': ['cucumber', 'cucumber bdd', 'gherkin', 'bdd testing', 'behavior driven development'],
    'katalon': ['katalon', 'katalon studio', 'katalon automation'],
    'mockito': ['mockito', 'mockito testing', 'java mocking', 'mock framework'],
    'sinon': ['sinon', 'sinon js', 'stub', 'spy', 'mock'],
    'testcontainers': ['testcontainers', 'container testing', 'integration test containers'],
    'vitest': ['vitest', 'vite test', 'unit test vite', 'testing framework'],
    
    # =========================
    # Security (Extended)
    # =========================
    'oauth': ['oauth', 'oauth2', 'oauth 2.0', 'oauth protocol', 'oauth flow', 'authorization server'],
    'jwt': ['jwt', 'json web token', 'jwt token', 'jwt authentication', 'jwt bearer'],
    'ssl': ['ssl', 'secure socket layer', 'ssl certificate', 'ssl tls', 'openssl'],
    'tls': ['tls', 'transport layer security', 'tls 1.2', 'tls 1.3', 'secure transport'],
    'owasp': ['owasp', 'owasp top 10', 'owasp security', 'owasp guidelines', 'owasp project'],
    'penetration testing': ['penetration testing', 'pen testing', 'pentest', 'ethical hacking', 'vulnerability assessment'],
    'vulnerability assessment': ['vulnerability assessment', 'va', 'vulnerability scanning', 'vulnerability management'],
    'security auditing': ['security auditing', 'security audit', 'audit', 'security audit log'],
    'identity management': ['identity management', 'idm', 'access management', 'iam', 'identity access management'],
    'security compliance': ['security compliance', 'compliance', 'gdpr', 'hipaa', 'pci dss', 'soc2', 'iso 27001'],
    'encryption': ['encryption', 'data encryption', 'cryptography', 'aes', 'rsa', 'public key encryption'],
    'firewall': ['firewall', 'firewall management', 'network firewall', 'web application firewall', 'waf'],
    'zero trust': ['zero trust', 'zero trust architecture', 'zero trust security', 'zero trust model'],
    'devsecops': ['devsecops', 'security devops', 'security pipeline', 'security automation'],
    'sast': ['sast', 'static application security testing', 'code scanning', 'static analysis'],
    'dast': ['dast', 'dynamic application security testing', 'dynamic analysis'],
    'secrets management': ['secrets management', 'vault', 'hashicorp vault', 'secret rotation'],
    'sso': ['sso', 'single sign-on', 'saml', 'sso integration'],
    'saml': ['saml', 'security assertion markup language', 'saml 2.0'],
    'cors': ['cors', 'cross-origin resource sharing', 'cors policy'],
    'csrf': ['csrf', 'cross-site request forgery', 'xsrf'],
    'xss': ['xss', 'cross-site scripting', 'xss attacks'],
    'sql injection': ['sql injection', 'sqli', 'injection attack', 'sql injection prevention'],
    'rate limiting': ['rate limiting', 'throttling', 'api rate limit', 'request limiting'],
    'api security': ['api security', 'rest security', 'graphql security', 'api gateway security'],
    'container security': ['container security', 'docker security', 'kubernetes security', 'cve scanning'],
    'cloud security': ['cloud security', 'aws security', 'azure security', 'gcp security', 'cloud hardening'],
    'network security': ['network security', 'network hardening', 'network protection', 'segmentation'],
    
    # =========================
    # Architecture & Design Patterns (Extended)
    # =========================
    'microservices': ['microservices', 'microservice architecture', 'microservices architecture', 'microservices design'],
    'monolith': ['monolith', 'monolithic', 'monolithic architecture', 'monolith application'],
    'serverless': ['serverless', 'serverless architecture', 'aws lambda', 'function as a service', 'faas'],
    'event driven architecture': ['event driven architecture', 'eda', 'event driven design', 'event driven system'],
    'mvc': ['mvc', 'model view controller', 'mvc pattern', 'mvc architecture'],
    'mvvm': ['mvvm', 'model view viewmodel', 'mvvm pattern'],
    'clean architecture': ['clean architecture', 'clean code', 'clean design', 'clean architecture design'],
    'domain driven design': ['domain driven design', 'ddd', 'domain driven', 'domain modeling'],
    'solid': ['solid', 'solid principles', 'solid design', 'solid architecture'],
    'design patterns': ['design patterns', 'gang of four', 'gof patterns', 'design pattern'],
    'restful design': ['restful design', 'rest api design', 'restful architecture', 'rest design'],
    'event sourcing': ['event sourcing', 'event sourcing architecture', 'event store'],
    'cqrs': ['cqrs', 'command query responsibility segregation', 'cqrs pattern'],
    'hexagonal architecture': ['hexagonal architecture', 'ports and adapters', 'hexagonal design'],
    'onion architecture': ['onion architecture', 'onion design', 'layered architecture'],
    'service mesh': ['service mesh', 'istio', 'linkerd', 'consul', 'service mesh architecture'],
    'circuit breaker': ['circuit breaker', 'circuit breaker pattern', 'resilience pattern'],
    'api gateway': ['api gateway', 'gateway', 'kong', 'apigee', 'traefik'],
    'message queue': ['message queue', 'mq', 'message broker', 'rabbitmq', 'activemq'],
    'pubsub': ['pubsub', 'publish subscribe', 'pub/sub', 'message bus'],
    'distributed systems': ['distributed systems', 'distributed architecture', 'distributed computing'],
    'fault tolerance': ['fault tolerance', 'resilience', 'fault tolerant', 'high availability'],
    'load balancing': ['load balancing', 'load balancer', 'lb', 'nginx load balancer', 'aws elb'],
    'caching': ['caching', 'cache', 'redis cache', 'memcached', 'caching strategy'],
    'cdk': ['cdk', 'aws cdk', 'cloud development kit', 'infrastructure as code'],
    'amazon cdk': ['cdk', 'aws cdk', 'cloud development kit', 'infrastructure as code'],
    'sam': ['sam', 'aws sam', 'serverless application model', 'serverless framework'],
    
    # =========================
    # HR & Talent Management (Extended)
    # =========================
    'human resources': ['human resources', 'hr', 'human resource management', 'hrm', 'hr management', 'hr generalist'],
    'hr operations': ['hr operations', 'hr ops', 'hr administration', 'hr shared services'],
    'hr strategy': ['hr strategy', 'strategic hr', 'hr planning', 'hr business partner', 'hrbp'],
    'talent acquisition': ['talent acquisition', 'ta', 'recruitment', 'recruiting', 'talent sourcing', 'sourcing', 'talent partner'],
    'full cycle recruiting': ['full cycle recruiting', 'end to end recruitment', '360 recruiting', 'full recruitment lifecycle', 'full cycle recruitment'],
    'candidate sourcing': ['candidate sourcing', 'talent sourcing', 'source candidates', 'sourcing strategy', 'sourcing channels'],
    'candidate screening': ['candidate screening', 'resume screening', 'application screening', 'phone screening', 'initial screening'],
    'candidate assessment': ['candidate assessment', 'candidate evaluation', 'assessment tools', 'psychometric assessment', 'skill assessment'],
    'interviewing': ['interviewing', 'interview techniques', 'behavioral interviewing', 'structured interviews', 'panel interview'],
    'offer management': ['offer management', 'offer negotiation', 'offer letter', 'compensation negotiation', 'offer approval'],
    'onboarding': ['onboarding', 'new hire onboarding', 'employee onboarding', 'orientation', 'induction'],
    'recruitment marketing': ['recruitment marketing', 'employer branding', 'talent branding', 'recruitment campaigns'],
    'applicant tracking system': ['applicant tracking system', 'ats', 'applicant tracking', 'recruitment system'],
    'workday': ['workday', 'workday hcm', 'workday recruitment', 'workday platform', 'workday integration'],
    'greenhouse': ['greenhouse', 'greenhouse ats', 'greenhouse recruiting', 'greenhouse platform'],
    'lever': ['lever', 'lever ats', 'lever recruitment', 'lever platform'],
    'recruiter': ['recruiter', 'linkedin recruiter', 'linkedin talent', 'linkedin recruiter seat'],
    'icims': ['icims', 'icims ats', 'icims platform'],
    'bamboo': ['bamboo', 'bamboo hr', 'bamboo hris'],
    'employee relations': ['employee relations', 'er', 'employee engagement', 'employee satisfaction', 'employee experience'],
    'employee engagement': ['employee engagement', 'engagement strategies', 'employee motivation', 'engagement surveys', 'pulse surveys'],
    'employee retention': ['employee retention', 'retention strategies', 'turnover reduction', 'retention programs'],
    'employee experience': ['employee experience', 'ex', 'employee journey', 'employee lifecycle'],
    'employee wellness': ['employee wellness', 'wellness programs', 'wellbeing', 'work life balance', 'health and wellness'],
    'diversity and inclusion': ['diversity and inclusion', 'd&i', 'dei', 'diversity equity inclusion', 'belonging', 'inclusion strategies'],
    'workplace culture': ['workplace culture', 'company culture', 'organizational culture', 'culture building', 'culture transformation'],
    'organizational development': ['organizational development', 'od', 'org development', 'change management', 'organization effectiveness'],
    'change management': ['change management', 'organizational change', 'change implementation', 'change leadership', 'change enablement'],
    'performance management': ['performance management', 'performance review', 'appraisal', 'performance evaluation', 'pm'],
    'performance appraisal': ['performance appraisal', 'appraisal system', 'review process', 'performance rating'],
    'goal setting': ['goal setting', 'okr', 'kpi', 'objectives and key results', 'performance goals', 'smart goals'],
    'performance improvement plan': ['performance improvement plan', 'pip', 'improvement plan', 'performance plan'],
    'talent management': ['talent management', 'talent development', 'talent strategy', 'talent optimization'],
    'succession planning': ['succession planning', 'succession management', 'talent pipeline', 'leadership pipeline'],
    'career development': ['career development', 'career progression', 'career pathing', 'career planning'],
    'career counseling': ['career counseling', 'career advising', 'career guidance', 'career mentoring'],
    'mentoring': ['mentoring', 'mentorship', 'mentoring program', 'mentor mentee'],
    'coaching': ['coaching', 'employee coaching', 'performance coaching', 'leadership coaching'],
    'learning and development': ['learning and development', 'l&d', 'learning development', 'training development', 'ld'],
    'training': ['training', 'training programs', 'employee training', 'staff training', 'training content'],
    'training delivery': ['training delivery', 'training facilitation', 'conducting training', 'training sessions'],
    'training needs analysis': ['training needs analysis', 'tna', 'training gap analysis', 'skills gap analysis'],
    'learning management system': ['learning management system', 'lms', 'learning platform', 'training platform'],
    'elearning': ['elearning', 'online learning', 'digital learning', 'virtual training', 'webinar training'],
    'instructional design': ['instructional design', 'curriculum design', 'training design', 'course design'],
    'workshop facilitation': ['workshop facilitation', 'facilitation', 'workshop delivery', 'group facilitation'],
    'corporate training': ['corporate training', 'corporate learning', 'professional development', 'workplace training'],
    'compensation': ['compensation', 'compensation management', 'salary administration', 'pay structure', 'remuneration'],
    'compensation and benefits': ['compensation and benefits', 'c&b', 'total rewards', 'comp & ben', 'cbd'],
    'benefits administration': ['benefits administration', 'employee benefits', 'benefits management', 'benefits coordination'],
    'salary benchmarking': ['salary benchmarking', 'salary surveys', 'market pricing', 'compensation benchmarking'],
    'payroll': ['payroll', 'payroll management', 'payroll processing', 'payroll administration'],
    'incentive programs': ['incentive programs', 'bonus programs', 'performance incentives', 'reward programs'],
    'stock options': ['stock options', 'equity compensation', 'employee stock', 'esop', 'employee stock options'],
    'hr compliance': ['hr compliance', 'compliance', 'employment compliance', 'regulatory compliance', 'hr regulations'],
    'labor law': ['labor law', 'employment law', 'labor legislation', 'labor relations', 'workplace law'],
    'hr policies': ['hr policies', 'hr policy development', 'employee policies', 'policy management'],
    'employee handbook': ['employee handbook', 'handbook development', 'policy manual', 'staff handbook'],
    'workplace safety': ['workplace safety', 'ohs', 'health and safety', 'occupational safety', 'ehs'],
    'data privacy': ['data privacy', 'gdpr compliance', 'privacy regulations', 'data protection', 'hipaa compliance'],
    'union relations': ['union relations', 'labor relations', 'collective bargaining', 'union negotiations'],
    'hris': ['hris', 'hr information system', 'hr system', 'hr technology', 'hr platform'],
    'hr analytics': ['hr analytics', 'people analytics', 'workforce analytics', 'hr data analysis', 'talent analytics'],
    'people analytics': ['people analytics', 'workforce analytics', 'talent analytics', 'people data'],
    'human capital management': ['human capital management', 'hcm', 'human capital', 'hc'],
    'hr reporting': ['hr reporting', 'hr metrics', 'hr dashboards', 'workforce reporting', 'hr analytics reporting'],
    'workforce planning': ['workforce planning', 'workforce management', 'staffing planning', 'talent planning'],
    'headcount planning': ['headcount planning', 'resource planning', 'capacity planning', 'staffing forecast'],
    
    # =========================
    # Business Development (Extended)
    # =========================
    'business development': ['business development', 'bd', 'new business', 'business growth', 'growth strategy'],
    'business strategy': ['business strategy', 'strategic planning', 'corporate strategy', 'business planning', 'strategy development'],
    'market expansion': ['market expansion', 'market growth', 'territory expansion', 'geographic expansion', 'market penetration'],
    'strategic partnerships': ['strategic partnerships', 'partnership development', 'strategic alliances', 'partner ecosystem'],
    'new market entry': ['new market entry', 'market entry strategy', 'market penetration', 'entering new markets'],
    'competitive analysis': ['competitive analysis', 'competitor analysis', 'market intelligence', 'competitive research'],
    'market research': ['market research', 'market analysis', 'market study', 'industry research', 'consumer insights'],
    'market analysis': ['market analysis', 'market assessment', 'market evaluation', 'market sizing'],
    'industry analysis': ['industry analysis', 'industry research', 'sector analysis', 'industry trends'],
    'due diligence': ['due diligence', 'business due diligence', 'financial due diligence', 'investment due diligence'],
    'sales': ['sales', 'sales management', 'sales strategy', 'selling', 'sales operations'],
    'sales strategy': ['sales strategy', 'sales planning', 'sales approach', 'sales methodology', 'sales execution'],
    'revenue growth': ['revenue growth', 'revenue generation', 'revenue development', 'top line growth', 'revenue strategy'],
    'sales pipeline': ['sales pipeline', 'pipeline management', 'deal pipeline', 'sales funnel'],
    'lead generation': ['lead generation', 'lead gen', 'new leads', 'prospecting', 'lead acquisition'],
    'client acquisition': ['client acquisition', 'customer acquisition', 'new client development', 'business acquisition'],
    'account management': ['account management', 'client management', 'customer retention', 'account planning'],
    'key account management': ['key account management', 'kam', 'strategic accounts', 'major accounts'],
    'sales operations': ['sales operations', 'sales ops', 'sales enablement', 'sales process'],
    'sales enablement': ['sales enablement', 'sales tools', 'sales support', 'sales training'],
    'cold calling': ['cold calling', 'cold outreach', 'sales calls', 'telemarketing'],
    'proposal writing': ['proposal writing', 'proposal development', 'rfp response', 'bid management', 'tender response'],
    'contract negotiation': ['contract negotiation', 'negotiation', 'deal negotiation', 'contract management', 'commercial negotiation'],
    'closing deals': ['closing deals', 'deal closing', 'sales closing', 'deal execution', 'closing'],
    'sales forecasting': ['sales forecasting', 'forecasting', 'revenue forecasting', 'sales projections'],
    'quote to cash': ['quote to cash', 'quote to cash process', 'q2c', 'order to cash'],
    'relationship building': ['relationship building', 'relationship management', 'client relationships', 'stakeholder management'],
    'stakeholder management': ['stakeholder management', 'stakeholder engagement', 'stakeholder communication'],
    'network development': ['network development', 'networking', 'business networking', 'professional networking'],
    'crm': ['crm', 'customer relationship management', 'salesforce crm', 'hubspot'],
    'salesforce': ['salesforce', 'salesforce crm', 'salesforce platform', 'salesforce admin'],
    'hubspot': ['hubspot', 'hubspot crm', 'hubspot platform', 'hubspot marketing'],
    'pipeline management': ['pipeline management', 'sales pipeline management', 'opportunity management'],
    'business planning': ['business planning', 'business plan', 'strategic planning', 'business strategy'],
    'go-to-market strategy': ['go-to-market strategy', 'gtm', 'go to market', 'market launch', 'market entry strategy'],
    'business model': ['business model', 'business model innovation', 'business design', 'business model canvas'],
    'business case': ['business case', 'business justification', 'proposal development', 'business proposal'],
    'investment analysis': ['investment analysis', 'investment evaluation', 'roi analysis', 'investment assessment'],
    'financial modeling': ['financial modeling', 'financial models', 'financial analysis', 'financial projections'],
    'budgeting': ['budgeting', 'budget management', 'financial planning', 'budget development'],
    'executive presentations': ['executive presentations', 'executive summary', 'board presentations', 'steering committee'],
    'pitch deck creation': ['pitch deck', 'investor pitch', 'pitch presentation', 'slide deck', 'funding presentation'],
    'public speaking': ['public speaking', 'presentations', 'speaking engagements', 'keynote speaking'],
    'business writing': ['business writing', 'professional writing', 'business communication', 'report writing'],
    'strategic thinking': ['strategic thinking', 'strategic mindset', 'strategic approach', 'strategic reasoning'],
    'strategic planning': ['strategic planning', 'strategy development', 'strategy formulation', 'strategic framework'],
    'strategic initiatives': ['strategic initiatives', 'strategic projects', 'key initiatives', 'execution strategy'],
    'mergers and acquisitions': ['mergers and acquisitions', 'm&a', 'acquisitions', 'mergers', 'acquisition strategy'],
    'joint ventures': ['joint ventures', 'jv', 'strategic alliances', 'partnerships', 'business partnerships'],
    'license agreements': ['license agreements', 'licensing', 'ip licensing', 'technology licensing', 'license management'],
    'venture capital': ['venture capital', 'vc', 'investment management', 'funding', 'capital investment'],
    'fundraising': ['fundraising', 'funding', 'capital raising', 'investor relations', 'capital fundraising'],
    'international business': ['international business', 'global business', 'cross-border', 'multinational', 'global operations'],
    'global strategy': ['global strategy', 'international strategy', 'global expansion', 'global planning'],
    'export': ['export', 'export management', 'international trade', 'export compliance'],
    'import': ['import', 'import management', 'import/export', 'import compliance'],
    'global supply chain': ['global supply chain', 'global sourcing', 'international logistics', 'supply chain'],
    
    # =========================
    # Marketing (Extended)
    # =========================
    'marketing': ['marketing', 'marketing strategy', 'marketing management', 'marketing operations'],
    'digital marketing': ['digital marketing', 'online marketing', 'internet marketing', 'digital marketing strategy'],
    'content marketing': ['content marketing', 'content strategy', 'content creation', 'content development'],
    'social media marketing': ['social media marketing', 'smm', 'social marketing', 'social media strategy'],
    'branding': ['branding', 'brand management', 'brand strategy', 'brand development'],
    'brand management': ['brand management', 'brand building', 'brand development', 'brand positioning'],
    'public relations': ['public relations', 'pr', 'media relations', 'press relations'],
    'communications': ['communications', 'corporate communications', 'strategic communications', 'internal comms'],
    'email marketing': ['email marketing', 'email campaigns', 'mailchimp', 'email automation'],
    'seo': ['seo', 'search engine optimization', 'search marketing', 'organic search'],
    'sem': ['sem', 'search engine marketing', 'paid search', 'ppc', 'google ads'],
    'google analytics': ['google analytics', 'ga', 'analytics', 'ga4', 'google analytics 4'],
    'product marketing': ['product marketing', 'product go to market', 'product launch', 'product positioning'],
    'growth hacking': ['growth hacking', 'growth marketing', 'growth strategy', 'growth tactics'],
    'influencer marketing': ['influencer marketing', 'influencer management', 'creator marketing'],
    'video marketing': ['video marketing', 'video content', 'youtube marketing', 'visual content'],
    'storytelling': ['storytelling', 'brand storytelling', 'narrative design', 'story brand'],
    'copywriting': ['copywriting', 'copy', 'content writing', 'ad copy'],
    
    # =========================
    # Leadership & Management (Extended)
    # =========================
    'leadership': ['leadership', 'leadership skills', 'people leadership', 'team leadership', 'leadership development'],
    'team leadership': ['team leadership', 'team lead', 'leading teams', 'team management', 'lead team'],
    'people management': ['people management', 'personnel management', 'staff management', 'people leader'],
    'project leadership': ['project leadership', 'project lead', 'leading projects', 'project director'],
    'strategic leadership': ['strategic leadership', 'executive leadership', 'leadership strategy', 'visionary leadership'],
    'mentorship': ['mentorship', 'mentoring', 'coaching', 'people development', 'mentorship program'],
    'team building': ['team building', 'building teams', 'team development', 'team engagement'],
    'delegation': ['delegation', 'task delegation', 'work delegation', 'empowerment'],
    'decision making': ['decision making', 'decision-making', 'strategic decisions', 'executive decisions'],
    'problem solving': ['problem solving', 'analytical problem solving', 'solution finding', 'troubleshooting'],
    'critical thinking': ['critical thinking', 'critical analysis', 'analytical thinking', 'strategic thinking'],
    'time management': ['time management', 'time optimization', 'prioritization', 'time allocation'],
    'project management': ['project management', 'project delivery', 'project coordination', 'project administration'],
    'program management': ['program management', 'program delivery', 'program leadership', 'program oversight'],
    'resource management': ['resource management', 'resource allocation', 'resource planning', 'capacity management'],
    'stakeholder management': ['stakeholder management', 'stakeholder engagement', 'stakeholder communication'],
    'conflict resolution': ['conflict resolution', 'conflict management', 'mediation', 'problem resolution'],
    'negotiation': ['negotiation', 'negotiating', 'deal making', 'commercial negotiation'],
    'influencing': ['influencing', 'influence', 'persuasion', 'negotiation', 'stakeholder influence'],
    'cross-functional collaboration': ['cross-functional collaboration', 'cross-functional teams', 'cross team collaboration'],
    'remote team management': ['remote team management', 'distributed teams', 'virtual teams', 'remote leadership'],
    
    # =========================
    # Communication (Extended)
    # =========================
    'communication': ['communication', 'excellent communication', 'strong communication', 'effective communication', 'communication skills'],
    'verbal communication': ['verbal communication', 'spoken communication', 'oral communication', 'speaking skills'],
    'written communication': ['written communication', 'writing skills', 'written skills', 'business writing'],
    'presentation skills': ['presentation skills', 'presenting', 'public speaking', 'presentation delivery'],
    'interpersonal skills': ['interpersonal skills', 'people skills', 'soft skills', 'relationship skills'],
    'active listening': ['active listening', 'listening skills', 'empathy', 'listening'],
    'emotional intelligence': ['emotional intelligence', 'eq', 'emotional awareness', 'emotional quotient'],
    'collaboration': ['collaboration', 'teamwork', 'collaborative', 'team player', 'teamwork skills'],
    'negotiation': ['negotiation', 'negotiating', 'persuasion', 'influence', 'commercial awareness'],
    
    # =========================
    # Financial Management (Extended)
    # =========================
    'financial analysis': ['financial analysis', 'financial modeling', 'financial evaluation', 'financial assessment'],
    'financial management': ['financial management', 'finance management', 'financial planning', 'financial oversight'],
    'budget management': ['budget management', 'budgeting', 'cost management', 'budget control'],
    'cost analysis': ['cost analysis', 'cost benefit analysis', 'cba', 'cost reduction'],
    'forecasting': ['forecasting', 'financial forecasting', 'predictive modeling', 'financial projections'],
    'risk assessment': ['risk assessment', 'risk analysis', 'risk evaluation', 'risk management'],
    'audit': ['audit', 'financial audit', 'internal audit', 'external audit', 'audit process'],
    'accounting': ['accounting', 'financial accounting', 'management accounting', 'accounting principles'],
    'accounts payable': ['accounts payable', 'ap', 'payables', 'vendor payments', 'invoicing'],
    'accounts receivable': ['accounts receivable', 'ar', 'receivables', 'invoicing', 'collections'],
    'tax compliance': ['tax compliance', 'taxation', 'tax management', 'tax planning'],
    
    # =========================
    # Legal (Extended)
    # =========================
    'contract law': ['contract law', 'contract management', 'contract review', 'contract drafting'],
    'corporate law': ['corporate law', 'business law', 'company law', 'corporate governance'],
    'intellectual property': ['intellectual property', 'ip', 'patents', 'trademarks', 'copyright', 'ip management'],
    'commercial law': ['commercial law', 'trade law', 'business regulations', 'commercial regulations'],
    'regulatory compliance': ['regulatory compliance', 'compliance management', 'regulations', 'compliance officer'],
    'commercial contracts': ['commercial contracts', 'business contracts', 'contract negotiation', 'contracts'],
    'employment law': ['employment law', 'labor law', 'employee rights', 'workplace law'],
    'data privacy': ['data privacy', 'gdpr', 'data protection', 'privacy compliance', 'ccpa'],
    'compliance management': ['compliance management', 'regulatory compliance', 'compliance officer'],
    'legal research': ['legal research', 'legal analysis', 'case law research', 'legal drafting'],
    
    # =========================
    # Consulting (Extended)
    # =========================
    'management consulting': ['management consulting', 'consulting', 'business consulting', 'management advisor'],
    'strategy consulting': ['strategy consulting', 'strategic consulting', 'strategy advisor'],
    'change management': ['change management', 'organizational change', 'transformation', 'change advisor'],
    'process improvement': ['process improvement', 'business process improvement', 'bpi', 'optimization'],
    'business transformation': ['business transformation', 'transformation management', 'organizational transformation'],
    'digital transformation': ['digital transformation', 'digital strategy', 'digital enablement'],
    'data driven decision making': ['data driven decision making', 'data driven decisions', 'dddm'],
    'analytics': ['analytics', 'data analytics', 'business analytics', 'analytics strategy'],
    'kpi': ['kpi', 'key performance indicators', 'metrics', 'measurement', 'performance metrics'],
    'benchmarking': ['benchmarking', 'performance benchmarking', 'competitive benchmarking'],
    
    # =========================
    # Languages (Extended)
    # =========================
    'english': ['english', 'fluent english', 'english language', 'native english', 'english proficiency'],
    'spanish': ['spanish', 'español', 'spanish language', 'fluent spanish'],
    'french': ['french', 'français', 'french language', 'fluent french'],
    'german': ['german', 'deutsch', 'german language', 'fluent german'],
    'mandarin': ['mandarin', 'chinese', '普通话', 'mandarin chinese', 'fluent mandarin'],
    'arabic': ['arabic', 'العربية', 'arabic language', 'fluent arabic'],
    'hindi': ['hindi', 'हिन्दी', 'hindi language', 'fluent hindi'],
    'japanese': ['japanese', '日本語', 'japanese language', 'fluent japanese'],
    'portuguese': ['portuguese', 'português', 'portuguese language', 'fluent portuguese'],
    'russian': ['russian', 'русский', 'russian language', 'fluent russian'],
    'italian': ['italian', 'italiano', 'italian language', 'fluent italian'],
    'korean': ['korean', '한국어', 'korean language', 'fluent korean'],
    'dutch': ['dutch', 'nederlands', 'dutch language', 'fluent dutch'],
    'turkish': ['turkish', 'türkçe', 'turkish language', 'fluent turkish'],
    'urdu': ['urdu', 'اردو', 'urdu language', 'fluent urdu'],
    'bengali': ['bengali', 'বাংলা', 'bengali language', 'fluent bengali'],
    'punjabi': ['punjabi', 'ਪੰਜਾਬੀ', 'punjabi language', 'fluent punjabi'],
    
    # =========================
    # Additional Technical Skills
    # =========================
    'blockchain': ['blockchain', 'blockchain technology', 'distributed ledger', 'web3', 'dlt'],
    'ethereum': ['ethereum', 'eth', 'solidity', 'ethereum blockchain', 'eth smart contracts'],
    'smart contracts': ['smart contracts', 'smart contract development', 'solidity contract', 'smart contract auditing'],
    'web3': ['web3', 'web3.0', 'web3 development', 'web3.js', 'ethers.js'],
    'reactjs': ['reactjs', 'react', 'react.js', 'react library', 'react development'],
    'vuejs': ['vuejs', 'vue', 'vue.js', 'vue framework', 'vue development'],
    'angularjs': ['angularjs', 'angular', 'angular.js', 'angular framework', 'angular development'],
    'nodejs': ['nodejs', 'node', 'node.js', 'node development', 'node backend'],
    'expressjs': ['expressjs', 'express', 'express.js', 'express server', 'express backend'],
    'flask': ['flask', 'flask framework', 'python flask', 'flask api'],
    'django': ['django', 'django framework', 'python django', 'django admin'],
    'spring boot': ['spring boot', 'springboot', 'spring-boot', 'springboot microservices'],
    'apache': ['apache', 'apache server', 'httpd', 'apache webserver', 'apache2'],
    'nginx': ['nginx', 'nginx server', 'nginx web server', 'nginx config', 'nginx proxy'],
    'tomcat': ['tomcat', 'apache tomcat', 'tomcat server', 'tomcat container'],
    'jboss': ['jboss', 'wildfly', 'jboss application server'],
    'weblogic': ['weblogic', 'oracle weblogic', 'weblogic server'],
    'websphere': ['websphere', 'ibm websphere', 'websphere application server'],
    'api gateway': ['api gateway', 'kong', 'apigee', 'traefik', 'aws api gateway'],
    'service mesh': ['service mesh', 'istio', 'linkerd', 'consul', 'envoy'],
    'envoy': ['envoy', 'envoy proxy', 'service proxy', 'lyft envoy'],
    'kafka': ['kafka', 'apache kafka', 'kafka streaming', 'kafka producer', 'kafka consumer'],
    'airflow': ['apache airflow', 'airflow', 'airflow dag', 'airflow operators', 'airflow pipeline'],
    'spark': ['spark', 'apache spark', 'pyspark', 'spark sql', 'spark streaming', 'spark ml', 'databricks spark'],
    'hadoop': ['hadoop', 'apache hadoop', 'hdfs', 'mapreduce', 'yarn', 'hive', 'hbase'],
    'snowflake': ['snowflake', 'snowflake data', 'snowflake cloud', 'snowflake warehouse'],
    'tableau': ['tableau', 'tableau visualization', 'tableau dashboard', 'tableau desktop', 'tableau server'],
    'power bi': ['power bi', 'microsoft power bi', 'powerbi', 'power bi dashboard', 'power query', 'dax'],
    'looker': ['looker', 'google looker', 'looker dashboard', 'looker studio', 'lookml'],
    'excel':['excel', 'microsoft excel', 'excel formulas', 'excel pivot tables', 'excel charts'],
    'microsoft sql server': ['microsoft sql server', 'sql server', 'mssql', 'tsql', 'sql server management studio'],
    'oracle database': ['oracle database', 'oracle db', 'oracle sql', 'pl/sql', 'oracle sql developer'],
    'google sheets': ['google sheets', 'gsheets', 'google spreadsheet', 'google docs spreadsheet'],
}

# ============================================================
# Skill Categories (Comprehensive)
# ============================================================

SKILL_CATEGORIES: Dict[str, Set[str]] = {
    # Programming Languages
    'programming_languages': {
        'python', 'javascript', 'typescript', 'java', 'c', 'c++', 'c#', 'go', 'rust',
        'kotlin', 'swift', 'php', 'ruby', 'scala', 'perl', 'r', 'matlab', 'dart',
        'objective-c', 'bash', 'powershell', 'assembly', 'julia', 'zig', 'crystal',
        'elixir', 'erlang', 'haskell', 'lua', 'clojure', 'groovy', 'f#', 'vb.net',
        'delphi', 'ada', 'fortran', 'cobol', 'pl/sql', 't-sql'
    },
    
    # Frontend
    'frontend': {
        'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind css', 'material ui',
        'ant design', 'chakra ui', 'react', 'next.js', 'vue', 'nuxt.js', 'angular',
        'svelte', 'redux', 'mobx', 'webpack', 'vite', 'jquery', 'styled-components',
        'emotion', 'framer motion', 'react router', 'react query', 'nextjs', 'gatsby',
        'remix', 'astro', 'solidjs', 'qwik', 'preact', 'lit', 'alpinejs', 'htmx'
    },
    
    # UI/UX Design
    'ui_ux_design': {
        'ui design', 'ux design', 'ux research', 'interaction design', 'information architecture',
        'wireframing', 'prototyping', 'visual design', 'user personas', 'user journey mapping',
        'accessibility', 'design thinking', 'product design', 'service design', 'design systems',
        'figma', 'sketch', 'adobe xd', 'invision', 'zeplin', 'abstract', 'framer', 'webflow',
        'balsamiq', 'ux writing', 'user testing', 'conversion optimization', 'a/b testing'
    },
    
    # Backend
    'backend': {
        'node.js', 'express.js', 'nestjs', 'django', 'flask', 'fastapi',
        'spring boot', 'spring', 'asp.net', '.net', 'laravel', 'symfony',
        'ruby on rails', 'gin', 'echo', 'actix', 'rocket', 'tornado', 'falcon',
        'hapi', 'koa', 'meteor', 'adonis', 'sails', 'loopback', 'strapi', 'directus',
        'graphql', 'grpc', 'rest api'
    },
    
    # Mobile
    'mobile': {
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
        'kotlin android', 'swift ios', 'cordova', 'capacitor', 'nativescript',
        'react native expo', 'android jetpack', 'swiftui', 'uikit', 'android xml',
        'android material', 'flutter widgets', 'react native navigation',
        'android permissions', 'ios permissions'
    },
    
    # AI & Machine Learning
    'ai_ml': {
        'machine learning', 'deep learning', 'artificial intelligence',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'opencv',
        'hugging face', 'langchain', 'llm', 'rag', 'prompt engineering',
        'llama', 'gpt', 'bert', 'computer vision', 'nlp', 'data science',
        'agentic ai', 'ai agents', 'langgraph', 'autogen', 'crewai', 'llamaindex',
        'semantic kernel', 'vector database', 'embedding', 'large language model',
        'claude', 'gemini', 'mistral', 'falcon', 't5', 'roberta', 'xlm-roberta',
        'electra', 'deberta', 'phi', 'mixtral', 'command', 'dbrx', 'grok', 'palm',
        'bloom', 'opt', 'knowledge graph', 'semantic search', 'hybrid search',
        'reranking', 'chunking', 'chain of thought', 'tree of thoughts', 'react',
        'self-consistency', 'constitutional ai', 'instruction tuning',
        'mlflow', 'weights & biases', 'tensorboard', 'model registry', 'feature store',
        'model monitoring', 'model deployment', 'model serving', 'onnx',
        'jax', 'numpy', 'pandas', 'matplotlib', 'seaborn', 'plotly', 'scipy',
        'statsmodels', 'gradio', 'streamlit', 'fastai', 'lightgbm', 'xgboost', 'catboost',
        'ai ethics', 'ai safety', 'bias detection', 'interpretability', 'explainable ai',
        'model fairness', 'privacy preserving ml'
    },
    
    # Computer Vision
    'computer_vision': {
        'computer vision', 'object detection', 'image classification', 'image segmentation',
        'object tracking', 'face recognition', 'pose estimation', 'optical flow',
        'depth estimation', '3d reconstruction', 'cnn', 'resnet', 'efficientnet',
        'vgg', 'inception', 'mobilenet', 'yolo', 'detectron', 'mask r-cnn',
        'faster r-cnn', 'retinanet', 'ssd', 'vision transformer', 'dino', 'clip',
        'sam', 'stable diffusion', 'dalle', 'midjourney', 'imagen', 'controlnet',
        'gan', 'dcgan', 'stylegan', 'cyclegan', 'pix2pix'
    },
    
    # NLP
    'nlp': {
        'nlp', 'text classification', 'ner', 'tokenization', 'sentiment analysis',
        'text summarization', 'machine translation', 'question answering',
        'text generation', 'topic modeling', 'word embeddings', 'transformer',
        'attention', 'encoder-decoder', 'fine-tuning', 'prompt tuning', 'qlora',
        'lora', 'peft'
    },
    
    # Databases
    'databases': {
        'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server',
        'mongodb', 'redis', 'cassandra', 'dynamodb', 'firebase', 'elasticsearch',
        'neo4j', 'influxdb', 'couchdb', 'supabase', 'arangodb', 'clickhouse',
        'cockroachdb', 'planetscale', 'hasura', 'singleStore', 'data lake',
        'delta lake', 'iceberg', 'hudi'
    },
    
    # Cloud
    'cloud': {
        'aws', 'azure', 'gcp', 'digitalocean', 'heroku', 'vercel', 'netlify',
        'cloudflare', 'alibaba cloud', 'oracle cloud', 'aws devops', 'azure devops',
        'google cloud run', 'google kubernetes', 'aws ecs', 'aws eks', 'azure aks',
        'linode', 'openstack'
    },
    
    # DevOps
    'devops': {
        'docker', 'kubernetes', 'jenkins', 'github actions', 'gitlab ci',
        'circleci', 'travis ci', 'terraform', 'ansible', 'chef', 'puppet',
        'argo', 'tekton', 'spinnaker', 'flux', 'crossplane', 'packer', 'vagrant',
        'istio', 'linkerd', 'consul', 'vault', 'nomad', 'helm', 'kustomize',
        'prometheus', 'grafana', 'elk stack', 'splunk', 'datadog', 'new relic'
    },
    
    # Testing
    'testing': {
        'junit', 'pytest', 'selenium', 'cypress', 'playwright', 'jest',
        'mocha', 'chai', 'testing library', 'unit testing', 'integration testing',
        'e2e testing', 'performance testing', 'security testing',
        'quality assurance', 'manual testing', 'automation testing',
        'api testing', 'mobile testing', 'appium', 'testng', 'cucumber', 'katalon',
        'mockito', 'sinon', 'testcontainers', 'vitest'
    },
    
    # Security
    'security': {
        'oauth', 'jwt', 'ssl', 'tls', 'owasp', 'penetration testing',
        'vulnerability assessment', 'security auditing', 'identity management',
        'security compliance', 'encryption', 'firewall', 'zero trust',
        'devsecops', 'sast', 'dast', 'secrets management', 'sso', 'saml',
        'cors', 'csrf', 'xss', 'sql injection', 'rate limiting', 'api security',
        'container security', 'cloud security', 'network security'
    },
    
    # Architecture
    'architecture': {
        'microservices', 'monolith', 'serverless', 'event driven architecture',
        'mvc', 'mvvm', 'clean architecture', 'domain driven design', 'solid',
        'design patterns', 'restful design', 'event sourcing', 'cqrs',
        'hexagonal architecture', 'onion architecture', 'service mesh',
        'circuit breaker', 'api gateway', 'message queue', 'pubsub',
        'distributed systems', 'fault tolerance', 'load balancing', 'caching'
    },
    
    # HR
    'hr': {
        'human resources', 'hr operations', 'hr strategy', 'talent acquisition',
        'full cycle recruiting', 'candidate sourcing', 'candidate screening',
        'candidate assessment', 'interviewing', 'offer management', 'onboarding',
        'recruitment marketing', 'applicant tracking system', 'workday',
        'greenhouse', 'lever', 'recruiter', 'icims', 'bamboo', 'employee relations',
        'employee engagement', 'employee retention', 'employee experience',
        'employee wellness', 'diversity and inclusion', 'workplace culture',
        'organizational development', 'change management', 'performance management',
        'performance appraisal', 'goal setting', 'performance improvement plan',
        'talent management', 'succession planning', 'career development',
        'career counseling', 'mentoring', 'coaching', 'learning and development',
        'training', 'training delivery', 'training needs analysis',
        'learning management system', 'elearning', 'instructional design',
        'workshop facilitation', 'corporate training', 'compensation',
        'compensation and benefits', 'benefits administration', 'salary benchmarking',
        'payroll', 'incentive programs', 'stock options', 'hr compliance',
        'labor law', 'hr policies', 'employee handbook', 'workplace safety',
        'data privacy', 'union relations', 'hris', 'hr analytics', 'people analytics',
        'human capital management', 'hr reporting', 'workforce planning',
        'headcount planning'
    },
    
    # Business Development
    'business_development': {
        'business development', 'business strategy', 'market expansion',
        'strategic partnerships', 'new market entry', 'competitive analysis',
        'market research', 'market analysis', 'industry analysis', 'due diligence',
        'sales', 'sales strategy', 'revenue growth', 'sales pipeline',
        'lead generation', 'client acquisition', 'account management',
        'key account management', 'sales operations', 'sales enablement',
        'cold calling', 'proposal writing', 'contract negotiation',
        'closing deals', 'sales forecasting', 'quote to cash',
        'relationship building', 'stakeholder management', 'network development',
        'crm', 'salesforce', 'hubspot', 'pipeline management',
        'business planning', 'go-to-market strategy', 'business model',
        'business case', 'investment analysis', 'financial modeling',
        'budgeting', 'executive presentations', 'pitch deck creation',
        'public speaking', 'business writing', 'strategic thinking',
        'strategic planning', 'strategic initiatives', 'mergers and acquisitions',
        'joint ventures', 'license agreements', 'venture capital', 'fundraising',
        'international business', 'global strategy', 'export', 'import',
        'global supply chain'
    },
    
    # Marketing
    'marketing': {
        'marketing', 'digital marketing', 'content marketing',
        'social media marketing', 'branding', 'brand management',
        'public relations', 'communications', 'email marketing',
        'seo', 'sem', 'google analytics', 'product marketing',
        'growth hacking', 'influencer marketing', 'video marketing',
        'storytelling', 'copywriting'
    },
    
    # Leadership
    'leadership': {
        'leadership', 'team leadership', 'people management', 'project leadership',
        'strategic leadership', 'mentorship', 'team building', 'delegation',
        'decision making', 'problem solving', 'critical thinking',
        'time management', 'project management', 'program management',
        'resource management', 'stakeholder management', 'conflict resolution',
        'negotiation', 'influencing', 'cross-functional collaboration',
        'remote team management'
    },
    
    # Communication
    'communication': {
        'communication', 'verbal communication', 'written communication',
        'presentation skills', 'interpersonal skills', 'active listening',
        'emotional intelligence', 'collaboration', 'negotiation'
    },
    
    # Financial
    'financial': {
        'financial analysis', 'financial management', 'budget management',
        'cost analysis', 'forecasting', 'risk assessment', 'audit',
        'accounting', 'accounts payable', 'accounts receivable', 'tax compliance'
    },
    
    # Legal
    'legal': {
        'contract law', 'corporate law', 'intellectual property',
        'commercial law', 'regulatory compliance', 'commercial contracts',
        'employment law', 'data privacy', 'compliance management', 'legal research'
    },
    
    # Consulting
    'consulting': {
        'management consulting', 'strategy consulting', 'change management',
        'process improvement', 'business transformation', 'digital transformation',
        'data driven decision making', 'analytics', 'kpi', 'benchmarking'
    },
    
    # Project Management Tools
    'project_tools': {
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'trello',
        'asana', 'monday.com', 'notion', 'slack', 'microsoft teams',
        'zoom', 'smartsheet', 'basecamp', 'clickup', 'linear', 'pivotal tracker'
    },
    
    # Languages
    'languages': {
        'english', 'spanish', 'french', 'german', 'mandarin', 'arabic',
        'hindi', 'japanese', 'portuguese', 'russian', 'italian', 'korean',
        'dutch', 'turkish', 'urdu', 'bengali', 'punjabi'
    },
    
    # Additional Technical
    'additional_tech': {
        'blockchain', 'ethereum', 'smart contracts', 'web3', 'reactjs',
        'vuejs', 'angularjs', 'nodejs', 'expressjs', 'flask', 'django',
        'spring boot', 'apache', 'nginx', 'tomcat', 'jboss', 'weblogic',
        'websphere', 'api gateway', 'service mesh', 'envoy', 'kafka',
        'airflow', 'spark', 'hadoop', 'snowflake', 'tableau', 'power bi',
        'looker'
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
        'os', 'networking', 'messaging', 'monitoring', 'additional_tech',
        'ui_ux_design', 'computer_vision', 'nlp'
    }
    for category in get_category_for_skill(skill):
        if category in tech_categories:
            return True
    return False