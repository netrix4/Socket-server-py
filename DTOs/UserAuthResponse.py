class UserAuthResponse:
    def __init__(self, status, message, user_id):
        self.status = status
        self.message = message
        self.user_id = user_id
    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "user_id": self.user_id
        }