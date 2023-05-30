class GetCourseApiException(Exception):
    pass


class UnauthorizedRequest(GetCourseApiException):
    """Wrong or expired api key"""

    status_code = 901


class KeyNotSpecified(GetCourseApiException):
    """Api key was not specified in query parameters"""

    status_code = 904


class FiltersRequired(GetCourseApiException):
    """At least one filter must be specified"""

    status_code = 908


class IncorrectDate(GetCourseApiException):
    """Incorrect value of query parameter with date"""

    status_code = 912


class IncorrectStatus(GetCourseApiException):
    """Incorrect value of "status" query parameter"""

    status_code = 914


class UnknownException(GetCourseApiException):
    """Congratulations! Your found that exception first"""
