import json
import logging

import upstream

class Context:
    port = 80
    upstream = []
    log_file = "access.log"
    log_level = logging.INFO
    logger = logging.getLogger("context")
    firewall_enabled = True
    model = None

    def __init__(self, config_path) -> None:
        self.parse_config(config_path)
        self.init_logger()
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(Context, "_instance"):
            Context._instance = object.__new__(cls)
        return Context._instance

    @classmethod
    def get_context(self):
        return Context._instance

    def init_logger(self):
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh = logging.FileHandler(self.log_file, encoding="utf-8")
        fh.setLevel(self.log_level)
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def parse_config(self, path: str = "config.json"):
        with open(path, "r") as config:
            config_data = json.load(config)
            self.port = config_data["port"]
            for srv in config_data["upstream"]:
                self.upstream.append(
                    upstream.UpstreamServer(
                        srv["upstream_addr"], srv["upstream_port"], srv["weight"]
                    )
                )
            self.log_level = logging.getLevelName(config_data["log_level"])
            self.log_file = config_data["log_file"]
            self.firewall_enabled = config_data["firewall"]["enable"]
            self.model = config_data["firewall"]["model"]

if __name__ == "__main__":
    pass