from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/hello'):
				self.send_response(200) #successful GET request
				self.send_header('Content-type', 'text/html')
				self.end_headers() 

				output = ""
				output += "<html><body>Hi there.</body></html>"
				self.wfile.write(output)
				print(output) #not required	
				return
		except IOError:
			self.send_error(404, "File not found for ", self.path)


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