# importing Tornado module
import tornado.ioloop
import tornado.web
import os

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
  PortNumber = str(8889)
  print(r'Server Running at http://localhost:' + PortNumber + r'/')
  print(r'To close press ctrl + c')
  application.listen(PortNumber)
  tornado.ioloop.IOLoop.instance().start()
