from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import webbrowser

PORT = 8000

class GPSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "lat" in params and "lon" in params:
            lat = params["lat"][0]
            lon = params["lon"][0]

            print("\n✔ GPS LOCATION RECEIVED")
            print("Latitude :", lat)
            print("Longitude:", lon)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GPS location received. Check your terminal.")
        else:
            self.send_response(200)
            self.end_headers()

            html = """
            <html>
            <body onload="getLocation()">
            <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;

                            window.location.href = "/?lat=" + lat + "&lon=" + lon;
                        },
                        function(error) {
                            document.body.innerHTML = "GPS Error: " + error.message;
                        }
                    );
                } else {
                    document.body.innerHTML = "Geolocation Not Supported";
                }
            }
            </script>
            <h2>Fetching GPS… Allow location permission.</h2>
            </body>
            </html>
            """

            self.wfile.write(html.encode())

server = HTTPServer(("localhost", PORT), GPSHandler)
print(f"🌍 GPS Server running at http://localhost:{PORT}")
print("📌 Open this link in your browser to get GPS")
webbrowser.open(f"http://localhost:{PORT}")
server.serve_forever()
