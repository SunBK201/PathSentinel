from aiohttp import web
import aiohttp
import time

from config import Context
import detect

VERSION = "0.0.1"

context = Context()
sentinel = detect.Sentinel(context=context)


async def persistent_session(app):
    app["PERSISTENT_SESSION"] = session = aiohttp.ClientSession()
    yield
    await session.close()


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
    node = context.nodeSelector.getNode(request.remote)
    addr = node.addr
    port = node.port

    method = request.method
    scheme = request.scheme
    path = str(request.rel_url)
    remote = request.remote
    url = scheme + "://" + addr + ":" + str(port) + path

    if context.firewall_enabled == True:
        payload = request2dict(method, addr, port, path, remote)
        result = sentinel.detect(payload)
        if result == detect.ATTACK:
            context.logger.warning(path + " (Attack)")
            return web.HTTPForbidden()

    context.logger.info(f"{addr}:{port} {path}")
    headers = request.headers.copy()
    headers["host"] = addr + ":" + str(port)
    body = await request.read()
    return await forward(request.app["PERSISTENT_SESSION"], method, url, headers, body)


def log_basic_info():
    print(f"PathSentinel version: {VERSION}")
    context.logger.info("start listen: " + str(context.port))
    context.logger.info("upstream server: " + str(len(context.upstreamList)))
    for ups in context.upstreamList:
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
    context.logger.info("log file: " + context.log_file_path)


if __name__ == "__main__":
    app = web.Application()
    app.cleanup_ctx.append(persistent_session)
    app.add_routes([web.route("*", "/{path_info:.*}", all_handler)])

    log_basic_info()

    web.run_app(app, port=context.port, access_log=None)
