# runsslserver.py

from django.core.management.commands.runserver import Command as RunServerCommand
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
import ssl

class Command(RunServerCommand):
    def get_handler(self, *args, **options):
        handler = super().get_handler(*args, **options)
        cert_path = options['certificate']
        key_path = options['key']
        server_address = options['addrport']
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert_path, key_path)
        return WSGIServer(server_address, WSGIRequestHandler, ssl_context=ssl_context, ipv6=False)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--certificate', default="C:\Windows\System32\cert.pem", help='Path to the SSL certificate file')
        parser.add_argument('--key', default="C:\Windows\System32\key.pem", help='Path to the SSL private key file')


