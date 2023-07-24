import json

import requests


# https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=
# http://m701.music.126.net/20230709000907/dd5b4db6e1ee70b5e5f70c5437692d3d/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/11320622858/eba7/8e7c/761d/d759cb8185e733a38dfee71af5eca2f9.m4a

# 搜索页：https://music.163.com/#/search/m/?id=1888566210&s=把回忆拼好给你&type=1

# https://music.163.com/#/song?id=1905004937

#https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=
#http://m701.music.126.net/20230709001757/82286f7535d151418cc475d48d3b639d/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/19900727286/24b6/fdd0/8cda/8f134f3f4779a8c6bad52694bb97bb59.m4a

import requests

# cookies = {
#     'NMTID': '00OtQCPwJ6oKYzS7EPPpDYUmT_756AAAAGJNiqEfw',
#     '_ntes_nnid': '93a433bda9a8166c8d748eb374cff222,1688830901351',
#     '_ntes_nuid': '93a433bda9a8166c8d748eb374cff222',
#     'WEVNSM': '1.0.0',
#     'WNMCID': 'dtnbwj.1688830903578.01.0',
#     'WM_NI': 'Ex1K6J6P%2F6U%2Fi9CpLAg7%2B1iFFQSltDN6TjHSK6ObYlYEpa4SWUydKNYIE7jw%2FkWoDOu%2Fh9qGSeKL35YTfR8FO0ksl36vdMtPyQJD7UNSYguNcwRe8S7xwFZZMONbFkk0MXA%3D',
#     'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee8afc61a5b584b7d23c92868aa7d15e829f8ab1d57da5adfba9c96681beb7dacd2af0fea7c3b92a87a8ffacb542f690e1d7d825abe78d91cf4ba5e9e5d2ec4e868f9d8df7508eea9c8bcb5989ea8183dc689b9bc082b759958bb785ca469b978bd8e97dedb59990c745b7f1a8daf44d91bb85adb23f9b8caab3bb4e8df0a594ef39f6aaacaef75cbb8f86a5b65f8e8d9788f846a1a99e86bb59f5a8b9a7d9528f918283c561a9f083b9c437e2a3',
#     'WM_TID': 'AD6%2BMVeGabBFRQRBFBaRxg95HImDPi9M',
#     'ntes_utid': 'tid._.P%252FFjbx2Int1EBlRVBUPAg1p5HdmGmQq9._.0',
#     'sDeviceId': 'YD-drdDEWG25RxBBgVUEELBxO4FOdCCUYNh',
#     'playerid': '23031223',
#     'JSESSIONID-WYYY': '1iIQPE8WN7qdUQxKQ6QXkfHapoNy2nTTvma9iQ83SixrvshKXxgs8dqwkXS7zhZOK%2Fq81AXcPB8BRq1tVFFJCokDT8b%2B9a%2Bvgik%5C21nP7UeXK6N6fkvfI%5CTUB%2FugpOKDXGQTNt%2BOk%2BEl%2F3AIj6E%2BRXVKoiTnfAJSrOFz5tuu0ixy7RuH%3A1688833598845',
#     '_iuqxldmzr_': '33',
# }
#
# headers = {
#     'authority': 'music.163.com',
#     'accept': '*/*',
#     'accept-language': 'zh,zh-CN;q=0.9',
#     'content-type': 'application/x-www-form-urlencoded',
#     'cookie': 'NMTID=00OtQCPwJ6oKYzS7EPPpDYUmT_756AAAAGJNiqEfw; _ntes_nnid=93a433bda9a8166c8d748eb374cff222,1688830901351; _ntes_nuid=93a433bda9a8166c8d748eb374cff222; WEVNSM=1.0.0; WNMCID=dtnbwj.1688830903578.01.0; WM_NI=Ex1K6J6P%2F6U%2Fi9CpLAg7%2B1iFFQSltDN6TjHSK6ObYlYEpa4SWUydKNYIE7jw%2FkWoDOu%2Fh9qGSeKL35YTfR8FO0ksl36vdMtPyQJD7UNSYguNcwRe8S7xwFZZMONbFkk0MXA%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8afc61a5b584b7d23c92868aa7d15e829f8ab1d57da5adfba9c96681beb7dacd2af0fea7c3b92a87a8ffacb542f690e1d7d825abe78d91cf4ba5e9e5d2ec4e868f9d8df7508eea9c8bcb5989ea8183dc689b9bc082b759958bb785ca469b978bd8e97dedb59990c745b7f1a8daf44d91bb85adb23f9b8caab3bb4e8df0a594ef39f6aaacaef75cbb8f86a5b65f8e8d9788f846a1a99e86bb59f5a8b9a7d9528f918283c561a9f083b9c437e2a3; WM_TID=AD6%2BMVeGabBFRQRBFBaRxg95HImDPi9M; ntes_utid=tid._.P%252FFjbx2Int1EBlRVBUPAg1p5HdmGmQq9._.0; sDeviceId=YD-drdDEWG25RxBBgVUEELBxO4FOdCCUYNh; playerid=23031223; JSESSIONID-WYYY=1iIQPE8WN7qdUQxKQ6QXkfHapoNy2nTTvma9iQ83SixrvshKXxgs8dqwkXS7zhZOK%2Fq81AXcPB8BRq1tVFFJCokDT8b%2B9a%2Bvgik%5C21nP7UeXK6N6fkvfI%5CTUB%2FugpOKDXGQTNt%2BOk%2BEl%2F3AIj6E%2BRXVKoiTnfAJSrOFz5tuu0ixy7RuH%3A1688833598845; _iuqxldmzr_=33',
#     'origin': 'https://music.163.com',
#     'referer': 'https://music.163.com/',
#     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
# }
#
# params = {
#     'csrf_token': '',
# }
#
# data = {
#     'params': 'I1mbUC3I6aUu18JGOpZ/u/6bmDqGqWVVjA3ANJd0hIlxDN13+W/W9sXu7hGmBR8KUi7qSV+OKz1DXpLaw0IXgOOxacxDwPno6DD1x5CGgcBseMTXCQHbOu74olTrZsNzwYo+3TJsHIB112Z2JcUXXg==',
#     'encSecKey': '0189f9c4728be3e03189502034db942285fff6e4cbcb7a7a71e679db89f03c541122ca146f4adfc08912084d0feda65a0848b4319a2ff8e40aee45a8058ead88c23acf4340c901cb57c3f0e3cf18e6041eb2aa89b6c693707e9c10e34062978182cbd23dc40b7286c098b2698632b5c1db8ea20ef3d1a99fc10059131ed0bb0c',
# }
#
# response = requests.post(
#     'https://music.163.com/weapi/song/enhance/player/url/v1',
#     params=params,
#     cookies=cookies,
#     headers=headers,
#     data=data,
# )
# # url = response.text['data']['url']
# print(response.text)
# json_data = json.loads(response.text)
# url = json_data['data'][0]['url']
#
# print(url)
#
# m = requests.get(url=url)
#
# with open('把回忆拼好给你.mp3','wb') as wp:
#     wp.write(m.content)

import requests

# https://music.163.com/#/search/m/?id=1888566210&s=把回忆拼好给你&type=1

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

params = {
    'id': '1403318151',
}

response = requests.get('https://y.music.163.com/m/song', params=params, headers=headers)

with open('wy.html','w',encoding='utf-8') as wp:
    wp.write(response.text)
