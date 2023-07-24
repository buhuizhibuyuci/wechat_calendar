from flask import Flask, request, send_file
import requests

app = Flask(__name__)

@app.route('/download_image', methods=['GET'])
def download_image():
    url = request.args.get('url')
    response = requests.get(url)
    if response.status_code == 200:
        # 获取文件名
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
        return send_file(filename, as_attachment=True)
    else:
        return "Failed to download image"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
