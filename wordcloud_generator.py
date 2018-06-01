import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 
import os

cwd = os.path.dirname(os.path.realpath(__file__))

def generate_wordcloud(text):
    wordcloud = WordCloud(font_path=os.path.join(cwd, 'static', 'Fonts', 'Roboto-Regular.ttf'),
                          width=1920,
                          height=1080,
                          background_color='white',
                          relative_scaling = 1.0,
                          stopwords = {'to', 'of', 'is', 'are', 'be', 'do'} # set or space-separated string
                          ).generate(text)
    wordcloud_img_result = os.path.join(cwd, "static", "wordcloud_img", "wc_result.png")
    wordcloud.to_file(wordcloud_img_result)
    return wordcloud_img_result