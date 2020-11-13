def find_my_domain(tagsstring):
    '''
        reads the tags string(got from sites) & maps it to my own domain
        to return a LIST of my_topics
    '''
    tagsstring = tagsstring.split(',')
    domains = []

    ''' I. Check the topic string as it is'''
    if ( belongstodevelopment(tagsstring)):
        domains.append('development')
    if ( belongstovisual(tagsstring)):
        domains.append('visual')
    if ( belongstomobile(tagsstring)):
        domains.append('mobile')
    if ( belongstosystems(tagsstring)):
        domains.append('systems')
    if ( belongstotools(tagsstring)):
        domains.append('tools')
    if ( belongstodatascience(tagsstring)):
        domains.append('datascience')
    if ( belongstoblockchain_finance(tagsstring)):
        domains.append('blockchain_finance')
    if ( belongstocse(tagsstring)):
        domains.append('cse')
    if ( belongstoscience_engineering(tagsstring)):
        domains.append('science_engineering')
    if ( belongstoproducts(tagsstring)):
        domains.append('products')
    if ( belongstocareer(tagsstring)):
        domains.append('career')
    if ( belongstosocial(tagsstring)):
        domains.append('social')

    ''' II. Make the input string smallcase & lemmetized '''
    tagsstring = clean_text(','.join(tagsstring))
    tagsstring.split(',')

    if ( belongstodevelopment(tagsstring)):
        domains.append('development')
    if ( belongstovisual(tagsstring)):
        domains.append('visual')
    if ( belongstomobile(tagsstring)):
        domains.append('mobile')
    if ( belongstosystems(tagsstring)):
        domains.append('systems')
    if ( belongstotools(tagsstring)):
        domains.append('tools')
    if ( belongstodatascience(tagsstring)):
        domains.append('datascience')
    if ( belongstoblockchain_finance(tagsstring)):
        domains.append('blockchain_finance')
    if ( belongstocse(tagsstring)):
        domains.append('cse')
    if ( belongstoscience_engineering(tagsstring)):
        domains.append('science_engineering')
    if ( belongstoproducts(tagsstring)):
        domains.append('products')
    if ( belongstocareer(tagsstring)):
        domains.append('career')
    if ( belongstosocial(tagsstring)):
        domains.append('social')


    ''' III. Remove duplicaets & return it'''

    domains = list(dict.fromkeys(domains))
    return domains

def belongstodevelopment(s):

    development_tags = [
        'algorithms',
        'o.s',
        'osdev',
        'hack',
        'database',
        'programming',
        'programing',
        'coding',
        'software',
        'plt',
        'c-language',
        'c language',
        'c++',
        'cpp',
        'golang',
        'go-lang',
        'go lang',
        'python',
        'elixir',
        'erlang',
        'fortran',
        'haskell',
        'java',
        'javascript',
        'lisp',
        'perl',
        'php',
        'ruby',
        'rust',
        'dotnet',
        'Kotlin',
        'rails',
        'django',
        'react js',
        'react-native',
        'react native',
        'flutter',
        'kotlin',
        'sql',
        'vcs',
        'git',
        'virtualiz',
        'browser',
        'aws',
        'cloud',
        'azuredevops',
        'kubernetes',
        'k8',
        'docker',
        'gcp',
        'emacs',
        'vim',
        'neovim',
        'devops',
        'security',
        'netsec',
        'compsec',
        'websec',
        'privacy',
        'webdev',
        'release',
        'announce',
        'debug',
        'testing',
        'practice',
        'tinycode',
        'api',
        'games',
        'gamedev',
        'tech',
        'productivity',
        'opensource',
        'open-source',
        'open source'
    ]

    dev_tags_exact = [
        'os',
        'c',
        'go',
        'js',
    ]

    return any(development_tag in ','.join(s) for development_tag in development_tags) or not set(dev_tags_exact).isdisjoint(s)

def belongstovisual(s):

    visual_tags = [
        'visualiz',
        'css',
        'html',
        'kotlin',
        'design',
        'designing',
        'graphic',
        'u.i',
        'u.x',
        'gif',
        'gifs'
    ]

    visual_tags_exact = [
        'ui',
        'ux'
    ]

    return any(visual_tag in ','.join(s) for visual_tag in visual_tags) or not set(visual_tags_exact).isdisjoint(s)


def belongstomobile(s):

    mobile_tags = [
        'mobile',
        'mobile-dev',
        'mobile dev',
        'ios',
        'android',
        'appdev',
        'iosdev',
        'iosprogramming',
        'androiddev',
        'iphone',
    ]
    return any(mobile_tag in ','.join(s) for mobile_tag in mobile_tags)


def belongstosystems(s):

    systems_tags = [
        'distributed',
        'system',
        'computerarchitecture',
        'computer-architecture',
        'architecture',
        'computer-arch',
        'comp-arch',
        'compiler',
        'o.s',
        'osdev',
        'osx',
        'macos',
        'windows',
        'linux',
        'kernel',
        'ubuntu',
        'archlinux',
        'unix',
        'databases',
        'oracle',
        'datatable',
        'bigdata',
        'apache',
        'spark',
        'hadoop',
        'devops',
        'scaling',
        'scale',
        'scalable',
        'performance',
        'browser',
        'chrome',
        'firefox',
        'safari',
        'opera',
        'google',
        'apple',
        'privacy',
    ]

    systems_tags_exact = [
        'os',
    ]

    return any(systems_tag in ','.join(s) for systems_tag in systems_tags) or not set(systems_tags_exact).isdisjoint(s)


