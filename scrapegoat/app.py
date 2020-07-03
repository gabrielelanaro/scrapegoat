import argparse
from pathlib import Path
import os
from aiohttp import web

from .learn.link_extractor_pipeline import suggest_new_links
from .types import Candidate, LinkType

routes = web.RouteTableDef()
routes.static("/static", path="ui/scrapegoat-ui/dist")

MAX_SIZE = 1024 * 1024 * 1024


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


@routes.post("/api/predictLinks/")
async def predict_links(request):
    data = await request.json()
    # We need to have data

    candidates = [Candidate.from_dict(c) for c in data["candidates"]]
    links = [LinkType.from_dict(c) for c in data["links"]]
    new_links = suggest_new_links(candidates, links)

    return web.json_response(data=[l.serialize() for l in new_links])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    return parser.parse_args()


def create_app():
    app = web.Application(client_max_size=MAX_SIZE)
    app.add_routes(routes)
    app["directory"] = os.environ["DATA_DIR"]
    return app


def main():
    args = parse_args()
    web.run_app(app, port=8081)


if __name__ == "__main__":
    main()
