#!/usr/bin/env python3

import json
import operator as op
import sys


"""
x-visibility.py
"""


class Environment:
    def __init__(self, env={}):
        if not isinstance(env, dict):
            env = env.env
        self.env = env.copy()


class XVisibilityEnvironment(Environment):
    def __init__(self, property_values, env={}):
        super().__init__(env)
        self.property_values = property_values

    def prop(self, property_name):
        return self.property_values[property_name]


def create_global_env():
    env = Environment({
        'not': op.not_,
        'and': lambda *args: all(args),
        'or': lambda *args: any(args),
        'member': lambda val, vals: val in vals
    })
    return env


GLOBAL_ENV = create_global_env()


def create_x_visibility_env(property_values):
    env = XVisibilityEnvironment(property_values, env=GLOBAL_ENV)
    return env


def eval(expr, env):
    if isinstance(expr, str):
        return env.env[expr]
    elif not isinstance(expr, list): # literal
        return expr
    elif expr[0] == 'quote':
        return expr[1]
    elif expr[0] == 'prop':
        return env.prop(expr[1])
    else:
        assert isinstance(expr, list)
        proc, *args = (eval(elem, env) for elem in expr)
        return proc(*args)


def main(schema_fname, input_fname):
    with open(schema_fname, 'r') as schema_file, \
         open(input_fname, 'r') as input_file:
        schema_json = json.load(schema_file)
        input_json = json.load(input_file)
    x_visibility_expr = schema_json['x-visibility']
    env = create_x_visibility_env(property_values=input_json)
    result = eval(x_visibility_expr, env)
    return result


if __name__ == '__main__':
    main(*sys.argv[1:])
