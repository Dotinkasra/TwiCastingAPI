class TwicastingException(Exception):
    def __init__(self, status_code: int, msg: str, description: str):
        self.msg = msg
        self.status_code = status_code
        self.description = description
        super().__init__(self.status_code, self.msg)

    def __str__(self) -> str:
        return f"{self.status_code}: {self.msg}\n{self.description}"


class InvalidTokenException(TwicastingException):
    """Invalid Token (code: 1000)"""
    def __init__(self):
        super().__init__(1000, "Invalid Token", "アクセストークンが不正です")


class ValidationError(TwicastingException):
    """Validation Error (code: 1001)"""
    def __init__(self, datails: dict):
        self.status_code = 1001
        self.msg = "バリデーションエラー時"
        self.code_description = {
            "key": "必須パラメータが指定されていない",
            "arrayType": "配列型でない",
            "stringType": "文字列型でない",
            "intVal": "正数または数字の文字列でない",
            "in": "文字列がホワイトリストに含まれない",
            "identical": "入力値が期待する値と一致しない",
            "length": "文字列の長さが不正、または配列の長さが不正",
            "max": "数値が閾値よりも大きい",
            "min": "	数値が閾値よりも小さい"
        }
        self.datails_msg = []
        for key, code in datails.items():
            self.datails_msg.append(f"{key}: {self.code_description[code]}")

    def __str__(self) -> str:
        return f"{self.status_code}: Validation Error {self.msg}\n{self.datails_msg}"


class ExecutionCountLimitationException(TwicastingException):
    """Execution Count Limitation (code: 2000)"""
    def __init__(self):
        super().__init__(2000, "Execution Count Limitation","API実行回数上限")


class ApplicationDisabledException(TwicastingException):
    """Application Disabled (code: 2001)"""
    def __init__(self):
        super().__init__(2001, "Application Disabled", "アプリケーションが無効になっている時（サポートへお問い合わせください）")


class ProtectedException(TwicastingException):
    """Protected (code: 2002)"""
    def __init__(self):
        super().__init__(2002, "Protected", "コンテンツが保護されている時 (合言葉配信等)")


class TooManyCommentsException(TwicastingException):
    """Too Many Comments (code: 2004)"""
    def __init__(self):
        super().__init__(2004, "Too Many Comments", "コメント数が上限に達している時 (一定数以上のコメントがある配信で、配信が終了している場合にこのエラーが発生することがあります)")


class OutOfScopeException(TwicastingException):
    """Out Of Scope (code: 2005)"""
    def __init__(self):
        super().__init__(2005, "Out Of Scope", "書込み・配信などの権限がない時")


class BadRequestException(TwicastingException):
    """Bad Request (code: 400)"""
    def __init__(self):
        super().__init__(400, "Bad Request", "パラメータが不正な時 (バリデーション上問題ないが、パラメータで指定した対象が存在しない場合等)")


class NotFoundException(TwicastingException):
    """Not Found (code: 404)"""
    def __init__(self):
        super().__init__(404, "Not Found", "コンテンツが見つからない時")


class InternalServerError(TwicastingException):
    """Internal Server Error (code: 500)"""
    def __init__(self):
        super().__init__(500, "Internal Server Error", "その他エラー時")
