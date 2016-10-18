import logging
import os
import json
import sys
import time
import itertools
from collections import defaultdict
from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.controlvalidation')


class ControlValidation(Plugin):
    name = 'ControlValidation'
    enabled = True
    err = sys.stderr

    def options(self, parser, env=os.environ):
        super(ControlValidation, self).options(parser, env=env)

    def configure(self, options, conf):
        super(ControlValidation, self).configure(options, conf)
        if not self.enabled:
            return
        self.results = defaultdict(dict)
        self.map_controls()

    def record(self, test, status):
        self.results[test.id()] = {
            "status": status,
            "timestamp": time.time()
        }

    def addSuccess(self, test):
        self.record(test, 'pass')

    def addError(self, test, err):
        self.record(test, 'error')

    def addFailure(self, test, err):
        self.record(test, 'fail')

    def map_controls(self):
        """
        Read which controls require which evidence demonstrated by which test,
        and return the inverted look up:

            {
                test:{
                    provides: {
                        evidence1: {
                            control1: [accreditation1],
                            control 2: [accreditation1, accreditation2]
                        },
                        evidence2: {
                            control1: [accreditation1],
                            control 3: [accreditation2]
                        },
                        evidence3: {
                            control2: [accreditation2],
                            control 4: [accreditation4]
                        }
                    }
                    ttl: 604800
                }
            }

        """
        # TODO: Reading from the graphDB instead of a file
        self.controls = json.load(open('controls.json'))

    def build_output(self, result):
        """
        Builds the output dict to store. This has the structure:

        {
            "accreditation1":{
                "control1": {
                    evidence1: {
                        test1: {pass: True, timestamp: now(), ttl: 604800},
                        test2: {pass: False, timestamp: now(), ttl: 604800},
                    },
                    evidence2: {
                        test3: {pass: True, timestamp: now(), ttl: 604800},
                        test4: {pass: False, timestamp: now(), ttl: 604800},
                    }
                },
                "control2": {
                    evidence1: {
                        test1: {pass: True, timestamp: now(), ttl: 604800},
                        test2: {pass: False, timestamp: now(), ttl: 604800},
                    }
                }
            }
        }
        """
        verified = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(
                    lambda: defaultdict(dict)
                )
            )
        )

        for t, provides in self.controls.items():
            for proof, v in provides.items():
                for ctrl, w in v.items():
                    for accreditation in w:
                        verified[accreditation][ctrl][proof] = self.results[t]
        return verified

    def _want_function(self, function):
        test = '.'.join([function.__module__, function.__name__])
        test_paths = self.controls.get(test, {})
        accreditations = [
            itertools.chain(*c.values()) for c in test_paths.values()
        ]
        accreditations = set(itertools.chain(*accreditations))
        return os.environ['ACCREDITATION'] in accreditations

    def wantFunction(self, function):
        """
        Only run those functions that are required for the accreditation.
        """
        return self._want_function(function)

    def wantMethod(self, method):
        """
        Only run those methods that are required for the accreditation.
        """
        return self._want_function(method)

    def finalize(self, result):
        verify = self.build_output(result)
        with open('results.json', 'w') as f:
            json.dump(verify, f)
