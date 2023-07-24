# -*- coding: utf-8 -*-
import datetime

import chat.mysqlrw
from chat import mysqlrw
from chat.lib import itchat



import sys
import io

from chat.lib.itchat.utils import logger



sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')





# 微信发送类

class WechatServer:
    __server = None
    sent_tasks = set()  # 记录已发送的任务ID
    user_id = 1

    def __new__(cls, *args, **kwargs):
        if cls.__server is None:
            cls.__server = super(WechatServer, cls).__new__(cls)
        return cls.__server

    def __init__(self):
        # self.nickname = nickname
        # self.msg = msg

        self.Msg_list = []
        self.startup()


        # self.find_friend(msg)
        # itchat.run()

    # def find_friend(self,msg):
    #     """
    #         用于查找传入微信号是否在好友列表中
    #         :param nickname: 好友昵称
    #         :return: None
    #         """
    #     friends = itchat.get_friends()
    #     for i in friends:
    #         print(f"微信名称：{i['NickName']}微信号:{i['UserName']}")
    #
    #     nickname_list = [friend['NickName'] for friend in friends]
    #     print(nickname_list)
    #     print(self.nickname in nickname_list)
    #     if self.nickname in nickname_list:
    #
    #         print("好友在列表中")
    #         self.friend(msg)
    #     else:
    #         print("好友不在列表中")

    def friend(self, msg, nickname):
        """
            传入好友昵称，发送消息
            :param f_username: 昵称
            :param msg: 消息内容
            :return: None
            """
        print(nickname)
        friend = itchat.search_friends(name=nickname)[0]
        itchat.send_image('emjo.jpg', toUserName=friend['UserName'])
        itchat.send(msg, toUserName=friend['UserName'])



    def startup(slef):
        itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
        itchat.auto_login(
            enableCmdQR=0,
            hotReload=True,
            statusStorageDir='itchat.pkl',
            # qrCallback=qrCallback,
            loginCallback=slef.login_callback,
            exitCallback=slef.logout_callback
        )
        user_id = itchat.instance.storageClass.userName
        name = itchat.instance.storageClass.nickName
        logger.info("微信登录成功 login success, 用户Id: {}, 用户名: {}".format(user_id, name))

    def login_callback(self):
        logger.info('--------------Hello---------------')

    def logout_callback(self):
        logger.info('Logout')
        self.startup()





    @classmethod
    def send_file(self, nickname, filepath):

        friend = itchat.search_friends(name=nickname)[0]['UserName']

        # 打印好友信息
        logger.info(friend)
        t = itchat.send_file(filepath, toUserName=friend)
        logger.info(t)

    @classmethod
    def send_image(self, nickname):

        friend = itchat.search_friends(name=nickname)[0]




        # 打印好友信息
        logger.info(friend)
        t = itchat.send_image('output.png', toUserName=friend['UserName'])
        logger.info(t)


    @classmethod
    def send_file_to_group(cls, group_name, file_path):
        chatrooms = itchat.search_chatrooms(name=group_name)
        if chatrooms:
            group_username = chatrooms[0]['UserName']

            itchat.send_file(file_path, toUserName=group_username)
            return '文件发送成功'
        else:
            return '未找到该群聊'

    # 下载文件到本地


    @classmethod
    def download_files(cls, msg):
        try:
            s = msg.download(f"finish{msg['FileName']}")
            logger.info(s)
            m = mysqlrw.MysqlRw()
            nickname = msg['User']['NickName']
            wechat_id = msg['FromUserName']
            # 获取当前日期
            today = datetime.date.today()

            # 计算本周的周一日期
            start_week_time = today - datetime.timedelta(days=today.weekday())
            rerest = m.mkdir_user(nickname, wechat_id, start_week_time)

            if rerest != None:
                logger.info(rerest)
                hh = m.read_excel(rerest,f"finish{msg['FileName']}")
                inner_tuple = rerest[0]  # 提取内部元组
                integer_value = inner_tuple[0]  # 提取整数值
                integer_result = int(integer_value)  # 将整数值转换为整数类型

                r = f"课表id:{integer_result}\n{hh}"

                logger.info('保存成功')

                return r
            else:
                return '课程表已经存在，请勿重复创建'
        except Exception as e:
            logger.info(e)

    @classmethod
    def receive_group_file(cls, msg):
        try:
            file_path = f"finish{msg['FileName']}"
            msg.download(file_path)
            logger.info(f"文件保存成功，路径：{file_path}")

            m = mysqlrw.MysqlRw()
            nickname = msg['User']['NickName']
            wechat_id = msg['FromUserName']

            today = datetime.date.today()
            start_week_time = today - datetime.timedelta(days=today.weekday())
            rerest = m.mkdir_user(nickname, wechat_id, start_week_time)



            if rerest is not None:
                logger.info(rerest)
                hh = m.read_excel(rerest,file_path)
                inner_tuple = rerest[0]
                integer_value = inner_tuple[0]
                integer_result = int(integer_value)

                r = f"课表id:{integer_result}\n{hh}"
                logger.info('保存成功')

                return r
            else:
                return '课程表已经存在，请勿重复创建'
        except Exception as e:
            logger.info('文件保存失败{}'.format(e))
            return None

    @classmethod
    def send_msg(self, msg, nickname):
        try:

                friend = itchat.search_friends(name=nickname)[0]
                itchat.send(msg=msg, toUserName=friend['UserName'])



        except Exception:

                chatrooms = itchat.search_chatrooms(name=nickname)
                if chatrooms:
                    for chatroom in chatrooms:
                        if chatroom['NickName'] == nickname:
                            logger.info("群聊名称: %s", chatroom['NickName'])
                            logger.info("群聊ID: %s", chatroom['UserName'])
                            # 发送消息到该群聊
                            # itchat.send(msg=msg, toUserName=chatroom['UserName'])
                            sql = chat.mysqlrw.MysqlRw()
                            at_user = sql.get_group_users(user_id=sql.return_user_id(nickname)[0])
                            itchat.send(msg=at_user + ' ' + msg, toUserName=chatroom['UserName'])


                else:
                    logger.info("未找到群聊:%s", nickname)


    @classmethod
    def send_task(self, task_id, msg, nickname):
        try:
            if task_id not in self.sent_tasks:
                friend = itchat.search_friends(name=nickname)[0]
                itchat.send(msg=msg, toUserName=friend['UserName'])

                self.sent_tasks.add(task_id)

        except Exception:
            if task_id not in self.sent_tasks:
                chatrooms = itchat.search_chatrooms(name=nickname)
                if chatrooms:
                    for chatroom in chatrooms:
                        if chatroom['NickName'] == nickname:
                            logger.info("群聊名称: %s", chatroom['NickName'])
                            logger.info("群聊ID: %s", chatroom['UserName'])
                            # 发送消息到该群聊
                            # itchat.send(msg=msg, toUserName=chatroom['UserName'])
                            sql = chat.mysqlrw.MysqlRw()
                            at_user = sql.get_group_users(user_id=sql.return_user_id(nickname)[0])
                            itchat.send(msg=at_user + ' ' + msg, toUserName=chatroom['UserName'])
                    self.sent_tasks.add(task_id)

                else:
                    logger.info("未找到群聊:%s", nickname)

    @classmethod
    def send_calendar(self, msg, nickname, isgroup=None):
        try:

                friend = itchat.search_friends(name=nickname)[0]
                itchat.send(msg=msg, toUserName=friend['UserName'])



        except Exception:
                chatrooms = itchat.search_chatrooms(name=nickname)
                if chatrooms:
                    for chatroom in chatrooms:
                        if chatroom['NickName'] == nickname:
                            logger.info("群聊名称: %s", chatroom['NickName'])
                            logger.info("群聊ID: %s", chatroom['UserName'])
                            # 发送消息到该群聊
                            # itchat.send(msg=msg, toUserName=chatroom['UserName'])
                            m = chat.mysqlrw.MysqlRw()
                            at_user = m.get_group_users(m.return_user_id(nickname))
                            itchat.send(msg=at_user + ' ' + msg, toUserName=chatroom['UserName'])


                else:
                    logger.info("未找到群聊:%s", nickname)

