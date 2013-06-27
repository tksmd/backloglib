see http://code.google.com/p/backloglib/

# Developers

## About Testing

run test class

    $ PYTHONPATH=src:test python -m unittest -v backloglibtest.test_Backlog

run single method

    $ PYTHONPATH=src:test python -m unittest -v backloglibtest.test_Backlog.BacklogTest.test_get_projects1
