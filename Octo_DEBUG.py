import web_scrape
import wordcloud_generator as wcg
import asymmetric_encryption as ae
import utils

private_key, public_key = ae.generate_keys()

def get_ordered_dict():
    url_arg = "https://www.bbc.co.uk/news/world-europe-44256152"
    url_scraped = web_scrape.go_scrape(url_arg)
    get_dict = web_scrape.get_dict_words(url_scraped)
    ordered_dict = web_scrape.sort_dict_first_hundreds(get_dict)
    return ordered_dict

ordered_dict = get_ordered_dict()
formated_words = utils.format_words_for_db(ordered_dict, public_key)
for formated_word in formated_words:
    for key, val in formated_word.items():
        encryptedword = formated_word["encryptedword"]
        word = formated_word['word']
        countedword = formated_word['countedword']
        sql_command = """INSERT INTO words (encryptedword, word, countedword) VALUES ("%s", "%s", %s)""" % (
            encryptedword, word, countedword)
        print sql_command
