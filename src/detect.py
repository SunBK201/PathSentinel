import rnn
from config import Context

NORMAL = 0
ATTACK = 1

class Sentinel:
    def __init__(self, context: Context) -> None:
        self.rnnSentinel = rnn.RNNSentinel(pt_path = context.model)

    def preg_detec(self, payload: dict) -> int:
        pass

    def rnn_detec(self, payload: dict) -> int:
        if self.rnnSentinel.evaluate(payload["request_path"]) == 0:
            return NORMAL
        else:
            return ATTACK

    def detect(self, payload: dict) -> int:
        result = self.rnn_detec(payload)
        return result
