# PathSentinel

PathSentinel is an application firewall that focuses on HTTP path protection. It uses deep neural network technology to provide web application security measures. PathSentinel is deployed using a reverse proxy, which provides robust protection for your web server.

# Features

-   Comprehensive HTTP path protection: PathSentinel provides robust security measures against various attacks targeted at HTTP paths, including SQL injection, cross-site scripting, and path traversal attacks.
-   Advanced artificial intelligence technology: PathSentinel's deep neural network technology accurately detects and responds to potential threats, providing intelligent defense for your web applications.
-   Reverse proxy deployment: PathSentinel is deployed using a reverse proxy, which acts as a secure gateway between the internet and your web server, ensuring that your server remains protected and secure.

# Getting Started

PathSentinel is easy to get started with. Simply deploy it as a reverse proxy in front of your web server and configure it to start monitoring HTTP traffic. PathSentinel will automatically detect and respond to potential threats to your web applications.

Please configure `config.conf` before you start using it:
```json
{
    "host": "0.0.0.0",
    "port": 9090,
    "upstream": [
        {
            "upstream_addr": "127.0.0.1",
            "upstream_port": 80,
            "weight": 2
        },
        {
            "upstream_addr": "127.0.0.1",
            "upstream_port": 81,
            "weight": 2
        }
    ],
    "log_level": "INFO",
    "log_file": "access.log",
    "firewall": {
        "enable": true,
        "model": "4w.pt"
    }
}
```

```bash
python server.py
```

## License

PathSentinel is licensed under the [BSD-2 License](./LICENSE).