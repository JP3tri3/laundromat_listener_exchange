import config
import json
import asyncio
import database
from sanic import Sanic
from sanic import response
from sanic.request import Request
from sanic.response import json
from sanic_jinja2 import SanicJinja2


app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    data = request.json

    persistent_data = data['persistent_data']

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:

        # separate json payload into variable data
        # use database set methods to set data

        # example:

        green_dot_30_min = data['green_dot_30_min']
        vwap_10_min = data['vwap_10_min']

        database.set_green_dot_30_min(True)
        database.set_vwap_10_min(12)

        # tell auto.py main function to check and trigger:

        main_flag = True

        return json({
            "code": "success",
            "message": "json updated"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
