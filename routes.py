import webapp2
from webapp2_extras import routes

class TaskHandler(webapp2.RequestHandler):
  def post(self):
    self.response.write("Task complete.")

app = webapp2.WSGIApplication([   
                                  webapp2.Route('/api/task_handler', handler=TaskHandler),   
                              ], debug=True)