def belongstotools(s):

    tools_tags = [
        'tableau',
        'dataisbeautiful',
        'excel',
        'vcs',
        'git',
        'virtualiz',
        'browser',
        'aws',
        'cloud',
        'azuredevops',
        'kubernetes',
        'k8',
        'docker',
        'gcp',
        'emacs',
        'vim',
        'neovim',
        'tool',
        'slack',
        'extension',
    ]
    return any(tools_tag in ','.join(s) for tools_tag in tools_tags)


def belongstodatascience(s):

    datascience_tags = [
        'computervision',
        'opencv',
        'imageprocessing',
        'datamining',
        'textdatamining',
        'machinelearn',
        'machinelearning',
        'm.l',
        'neuralnetwork',
        'deeplearning',
        'deeplearn',
        'datascience',
        'dataset',
        'statistics',
        'rlang',
        'rstat',
        'matlab',
        'scikit',
        'jupyter',
        'kaggle',
        'nlp',
        'natural-language',
        'tableau',
        'dataisbeautiful',
        'excel',
        'artificial',
        'a.i',
    ]

    datascience_tags_exact = [
        'ml',
        'ai',
        'scala',
    ]
    return any(datascience_tag in ','.join(s) for datascience_tag in datascience_tags) or not set(datascience_tags_exact).isdisjoint(s)


def belongstoblockchain_finance(s):

    blockchain_finance_tags = [
        'crypto',
        'cryptography',
        'economics',
        'economy',
        'financ',
        'finance',
        'accounting',
        'invest',
        'blockchain',
        'block-chain',
        'bitcoin',
    ]
    return any(blockchain_finance_tag in ','.join(s) for blockchain_finance_tag in blockchain_finance_tags)

def belongstocse(s):

    cse_tags = [
        'compsci',
        'computerscience',
        'computer-science',
        'computer science',
        'datastructure',
        'data structure',
        'dsa',
        'algorithms',
        'gametheory',
        'game-theory',
        'discretemathematics',
        'discrete-mathematics',
        'logic',
        'networking',
        'network',
        'computer-network',
        'computernetwork',
        'computervision',
        'opencv' 
    ]
    return any(cse_tag in ','.join(s) for cse_tag in cse_tags)

def belongstoscience_engineering(s):

    science_engineering_tags = [
        'gametheory',
        'game-theory',
        'discretemathematics',
        'discrete-mathematics',
        'discrete mathematics',
        'logic',
        'science',
        'chemistry',
        'biology',
        'medicine',
        'neuro',
        'geology',
        'environment',
        'health',
        'Physics',
        'space',
        'quantum',
        'energy',
        'fluid',
        'aero',
        'engineering',
        'electronics',
        'electrical',
        'mechanicalengineering',
        'rocketry',
        'aviation',
        'nasa',
        'spacex',
        'aerodynamics',
        '3dprint',
        '3d-print',
        'math',
        'mathematics',
        'calculus',
        'differential',
        'algebra',
        'graphtheory',
        'reverseengineering',
        'reverse-engineering',
        'reverse engineering',
        'reversing',
        'robotic',
        'arduino',
        'virtualreality',
        'virtual-reality',
        'virtual reality',
        'augmentedreality',
        'augmented-reality',
        'augmented reality',
        'a.r',
        'a-r',
        'v.r',
        'v-r',
        'iot',
        'health',
        'fitness',
    ]

    science_engineering_tags_exact = [
        'ar',
        'vr'
    ]
    return any(science_engineering_tag in ','.join(s) for science_engineering_tag in science_engineering_tags) or not set(science_engineering_tags_exact).isdisjoint(s)

def belongstoproducts(s):

    products_tags = [
        'business',
        'flipping',
        'launch',
        'launchHN',
        'product_hunt',
        'startup',
        'entrepreneur',
        'digitalnomad',
        'saas',
        'showhn',
        'sideproject',
        'marketing',
        'seo'
    ]
    return any(products_tag in ','.join(s) for products_tag in products_tags)

def belongstocareer(s):

    career_tags = [
        'job',
        'hire',
        'career',
        'interview',
        'freelance',
        'upwork',
        'recruit'
    ]
    return any(career_tag in ','.join(s) for career_tag in career_tags)

def belongstosocial(s):

    social_tags = [
        'truereddit',
        'wikipedia',
        'geek',
        'tellhn',
        'person',
        'blog',
        'article',
        'education',
        'law',
        'book',
        'books',
        'phil',
        'historical',
        'history',
        'society',
        'entertainment',
        'meta',
        'photography',
        'social',
        'facebook',
        'instagram',
        'whatsapp',
        'youtube',
        'you tube',
        'you-tube',
        'snapchat',
        'social media',
        'social-media',
        'twitter',
        'education',
        'music',
        'news',
        'netflix',
        'travel',
        'movie',
        'covid'
    ]
    return any(social_tag in ','.join(s) for social_tag in social_tags)




import string
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wordnet = WordNetLemmatizer()

def clean_text(text):
    """Clean raw text using different methods :
       1. tokenize text
       2. lower text
       3. remove punctuation
       4. remove non-alphabetics char
       5. remove stopwords
       6. lemmatize
    
    Arguments:
        text {string} -- raw text
    
    Returns:
        [string] -- clean text
    """
    # text = text.split(',')
    # text = ' '.join(text)
    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    stemmed = [wordnet.lemmatize(word) for word in words]

    return ','.join(stemmed)