#!/usr/bin/env python3

import pika
import subprocess

with open('hosts.conf') as f:
    hosts = f.readlines()

rabbitmq_host = 'localhost'
rabbitmq_exchange = 'temp_exchange'

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='direct', durable=True)

for host in hosts:
    host = host.strip()
    if host and not host.startswith('#') and ':' in host:
        name, ip = host.split(':')
        
        result = subprocess.run(['snmpget', '-v2c', '-c', 'public', ip, 'snmp.sys.uptime.value'], capture_output=True, text=True)
        temperature = result.stdout.split(' ')[-1].strip()
        
        channel.basic_publish(exchange=rabbitmq_exchange, routing_key=name, body=temperature)
        print(f"Published temperature for {name} ({ip}): {temperature}")
    else:
        print(f"Invalid host entry: {host}")

connection.close()
