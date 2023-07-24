"""
webapi接口
搜索结果：https://music.163.com/weapi/cloudsearch/get/web?csrf_token=（post）
评论：https://music.163.com/weapi/comment/resource/comments/get?csrf_token=
歌词：https://music.163.com/weapi/song/lyric?csrf_token=
详情（包括音质）：https://music.163.com/weapi/v3/song/detail?csrf_token=
歌曲下载：https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=

iw233网站解析链接
https://iw233.cn/music/?name=コトダマ紬ぐ未来&type=netease

外链：http://music.163.com/song/media/outer/url?id=534544522.mp3

音乐外链播放器：https://music.163.com/outchain/player?type=2&id=473403600&auto=1&height=66
"""
import base64
import codecs
import json
import math
import random

import requests
from Crypto.Cipher import AES
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''

var bKB3x = window.asrsea(JSON.stringify(i3x), buU1x(["流泪", "强"]), buU1x(Rg7Z.md), buU1x(["爱心", "女孩", "惊恐", "大笑"]));
            e3x.data = j3x.cr3x({
                params: bKB3x.encText,
                encSecKey: bKB3x.encSecKey
            })


    window.asrsea = d,

    d: {"hlpretag":"<span class="s-fc7">","hlposttag":"</span>","s":"コトダマ紬ぐ未来","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
    e:010001
    f:00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    g:0CoJUm6Qyw8W8jud
        function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }

        function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
'''

class wangyiyun:
    def __init__(self):
        self.e = '010001'
        self.f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g = '0CoJUm6Qyw8W8jud'

    # 获取一个随意字符串，length是字符串长度
    def generate_str(self, lenght):
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for i in range(lenght):
            index = random.random() * len(str)  # 获取一个字符串长度的随机数
            index = math.floor(index)  # 向下取整
            res = res + str[index]  # 累加成一个随机字符串
        return res

    # AES加密获得params
    def AES_encrypt(self, text, key):
        iv = '0102030405060708'.encode('utf-8')  # iv偏移量
        text = text.encode('utf-8')  # 将明文转换为utf-8格式
        pad = 16 - len(text) % 16
        text = text + (pad * chr(pad)).encode('utf-8')  # 明文需要转成二进制，且可以被16整除
        key = key.encode('utf-8')  # 将密钥转换为utf-8格式
        encryptor = AES.new(key, AES.MODE_CBC, iv)  # 创建一个AES对象
        encrypt_text = encryptor.encrypt(text)  # 加密
        encrypt_text = base64.b64encode(encrypt_text)  # base4编码转换为byte字符串
        return encrypt_text.decode('utf-8')

    # RSA加密获得encSeckey
    def RSA_encrypt(self, str, key, f):
        str = str[::-1]  # 随机字符串逆序排列
        str = bytes(str, 'utf-8')  # 将随机字符串转换为byte类型的数据
        sec_key = int(codecs.encode(str, encoding='hex'), 16) ** int(key, 16) % int(f, 16)  # RSA加密
        return format(sec_key, 'x').zfill(256)  # RSA加密后字符串长度为256，不足的补x

    # 获取参数
    def get_params(self, d, e, f, g):
        i = self.generate_str(16)    # 生成一个16位的随机字符串
        # i = 'aO6mqZksdJbqUygP'
        encText = self.AES_encrypt(d, g)
        # print(encText)    # 打印第一次加密的params，用于测试d正确
        params = self.AES_encrypt(encText, i)  # AES加密两次后获得params
        encSecKey = self.RSA_encrypt(i, e, f)  # RSA加密后获得encSecKey
        return params, encSecKey

    # 传入msg和url,获取返回的json数据
    def get_data(self, msg, url):
        encText, encSecKey = self.get_params(msg, self.e, self.f, self.g)   # 获取参数
        params = {
            "params": encText,
            "encSecKey": encSecKey
        }
        re = requests.post(url=url, params=params, verify=False)    # 向服务器发送请求
        return re.json()    #返回结果

    # 返回搜索数据
    def get_search_data(self, s='', type=1, offset=0, total='true', limit=30, csrf_token=''):
        msg = r'{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>",' + f'"s":"{s}","type":"{type}","offset":"{offset}","total":"{total}","limit":"{limit}","csrf_token":"{csrf_token}"' + '}'
        url = f'https://music.163.com/weapi/cloudsearch/get/web?csrf_token={csrf_token}'
        return self.get_data(msg, url)

    # 返回歌词数据
    def get_lyric_data(self, id, lv=-1, tv=-1, csrf_token=''):
        msg = '{' + f'"id":"{id}","lv":"{lv}","tv":"{tv}","csrf_token":"{csrf_token}"' + '}'
        url = f'https://music.163.com/weapi/song/lyric?csrf_token={csrf_token}'
        return self.get_data(msg, url)

    # 返回音乐详情,包含了音质等级和可下载权限
    def get_detail_data(self, id, csrf_token=''):
        msg = '{' + f'"id":"{id}",' + r'"c":"[{\"id\":\"' + str(id) + r'\"}]",' + f'"csrf_token":"{csrf_token}"' + '}'
        url = f'https://music.163.com/weapi/v3/song/detail?csrf_token={csrf_token}'
        return  self.get_data(msg, url)

    # 返回下载数据，level代表音质等级，encodeType代表编码类型，flac可存储无损音质，目前无法下载无损音乐
    # # 音质 standard标准 higher较高 exhigh极高 lossless无损 hires
    # # 编码类型 aac flac
    def get_download_data(self, id, level='exhigh', encodeType='flac', csrf_token=''):
        msg = '{' + f'"ids":"{id}","level":"{level}","encodeType":"{encodeType}","csrf_token":"{csrf_token}"' + '}'
        url = f'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token={csrf_token}'
        return self.get_data(msg, url)

    # 通过播放器外链的方式返回的音乐详情数据
    def get_detail_outdata(self, id, limit=10000, offset=0, csrf_token=''):
        msg = '{' + f'"id":"{id}",' + r'"ids":"[\"' + str(id) + r'\"]",' + f'"limit":{limit},"offset":{offset},"csrf_token":"{csrf_token}"' + '}'
        url = 'https://music.163.com/weapi/song/detail'
        return self.get_data(msg, url)

    # 通过播放器外链的方式返回的音乐下载数据
    # br代表音质，四个等级 标准128000 较高192000 极高320000 无损999000
    def get_download_outdata(self, id, br=320000, csrf_token=''):
        msg = '{' + f'"ids":"{id}","br":{br},"csrf_token":"{csrf_token}"' + '}'
        url = 'https://music.163.com/weapi/song/enhance/player/url'
        return self.get_data(msg, url)

