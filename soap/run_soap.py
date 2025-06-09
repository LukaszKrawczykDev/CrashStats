from wsgiref.simple_server import make_server
from soap_service import soap_wsgi_app

if __name__ == "__main__":
    server = make_server("0.0.0.0", 8001, soap_wsgi_app)
    print("⚙️ SOAP service listening on http://0.0.0.0:8001")
    server.serve_forever()