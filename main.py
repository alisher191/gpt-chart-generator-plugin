import json

import quart
import quart_cors
from quart import request, send_from_directory

# components used for generating charts.
from pyecharts.charts.base import Base
from quickchart import QuickChart

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

async def make_chart(prompt):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.config = prompt
    return qc.get_short_url()

@app.post('/charts')
async def get_chart():
    prompt = await request.get_json()
    # Or write the chart to a file
    # qc.to_file('mychart_line.png')
    chart_url = await make_chart(prompt=prompt)
    return json.dumps({"chart_url": chart_url})

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
