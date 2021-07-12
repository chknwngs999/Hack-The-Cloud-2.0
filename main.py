from gevent.pywsgi import WSGIServer
from flaskr.__init__ import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

#https://hack-the-cloud-20.ryanlee35.repl.co/