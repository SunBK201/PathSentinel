class UpstreamServer:
    def __init__(self, addr: str, port: int, weight: int = 2) -> None:
        self.addr = addr
        self.port = port
        self.weight = weight
        self.currentWeight = weight
        self.connection_n = 0


class NodeSelector:
    def __init__(self, nodeList: list[UpstreamServer], policy) -> None:
        self.nodeList = nodeList
        self.policy = policy

    def round_robin_get(self) -> UpstreamServer:
        total_weight = 0
        for node in self.nodeList:
            total_weight += node.weight
            node.currentWeight += node.weight
        best = max(self.nodeList, key=lambda node: node.currentWeight)
        best.currentWeight -= total_weight
        best.connection_n += 1
        return best

    def getNode(self) -> UpstreamServer:
        return self.round_robin_get()


if __name__ == "__main__":
    list = [
        UpstreamServer("1.1.1.1", "80", weight=2),
        UpstreamServer("2.2.2.2", "81", weight=2),
        UpstreamServer("3.3.3.3", "82", weight=2),
    ]
    nodeSelector = NodeSelector(list)
    for i in range(10):
        print(nodeSelector.getNode().addr)
