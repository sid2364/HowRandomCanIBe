import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_handler import getAllRestaurants, getNameOfRestaurantFromID, updateNameForID, createNew, deleteRestaurantFromID
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/hello'):
				self.send_response(200) #successful GET request
				self.send_header('Content-type', 'text/html')
				self.end_headers() 

				output = ""
				output += "<html><body>Hi there."
				output += "<form method='POST', enctype='multipart/form-data' " + \
				"action='/hello'><h2>What do you wanna say?<h2> " + \
				"<input name='message' type='text'><input type='submit' " + \
				"value='Submit'></form>"
				output += "</body></html>"

				self.wfile.write(output)
				print(output) #not required
				return
			if self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				
				output += "<a href='/restaurants/new'>Add a new restaurant</a>"

				restaurants = getAllRestaurants()
				for restaurant in restaurants:
					output += "<h2>%s</h2>" % restaurant.name
					output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id 
					output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
					output += "<br>"
				
				output += "</body></html>"
				print(output)
				self.wfile.write(output)
				return

			if self.path.endswith('/edit'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				id_r = self.path.split('/')[-2]
				print(self.path, id_r)
				# since URL is in the form of .../restaurants/<id>/edit/
				# and we need the second to last part
				
				try:
					res_name = getNameOfRestaurantFromID(id_r)
				except:
					print("ERROR")
					raise IOError
				
				output = ""
				output += "<html><body>"
				output += "<h2>Edit details about %s" % res_name
				output += "<form method='POST', enctype='multipart/form-data' " + \
				"action='/"+id_r+"/edit'><h2>What do you wanna change here?</h2> " + \
				"<input name='newname' type='text' placeholder='"+res_name+"'><input type='submit' " + \
				"value='Submit'></form>"

				output += "</body></html>"
				print(output)
				self.wfile.write(output)
				return

			if self.path.endswith('/delete'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				id_r = self.path.split('/')[-2]
				print(self.path, id_r)
				# since URL is in the form of .../restaurants/<id>/edit/
				# and we need the second to last part
				try:
					res_name = getNameOfRestaurantFromID(id_r)
				except:
					print("ERROR")
					raise IOError

				
				output = ""
				output += "<html><body>"
				output += "<h2>Sure about deleting %s?" % res_name
				output += "<form method='POST', enctype='multipart/form-data' " + \
				"action='/"+id_r+"/delete'><h2>Confirm</h2> " + \
				"<input type='submit' " + \
				"value='Submit'></form>"

				output += "</body></html>"
				print(output)
				self.wfile.write(output)
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h2>Add a new restaurant</h2>"
				output += "<form method='POST', enctype='multipart/form-data' " + \
				"action='/restaurants/new'><h3>Enter a restaurant name</h3> " + \
				"<input name='newname' type='text'><input type='submit' " + \
				"value='Submit'></form>"

				output += "</body></html>"
				print(output)
				self.wfile.write(output)
				return
		except IOError:
			self.send_error(404, "File not found: %s" % self.path)
	def do_POST(self): #override base class function
		try:
			if self.path.endswith("/hello"):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ''
				output += '<html><body>'
				output += '<h1>%s</h1>' % (messagecontent[0])

				output += "<form method='POST', enctype='multipart/form-data' " + \
					"action='/hello'><h2>What do you wanna say?<h2> " + \
					"<input name='message' type='text'><input type='submit' " + \
					"value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/edit"):
				self.send_response(301)
				self.end_headers()

				id_r = self.path.split('/')[-2]
				print(id_r)

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					newname = fields.get('newname')[0]

				updateNameForID(id_r, newname)

				output = ''
				output += '<html><body>'
				output += '<h1>Name updated to %s</h1>' % (newname)

				output += "<a href='/restaurants'>Back to the home page</a>"
				output += "</body></html>"
				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/delete"):
				self.send_response(301)

				id_r = self.path.split('/')[-2]
				print(id_r)

				deleteRestaurantFromID(id_r)

				self.send_header("Content-type", "text/html")
				self.send_header("Location", "/restaurants")
				self.end_headers()
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(301)
				#self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					newname = fields.get('newname')

				createNew(newname)

				self.send_header("Content-type", "text/html")
				self.send_header("Location", "/restaurants")
				self.end_headers()
				return
		except IOError:
			self.send_error(404, 'File not found: %s' % self.path)

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print("Web server running on port", port)
		server.serve_forever()
	except KeyboardInterrupt:
		print("Stopped serving")
		server.socket.close()

if __name__ == "__main__":
	main()

	'''
	For an actual project, create all the routes first. So there is a 
	"virtual" map of the entire website. Add structure first and then functionality.
	Once that is in place, move forward with building one functionality at a time,
	and only moving on the next one when the entire thing is completed.
	'''