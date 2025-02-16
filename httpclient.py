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
        data = data.split()

        return int(data[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
    
        return data.split("\r\n\r\n")[1]
    
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
        host = url_parsed_list.hostname
        path = url_parsed_list.path
        port = 80
        if path[-1:] != '/':
            path += '/'

        #Does it start with http?
        if url_parsed_list.scheme != 'http':
            return HTTPResponse(400, 'Bad Request') 

        #Handle args
        i = 0
        args_body = '?'
        if args != None:
            for x in args:        
                if i != 0:
                    args_body += f"&{x}={args[x]}"
                else:
                    args_body += f"{x}={args[x]}"
                i+=1 #Goes through if after first iteration

        #Append args as query params
        path += args_body
        
        if url_parsed_list.port:
            port = url_parsed_list.port


        #Connecting
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
        self.connect(host, int(port))
        req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {user_agent}\r\nAccept: text/html\r\nAccept-Language: en\r\nAccept-Endoding: gzip\r\nDNT: 1\r\nConnection: close\r\n\r\n"
        self.sendall(req)

        #Receiving
        data = self.recvall(self.socket)  
        

        code = self.get_code(data)
        body = self.get_body(data)
        self.close()
        return HTTPResponse(code, body)

        

    def POST(self, url, args=None):
        code = 200
        #parse url
        #Format: https://docs.python.org/3/library/urllib.parse.html#url-parsing
        url_parsed_list = urlparse(url) 
        host = url_parsed_list.hostname
        path = url_parsed_list.path
        port = 80
        if path[-1:] != '/':
            path += '/'
        
        #Does it start with http?
        if url_parsed_list.scheme != 'http':
            return HTTPResponse(400, 'Bad Request') 

        if url_parsed_list.port:
            port = url_parsed_list.port

        #Handling args
        args_body = ''
        i = 0
       
        if args != None:
            for x in args:        
                if i != 0:
                    args_body += f"&{x}={args[x]}"
                else:
                    args_body += f"{x}={args[x]}"
                i+=1 #Goes through if after first iteration

        #Content Length        
        args_length = len(args_body)
               

        #Connecting/Sending
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
        self.connect(host, int(port))
        req = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {user_agent}\r\nAccept: text/html\r\nAccept-Language: en\r\nAccept-Endoding: gzip\r\nDNT: 1\r\nContent-Length: {args_length}\r\nConnection: close\r\n\r\n{args_body}"
        self.sendall(req)

        #Receiving
        data = self.recvall(self.socket)    

        code = self.get_code(data)
        body = self.get_body(data)
        self.close()
        return HTTPResponse(code, body)

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
