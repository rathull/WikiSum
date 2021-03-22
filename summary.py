import bs4 as bs  # haha funny
import urllib.request
import re
import nltk
import heapq as hq
import sys

# try:
#     n = int(input('How thorough do you want your summary (1-20): ')) - 1
# except:
#     print("Enter a number.")
#     sys.exit()


# if 'W' in str(input('Do you want a wikipedia article (W) or general text (T): ')).upper():
#     parsed = bs.BeautifulSoup(
#         urllib.request.urlopen(
#             str(
#                 input('Link: ')
#             )
#         ).read(),
#         'lxml'
#     )
# else:
#     parsed = str(
#         input(
#             'Text: '
#         )
#     )

def summary(n, url):
    n = max(0, n - 1)
    parsed = bs.BeautifulSoup(
        urllib.request.urlopen(
            str(
                url
            )
        ).read(),
        'lxml'
    )
    try:
        STOPWORDS = nltk.corpus.stopwords.words('english')
    except:
        nltk.download('stopwords')
        STOPWORDS = nltk.corpus.stopwords.words('english')
        nltk.download('punkt')


    paragraphs = parsed.find_all('p')

    text = ''

    for p in paragraphs:
        text += p.text

    # Remove weird characters
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    # Remove weird spaces
    article_text = re.sub(r'\s+', ' ', article_text)

    # Remove weird characters
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    # Remove weird stuff in general
    formatted = re.sub(r'\s+', ' ', formatted_article_text)
    try:
        sentences = nltk.sent_tokenize(article_text)
    except:
        nltk.download('punkt')

    first = nltk.sent_tokenize(article_text)[0]

    # Create a frequency distribution
    freq_dist = {}
    for w in nltk.word_tokenize(formatted):
        if w not in STOPWORDS:
            if w not in freq_dist.keys(): freq_dist[w] = 1
            else: freq_dist[w] += 1
    max_freq = max(freq_dist.values())

    # Calculate score of each sentence based on frequency distribution
    sent_scores = {}
    for s in sentences:
        for w in nltk.word_tokenize(s.lower()):
            if w in freq_dist.keys() and len(s.split(' ')) < 30:
                if s not in sent_scores.keys(): sent_scores[s] = freq_dist[w]
                else: sent_scores[s] += freq_dist[w]
    if first in sent_scores.keys():
        sent_scores[first] = -1
    # sentence_scores.get
    summary_list = hq.nlargest(n, sent_scores, key=sent_scores.get)
    # print(first,' '.join(summary_list))
    return str(first + ' ' + ' '.join(summary_list))
# print(
#     summary(3, 'https://en.wikipedia.org/wiki/Economic_diplomacy')
# )

def summaryWithoutFirst(n, url):
    n = max(0, n - 1)
    parsed = bs.BeautifulSoup(
        urllib.request.urlopen(
            str(
                url
            )
        ).read(),
        'lxml'
    )
    try:
        STOPWORDS = nltk.corpus.stopwords.words('english')
    except:
        nltk.download('stopwords')
        STOPWORDS = nltk.corpus.stopwords.words('english')
        nltk.download('punkt')


    paragraphs = parsed.find_all('p')

    text = ''

    for p in paragraphs:
        text += p.text

    # Remove weird characters
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    # Remove weird spaces
    article_text = re.sub(r'\s+', ' ', article_text)

    # Remove weird characters
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    # Remove weird stuff in general
    formatted = re.sub(r'\s+', ' ', formatted_article_text)
    try:
        sentences = nltk.sent_tokenize(article_text)
    except:
        nltk.download('punkt')

    # Create a frequency distribution
    freq_dist = {}
    for w in nltk.word_tokenize(formatted):
        if w not in STOPWORDS:
            if w not in freq_dist.keys(): freq_dist[w] = 1
            else: freq_dist[w] += 1
    max_freq = max(freq_dist.values())

    # Calculate score of each sentence based on frequency distribution
    sent_scores = {}
    for s in sentences:
        for w in nltk.word_tokenize(s.lower()):
            if w in freq_dist.keys() and len(s.split(' ')) < 30:
                if s not in sent_scores.keys(): sent_scores[s] = freq_dist[w]
                else: sent_scores[s] += freq_dist[w]
    
    
    summary_list = hq.nlargest(n, sent_scores, key=sent_scores.get)
    return str(first + ' ' + ' '.join(summary_list))
