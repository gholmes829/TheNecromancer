"""

"""

from flask import request
from functools import wraps
from typing import Callable, Any
from icecream import ic
import sys
import os.path as osp
from search.querying import search
from analysis import statistics

# PAR_PATH = osp.dirname(osp.realpath(__file__))
# ROOT_PATH = osp.join(PAR_PATH, '..', '..')
# MODEL_GEN_CORE = osp.join(ROOT_PATH, 'model-gen', 'mgcore')
# sys.path.append(MODEL_GEN_CORE)

from analysis import prev_over_time

endpoints = {}
def register_endpoint(endpoint: str, request_type: str = 'GET') -> Callable:
    def _register_endpoint(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            return fn(*args, **kwargs)
        assert endpoint not in endpoints
        endpoints[endpoint, request_type.upper()] = wrapper
        return wrapper
    return _register_endpoint


@register_endpoint('/prev')
def PrevalenceScore():
    ic(request.args.get('query'))
    query = request.args.get('query')
    return prev_over_time(query)

@register_endpoint('/docs')
def DocumentRelevance():
    ic(request.args.get('query'))
    query = request.args.get('query')
    return search(query)

@register_endpoint('/stats')
def QueryStatistics():
    ic(request.args.get('query'))
    query = request.args.get('query')
    return {"values": statistics(query)}
