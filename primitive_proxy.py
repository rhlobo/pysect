#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import requests

from flask import Flask
from flask import Response
from flask import request


app = Flask(__name__)


@app.route('/<path:url>')
def all(url):
    return proxy(url)


def proxy(url):
    headers = {header: content for header, content in request.headers}
    req = requests.get(url, headers=headers)
    # return Response(req.content, content_type=req.headers['content-type'])
    return Response(req.text, content_type=req.headers['content-type'])


if __name__ == '__main__':
    utils.config_graceful_exit()
    app.run(host='0.0.0.0', debug=True)
