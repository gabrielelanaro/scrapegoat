from aiohttp import web
import argparse
from pathlib import Path

routes = web.RouteTableDef()
routes.static("/static", path="ui/scrapegoat-ui/dist")


@routes.get("/")
async def index(request):
    raise web.HTTPFound("/static/index.html")


@routes.get("/fs/{file}")
async def fs_get(request):
    path = Path(request.app["directory"]) / request.match_info["file"]
    return web.FileResponse(str(path))


@routes.put("/fs/{file}")
async def fs_post(request):
    path = Path(request.app["directory"]) / request.match_info["file"]

    data = await request.read()
    with path.open("wb") as fd:
        fd.write(data)
    return web.Response(text="File written")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    return parser.parse_args()


def main():
    args = parse_args()

    app = web.Application()
    app.add_routes(routes)

    app["directory"] = args.dir
    web.run_app(app, port=8081)


if __name__ == "__main__":
    main()
