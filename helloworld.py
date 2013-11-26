import cgi
import urllib
from google.appengine.api import taskqueue
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        task = taskqueue.Task(
                url='/api/task_handler'                
            )
        queue = taskqueue.Queue('task-queue')
        queue.add(task)

        self.response.write("Task enqueued")

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)