# importing Tornado module
import tornado.ioloop
import tornado.web
import os

from tornado.options import define, options
 
define("port", default=8080, help="run on the given port", type=int)

# Setting up the main template
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')




settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'debug': True
    }

# setting up the root of the web app
application = tornado.web.Application([
    (r"/", MainHandler)
], **settings)

# Start the server at port 8889
if __name__ == "__main__":
  tornado.options.parse_command_line()
  print(r'Server Running at http://localhost:' + str(options.port) + r'/')
  print(r'To close press ctrl + c')
  application.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
