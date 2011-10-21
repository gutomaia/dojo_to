# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.options import parse_config_file, options

from testutils import init_db, drop_db
from subprocess import call

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))


parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")


try:
    #mysql -u username -ppassword -h hostname databasename
    retcode = call('mysql -h %s -u %s -p%s  %s< %s' % 
    		(
    			options.database_host,
    			options.database_username,
    			options.database_password,
    			options.database_name,
    			os.path.join(APP_ROOT, 'sql', "create_schema.sql")
    		),
    		shell=True
    	)
    if retcode != 0:
        print >>sys.stderr, 'Child was terminated by signal a', -retcode
        raise Exception('Mysql problem on: '+ "create_schema.sql")
except OSError, e:
    print >>sys.stderr, 'Execution failed:', e

