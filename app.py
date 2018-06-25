# importing Tornado module
import tornado.ioloop
import tornado.web

import torndb
import MySQLdb

import os
import subprocess



from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="wordcloudstore", help="blog database name")
define("mysql_user", default="wordcloud_user", help="blog database user")
define("mysql_password", default="torncloud", help="blog database password")

# Custom imports
import web_scrape
import wordcloud_generator as wcg
import asymmetric_encryption as ae
import utils
private_key, public_key = ae.generate_keys()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/admin", AdminHandler),
            (r"/word_cloud", WordCloudHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        self.init_create_tables()

    def init_create_tables(self):
        try:
            self.db.get("SELECT COUNT(*) from entries;")
        except MySQLdb.ProgrammingError:
            subprocess.check_call(['mysql',
                                   '--host=' + options.mysql_host,
                                   '--database=' + options.mysql_database,
                                   '--user=' + options.mysql_user,
                                   '--password=' + options.mysql_password],
                                  stdin=open('schema.sql'))

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

# Setting up the main template
class HomeHandler(BaseHandler):
  def get(self):
    self.render('index.html')


class WordCloudHandler(BaseHandler):
    def post(self):
        url_arg = self.get_argument('my_url')
        url_scraped = web_scrape.go_scrape(url_arg)
        get_dict = web_scrape.get_dict_words(url_scraped)
        ordered_dict = web_scrape.sort_dict_first_hundreds(get_dict)
        dict_to_string = web_scrape.latest_dict_to_string(ordered_dict)
        wcg.generate_wordcloud(dict_to_string)
        formated_words = utils.format_words_for_db(ordered_dict, public_key)
        for formated_word in formated_words:
            encryptedword = formated_word["encryptedword"]
            word = formated_word['word']
            countedword = formated_word['countedword']
            sql_command = """INSERT INTO words (encryptedword, word, countedword) VALUES ("%s", "%s", %s)""" % (
                encryptedword, word, countedword)
            self.db.execute(sql_command)
        self.render('wordCloud.html')

class AdminHandler(BaseHandler):
    def get(self):
        db_encrypted_words = [word.word for word in self.db.query("SELECT * FROM words")]
        db_decrypted_words = [ae.decrypt_message(word, private_key) for word in db_encrypted_words]
        countedword = [word.countedword for word in self.db.query("SELECT * FROM words")]
        word_and_count = zip(db_decrypted_words, countedword)
        self.render('admin2.html', words=word_and_count)


def main():
    tornado.options.parse_command_line()
    print(r'Server Running at http://localhost:' + str(options.port) + r'/')
    print(r'To close press ctrl + c')
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
