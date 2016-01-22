
import logging
import webapp2

from google.appengine.api import taskqueue
from google.appengine.api.modules import modules

module = modules.get_current_module_name()
version = modules.get_current_version_name()
hostname = modules.get_hostname()
where = "__module=%s__version=%s__hostname=%s" %(module, version, hostname)

SEP = "__"
LOCATOR = "LAST_TESTS - "

skip_headers = ["X-Appengine-Country","Cache-Control","Content-Type","User-Agent","Accept","Accept-Language",
                "X-Appengine-Citylatlong","X-Appengine-Region", "X-Appengine-City", "X-Appengine-Default-Namespace",
                "X-Google-Apps-Metadata", "X-Zoo"]


def to_log(msg):
    return msg.replace(SEP, " ")


def to_html(msg):
    return msg.replace(SEP, "<br/>")


def headers(request):

    return SEP + "HEADERS" + SEP + SEP.join([k+ "->" + v for k,v in request.headers.iteritems() if k not in skip_headers])


def extra_info(request):

    return SEP + "REFERRER" + SEP + request.referrerSEP.join([k+ "->" + v for k,v in request.headers.iteritems() if k not in skip_headers])


class MainPage(webapp2.RequestHandler):
    def get(self):
        task = taskqueue.Task(
                url='/api/task_handler',
                params={'from_module': module,
                        'from_version': version,
                        'from_hostname': hostname},
                # this works as a workaround
                # headers={'Host':'apiversion.api.marcial-languages.appspot.com'}

            )
        queue = taskqueue.Queue('task-queue')
        queue.add(task)

        msg = LOCATOR + SEP + "REquest received in: " + where + SEP + SEP + headers(self.request)
        self.response.write(to_html(msg))
        logging.debug(to_log(msg))


class TaskHandler(webapp2.RequestHandler):

    def post(self):
        msg = LOCATOR + "Task completed in "+ where + SEP + SEP + headers(self.request)
        self.response.write(to_html(msg))
        logging.debug(to_log(msg))

    def get(self):
        msg = LOCATOR + "Task should be POSTed! and should be handled in "+ where + SEP + SEP + headers(self.request)
        self.response.write(to_html(msg))
        logging.debug(to_log(msg))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/api/task_handler', handler=TaskHandler),
], debug=True)

