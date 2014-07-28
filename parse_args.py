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
    parser.add_option("-q", "--quiet", **quiet_options)
    (options, args) = parser.parse_args()
    opts = dict(options.__dict__)
    opts['command_line_args'] = args
    return opts

