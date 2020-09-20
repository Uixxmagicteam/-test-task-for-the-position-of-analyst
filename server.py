import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from DataProvider import DataProvider

data_provider = DataProvider()


def router(path: str) -> str:
    parsed = parse.urlparse(path)
    splited = parsed.path.split('/') # 0 index is for geonames
    query_args = parse.parse_qs(parsed.query)

    if splited[1] != 'geonames':
        return 'Unknown resource'

    if splited[2] == 'collection':
        return json.dumps(data_provider.get_page(query_args.get('page_size'), query_args.get('page')))

    if splited[2] == 'compare':
        return json.dumps(data_provider.compare_cities('Скрипково', 'Киров'))

    if splited[2]: # значит id, пример http://localhost:8080/geonames/451765
        return json.dumps(data_provider.get_by_id(splited[2]))

    return 'Unknown request'


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write(router(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')
