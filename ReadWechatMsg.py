import threading
import time

from chat.chatgpt import ChatGpt
from chat.lib.itchat.utils import logger
from chat.mj.Mj_ext import mj
from chat.mulic import  music_search
from chat.mysqlrw import MysqlRw
from chat.chatgpttime import GptTime
from chat.wechat_server import WechatServer
from chat.youdao import translation
from chat.lib import itchat
from chat.lib.itchat.content import FRIENDS, TEXT, ATTACHMENT

'''
读取微信消息菜单类
'''





class ReadWechatMsg:
    translating = False  # 标记是否处于翻译状态
    flag = False
    # translate_text = ''  # 存储需要翻译的文本
    chatbots = {}  # 存储ChatGpt对象的字典

    def __init__(self, sql):
        self.sql = sql
        self.task_strings = []
        self.task_list = []




    # 图片对应itchat.content.PICTURE
    # 语音对应itchat.content.RECORDING
    # 名片对应itchat.content.CARD




    def run_file(self):

        @itchat.msg_register(itchat.content.ATTACHMENT)
        def file_reply(msg):
            try:
                if msg['Type'] == itchat.content.ATTACHMENT:
                    rt = WechatServer.download_files(msg)
                    return '我收到了你的课程表，正在检查是否成功\n' + rt
                else:
                    return 'Error'
            except Exception as e:
                return '课程表已存在，请勿重复创建\n' \
                       f'{str(e)}'

    def run_group_file(self):
        @itchat.msg_register(itchat.content.ATTACHMENT, isGroupChat=True)
        def group_file_reply(msg):
            if msg['Type'] == itchat.content.ATTACHMENT:
                rt = WechatServer.receive_group_file(msg)
                if rt is not None:
                    return '我收到了你的课程表，正在检查是否成功\n' + rt
                else:
                    return '文件保存失败'
            else:
                return 'Error'

    def run_test(self):
        @itchat.msg_register(itchat.content.TEXT)
        def text_reply(msg):
            # logger.info(msg)  获取发送者的所有信息
            nickname = msg['User']['NickName']
            username = msg['FromUserName']
            logger.info('用户名:{}：'.format(nickname))
            logger.info('用户ID:{}：'.format(username))

            # logger.info('微信号:{}'.format(msg['UserName']))

            fenge = ['--------------------------------------------\n', '--------------------------------------------']


            hello = f'{fenge[0]}{nickname} 你好呀😊，我是Server酱\n我可以帮你解答很多问题\n也可以当你的备忘录\n' \
                    f'比如明天早上8点叫我起床\n当然还有很多功能，如果想试试的话\n发送咒语:菜单\n{fenge[1]}'
            menum = f'{fenge[0]}' \
                    f'⏰ 1.创建定时任务提醒\n' \
                    f'⏰ 2 取消定时任务\n' \
                    f'⏰ 3 查看定时任务列表\n' \
                    f'⏰ 4 修改更新定时任务\n' \
                    f'📅 5 创建课程表\n' \
                    f'📅 6 删除课程表\n' \
                    f'📅 7 查看课程表\n' \
                    f'🔤 8 有道翻译\n' \
                    f'🛠 9 技术支持，人工服务\n' \
                    f'🎵 10 emo网易云\n' \
                    f'🎵 11 mj AI绘画\n' \
                    f'{fenge[1]}'


            time_task = f'{fenge[0]}⏰ 创建定时任务：\n注意：定时任务 时间 事件之间留有空格\n' \
                        '   格式：       时间      事件\n' \
                        '例如:定时任务 明天早上8点30 起床\n' \
                        '例如:定时任务 每天晚上11点 睡觉\n' \
                        f'例如:定时任务 每天早上七点 背单词\n' \
                        f'例如:定时任务 2023年7月24日下午5点 取快递\n' \
                        f'例如:定时任务 每周三下午五点 健身\n{fenge[1]}'

            author = f'{fenge[0]}作者:早睡不早起\n微信:X_special_s\n{fenge[1]}'

            title = "定时任务"
            msg_list = ['①.完成报告', '②.开会讨论', '③.处理邮件']
            details = "{}\n{}\n{}".format(msg_list[0], msg_list[1], msg_list[2])

            message = f" {title} ⏰⏰⏰⏰\n{fenge[0]}{details}\n" \
                      f"{fenge[1]}"
            deltle = '格式:\n删除任务：id\n' \
                     '格式:\n删除多项任务：id1 id2 id3..'

            update = f'格式:\n' \
                     f'更新任务时间：id 任务时间\n' \
                     f'更新任务事件：id 任务事件\n' \

            youdao = '有道翻译\n' \
                     '格式：\n' \
                     '有道：要翻译的内容\n' \
                     '或者\n' \
                     '翻译：要翻译的内容'

            music = '网易云歌曲搜索\n' \
                    '格式:\n'\
                    '点歌：歌手名或歌曲名\n'\
                    '点歌：周杰伦 烟花易冷\n' \
                    '网易云：最好的安排'
            deltle_user = '删除课程表:\n' \
                          '直接输入:：\n'\
                          '删除课程表'

            show_calendar = '查询课程信息：\n' \
                            '格式：\n' \
                            '查询课程\n' \
                            '(如果不指定星期默认为今天)\n' \
                            '查询：1\n'\
                            '查询星期：7'




            # 获取好友的UserName，可以通过itchat.search_friends()方法获取好友列表，然后根据好友的备注名或昵称查找对应的UserName
            if msg['Text'] == '你好':
                return hello
            elif '11' == msg['Text']:
                server.send_calendar('绘画：提示词',nickname)
            elif '绘画：' in msg['Text']:
                pmomt = msg['Text'].split('：')[1]
                mj(pmomt,nickname)

            elif '每日英文阅读' in msg['Text']:
                words = msg['Text'].split('：')[1]
                logger.info(words)
                g = GptTime()

                return g.words_teachers(words=words)


            elif msg['Text'] == '5':
                WechatServer.send_file(nickname,'calendar.xlsx')
                return '按照模板填写后发送给我即可'
            elif msg['Text'] == '6':

                return f"{deltle_user}"

            elif msg['Text'] == '7':
                logger.info(nickname)
                return show_calendar
            elif '查询' in msg['Text']:
                if '：' in msg['Text']:
                    select_msg = int(msg['Text'].split('：')[1])
                    if 1 <= select_msg <= 7:
                        return sql.get_user_courses(nickname,select_msg)
                    else:
                        return '星期数不能小于1或大于7'
                else:
                    return sql.get_user_courses(nickname)

            elif '删除课程' in msg['Text']:
                user_id = sql.return_user_id(nickname)
                return sql.del_user_and_calendar(nickname)
            elif msg['Text'] == '菜单':
                return menum
            elif msg['Text'] == '1':
                return time_task
            elif msg['Text'] == '2':
                return deltle
            elif '删除任务' in msg['Text']:
                # 删除单项任务
                id = msg['Text'].split('：')[1]

                return self.sql.del_task(nickname, id)
            elif '删除多项任务' in msg['Text']:
                # 删除多项任务：10 11 12 13
                text = msg['Text'].split('：')[1]
                logger.info(text)
                id_list = text.split(" ")
                logger.info(id_list)

                return self.sql.del_task(nickname, id_list)
            elif msg['Text'] == '3':
                return self.sql.read_task(nickname)
            elif msg['Text'] == '4':
                return update

            elif '更新任务时间：' in msg['Text']:
                try:
                    update_str = msg['Text'].split('：')[1]
                    update_list = update_str.split(' ')
                    update_id = update_list[0]
                    update_time = update_list[1]
                    g = GptTime()
                    update_time = g.parse_time(update_time)
                    return self.sql.update_task(nickname, update_id, new_time=update_time)
                except Exception as e:
                    info = '解析时间出错，请检查格式是否正确\n错误原因:\n' + str(e)
                    logger.info(info)
                    return info

            elif '更新任务事件：' in msg['Text']:
                try:
                    update_str = msg['Text'].split('：')[1]
                    update_list = update_str.split(' ')
                    update_id = update_list[0]
                    update_event = update_list[1]
                    return self.sql.update_task(nickname, update_id, new_task=update_event)
                except Exception as e:
                    info = '解析事件出错，请检查格式是否正确\n错误原因:\n' + str(e)
                    logger.info(info)
                    return info

            elif msg['Text'] == '9':
                return author
            elif msg['Text'] == '任务':
                return message
            elif '定时任务' in msg['Text']:
                try:
                    time_l = msg['Text']
                    t = time_l.split(" ")[1]
                    task = time_l.split(" ")[2]
                    g = GptTime()
                    resuat = g.parse_time(t)
                    if isinstance(resuat, str):
                        print(resuat)
                        logger.info(resuat)
                        return self.sql.write_task(nickname, resuat, task)

                    elif isinstance(resuat, list):
                        s = ''
                        for i in resuat:
                            print(i)
                            s += i + ' '
                            # logger.info(s)
                        return s
                except Exception as e:
                    info = '解析时间出错，请检查格式是否正确,如格式正确，可重试一次\n错误原因:\n' + str(e)
                    logger.info(info)
                    return info
            elif msg['Text'] == '8':
                return youdao
            elif msg['Text'] == '10':
                return music

            elif '点歌：' in msg['Text'] or '网易云：' in msg['Text']:

                song = msg['Text'].split('：')[1]
                logger.info(song)
                r = music_search(song)
                logger.info(r)
                result = '\n'.join(r)
                return result

            elif '有道' in msg['Text'] or '翻译' in msg['Text']:
                # f = msg['Text'].split('：')[1]
                # logger.info(f)
                # y = YouDao(f)
                # return '翻译结果:' + y.translation()
                self.translating = True
                return '进入翻译模式，退出输入quit'
            elif '获取今日单词' in msg['Text']:
                word_list = sql.get_words(nickname)
                result = '\n'.join([f'{word[0]} {word[3]}' for word in word_list])

                lines = result.split('\n')
                lines = [line.strip() for line in lines if line.strip()]

                result = '\n'.join(lines)
                return result
            elif '我要背单词' in msg['Text']:
                return sql.word_user(nickname)

            elif self.translating:
                if msg['Text'] == 'quit':
                    self.translating = False
                    return '翻译结束'
                else:
                    translate_text = msg['Text']
                    logger.info(translate_text)
                    return '翻译结果:\n' + translation(translate_text)

            elif msg['Text'] == '背单词':
                self.flag = True
                return '进入背单词模式,推出输入:exit'

            elif self.flag:
                if msg['Text'] == 'exit':
                    self.translating = False
                    return '背单词结束'
                else:
                    translate_text = sql.check_words()
                    logger.info(translate_text)

                    g = GptTime()
                    g.check_word(translate_text)
                    return g.response

            else:
                username = nickname
                user_message = msg['Text']

                if username in self.chatbots:
                    chatbot = self.chatbots[username]
                else:
                    chatbot = ChatGpt()
                    self.chatbots[username] = chatbot

                reply = chatbot.send_message(user_message)
                logger.info(reply)
                return reply






        # content = Instnace.instance.MSGrequst(msg['Text'])
        #
        #
        # return content

    def run_group_test(self):
        @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
        def reply_group_message(msg):
            if msg['IsAt']:
                # Remove '@Wechat_Server' from the message text
                text = msg['Text'].replace('@Wechat_Server', ' ')
                logger.info(text)
                message_text = text.strip()

                logger.info(len(message_text))
                logger.info(message_text)
                # logger.info(msg)  获取发送者的所有信息
                nickname = msg['User']['NickName']
                username = msg['FromUserName']
                logger.info('用户名:{}：'.format(nickname))
                logger.info('用户ID:{}：'.format(username))

                # logger.info('微信号:{}'.format(msg['UserName']))

                fenge = ['--------------------------------------------\n',
                         '--------------------------------------------']


                hello = f'{fenge[0]}{nickname} 你好呀😊，我是Server酱\n我可以帮你解答很多问题\n也可以当你的备忘录\n' \
                        f'比如明天早上8点叫我起床\n当然还有很多功能，如果想试试的话\n发送咒语:菜单\n{fenge[1]}'
                menum = f'{fenge[0]}' \
                        f'⏰ 1.创建定时任务提醒\n' \
                        f'⏰ 2 取消定时任务\n' \
                        f'⏰ 3 查看定时任务列表\n' \
                        f'⏰ 4 修改更新定时任务\n' \
                        f'📅 5 创建课程表\n' \
                        f'📅 6 删除课程表\n' \
                        f'📅 7 查看课程表\n' \
                        f'🔤 8 有道翻译\n' \
                        f'🛠 9 技术支持，人工服务\n' \
                        f'🎵 10 emo网易云\n' \
                        f'🎵 11 mj AI绘画\n' \
                        f'{fenge[1]}'

                time_task = f'{fenge[0]}⏰ 创建定时任务：\n注意：定时任务 时间 事件之间留有空格\n' \
                            '   格式：       时间      事件\n' \
                            '例如:定时任务 明天早上8点30 起床\n' \
                            '例如:定时任务 每天晚上11点 睡觉\n' \
                            f'例如:定时任务 每天早上七点 背单词\n' \
                            f'例如:定时任务 2023年7月24日下午5点 取快递\n' \
                            f'例如:定时任务 每周三下午五点 健身\n{fenge[1]}'

                author = f'{fenge[0]}作者:早睡不早起\n微信:X_special_s\n{fenge[1]}'

                title = "定时任务"
                msg_list = ['①.完成报告', '②.开会讨论', '③.处理邮件']
                details = "{}\n{}\n{}".format(msg_list[0], msg_list[1], msg_list[2])

                message = f" {title} ⏰⏰⏰⏰\n{fenge[0]}{details}\n" \
                          f"{fenge[1]}"
                deltle = '格式:\n删除任务：id\n' \
                         '格式:\n删除多项任务：id1 id2 id3..'

                update = f'格式:\n' \
                         f'更新任务时间：id 任务时间\n' \
                         f'更新任务事件：id 任务事件\n' \

                youdao = '有道翻译\n' \
                                 '格式：\n' \
                                 '有道：要翻译的内容\n' \
                                 '或者\n' \
                                 '翻译：要翻译的内容'

                music = '网易云歌曲搜索\n' \
                        '格式:\n' \
                        '点歌：歌手名或歌曲名\n' \
                        '点歌：周杰伦 烟花易冷\n' \
                        '网易云：最好的安排'
                deltle_user = '删除课程表:\n' \
                              '直接输入:：\n' \
                              '删除课程表'

                show_calendar = '查询课程信息：\n' \
                                '格式：\n' \
                                '查询课程\n' \
                                '(如果不指定星期默认为今天)\n' \
                                '查询：1\n' \
                                '查询星期：7'
                use_group_user = "指定被@的群成员\n" \
                                 "格式:\n" \
                                 "指定@成员：@成员1 @成员2 @成员3..."

                # 获取好友的UserName，可以通过itchat.search_friends()方法获取好友列表，然后根据好友的备注名或昵称查找对应的UserName
                if message_text == '你好':
                    return hello
                elif message_text == '5':
                    WechatServer.send_file_to_group(nickname, 'calendar.xlsx')
                    return '按照模板填写后发送给我即可'
                elif message_text == '6':

                    return f"{deltle_user}"
                elif '指定群成员'  == message_text:
                    return use_group_user
                elif '指定@成员' in message_text:
                    users = message_text.split('：')[1]
                    logger.info(users)
                    user_id = sql.return_user_id(nickname)

                    return sql.use_users(users,user_id)
                elif message_text == '查询@群成员':
                    return sql.get_group_users(user_id=sql.return_user_id(nickname)[0])

                elif message_text == '7':
                    logger.info(nickname)
                    return show_calendar
                elif '查询' in message_text:
                    if '：' in message_text:
                        select_msg = int(message_text.split('：')[1])
                        if 1 <= select_msg <= 7:
                            return sql.get_user_courses(nickname, select_msg)
                        else:
                            return '星期数不能小于1或大于7'
                    else:
                        return sql.get_user_courses(nickname)

                elif '删除课程' in message_text:
                    user_id = sql.return_user_id(nickname)
                    return sql.del_user_and_calendar(nickname)
                elif message_text == '菜单':
                    return menum
                elif message_text == '1':
                    return time_task
                elif message_text == '2':
                    return deltle
                elif '删除任务' in message_text:
                    # 删除单项任务
                    id = message_text.split('：')[1]

                    return self.sql.del_task(nickname, id)
                elif '删除多项任务' in message_text:
                    # 删除多项任务：10 11 12 13
                    text = message_text.split('：')[1]
                    logger.info(text)
                    id_list = text.split(" ")
                    logger.info(id_list)

                    return self.sql.del_task(nickname, id_list)
                elif message_text == '3':
                    return self.sql.read_task(nickname)
                elif message_text == '4':
                    return update

                elif '更新任务时间：' in message_text:
                    try:
                        update_str = message_text.split('：')[1]
                        update_list = update_str.split(' ')
                        update_id = update_list[0]
                        update_time = update_list[1]
                        g = GptTime()
                        update_time = g.parse_time(update_time)
                        return self.sql.update_task(nickname, update_id, new_time=update_time)
                    except Exception as e:
                        info = '解析时间出错，请检查格式是否正确\n错误原因:\n' + str(e)
                        logger.info(info)
                        return info

                elif '更新任务事件：' in message_text:
                    try:
                        update_str = message_text.split('：')[1]
                        update_list = update_str.split(' ')
                        update_id = update_list[0]
                        update_event = update_list[1]
                        return self.sql.update_task(nickname, update_id, new_task=update_event)
                    except Exception as e:
                        info = '解析事件出错，请检查格式是否正确\n错误原因:\n' + str(e)
                        logger.info(info)
                        return info

                elif message_text == '9':
                    return author
                elif message_text == '任务':
                    return message
                elif '定时任务' in message_text:
                    try:
                        time_l = message_text
                        t = time_l.split(" ")[1]
                        task = time_l.split(" ")[2]
                        g = GptTime()
                        resuat = g.parse_time(t)
                        if isinstance(resuat, str):
                            print(resuat)
                            logger.info(resuat)
                            return self.sql.write_task(nickname, resuat, task)

                        elif isinstance(resuat, list):
                            s = ''
                            for i in resuat:
                                print(i)
                                s += i + ' '
                                # logger.info(s)
                            return s
                    except Exception as e:
                        info = '解析时间出错，请检查格式是否正确,如格式正确，可重试一次\n错误原因:\n' + str(e)
                        logger.info(info)
                        return info
                elif message_text == '8':
                    return youdao
                elif message_text == '10':
                    return music

                elif '点歌：' in msg['Text'] or '网易云：' in msg['Text']:

                    song = message_text.split('：')[1]
                    logger.info(song)
                    r = music_search(song)
                    logger.info(r)
                    result = '\n'.join(r)
                    return result

                elif '有道' in message_text or '翻译' in message_text:
                    # f = msg['Text'].split('：')[1]
                    # logger.info(f)
                    # y = YouDao(f)
                    # return '翻译结果:' + y.translation()
                    self.translating = True
                    return '进入翻译模式，退出输入quit'
                elif '获取今日单词' in message_text:
                    word_list = sql.get_words(nickname)
                    result = '\n'.join([f'{word[0]} {word[3]}' for word in word_list])

                    lines = result.split('\n')
                    lines = [line.strip() for line in lines if line.strip()]


                    result = '\n'.join(lines)
                    return result
                elif '我要背单词' in message_text:
                    return sql.word_user(nickname)



                elif self.translating:
                    if message_text == 'quit':
                        self.translating = False
                        return '翻译结束'
                    else:
                        translate_text = message_text
                        logger.info(translate_text)
                        return '翻译结果:\n' + translation(translate_text)
                else:
                    username = nickname
                    user_message = message_text

                    if username in self.chatbots:
                        chatbot = self.chatbots[username]
                    else:
                        chatbot = ChatGpt()
                        self.chatbots[username] = chatbot

                    reply = chatbot.send_message(user_message)
                    logger.info(reply)
                    return reply

if __name__ == '__main__':
    server = WechatServer()
    sql = MysqlRw()
    r = ReadWechatMsg(sql)


    itchat_thread = threading.Thread(target=itchat.run)
    itchat_thread.setDaemon(True)  # 将线程设置为后台线程
    itchat_thread.start()

    r_thread = threading.Thread(target=r.run_test)
    r_thread.setDaemon(True)

    r_thread.start()

    group = threading.Thread(target=r.run_group_test)
    group.setDaemon(True)

    group.start()

    run_f = threading.Thread(target=r.run_file)
    run_f.setDaemon(True)

    run_f.start()

    check_mysql = threading.Thread(target=sql.check_time_tasks)
    check_mysql.setDaemon(True)
    check_mysql.start()
    time.sleep(5)

    send_cal = threading.Thread(target=sql.check_calendar_time)
    send_cal.setDaemon(True)
    send_cal.start()



    run_g = threading.Thread(target=r.run_group_file)
    run_g.setDaemon(True)
    run_g.start()


    itchat_thread.join()
    check_mysql.join()
    send_cal.join()
    run_g.join()

