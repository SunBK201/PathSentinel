# PathSentinel

PathSentinel is an application firewall that focuses on HTTP path protection. It uses deep neural network to provide web application security. PathSentinel is deployed using a reverse proxy way, which provides robust protection for your web server.

## Features

-   Comprehensive HTTP path protection: PathSentinel provides robust security measures against various attacks targeted at HTTP paths, including SQL injection, cross-site scripting, and path traversal attacks.
-   Advanced artificial intelligence: PathSentinel's deep neural network accurately detects and responds to potential threats, providing intelligent defense for your web applications.
-   Reverse proxy deployment: PathSentinel is deployed using a reverse proxy, which acts as a secure gateway between the internet and your web server, ensuring that your server remains protected and secure.
-   Load balancing: Supports multiple load balancing strategies: weighted round-robin strategy, source address hashing strategy, and random strategy.

# Getting Started

PathSentinel is easy to get started with. Simply deploy it as a reverse proxy in front of your web server and configure it to start monitoring HTTP traffic.

Please configure `conf/sentinel.json` before you start using it:
```json
{
    "host": "0.0.0.0",
    "port": 80,
    "policy": "round_robin",
    "upstream": [
        {
            "upstream_addr": "127.0.0.1",
            "upstream_port": 9090,
            "weight": 2
        },
        {
            "upstream_addr": "127.0.0.1",
            "upstream_port": 9091,
            "weight": 3
        }
    ],
    "log_level": "INFO",
    "log_file": "access.log",
    "firewall": {
        "enable": false,
        "model": "4w.pt"
    }
}
```

```bash
python src/main.py -c conf/sentinel.json -l access.log
```

## Load Balance Policy
- `round_robin`: Round-robin load balance policy.
- `ip_hash`: IP-hash load balance policy.
- `random`: Random load balance policy.



## License

PathSentinel is licensed under the [BSD-2 License](./LICENSE).