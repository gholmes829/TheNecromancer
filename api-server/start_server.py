"""

"""

import sys
import argparse
import os.path as osp, os
from icecream import ic
PATH = osp.dirname(osp.realpath(__file__))
sys.path.append(PATH)

from flask import Flask
from flask_cors import CORS
import endpoints

def make_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(description='API endpoint server')
    argparser.add_argument('--host', help = 'server domain')
    argparser.add_argument('--port', type = int, help = 'server port')
    return argparser


def main():
    argparser = make_argparser()
    args = argparser.parse_args()
    host: str = args.host
    port: int = args.port

    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    for (endpoint, request_type), callback in endpoints.endpoints.items():
        app.route(endpoint, methods=(request_type,))(callback)

    app.run(debug = True, host = host, port = port)


if __name__ == '__main__':
    main()