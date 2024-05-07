from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, and a second function for generating the contact log page html.

# global variable contains dummy data
contacts = [
    {"first": "John", "email": "john@hismail.com", "bookDate": "2023-11-05", "translator": "no", "choice": "personal"},
    {"first": "Jane", "email": "jane@theirmail.com", "bookDate": "2023-11-06", "translator": "yes", "choice": "family"},
    {"first": "Jing", "email": "jlang@theirmail.com", "bookDate": "2023-11-08", "translator": "yes", "choice": "VIP package"}
]

# parse url and store data in contact list
def parse_url(url, data):
    parsed_url = urllib.parse.urlparse(url)
    query_parameters = urllib.parse.parse_qs(parsed_url.query)
    
    name = query_parameters.get("first", [None])[0]
    email = query_parameters.get("email", [None])[0]
    date = query_parameters.get("bookDate", [None])[0]
    translator = query_parameters.get("translator", [None])[0]
    option = query_parameters.get("choice", [None])[0]
    
    # solve to display yes/no instead of on/None
    if (translator) == "on":
        translator = "yes"
    else:
        translator = "no"
    if name == None or email == None or date == None or option == None:
        return data
    # Create a contact dictionary from the collected data in url
    contact = {
        "first": name,
        "email": email,
        "bookDate": date,
        "translator": translator,
        "choice": option
    }
    
    # Add the contact to the global contacts list
    data.append(contact)
    return data

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
            <h1>My Contact List</h1>
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
        html_table += "<tr>"
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

def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?
    name=joe` then the `url` parameter will have the value "/contact?name=joe".
    (so the schema and authority will not be included, but the full path, any query, and any anchor
    will be included) This function is called each time another program/computer makes a request to
    this website. The URL represents the requested file. This function should return three values 
    (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    #YOUR CODE GOES HERE!
    decoded_url = urllib.parse.unquote(url)
    parsed_url = urllib.parse.urlparse(decoded_url)
    path = parsed_url.path

    if path == "/" or path == "/main":
        return open("static/html/mainpage.html").read(), "text/html", 200
    elif path == "/contact":
        # if "?" in url:
        #     parse_url(url, contacts)
        return open("static/html/contactform.html").read(), "text/html", 200
    elif path == "/testimonies":
        return open("static/html/testimonies.html").read(), "text/html", 200
    elif path == "/main.css":
        return open("static/css/main.css").read(), "text/css", 200
    elif path == "/admin/contactlog":
        temp_file = create_html_table(contacts)
        return temp_file, "text/html", 200
    elif path == "/main.dark.css":
        return open("static/css/main.dark.css").read(), "text/css", 200
    elif path == "/js/table.js":
        return open("static/js/table.js").read(), "text/javascript", 200
    elif path == "/js/contact.js":
        return open("static/js/contact.js").read(), "text/javascript", 200
    elif path == "/js/main.js":
        return open("static/js/main.js").read(), "text/javascript", 200
    elif path == "/images/main":
        return open("static/images/angkorWatt.jpeg", "rb").read(), "image/jpeg", 200
    else:
        return open("static/html/404.html").read(), "text/html", 404
    
def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)
    This function is called each time another program/computer makes a POST request
    to this website. This function should return three values (string or bytes, string, int) in a
    list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """

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

    decoded_url = urllib.parse.unquote(url)
    parsed_url = urllib.parse.urlparse(decoded_url)
    path = parsed_url.path
        
    if path != "/contact":
        return open("static/html/404.html").read(), "text/html", 404
    
    # split each key-value pair
    key_value_pairs = body.split("&")
    # Create a dictionary to store the extracted key-value pairs
    extracted_data = {}

    # Loop through the key-value pairs and split them into keys and values
    for pair in key_value_pairs:
        key, value = pair.split("=")
        # store in temporary dictionary
        extracted_data[key] = value

    # check for missing information
    if (extracted_data["first"] == "") or (extracted_data["last"] == ""):
        return unsuccess_html, "text/html", 400
    elif (extracted_data["email"] == "") or (extracted_data["bookDate"] == ""):
        return unsuccess_html, "text/html", 400
    else:
        parse_url(url+"?"+body, contacts)
        return confirm_html, "text/html", 201

# You shouldn't need to change content below this. It would be best if you just left it alone.
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get('Content-Length',0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        # Send the file.
        self.wfile.write(message)
        return
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        # Send the file.
        self.wfile.write(message)
        return
def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
