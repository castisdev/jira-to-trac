import simplejson as json
import pprint
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
#import xmlrpclib
import xmlrpc.client


trac_url = '172.16.33.2:8080/trac'
user = 'user'
password = 'password'
cc = 'cc'

class postRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		content_length = self.headers['Content-Length']
		if content_length:
			content_length = int(content_length)
			self.send_response(200)
			self.end_headers()
			body = self.rfile.read(content_length)
			post_data = json.loads(body)
			#print('Commit added with description: %s' % post_data["issue"]["fields"]["description"])
			#print('Commit added with due_date: %s' % post_data["issue"]["fields"]["duedate"])
			#print('Commit added with summary : %s' % post_data["issue"]["fields"]["summary"])
			#print('Commit added with reporter : %s' % post_data["issue"]["fields"]["reporter"]["displayName"])
			#print('Commit added with component : %s' % post_data["issue"]["fields"]["components"]["name"])
			#print('Commit added with owner : %s' % post_data["issue"]["fields"]["assignee"])
			
			trac_rpc_url = 'http://%s:%s@%s/login/rpc' % (user, password, trac_url)
			server = xmlrpc.client.ServerProxy(trac_rpc_url)
 
			description = post_data["issue"]["fields"]["description"]
			summary = post_data["issue"]["fields"]["summary"]
			reporter = post_data["issue"]["fields"]["reporter"]["displayName"]
			#owner = post_data["issue"]["fields"]["assignee"]
			
			ret = server.ticket.create(summary, description, {'component':'', 'type': '', 'due_date': '2015.1R(0102)', 'reporter': reporter, 'exp_duedate': '2015.1R(0102)', 'owner': 'jhahn', 'priority': '1', 'milestone':'', 'cc':cc, 'man_day':'', 'ex_man_day':''})
			print('ticket #%d [%s] created.' % (ret, server.ticket.get(ret)[3]['summary']))
		#else:
		#	self.send_error(404, 'File Not Found %s' % self.path)
		 
		return
		

 
		 
def run():
	server = HTTPServer(('', 8000), postRequestHandler)
	print('Server started')
	server.serve_forever()
		 
if __name__ == '__main__':
	run()
