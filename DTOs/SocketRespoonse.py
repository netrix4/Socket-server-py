class SocketResponse:
    def __init__(self, command_received, output):
        self.command_received = command_received
        self.output = output

    def to_JSON_String(self):
        return f'{{"commandReceived":{self.command_received},"output":"{self.output}"}}'