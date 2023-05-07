import random
from hashlib import md5


class UpstreamServer:
    def __init__(self, addr: str, port: int, weight: int = 2) -> None:
        self.addr = addr
        self.port = port
        self.weight = weight
        self.currentWeight = weight
        self.request_n = 0


class NodeSelector:
    POLICY = ("ROUND_ROBIN", "IP_HASH", "RANDOM")
    ROUND_ROBIN = 0
    IP_HASH = 1
    RANDOM = 2

    def __init__(self, nodeList: list[UpstreamServer], policy="ROUND_ROBIN") -> None:
        self.nodeList = nodeList
        self.node_n = len(nodeList)
        self.policy = self.POLICY.index(policy.upper())

    def round_robin_get(self) -> UpstreamServer:
        total_weight = 0
        for node in self.nodeList:
            total_weight += node.weight
            node.currentWeight += node.weight
        best = max(self.nodeList, key=lambda node: node.currentWeight)
        best.currentWeight -= total_weight
        return best

    def ip_hash_get(self, src: str) -> UpstreamServer:
        hash_value = int(md5(src.encode()).hexdigest(), 16) % self.node_n
        return self.nodeList[hash_value]

    def random_get(self) -> UpstreamServer:
        return random.choice(self.nodeList)

    def getNode(self, src: str) -> UpstreamServer:
        targetNode: UpstreamServer = None
        match self.policy:
            case self.ROUND_ROBIN:
                targetNode = self.round_robin_get()
            case self.IP_HASH:
                targetNode = self.ip_hash_get(src)
            case self.RANDOM:
                targetNode = self.random_get()

        targetNode.request_n += 1
        return targetNode


if __name__ == "__main__":
    list = [
        UpstreamServer("1.1.1.1", "80", weight=2),
        UpstreamServer("2.2.2.2", "81", weight=2),
        UpstreamServer("3.3.3.3", "82", weight=2),
    ]
    nodeSelector = NodeSelector(list, "ROUND_ROBIN")
    for i in range(10):
        print(nodeSelector.getNode("127.0.0.1").addr)
