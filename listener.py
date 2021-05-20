import config
import json
import asyncio
from sanic import Sanic 
from sanic.response import json
from sanic_jinja2 import SanicJinja2
import logic

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    data = request.json

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:


        logic.store_data(data)


        return json({
            "code": "success",
            "message": "json updated"
        })

# heartbeat
async def db_heartbeat():
    await logic.db_heartbeat()
    await asyncio.sleep(0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
