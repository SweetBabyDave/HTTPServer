from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes

class CS2610Assn1(BaseHTTPRequestHandler):
    def do_GET(self):
        fileType = mimetypes.guess_type(self.path)

        if self.path[1:] in os.listdir():
            data = CS2610Assn1.openFile(self, self.path[1:])
            CS2610Assn1.do_HEAD(self, fileSize=len(data), fileType=fileType)
            self.wfile.write(data)

        elif self.path.startswith("/index") or self.path == "/":
            data = CS2610Assn1.openFile(self, "index.html")
            CS2610Assn1.do_HEAD(self, location="http://localhost:8000/index.html", code=301)
            self.wfile.write(data)

        elif self.path.startswith("/about") or self.path.startswith("/bio"):
            data = CS2610Assn1.openFile(self, "about.html")
            CS2610Assn1.do_HEAD(self, location="http://localhost:8000/about.html", code=301)
            self.wfile.write(data)

        elif self.path.startswith("/tips") or self.path.startswith("/help") or self.path.startswith("/techtips+css"):
            data = CS2610Assn1.openFile(self, "techtips+css.html")
            CS2610Assn1.do_HEAD(self, location="http://localhost:8000/techtips+css.html", code=301)
            self.wfile.write(data)

        elif self.path.startswith("/techtips-css"):
            data = CS2610Assn1.openFile(self, "techtips-css.html")
            CS2610Assn1.do_HEAD(self, location="http://localhost:8000/techtips-css.html", code=301)
            self.wfile.write(data)

        elif self.path.startswith("/plan"):
            data = CS2610Assn1.openFile(self, "plan.html")
            CS2610Assn1.do_HEAD(self, location="http://localhost:8000/plan.html", code=301)
            self.wfile.write(data)

        elif self.path == "/debugging":
            newline = "\n<li>"

            fileWrite = bytes(f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <link rel="stylesheet" href="style.css" type="text/css"/>
                    <title>template.html</title>
                </head>
                <body>
                    <h1>Debugging Page</h1>
                    <h2>A Quick Look At the Nitty Gritty</h2>
                    <ul>
                        <li>Server's version string - {self.server_version + " " + self.sys_version}</li>
                        <li>Server's current date and time - {CS2610Assn1.date_time_string(self)}</li>
                        <li>Client's IP address - {CS2610Assn1.address_string(self)}</li>
                        <li>Client's port number - {self.client_address[1]}</li>
                        <li>Requested path - {self.path}</li>
                        <li>HTTP request type - {self.command}</li>
                        <li>HTTP version of request - {self.request_version}</li>
                    </ul>

                    <h2>List of HTTP Request Headers</h2>
                    <ol>
                        {"<li>" + newline.join(f"{header}: {value}</li>" for header, value in self.headers.items())}
                    </ol>
                <p> If you are done checking out this page go and check out the <a href="index.html">home</a> page!
                </body>
            </html>""", encoding="utf8")

            CS2610Assn1.do_HEAD(self, fileSize=len(fileWrite), fileType="text/html")
            self.wfile.write(fileWrite)

        elif self.path == "/teapot":
            CS2610Assn1.do_HEAD(self, fileType="text/html", code=418)
            self.wfile.write(bytes(f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <link rel="stylesheet" href="style.css" type="text/css"/>
                    <title>template.html</title>
                </head>
                <body>
            		<h1>No Teapots here!</h1>
                    <p>Maybe if you look harder you will find a coffee pot. In the meantime, go check out the <a href="index.html">home</a> page</p>
                </body>
            </html>""", encoding="utf-8"))

        elif self.path == "/forbidden":
            CS2610Assn1.do_HEAD(self, fileType="text/html", code=403)
            self.wfile.write(bytes(f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <link rel="stylesheet" href="style.css" type="text/css"/>
                    <title>template.html</title>
                </head>
                <body>
            		<h1>You May Not Pass!</h1>
                    <p>It's dangerous to go alone, so while you're waiting for your sword, check out the <a href="index.html">home</a> page!</p>
                </body>
            </html>""", encoding="utf-8"))

        else:
            CS2610Assn1.do_HEAD(self, fileType="text/html", code=404)
            self.wfile.write(bytes(f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <link rel="stylesheet" href="style.css" type="text/css"/>
                    <title>template.html</title>
                </head>
            
                <body>
                    <h1>Page Not Found</h1>
                    <p>You asked for a webpage named {self.path}, and it just isn't there. Instead, go check out the <a href="index.html">home</a> page!</p>
                </body>
            </html>""", encoding="utf-8"))

    def do_HEAD(self, fileSize=None, fileType=None, location=None, code=200):
        CS2610Assn1.send_response(self, code)
        CS2610Assn1.send_header(self, "Connection", "close")
        CS2610Assn1.send_header(self, "Cache-Control", "max-age=30")

        if code == 403 or code == 404 or code == 418 or code == 200:
            CS2610Assn1.send_header(self, "Content-Type", f"{fileType}")
            if code == 200:
                CS2610Assn1.send_header(self, "Content-Length", f"{fileSize}")
        elif code == 301:
            CS2610Assn1.send_header(self, "Location", f"{location}")

        CS2610Assn1.end_headers(self)

    def openFile(self, file):
        file = open(file, "rb")
        data = file.read()
        file.close()
        return data

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, CS2610Assn1).serve_forever()
    except KeyboardInterrupt:
        print("Exiting")
        exit(0)

