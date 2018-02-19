import socket
import random
import time
import sys
import select


def traceroute(addy):
	ttl = 1
	hops = 30
	packets = 0
	# The icmp protocol does not use a port, but it expects it - so just give it a dummy port
	port = 33435

	try: 
		ip = socket.gethostbyname(addy)
	except socket.error as e:
		raise IOError('Unable to resolve {}: {}', addy, e)

	print('traceroute to {} ({}), {} hops max'.format(addy, ip, hops))
	completionTime = 0

	while True:
		end = None
		start = time.time()

		#creates reciver socket
		rs = socket.socket(
			family=socket.AF_INET,
			type=socket.SOCK_RAW,
			proto=socket.IPPROTO_ICMP
		)

		try:
			rs.bind(('', port))
		except socket.error as e:
			raise IOError('Unable to bind reciever socket: {}'.format(e))

		receiver = rs

		#creates sender socket
		ss = socket.socket(
			family=socket.AF_INET,
			type=socket.SOCK_DGRAM,
			proto=socket.IPPROTO_UDP
		)
		ss.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

		sender = ss
		sender.sendto(b'', (addy, port))

		addr = None

		#for timeout so it does not hang on recv
		receiver.setblocking(0)
		ready = select.select([receiver], [], [], 5)
		try:
			if ready[0]:
				data, addr = receiver.recvfrom(1024)
			else:
				continue
		except socket.error:
			raise IOError('Socket error - {}'.format(e))
		finally:
			end = time.time()
			receiver.close()
			sender.close()

		hostname = lookup(addr[0])
		totalTime = int(round((end-start) * 1000))
		completionTime += totalTime
		
		if addr:
			print('{:<4} {} ({}) {}ms'.format(ttl, hostname[0], addr[0], totalTime))
		else:
			print('{:<4} *'.format(ttl))

		ttl += 1

		if addr[0] == ip or ttl > hops:
			break

	print('total completetion time: {}ms'.format(completionTime))

def lookup(adr):
	try:
		return socket.gethostbyaddr(adr)
	except socket.herror:
		return '<no DNS entry>', None, None		


#getting input from command line
x = traceroute(sys.argv[1])
