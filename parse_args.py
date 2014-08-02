import sys

# Function: parse_args
# See: DocString
def parse_args():
    """
    Parse the command line options and arguments and pass them along as a
    dictionary of key-value pairs
    """
    from optparse import OptionParser
    import sys
    parser = OptionParser()
    file_options = {
        'dest': 'filename',
        'help': 'write report to FILE',
        'type': 'string',
        'metavar': 'FILE',
    }
    quiet_options = {
        'dest': 'verbose',
        'default': True,
        'action': 'store_false',
        'help': "don't print status messages to stdout",
    }
    daemon_options = {
        'dest': 'daemon',
        'default': False,
        'action': 'store_true',
        'help': "let MaioGet know that the process is running in daemon mode. Setting this flag will supress output to STDOUT",
    }
    loglevel_options = {
        'dest': 'loglevel',
        'default': 'INFO',
        'type': 'string',
        'help': "configure the log level of MaioGet. One of DEBUG, INFO, WARNING, ERROR, or CRITICAL",
        'metavar': 'LOGLEVEL',
    }
    foo_options = {
        'dest': 'foo',
        'default': 'bar',
        'metavar': 'FOO',
        'help': 'be a FOO and help BAR be a BAZ',
    }
    threads_options = {
        'dest': 'threads',
        'default': 5,
        'type': 'int',
        'metavar': 'THREADS',
        'help': 'spread the profiles list into THREADS threads',
    }
    parser.add_option('-t', '--threads', **threads_options)
    parser.add_option('-q', '--quiet', **quiet_options)
    parser.add_option('-d', '--daemon', **daemon_options)
    parser.add_option('-l', '--log-level', **loglevel_options)
    (options, args) = parser.parse_args()
    opts = dict(options.__dict__)
    opts['command_line_args'] = args
    opts['loglevel'] = opts['loglevel'].upper()
    if opts['loglevel'] not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        print "%s: error: option -l|--log-level: invalid string value: '%s'" % (sys.argv[0], opts['loglevel'])
        parser.print_help()
        sys.exit(1)
    return opts

