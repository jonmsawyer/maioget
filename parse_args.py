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
    daemon_options = {
        'dest': 'daemon',
        'default': False,
        'action': 'store_true',
        'help': "Enable daemon mode. Setting this flag will supress output to STDOUT. Default is non-daemon mode.",
    }
    loglevel_options = {
        'dest': 'loglevel',
        'default': 'INFO',
        'type': 'string',
        'help': "Configure the logging level. Must be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL. Default is INFO.",
        'metavar': 'LOG_LEVEL',
    }
    logsdir_options = {
        'dest': 'logsdir',
        'default': 'logs',
        'type': 'string',
        'help': "Put the logs into the LOGS_DIR directory.",
        'metavar': 'LOGS_DIR',
    }
    name_options = {
        'dest': 'name',
        'default': 'UNNAMED',
        'type': 'string',
        'help': "The name of the MaioGet app.",
        'metavar': 'NAME',
    }
    threads_options = {
        'dest': 'threads',
        'default': 5,
        'type': 'int',
        'metavar': 'NUM_THREADS',
        'help': 'Process the profiles list using NUM_THREADS threads. Default is 5.',
    }
    parser.add_option('-d', '--daemon', **daemon_options)
    parser.add_option('-D', '--logs-dir', **logsdir_options)
    parser.add_option('-l', '--log-level', **loglevel_options)
    parser.add_option('-n', '--name', **name_options)
    parser.add_option('-t', '--threads', **threads_options)
    (options, args) = parser.parse_args()
    opts = dict(options.__dict__)
    opts['command_line_args'] = args
    
    # Make sure that the log level flag is upper case and that the
    # log level is valid. Exit if not.
    opts['loglevel'] = opts['loglevel'].upper()
    if opts['loglevel'] not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        print "%s: error: option -l|--log-level: invalid string value: '%s'" % (sys.argv[0], opts['loglevel'])
        parser.print_help()
        sys.exit(1)
    
    return opts

