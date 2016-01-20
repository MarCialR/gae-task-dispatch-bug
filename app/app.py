import os
from google.appengine.api import taskqueue
from google.appengine.api.modules import modules
import webapp2
import logging

module = os.getenv('YAML_MODULE', "YAML_MODULE Not defined")
version = os.getenv('YAML_VERSION', "YAML_VERSION Not defined")
hostname = modules.get_hostname()
where = "module=%s version=%s hostname=%s" %(module, version, hostname)
where_html = "<br/>module=%s<br/>version=%s<br/>hostname=%s<br/>" %(module, version, hostname)

LOCATOR = "asdfg - "

class MainPage(webapp2.RequestHandler):
    def get(self):
        task = taskqueue.Task(
                url='/api/task_handler',
                params={'from_module': module,
                        'from_version': version,
                        'from_hostname': hostname}

            )
        queue = taskqueue.Queue('task-queue')
        queue.add(task)
        msg = LOCATOR + "Task enqueued in "
        self.response.write(msg + where_html)
        logging.debug(msg + where)     

class TaskHandler(webapp2.RequestHandler):
  def post(self):
    msg = LOCATOR + "Task completed in "
    self.response.write(msg + where_html)
    logging.debug(msg + where)     
  
  def get(self):
    msg = LOCATOR + "Task should be POSTed! and should be handled in "
    self.response.write(msg + where_html)
    logging.debug(msg + where)     

application = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/api/task_handler', handler=TaskHandler), 
], debug=True)

