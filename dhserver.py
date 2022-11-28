from socket import *

# First 24 bits are part of the same subnet
DHCP_SERVER = ('192.168.0.1', 24)
DHCP_CLIENT = ('255.255.255.255', 67)

# Create a pool of addresses
IP_ADDRESS_POOL = [ '192.168.0.10',
					'192.168.0.11',
					'192.168.0.12',
					'192.168.0.13',
					'192.168.0.14',
					'192.168.0.15']

# Create packet
# def BuildPacket:


# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

# Recieve a UDP message
msg, addr = s.recvfrom(1024)

# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
for i in range(29, 34):
	print(":" + format(msg[i], 'x'), end = '')
print()

# Print client's DHCP Discover
print("Client's DHCP Discover is " , end = '')
for i,n in enumerate(msg):
	print(":" + format(msg[i], 'x'), end = '')
print()

# Send a UDP message (Broadcast)
s.sendto(b'Hello World!', DHCP_CLIENT)
