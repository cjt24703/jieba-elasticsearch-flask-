import json
from werkzeug.exceptions import HTTPException
from exception.base_exception import APIException
class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0
    data = None

    def get_body(self,environ=None):
        body = dict(
            msg = self.msg,
            error_code = self.error_code,
            data = self.data
        )
        text = json.dumps(body)
        return text