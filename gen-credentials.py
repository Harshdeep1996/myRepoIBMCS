#!/usr/bin/env python
# -*- coding:utf-8; mode:python -*-

'''This script generates a config file suitable to be used by
`utilitarian.credentials.Config` from envvars. This is useful for
Travis CI that allows to deploy credentials safely using envvars.

Any new supported credential must be added to SUPPORTED_SECTIONS which
includes a list of sections of `Config` supported by the script. For
example, adding 'github' will make the script to generate
`github.username` from GITHUB_USERNAME and `github.password` from
GITHUB_PASSWORD, if both envvars are defined.
'''

import os
import sys
import ConfigParser


SUPPORTED_SECTIONS = ['github', 'fogbugz']


def main():
    matched_keys = filter(
        lambda k: any([k.lower().startswith(x) for x in SUPPORTED_SECTIONS]),
        os.environ.keys()
    )
    if not matched_keys:
        return 0

    cfg_parser = ConfigParser.ConfigParser()
    for k in matched_keys:
        section = k.split('_')[0]
        option = k.split(section)[1][1:].lower()
        section = section.lower()
        if not cfg_parser.has_section(section):
            cfg_parser.add_section(section)
        cfg_parser.set(section, option, os.environ[k])

    cfg_parser.write(sys.stdout)

    return 0


if __name__ == '__main__':
    exit(main())
