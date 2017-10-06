class Error(Exception):
    """Base class for exeptions"""
    pass


class IsNotMondayError(Error):
    """Raised when the datetime object is not Monday"""
    pass


class ParseError(Error):
    """Raised when unable to do parsing"""
    pass


class IsNotFreeError(Error):
    """Raised when not free"""
    pass


class QueryError(Error):
    """Raised when the format is correct, but failed to perform Google Calendar queries"""
    pass
