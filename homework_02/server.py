from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, and a second function for generating the contact log page html.

# global variable contains dummy data
contacts = [
    {"first": "John", "email": "john@hismail.com", "bookDate": "2023-10-05", "translator": "no", "choice": "personal"},
    {"first": "Jane", "email": "jane@theirmail.com", "bookDate": "2023-10-06", "translator": "yes", "choice": "family"},
    {"first": "Jing", "email": "jlang@theirmail.com", "bookDate": "2023-10-08", "translator": "yes", "choice": "VIP package"}
]

# parse url and store data in contact list
def parse_url(url, data):
    parsed_url = urllib.parse.urlparse(url)
    query_parameters = urllib.parse.parse_qs(parsed_url.query)
    
    name = query_parameters.get("first")[0]
    email = query_parameters.get("email")[0]
    date = query_parameters.get("bookDate")[0]
    translator = query_parameters.get("translator", [None])[0]
    option = query_parameters.get("choice")[0]
    
    # solve to display yes/no instead of on/None
    if (translator) == "on":
        translator = "yes"
    else:
        translator = "no"

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

# create an html table for contact log
def create_html_table(data):
    html_table = """<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Contactlog</title>
            <link rel="stylesheet" href="/css">
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
            </div>
            <h1>My Contact List</h1>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Email</th>   
                    <th>Scheduled Date</th>
                    <th>Translator</th>
                    <th>Option</th>
                </tr>"""

    # extract all data in the contact list
    for row in data:
        html_table += "<tr>"
        html_table += f'<td>{row["first"]}</td><td>'
        html_table += f'<a href="mailto:{row["email"]}">'
        html_table += f'{row["email"]}</a></td>'
        html_table += f'<td>{row["bookDate"]}</td>'
        html_table += f'<td>{row["translator"]}</td>'
        html_table += f'<td>{row["choice"]}</td>'
        html_table += "</tr>"
    html_table += "</table></body></html>"
    return html_table

def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
    """
    #YOUR CODE GOES HERE!
    
    decoded_url = urllib.parse.unquote(url)
    parsed_url = urllib.parse.urlparse(decoded_url)
    path = parsed_url.path

    if path == "/" or path == "/main":
        return open("static/html/mainpage.html").read(), "text/html"
    elif path == "/contact":
        if "?" in url:
            parse_url(url, contacts)
        return open("static/html/contactform.html").read(), "text/html"
    elif path == "/testimonies":
        return open("static/html/testimonies.html").read(), "text/html"
    elif path == "/css":
        return open("static/css/main.css").read(), "text/css"
    elif path == "/admin/contactlog":
        temp_file = create_html_table(contacts)
        return temp_file, "text/html"
    elif path == "/images/main":
        return open("static/images/angkorWatt.jpeg", "rb").read(), "image/jpeg"
    else:
        return open("static/html/404.html").read, "text/html"

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = server(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
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
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
