#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import xmlrpc.client

TRAC_URL = '172.16.33.2:8080/trac'
USER = 'user'
PASSWORD = 'password'
CC = 'cc'


class JiraWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = self.headers['Content-Length']
        if content_length:
            content_length = int(content_length)
            self.send_response(200)
            self.end_headers()
            body = self.rfile.read(content_length)
            post_data = json.loads(body)

            trac_rpc_url = 'http://%s:%s@%s/login/rpc' % (USER, PASSWORD, TRAC_URL)
            server = xmlrpc.client.ServerProxy(trac_rpc_url)

            description = post_data["issue"]["fields"]["description"]
            summary = post_data["issue"]["fields"]["summary"]
            reporter = post_data["issue"]["fields"]["reporter"]["displayName"]
            # owner = post_data["issue"]["fields"]["assignee"]

            ret = server.ticket.create(summary, description,
                                       {'component': '', 'type': '', 'due_date': '2015.1R(0102)', 'reporter': reporter,
                                        'exp_duedate': '2015.1R(0102)', 'owner': 'jhahn', 'priority': '1',
                                        'milestone': '', 'cc': CC, 'man_day': '', 'ex_man_day': ''})
            print('ticket #%d [%s] created.' % (ret, server.ticket.get(ret)[3]['summary']))
        else:
            print('no content-length.')
            print(self.headers)


def run():
    server = HTTPServer(('', 8000), JiraWebhookHandler)
    print('Server started')
    server.serve_forever()


if __name__ == '__main__':
    run()
