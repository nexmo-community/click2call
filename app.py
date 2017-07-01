# encoding: utf-8
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from string import Template
import nexmo
import json


class NexmoConfig(object):

    def __init__(self):
        try:
            from dotenv import load_dotenv, find_dotenv
            load_dotenv(find_dotenv())
        except:
            pass  # python-dotenv not installed

        try:
            self.MY_NUMBER = os.environ['MY_NUMBER']
            self.MY_LVN = os.environ['MY_LVN']
            self.APP_ID = os.environ['APP_ID']
            self.URL = self._get_url()
            self.PRIVATE_KEY = self._get_private_key()
        except KeyError:
            raise Exception("Missing required Nexmo config variable")

    @staticmethod
    def _get_url():
        try:
            return "{name}.herokuapp.com".format(
                name=os.environ['NAME']
            )
        except:
            return os.environ['URL']

    @staticmethod
    def _get_private_key():
        try:
            return os.environ['PRIVATE_KEY']
        except:
            with open('private.key', 'r') as f:
                private_key = f.read()

            return private_key


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        html = 'templates/index.html'

        with open(html, 'rb') as f:
            data = f.read()

        self.write(data)
        self.set_header("Content-Type", 'text/html')
        self.finish()


class CallHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.config = NexmoConfig()
        super(CallHandler, self).__init__(*args, **kwargs)

    @tornado.web.asynchronous
    def post(self):
        data = json.loads(self.request.body)

        client = nexmo.Client(
            application_id=self.config.APP_ID,
            private_key=self.config.PRIVATE_KEY,
            # Dummy values for key and secret as the lib requires them even though they're not used
            key='dummy',
            secret='dummy'
        )

        request = {
            'to': [{'type': 'phone', 'number': self.config.MY_NUMBER}],
            'from': {'type': 'phone', 'number': self.config.MY_LVN},
            'answer_url': ['https://{url}/ncco?name={name}&number={number}'.format(
                url=self.config.URL,
                name=data['name'],
                number=data['number']
            )]
        }

        response = client.create_call(request)

        self.write(response)
        self.finish()


class NCCOHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.config = NexmoConfig()
        super(NCCOHandler, self).__init__(*args, **kwargs)

    @tornado.web.asynchronous
    def get(self):
        data = {
            'name': self.get_argument('name'),
            'number': self.get_argument('number'),
            'url': self.config.URL,
            'lvn': self.config.MY_LVN
        }

        filein = open('templates/ncco.json')
        src = Template(filein.read())
        filein.close()

        ncco = json.loads(src.substitute(data))

        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json')
        self.finish()


def main():
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    application = tornado.web.Application([
        (r"/", MainHandler),
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
