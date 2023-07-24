import requests

# 将链接发送给代理服务器下载
def download_image(url):
    params = {'url': url}
    response = requests.get('http://154.7.177.80:5000/download_image', params=params)
    if response.status_code == 200:

        with open('output.png', 'wb') as f:
            f.write(response.content)

        return True
    else:
        return False

if __name__ == '__main__':
    image_url = 'https://cdn.discordapp.com/attachments/1126964049335304302/1131877211239096411/johnhess_Catgirlwhite_stockingsbeautiful_woman_e6820b0b-aa33-4cd4-9604-2963fbacfc13.png'  # 替换为实际的图片URL
    print(download_image(image_url))
