from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import re
import requests
import nltk
import os

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
cwd = os.path.dirname(os.path.realpath(__file__))

def go_scrape(url):
  page_response = requests.get(url, timeout=5)
  soup = BeautifulSoup(page_response.content, "html.parser")
  if "bbc" in url:
    class_html = 'story-body__inner'
  if "wikipedia" in url:
    class_html = 'mw-content-ltr'
  article_div = soup.find('div', class_=class_html)
  paragraphs = article_div.find_all('p')
  return paragraphs

def get_dict_words(paragraphs_list):
  string_words = ' '.join(s.text for s in paragraphs_list if s != punctuation)
  tokens = nltk.word_tokenize(string_words)
  tagged = nltk.pos_tag(tokens)
  nouns_and_verbs = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ')]
  downcased = [x.lower() for x in nouns_and_verbs]
  counter = Counter(downcased)
  words_dict = {}
  for word, count in counter.items():
    words_dict[word] = count
  return words_dict

def sort_dict_first_hundreds(words_dict):
  latest_dict = {}
  new_list = sorted(words_dict.items(), reverse=True, key=lambda kv: kv[1])
  for n in new_list[:100]:
      latest_dict[n[0]] = n[1]
  return latest_dict

def latest_dict_to_string(latest_dict):
  final_scraped_words_string = " ".join(k for k,v in latest_dict.items())
  return final_scraped_words_string
    
    