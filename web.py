from quart import Quart, render_template, websocket

app = Quart(__name__, template_folder='site', static_folder='site/assets')

@app.route("/")
async def hello():
    return await render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
