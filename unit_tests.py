#!/usr/bin/env python3

import sys
import os
import x_visibility


TESTS_DIR = 'tests'
tests = [(os.path.join(TESTS_DIR, schema_fname),
          os.path.join(TESTS_DIR, input_fname),
          expected)
          for schema_fname, input_fname, expected in (
    ('test-schema-1.json', 'test-input-1.json', True),
    ('test-schema-1.json', 'test-input-2.json', False),
    ('test-schema-2.json', 'test-input-3.json', True),
    ('test-schema-2.json', 'test-input-4.json', True),
)]


def main(*args):
    results = [x_visibility.main(schema_fname, input_fname) == expected
               for schema_fname, input_fname, expected in tests]
    n_tests = len(results)
    n_passed = sum(1 for r in results if r)
    for i, r in enumerate(results):
        print("[{}/{}] {}".format(i + 1, n_tests, "Passed" if r else "Failed"))
    print("Total: {} passed out of {}".format(n_passed, n_tests))


if __name__ == '__main__':
    main(*sys.argv[1:])
