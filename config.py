import json
import argparse
import logging

import upstream


class Context:
    port = 80
    upstreamList = []
    nodeSelector = None
    log_file_path = "access.log"
    log_level = logging.INFO
    argparser = argparse.ArgumentParser(description=f"PathSentinel")
    args = None
    logger = logging.getLogger("context")
    firewall_enabled = True
    model = None

    def __init__(self) -> None:
        self.init_argparser()
        self.parse_config(self.args.config)
        self.init_logger()
        self.init_nodeSelector()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Context, "_instance"):
            Context._instance = object.__new__(cls)
        return Context._instance

    @classmethod
    def get_context(self):
        return Context._instance
    
    def init_nodeSelector(self):
        self.nodeSelector = upstream.NodeSelector(self.upstreamList)

    def init_logger(self):
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh = logging.FileHandler(self.log_file_path, encoding="utf-8")
        fh.setLevel(self.log_level)
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def init_argparser(self):
        self.argparser.add_argument(
            "--version",
            "-v",
            action="version",
            version="PathSentinel Version: 0.0.1",
            help="show the version",
        )
        self.argparser.add_argument(
            "--config",
            "-c",
            default="conf/sentinel.json",
            type=str,
            help="set config file path",
        )
        self.argparser.add_argument(
            "--log", "-l", type=str, help="set log file path", dest="log_file_path"
        )
        self.args = self.parse_arg()

    def parse_arg(self):
        args = self.argparser.parse_args()
        return args

    def parse_config(self, path: str = "sentinel.json"):
        with open(path, "r") as config:
            config_data = json.load(config)
            self.port = config_data["port"]
            for srv in config_data["upstream"]:
                self.upstreamList.append(
                    upstream.UpstreamServer(
                        srv["upstream_addr"], srv["upstream_port"], srv["weight"]
                    )
                )
            self.log_level = logging.getLevelName(config_data["log_level"])
            self.log_file_path = (
                self.args.log_file_path
                if self.args.log_file_path
                else config_data["log_file"]
            )
            self.firewall_enabled = config_data["firewall"]["enable"]
            self.model = config_data["firewall"]["model"]


if __name__ == "__main__":
    pass
