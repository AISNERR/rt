# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    sqlllpy.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aisner <aisner@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/03/05 11:47:09 by aisner            #+#    #+#              #
#    Updated: 2022/03/05 11:47:10 by aisner           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sqlpy.py
#

"""
Query SQL and dump as CSV.
"""

import sys
import optparse
import urlparse

import MySQLdb

def sqlpy(url, query):
    if not query.lower().strip().startswith('select'):
        raise ValueError('only select statements supported')

    user, password, host, db = _parse_db_url(url)
    conn = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
    cursor = conn.cursor()
    cursor.execute(query)

    for row in cursor:
        print u'\t'.join(map(unicode, row))

def _parse_db_url(url):
    parts = urlparse.urlparse(url)
    if parts.scheme != 'mysql':
        raise ValueError('unsupported scheme %s' % parts.scheme)

    try:
        userpassword, host = parts.netloc.split('@')
        user, password = userpassword.split(':')
        db = parts.path.lstrip('/')
    except ValueError:
        raise ValueError('invalid url: %s' % url)

    if not all([user, password, host, db]):
        raise ValueError('invalid url: %s' % url)

    return user, password, host, db

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options] mysql://user:pass@host/db query
Execute the query against the given database, printing the output rows as
tab-delimited CSV."""

    parser = optparse.OptionParser(usage)

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    try:
        sqlpy(*args)
    except (IOError, KeyboardInterrupt):
        pass

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])