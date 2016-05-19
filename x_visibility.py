#!/usr/bin/env python3

import json
import operator as op
import sys


"""
x-visibility.py
"""


Environment = dict
# class Environment:
#     def __init__(self):
#         self.env = {}


def member_closure(property_values):
    def member(property_name, values_list):
        property_value = property_values[property_name]
        return property_value in values_list
    return member


def create_global_env():
    env = Environment()
    env.update({
        'not': op.not_,
        'and': lambda *args: all(args),
        'or': lambda *args: any(args)
    })
    return env


GLOBAL_ENV = create_global_env()


def create_x_visibility_env(property_values):
    env = GLOBAL_ENV.copy()
    env['member'] = member_closure(property_values)
    return env


def eval(expr, env):
    if isinstance(expr, str):
        return env[expr]
    elif not isinstance(expr, list): # literal
        return expr
    elif expr[0] == 'quote':
        return expr[1]
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
