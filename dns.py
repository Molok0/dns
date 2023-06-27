import socket
import dnslib
from collections import defaultdict

from dns_cache import DNSCache

PORT = 53


class DNSServer:
    def __init__(self, server, cache_path):
        self.port = PORT
        self.server = server
        self.cache_path = cache_path
        self.dns_cache = DNSCache(cache_path)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', self.port))
            while True:
                try:
                    data, address = s.recvfrom(1024)
                    server_response = self.accept_request(data)
                    s.sendto(server_response, address)
                except ConnectionError as e:
                    print(f"Connection Error: {e}")

                except socket.gaierror as e:
                    print(f"Socket Error: {e}")

                except Exception as e:
                    print(f"Exception: {e}")

    def accept_request(self, data):
        try:
            dns_request = dnslib.DNSRecord.parse(data)
            qname, qtype = dns_request.q.qname, dns_request.q.qtype
            record_cache = self.dns_cache.get_response((qname, qtype))

            if record_cache is not None:
                print(f'Запрос {qname} обработан из кэша')
                response = dnslib.DNSRecord(header=dns_request.header)
                response.add_question(dns_request.q)
                response.rr.extend(record_cache)
                return response.pack()

            dns_response = dns_request.send(self.server, 53, timeout=4)
            dns_response = dnslib.DNSRecord.parse(dns_response)

            if dns_response.header.rcode != dnslib.RCODE.NOERROR:
                print(f'Ошибка обработки запроса {qname} {qtype}')
                return None

            records = (dns_response.rr, dns_response.auth, dns_response.ar)
            record_dict = defaultdict(list)

            for record in records:
                for rr in record:
                    record_key = (rr.rname, rr.rtype)
                    record_dict[record_key].append(rr)
                    self.dns_cache.put_answer(
                        record_key, record_dict[record_key], rr.ttl)

            print(f'Запрос {qname} {qtype} обработан')
            return dns_response.pack()
        except Exception as e:
            print(f'Ошибка обработки запроса: {e}')
            return None
