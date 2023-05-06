import json
import logging
import pathlib

import upstream


class Context:
    port = 80
    upstream = []
    log_file = "access.log"
    log_level = logging.INFO
    logger = logging.getLogger("context")
    firewall_enabled = True
    model = None

    def __init__(self) -> None:
        self.parse_config("config.json")
        self.init_logger()

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
        BASE_DIR = pathlib.Path(__file__).parent
        path = BASE_DIR / 'config.json'
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

context = Context()