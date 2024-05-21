from pysnmp.hlapi import *
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='temperature')

community_string = 'public'
oids = [ObjectType(ObjectIdentity('1.3.6.1.2.1.25.1.5.0'))]  

def get_temperature(host):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(community_string),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              *oids):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                 errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                temperature = varBind[-1]
                channel.basic_publish(exchange='',
                                      routing_key='temperature',
                                      body=f'Temperature: {temperature} for host {host}')
                print(f'Temperature: {temperature} recorded for host {host}')

with open('hosts.conf', 'r') as file:
    hosts = file.readlines()

hosts = [host.strip().split(':') for host in hosts]

ip_addresses = [host[1] for host in hosts]

for ip_address in ip_addresses:
    get_temperature(ip_address)
