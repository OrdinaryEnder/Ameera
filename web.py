from quart import Quart, render_template, websocket

app = Quart(__name__, template_folder="site", static_folder='site/assets')


@app.route("/")
async def hello():
    return await render_template("index.html")

@app.route("/game")
async def game():
     return await render_template("game.html")
