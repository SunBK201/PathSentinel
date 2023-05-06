import rnn

NORMAL = 0
ATTACK = 1


def rnn_detec(payload: dict) -> int:
    if rnn.evaluate(payload["request_path"]) == 0:
        return NORMAL
    else:
        return ATTACK


def preg_detec(payload: dict) -> int:
    pass


def detect(payload: dict) -> int:
    result = rnn_detec(payload)
    return result
