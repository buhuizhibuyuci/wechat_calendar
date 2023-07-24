'''
电话通知类
'''
import logging

# 43505601
# key: FTfcF8wetpYOJbt3
from lib import itchat
from lib.itchat.utils import logger


def send_file(nickname,filepath):

    friend = itchat.search_friends(name=nickname)[0]['UserName']

    # 打印好友信息
    logger.info(friend)

    # Specify the file path of the voice message


    # Send the voice message to a specific user
     # Replace with the actual UserName of the recipient
    t = itchat.send_file(filepath, toUserName=friend)
    logger.info(t)




