class UpstreamServer:
    def __init__(self, addr: str, port: int, weight: int = 2) -> None:
        self.addr = addr
        self.port = port
        self.weight = weight
