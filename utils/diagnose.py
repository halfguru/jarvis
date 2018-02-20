import logging, socket

def check_network_connection(server="www.google.com"):
    """
    Checks if jasper can connect a network server.
    Arguments:
        server -- (optional) the server to connect with (Default:
                  "www.google.com")
    Returns:
        True or False
    """
    logger = logging.getLogger(__name__)
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(server)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, 80), 2)
    except Exception:
        logger.debug("Network connection not working")
        return False
    else:
        logger.debug("Network connection working")
        return True
