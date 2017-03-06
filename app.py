# encoding: utf-8
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from string import Template
import nexmo
import json

mynumber = os.environ['MY_NUMBER'] #Where you want the callers to be connected to
mylvn = os.environ['MY_LVN'] # Your Nexmo number, used as the CLI to both parties
if os.getenv('NAME'):
    url = os.getenv('NAME') + '.herokuapp.com' 
else:
    url = os.environ['URL']
application_id = os.environ['APP_ID'] # Application ID returned by the nexmo cli when you create the applicaiton
try:
    private_key = os.environ['PRIVATE_KEY']
except:
    with open('private.key', 'r') as f:
        PRIVATE_KEY = f.read()


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        html = 'static/index.html'
        with open(html, 'rb') as f:
            data = f.read()
        self.write(data)
        self.set_header("Content-Type", 'text/html')
        self.finish()


class CallHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
		data = json.loads(self.request.body)
		client = nexmo.Client(application_id=application_id, private_key=private_key, key='dummy', secret='dummy') #Dummy values for key and secret as the lib requires them even though they are not used
		request = {
		  'to': [{'type': 'phone', 'number': mynumber}],
		  'from': {'type': 'phone', 'number': mylvn},
		  'answer_url': ['https://{}/ncco?name={}&number={}'.format(url, data['name'], data['number'])]
		}
		print request
		response = client.create_call(request)
		self.write(response)
		self.finish()


class NCCOHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
		data={}
		data['name'] = self.get_argument('name')
		data['number'] = self.get_argument('number')
		data['url'] = url
		data['lvn'] = mylvn
		filein = open('ncco.json')
		src = Template(filein.read())
		filein.close()
		ncco = json.loads(src.substitute(data))
		self.write(json.dumps(ncco))
		self.set_header("Content-Type", 'application/json')
		self.finish()


def main():
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    print static_path
    application = tornado.web.Application([(r"/", MainHandler),
                                           (r"/call", CallHandler),
										   (r"/ncco", NCCOHandler),
                                           (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
                                           ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
