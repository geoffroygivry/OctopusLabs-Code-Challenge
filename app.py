# importing Tornado module
import tornado.ioloop
import tornado.web
import os

# Custom imports
import web_scrape
import wordcloud_generator as wcg

# Setting up the main template
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')

class WordCloudHandler(tornado.web.RequestHandler):
    def post(self):
        url_arg = self.get_argument('my_url')
        url_scraped = web_scrape.go_scrape(url_arg)
        get_dict = web_scrape.get_dict_words(url_scraped)
        ordered_dict = web_scrape.sort_dict_first_hundreds(get_dict)
        dict_to_string = web_scrape.latest_dict_to_string(ordered_dict)
        wordCloud_result = wcg.generate_wordcloud(dict_to_string)
        self.render('wordCloud.html')


settings = {
    'template_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'),
    'static_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static'),
    'debug': True
    }

# setting up the root of the web app
application = tornado.web.Application([
    (r"/", MainHandler), (r"/word_cloud", WordCloudHandler)], **settings)

# Start the server at port 8889
if __name__ == "__main__":
  PortNumber = str(8888)
  print(r'Server Running at http://localhost:' + PortNumber + r'/')
  print(r'To close press ctrl + c')
  application.listen(PortNumber)
  tornado.ioloop.IOLoop.instance().start()
