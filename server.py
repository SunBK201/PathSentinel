from aiohttp import web
import aiohttp
import time

import config
import detect

context = config.Context("conf/config.json")
sentinel = detect.Sentinel(context=context)


async def persistent_session(app):
    app["PERSISTENT_SESSION"] = session = aiohttp.ClientSession()
    yield
    await session.close()


def test_request(request):
    print("host:", request.host, "type:", type(request.host))
    print("remote:", request.remote, "type:", type(request.remote))
    print("method:", request.method, "type:", type(request.method))
    print("scheme:", request.scheme, "type:", type(request.scheme))
    print("request.url:", request.url, "type:", type(request.url))
    print("request.rel_url:", request.rel_url, "type:", type(request.rel_url))
    print("request.forwarded:", request.forwarded, "type:", type(request.forwarded))
    print("request.headers:", request.headers, "type:", type(request.headers))
    print(
        "request.raw_headers:", request.raw_headers, "type:", type(request.raw_headers)
    )
    print("request.keep_alive:", request.keep_alive, "type:", type(request.keep_alive))


async def get_up(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            return web.Response(text=text)


def request2dict(method, addr, port, path, remote):
    """request data to dict"""
    payload = {
        "method": method,
        "src": remote,
        "dst": addr,
        "request_path": path,
        "request_body": None,
        "date": time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()),
    }
    return payload


async def forward(session, method, url, headers, body=None):
    match method:
        case "GET":
            async with session.get(url, headers=headers) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "POST":
            async with session.post(url, headers=headers, data=body) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "HEAD":
            async with session.head(url, headers=headers) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "PUT":
            async with session.put(url, headers=headers, data=body) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "DELETE":
            async with session.delete(url, headers=headers) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "OPTIONS":
            async with session.options(url, headers=headers) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)
        case "PATCH":
            async with session.patch(url, headers=headers, data=body) as resp:
                data = await resp.read()
                return web.Response(body=data, headers=resp.headers)


async def all_handler(request):
    method = request.method
    scheme = request.scheme
    addr = context.upstream[0].addr
    port = context.upstream[0].port
    path = str(request.rel_url)
    remote = request.remote
    url = scheme + "://" + addr + ":" + str(port) + path

    if context.firewall_enabled == True:
        payload = request2dict(method, addr, port, path, remote)
        result = sentinel.detect(payload)
        if result == detect.ATTACK:
            context.logger.warning(path + " (Attack)")
            return web.HTTPForbidden()

    context.logger.info(path)
    headers = request.headers.copy()
    headers["host"] = addr + ":" + str(port)
    body = await request.read()
    return await forward(request.app["PERSISTENT_SESSION"], method, url, headers, body)


if __name__ == "__main__":
    app = web.Application()
    app.cleanup_ctx.append(persistent_session)
    app.add_routes([web.route("*", "/{path_info:.*}", all_handler)])
    print("PathSentinel version: 0.0.1")
    context.logger.info("start listen: " + str(context.port))
    context.logger.info("upstream server: " + str(len(context.upstream)))
    for ups in context.upstream:
        context.logger.info(
            "upstream server "
            + ups.addr
            + ":"
            + str(ups.port)
            + ", weight="
            + str(ups.weight)
        )
    context.logger.info("firewall enabled: " + str(context.firewall_enabled))
    context.logger.info("firewall model: " + context.model)
    context.logger.info("log file: " + context.log_file)
    web.run_app(app, port=context.port, access_log=None)
