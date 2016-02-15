#!/usr/bin/env python3
import http.server
import socketserver
import json
from urllib.parse import parse_qsl as parse_query, urlparse as parse_url

def run_server(info, port):
	response_cache = {}
	class MyHandler(http.server.SimpleHTTPRequestHandler):
		def respond(self, content, content_type='application/json', code=200):
			self.send_response(code)
			self.send_header("Content-type", content_type)
			self.end_headers()
			self.wfile.write(bytes(json.dumps(content), 'UTF-8'))
	
		def not_implemented(self):
			self.respond({'error':'{} not implemented'.format(self.path)}, code=404)
	
		def not_found(self, key = False):
			key = key or self.path
			self.respond({'error': key + ' not found'}, code=404)
	
		def do_GET(self):
			request = parse_url(self.path).path.split('/')[1]
			query_vars = dict(parse_query(parse_url(self.path).query))

			try:
				if self.path not in response_cache:
					info_getter = getattr(info, 'get_' + request)
					response_cache[self.path] = info_getter(**query_vars)
				self.respond(response_cache[self.path])
			except AttributeError:
				self.not_found()
			except NotImplementedError:
				self.not_implemented()
			# todo: KeyError -> 404(key)

	httpd = socketserver.TCPServer(("", port), MyHandler)
	print("serving at port", port)
	httpd.serve_forever()
