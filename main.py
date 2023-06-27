from arguments_parser import MyParser
from dns import DNSServer

if __name__ == '__main__':
    my_parser = MyParser("DNS")
    arguments = my_parser.parse_args()
    my_dns = DNSServer(arguments.server, arguments.path)
    try:
        my_dns.run()
    except KeyboardInterrupt:
        my_dns.dns_cache.save_cache()
