full featured and flexible logging system
log messages are sent to a file or to sys.stderr



import logging
logging.debug('Debugging information')
logging.info('Informational message')
logging.warning('Warning:config file %s not found', 'server.conf')
logging.error('Error occurred')
logging.critical('Critical error -- shutting down')


By default
    informational and debugging messages are suppressed
    output is sent to standard error
    
Other output options include routing messages through
    email
    datagrams
    sockets
    to an HTTP Server
    
New filters can select different routing based on message priority
    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL

The logging system can be configured directly from Python
can be loaded from a user editable configuration file for customized logging without altering the application

key benefit
    all Python modules can participate in logging
    application log can include your own messages integrated with messages from third-party modules


basic classes defined by the module, together with their functions
    - Loggers expose the interface that application code directly uses
    - Handlers send the log records (created by loggers) to the appropriate destination
    - Filters provide a finer grained facility for determining which log records to output
    - Formatters specify the layout of log records in the final output

