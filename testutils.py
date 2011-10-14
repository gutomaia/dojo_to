# -*- coding: utf-8 -*-

import os, os.path, sys
from subprocess import call

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

def mysql_run(file, app=None):
    try:
        retcode = call("mysql %s < %s" % ("dojo_to", os.path.join(APP_ROOT, 'sql', file)), shell=True)
        if retcode != 0:
            print >>sys.stderr, "Child was terminated by signal a", -retcode
            raise Exception("Mysql problem on: "+file)
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

def init_db(app=None):
    mysql_run('create_schema.sql')
    mysql_run('test_data.sql')

def drop_db(app=None):
    mysql_run('drop_schema.sql')
