from rest_framework import status


class UrlSpaceExhaust(Exception):
    content = {"error": "The specify url space is exhausted."}
    code = 507
    api_status = status.HTTP_507_INSUFFICIENT_STORAGE


class NeedPassword(Exception):
    content = {"error": "need password"}
    code = 401
    api_status = status.HTTP_401_UNAUTHORIZED


class BadParams(Exception):
    content = {"error": "bad params"}
    code = 400
    api_status = status.HTTP_400_BAD_REQUEST


class UrlHasBeenUsed(Exception):
    content = {"error": "specify url has been used"}
    code = 400
    api_status = status.HTTP_400_BAD_REQUEST
