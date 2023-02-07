#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
    
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #parse url
        #Format: https://docs.python.org/3/library/urllib.parse.html#url-parsing
        url_parsed_list = urlparse(url) 
        scheme = url_parsed_list[0]
        netloc = url_parsed_list[1]
        path = url_parsed_list[2]
        if path[-1:] != '/':
            path += '/'
        
        #Connecting
        #host = "127.0.0.1"
        #host = str(url_parsed_list[1])
        host = url_parsed_list[1]
        port = 80
        #check if : is in host
        
        if(':' in host):
            port = host[-4:]
            l = len(port)+1
            host = host[:-l]
            print(f"My port {port}") 

        
        print(f"My Host: {host} ")
        print(f"My Path: {path} ")
        remote_ip = socket.gethostbyname(host)
        self.connect(host, int(port))#change
        req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n"
        self.socket.send(req.encode())
        data = self.socket.recv(4096).decode()
        print(data)
        data_list = data.split()
        body_list = data.split('\r\n\r\n')
        real_body = body_list[1]
        #print(real_body)
        self.close()

        
        code = int(data_list[1])
        body = data+f"{path}"
        find_path = body.find(path)
        #print(f"This is my path {find_path}")
        #print("this is my code:",code)
        #print(f"This is my body: {body}")
        
        return HTTPResponse(code, body)

        '''
        #Get data      
        req = f"GET /{path} HTTP/1.1\r\n" 
        req += f"Host: {netloc}\r\n"
        req += f"Accept: text/html\r\n"
        req += f"Connection: keep-alive\r\n"
        req += f"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        self.sendall(req)

        #Receiving data
        data = self.recvall(self.socket) 
        data_list = data.split()
        print("This is code ",data_list[1])
        print(data)
        code = data_list[1]
        body = data

        self.close()
        
        return HTTPResponse(code, body) '''

    def POST(self, url, args=None):
        '''
        url_parsed_list = urlparse(url) 
        scheme = url_parsed_list[0]
        netloc = url_parsed_list[1]
        path = url_parsed_list[2]
        
        #Connecting
        self.connect('\www.google.com', 80)#change

        to_send = "<h1>KLYDE WAS HERE</h1>"
        #Get data      
        req = f"POST /{path} HTTP/1.1\r\n" 
        req += f"Host: {netloc}\r\n"
        req += f"Accept: text/html\r\n"
        req += f"Connection: keep-alive\r\n"
        req += f"Content-Type: application/x-www-form-urlencoded\r\n"
        req += f"Content-Length: {len(to_send)}\r\n\r\n"#only for post

        req += to_send

        self.sendall(req)

        #Receiving data
        data = self.recvall(self.socket) 
        data_list = data.split()
        print("This is code ",data_list[1])
        print(data)
        code = data_list[1]
        body = data
        
        return HTTPResponse(code, body) '''

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
