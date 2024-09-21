from twicas.errors.twicasting_exceptions import *

class TwiCastingModule:
    @classmethod
    def response_validation(self, response):
        if "error" not in response:
            return response
        
        match response["error"]["code"]:
            case 400:
                raise BadRequestException()
            case 404:
                raise NotFoundException()
            case 500:
                raise InternalServerError()
            case 1000:
                raise InvalidTokenException()
            case 2000:
                raise ExecutionCountLimitationException()
            case 2001:
                raise ApplicationDisabledException()
            case 2002:
                raise ProtectedException()
            case 2004:
                raise TooManyCommentsException()
            case 2005:
                raise OutOfScopeException()        
            case _:
                raise Exception(response)