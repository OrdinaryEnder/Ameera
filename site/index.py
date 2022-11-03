from quart import Quart, render_template, websocket

app = Quart(__name__, static_folder='assets')


@app.route("/")
async def hello():
    return await render_template("index.html")
