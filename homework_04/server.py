from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib #Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re


# If you need to add anything above here you should check with course staff first.
next_id = 3
sale = {"active": True, "message": "25% off every package"}
# global variable contains dummy data
contacts = [
    {"id": 0, "first": "John", "email": "john@hismail.com", "bookDate": "2023-11-05", "translator": "no", "choice": "personal"},
    {"id": 1, "first": "Jane", "email": "jane@theirmail.com", "bookDate": "2023-11-06", "translator": "yes", "choice": "family"},
    {"id": 2, "first": "Jing", "email": "jlang@theirmail.com", "bookDate": "2023-11-08", "translator": "yes", "choice": "VIP package"}
]

# function to create password protection
# use authentication for admin access
def authentication(headers):
    if "Authorization" in headers:
        auth_header = headers["Authorization"]
        if auth_header.startswith("Basic "):
            encoded = auth_header[6:]
            # check for empty password or username
            if encoded == None:
                return 401
            # Decode the base64 encoded credentials
            credentials = base64.b64decode(encoded).decode("utf-8")
            auth_username, auth_password = credentials.split(":", 1)
            if (auth_username == "admin") and (auth_password == "password"):
                return 200
            return 403
    return 401

# create an html table for contact log
def create_html_table(data):
    html_table = """<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Contactlog</title>
            <link id="css-mode" rel="stylesheet" href="/main.css">
            <script src="/js/main.js"></script>
            <script src="/js/table.js"></script>
        </head>
        <body>
            <div class="topNav">
                <div>
                    <a href="/main">Home</a>
                </div>
                <div>
                    <a href="/testimonies">Testimonials</a>
                </div>
                <div>
                    <a href="/contact">Contact Us</a>
                </div>
                <div>
                    <a href="/admin/contactlog">Contacts</a>
                </div>
                <div>
                    <a id="dark-light">Dark Mode</a>
                </div>
            </div>
            <div class="sale-section">
                <label for="input-sale">Set sale text</label>
                <input type="text" name="input-sale" id="input-sale">
                <br>
                <button id="set-sale">Set sale</button>
                <button id="end-sale">End sale</button>
            </div>
            <h1>My Contact List</h1>
            <h2 id="sale-change"></h2>
            <table id="contact-table">
                <tr>
                    <th>Name</th>
                    <th>Email</th>   
                    <th>Scheduled Date</th>
                    <th>Translator</th>
                    <th>Option</th>
                    <th>Remove Contact</th>
                </tr>"""

    # extract all data in the contact list
    for row in data:
        html_table += f'<tr id="{row["id"]}">'
        html_table += f'<td>{row["first"]}</td><td>'
        html_table += f'<a href="mailto:{row["email"]}">'
        html_table += f'{row["email"]}</a></td>'
        html_table += f'<td class="appointment-date">{row["bookDate"]}</td>'
        html_table += f'<td>{row["translator"]}</td>'
        html_table += f'<td>{row["choice"]}</td>'
        html_table += '<td><button>Remove</button>'
        html_table += "</tr>"
    html_table += "</table></body></html>"
    return html_table

confirm_html = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Contactlog</title>
            <link id="css-mode" rel="stylesheet" href="/main.css">
            <script src="/js/main.js"></script>
        </head>
        <body>
            <div class="topNav">
                <div>
                    <a href="/main">Home</a>
                </div>
                <div>
                    <a href="/testimonies">Testimonials</a>
                </div>
                <div>
                    <a href="/contact">Contact Us</a>
                </div>
                <div>
                    <a href="/admin/contactlog">Contacts</a>
                </div>
                <div>
                    <a id="dark-light">Dark Mode</a>
                </div>
            </div>
            <h1>Schedule an Appointment</h1>
            <h2>Schedule Confirmed!</h2>
        </body>
        """
    
unsuccess_html = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Contactlog</title>
            <link id="css-mode" rel="stylesheet" href="/main.css">
            <script src="/js/main.js"></script>
        </head>
        <body>
            <div class="topNav">
                <div>
                    <a href="/main">Home</a>
                </div>
                <div>
                    <a href="/testimonies">Testimonials</a>
                </div>
                <div>
                    <a href="/contact">Contact Us</a>
                </div>
                <div>
                    <a href="/admin/contactlog">Contacts</a>
                </div>
                <div>
                    <a id="dark-light">Dark Mode</a>
                </div>
            </div>
            <h1>Schedule an Appointment</h1>
            <h2>Oops! Something Went Wrong!<br>Unable to schedule appointment!</h2>
        </body>
        """

# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
def server(method: str, url: str, body: Optional[str], headers: dict[str, str]) ->tuple[Union[str, bytes], int, dict[str, str]]:
    """
    method will be the HTTP method used, for our server that's GET, POST, DELETE
    url is the partial url, just like seen in previous assignments
    body will either be the python special None (if the body wouldn't be sent)
    or the body will be a string-parsed version of what data was sent.
    headers will be a python dictionary containing all sent headers.
    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in
    the example below.
    """
    # add global id
    global next_id
    global sale
    # Parse URL -- this is probably the best way to do it. Delete if you want.
    url, *parameters = url.split("?", 1)
    path = urllib.parse.unquote(url)
    # And another freebie -- the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now?]
    # I am sorry that you're going to have to do a bunch of boring refactoring.
    if method == "GET" and (path == "/" or path == "/main"):
        return open("static/html/mainpage.html").read(), 200, {"Content-Type": "text/html"}
    elif method == "POST" and path == "/contact":
        # some garbage or incorrect format for POST request
        if "?" not in body:
            return unsuccess_html, 400, {"Content-Type": "text/html"}
        if body != "":
            # solve issue to display @ character in email(s)
            body = urllib.parse.unquote(body)
            key_value_pairs = body.split("&")
            # Create a dictionary to store the extracted key-value pairs
            extracted_data = {}

            # check if translator key exist
            translator_exist = False
            #add id to data
            extracted_data["id"] = next_id
            next_id = next_id + 1
            # Loop through the key-value pairs and split them into keys and values
            for pair in key_value_pairs:
                key, value = pair.split("=", 1)
                if key == "" or key == "&":
                    return unsuccess_html, 400, {"Content-Type": "text/html"}
                if (key != "first") and (key != "last") and (key != "bookDate") and (key != "email") and (key != "translator"):
                    return unsuccess_html, 400, {"Content-Type": "text/html"}
                if key == "translator":
                    translator_exist = True
                # store in temporary dictionary
                extracted_data[key] = value
            if translator_exist == False:
                extracted_data["translator"] = "no"
            if (extracted_data["translator"] == "on"):
                extracted_data["translator"] = "yes"

            # check for missing information
            if (extracted_data["first"] == "") or (extracted_data["last"] == ""):
                return unsuccess_html, 400, {"Content-Type": "text/html"}
            elif (extracted_data["email"] == "") or (extracted_data["bookDate"] == ""):
                return unsuccess_html, 400, {"Content-Type": "text/html"}
            elif ("&" in extracted_data["first"]) or ("&" in extracted_data["last"]):
                return unsuccess_html, 400, {"Content-Type": "text/html"}
            elif ("&" in extracted_data["email"]) or ("&" in extracted_data["bookDate"]):
                return unsuccess_html, 400, {"Content-Type": "text/html"}
            else:
                contacts.append(extracted_data)
                return confirm_html, 201, {"Content-Type": "text/html"}
    elif method == "GET" and path == "/contact":
        return open("static/html/contactform.html").read(), 200, {"Content-Type": "text/html"}
    elif method == "GET" and path == "/testimonies":
        return open("static/html/testimonies.html").read(), 200, {"Content-Type": "text/html"}
    elif method == "GET" and path == "/main.css":
        return open("static/css/main.css").read(), 200, {"Content-Type": "text/css"}
    elif method == "GET" and path == "/main.dark.css":
        return open("static/css/main.dark.css").read(), 200, {"Content-Type": "text/css"}
    elif method == "GET" and path == "/js/table.js":
        return open("static/js/table.js").read(), 200, {"Content-Type": "text/javascript"}
    elif method == "GET" and path == "/js/contact.js":
        return open("static/js/contact.js").read(), 200, {"Content-Type": "text/javascript"}
    elif method == "GET" and path == "/js/main.js":
        return open("static/js/main.js").read(), 200, {"Content-Type": "text/javascript"}
    elif method == "GET" and path == "/images/main":
        return open("static/images/angkor.jpeg", "rb").read(), 200, {"Content-Type": "image/jpeg"}
    elif method == "GET" and path == "/api/sale":
        # get current sale, return a JSON object
        if ("active" in sale) and (sale["active"] == True):
            response = json.dumps(sale, indent=3)
        else:
            response = json.dumps({"active": False})
        return response, 200, {"Content-Type": "application/json"}
    
    # paths that need to verify admin login
    elif method == "GET" and path == "/admin/contactlog":
        if authentication(headers) == 200:
            temp_file = create_html_table(contacts)
            return temp_file, 200, {"Content-Type": "text/html"}
        
        if authentication(headers) == 401:
            return "Unauthorized Access!", 401, {"Content-Type": "text/plain", "WWW-Authenticate": 'Basic realm="User Visible Realm"'}
        if authentication(headers) == 403:
            return "Incorrect password or username!", 403, {"Content-Type": "text/plain"}

    # remove contact(s) from contact list 
    elif method == "DELETE" and path == "/api/contact":
        if authentication(headers) == 200:
            body = json.loads(body)
            if not headers["Content-Type"] == "application/json":
                return "body is not a json file!", 400, {"Content-Type": "text/plain"}
            else:
                try:
                    if "id" not in body:
                        return "ID required!", 400, {"Content-Type": "text/plain"}
                    else:
                        for contact in contacts:
                            if contact["id"] == body["id"]:
                                contacts.remove(contact)
                                return "Request ok", 200, {"Content-Type": "text/plain"}
                        return "ID does not exist!", 404, {"Content-Type": "text/plain"}
                except:
                    return "Invalid body!", 400, {"Content-Type": "text/plain"}
        if authentication(headers) == 401:
            return "Unauthorized Access!", 401, {"Content-Type": "text/plain", "WWW-Authenticate": 'Basic realm="User Visible Realm"'}
        if authentication(headers) == 403:
            return "Incorrect password or username!", 403, {"Content-Type": "text/plain"}
                
    # post request for sale
    elif method == "POST" and path == "/api/sale":
        if authentication(headers) == 200:
            # set current sale, takes in a JSON object
            response = json.loads(body)
            if not headers["Content-Type"] == "application/json":
                return "body is not a json file!", 400, {"Content-Type": "text/plain"}
            elif "message" not in response:
                return "body does not have sale text!", 400, {"Content-Type": "text/plain"}
            else:
                sale = {"active": True, "message": response["message"]}
                response = json.dumps(sale, indent=3)
                return response, 200, {"Content-Type": "text/plain"}
            
        if authentication(headers) == 401:
            return "Unauthorized Access!", 401, {"Content-Type": "text/plain", "WWW-Authenticate": 'Basic realm="User Visible Realm"'}
        if authentication(headers) == 403:
            return "Incorrect password or username!", 403, {"Content-Type": "text/plain"}
            
    # delete api
    elif method == "DELETE" and path == "/api/sale":
        if authentication(headers) == 200:
            # remove current sale, takes no input
            sale = {"active": False}
            response = json.dumps(sale, indent=3)
            return response, 200, {"Content-Type": "application/json"}
        
        if authentication(headers) == 401:
            return "Unauthorized Access!", 401, {"Content-Type": "text/plain", "WWW-Authenticate": 'Basic realm="User Visible Realm"'}
        if authentication(headers) == 403:
            return "Incorrect password or username!", 403, {"Content-Type": "text/plain"}

    return open("static/html/404.html").read(), 404, {"Content-Type": "text/html"}

# You shouldn't need to change content below this. It would be best if you just left it alone.
class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body
    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)
        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        # Send the file.
        self.wfile.write(message)
    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        try:
            # Step 2: handle it.
            message, response_code, headers = server("POST", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server("GET", self.path, None, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        try:
            # Step 2: handle it.
            message, response_code, headers = server("DELETE", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
