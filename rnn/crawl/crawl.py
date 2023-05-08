import subprocess
import json
import io
import os
from urllib.parse import urlparse

JSON_PATH = "rnn/crawl/result.json"
TXT_PATH = "rnn/crawl/result.txt"

def main():
    if os.path.exists(JSON_PATH):
        os.remove(JSON_PATH)
    target = "https://www.ithome.com"
    cmd = [
        "rnn/crawl/crawlergo",
        "-c",
        "rnn/crawl/Chromium.app/Contents/MacOS/Chromium",
        "-t",
        "20",
        "--output-json",
        JSON_PATH,
        target,
    ]
    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()


def clean():
    with open(JSON_PATH) as f:
        data = json.load(f)

    urls = []
    for request in data["all_req_list"]:
        urls.append(request["url"])

    with io.open(TXT_PATH, "w", encoding="utf8") as f:
        for url in urls:
            parsed_url = urlparse(url)
            dels = parsed_url.scheme + "://" + parsed_url.netloc
            f.write(url.replace(dels, "") + "\n")


if __name__ == "__main__":
    main()
    clean()
