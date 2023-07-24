import datetime
import json
import random
import re
import time


import pandas as pd
import pymysql

import chat.wechat_server
from chat.lib.itchat.utils import logger


class MysqlRw:
    # 读取配置文件
    with open('config.json') as f:
        config_data = json.load(f)
    mysql_host = config_data['mysql_host']
    mysql_username = config_data['mysql_username']
    mysql_password = config_data['mysql_password']
    mysql_databases = config_data['mysql_databases']


    def __init__(self):
        self.connection = None
        self.outcome = []
        self.reusest = None


    def connect_mysql(self):
        try:
            # 创建连接对象
            connection = pymysql.connect(
                host=self.mysql_host,  # 数据库主机地址
                user=self.mysql_username,  # 数据库用户名
                password=self.mysql_password,  # 数据库密码
                database=self.mysql_databases,  # 数据库名称
                charset = 'utf8'
            )

            # 创建游标对象
            cursor = connection.cursor()
            return cursor
        except Exception as e:
            logger.info(f'数据库连接失败{e}')



    def close_mysql(self):
        if self.connection:
            # 关闭连接
            self.connection.close()
            logger.info('关闭数据库连接')


    def check_expired_tasks(self):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()

            # 执行查询操作，选择所有过期的任务
            result = self.select('TimeTask',None,'id, sleep_time')

            current_time = datetime.datetime.now()

            for row in result:
                task_id = row[0]
                sleep_time = row[1]

                if sleep_time.startswith('EveryDay '):
                    # 跳过带有 "EveryDay" 标记的任务
                    continue
                else:
                    # 日期时间格式
                    task_datetime = datetime.datetime.strptime(sleep_time, '%Y-%m-%d %H:%M')

                # 检查任务是否过期
                if current_time > task_datetime + datetime.timedelta(minutes=3):
                    # 执行删除操作
                    delete_query = "DELETE FROM TimeTask WHERE id = %s"
                    cursor.execute(delete_query, (task_id,))
                    cursor.connection.commit()
                    logger.info(task_id)

            # 关闭游标
            cursor.close()

        except pymysql.Error as error:
            self.reusest = "执行过期任务检查时发生错误：" + str(error)

            return self.reusest


    def check_time_tasks(self):
        logger.info('------------->check_time_tasks')
        global user_name
        while True:

            try:
                self.check_expired_tasks()
                # 执行查询操作，选择所有任务
                result = self.select('TimeTask',None,'id,username, sleep_time, event')


                for row in result:
                    # 清理过期任务
                    task_id = row[0]
                    user_name = row[1]
                    sleep_time = row[2]
                    event = row[3]

                    if sleep_time.startswith('EveryDay'):
                        current_time = datetime.datetime.now().strftime('%H:%M')
                        target_time = datetime.datetime.strptime(sleep_time.split(' ')[1], '%H:%M').strftime('%H:%M')
                        if current_time == target_time:
                            self.reusest = f'{user_name} \n时间到了:{sleep_time}\n该提醒你: {event}了'
                            logger.info(self.reusest)
                            self.send_message_to_friend(task_id, self.reusest, nickname=user_name)
                    else:
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                        if current_time == sleep_time:
                            self.reusest = f'{user_name} \n时间到了:{sleep_time}\n该提醒你: {event}了'
                            logger.info(self.reusest)
                            self.send_message_to_friend(task_id, self.reusest, nickname=user_name)


            except pymysql.Error as error:
                self.reusest = "执行查询任务时发生错误：" + str(error)

                self.send_clandar(self.reusest, nickname=user_name)


            # 每隔一段时间检查一次
            time.sleep(30)  # 60秒 = 1分钟


    def send_message_to_friend(self, task_id, message, nickname):
        chat.wechat_server.WechatServer.send_task(task_id, message, nickname)

    # 根据用户名取出事件 详情

    def read_task(self, nickname):
        try:
            cursor = self.connect_mysql()
            query = "SELECT id, sleep_time, event FROM TimeTask WHERE username = %s"
            cursor.execute(query, (nickname,))
            result = cursor.fetchall()

            if result:
                self.task_list = list(result)
                result_strings = [
                    '\t'.join(str(info) + ' ' * (12 if re.match(r'\d{2}:\d{2}', str(info)) else 1) for info in task)
                    for task in result]
                result_string = '\n'.join(result_strings)



                title = "id       日期         事件\n"

                return title + result_string
            else:
                self.reusest = "没有查询到当前用户定时任务，快去创建吧"

                return self.reusest


        except pymysql.Error as error:
            self.reusest = '执行读取时发生错误，请联系管理员'
            return self.reusest

    # 写入定时任务
    def write_task(self, nick_name, task_time, task):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()
            title = "id       日期         事件\n"

            # 检查是否存在相同的记录
            query = "SELECT COUNT(*) FROM TimeTask WHERE UserName = %s AND sleep_time = %s AND event = %s"
            values = (nick_name, task_time, task)
            cursor.execute(query, values)
            count = cursor.fetchone()[0]

            if count > 0:
                self.reusest = "已经有相同的任务了哦，请勿重复创建"
                return self.reusest

            # 执行写入操作
            query = "INSERT INTO TimeTask (UserName, sleep_time, event) VALUES (%s, %s, %s)"
            values = (nick_name, task_time, task)
            cursor.execute(query, values)
            cursor.connection.commit()

            # 获取插入后的数据
            query = "SELECT  id,sleep_time,event FROM TimeTask WHERE UserName = %s AND sleep_time = %s AND event = %s"
            values = (nick_name, task_time, task)
            cursor.execute(query, values)
            inserted_row = cursor.fetchone()

            # 关闭游标
            cursor.close()

            self.reusest = "定时任务创建成功\n" + title + f"{inserted_row[0]}   {inserted_row[1]}   {inserted_row[2]}"
            return self.reusest

        except pymysql.Error as error:
            self.reusest = "执行写入操作时发生错误：\n" + str(error)
            return self.reusest

    # 更新定时任务
    def update_task(self, username, id, new_time=None, new_task=None):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()
            title = "id       日期         事件\n"

            # 检查是否存在匹配的记录
            query = "SELECT COUNT(*) FROM TimeTask WHERE id = %s AND UserName = %s"
            values = (id, username)
            cursor.execute(query, values)
            count = cursor.fetchone()[0]

            if count == 0:
                self.reusest = "未查询到任务Id或任务Id不属于当前用户"
                return self.reusest

            if new_task is None and new_time is None:
                self.reusest = "未提供新任务或新时间，无需更新"
                return self.reusest

            if new_task is None:
                # 只更新时间
                query = "UPDATE TimeTask SET sleep_time = %s WHERE id = %s"
                values = (new_time, id)
            elif new_time is None:
                # 只更新任务
                query = "UPDATE TimeTask SET event = %s WHERE id = %s"
                values = (new_task, id)
            else:
                # 同时更新任务和时间
                query = "UPDATE TimeTask SET event = %s, sleep_time = %s WHERE id = %s"
                values = (new_task, new_time, id)

            # 执行更新操作
            cursor.execute(query, values)
            cursor.connection.commit()

            # 获取更新后的数据
            query = "SELECT * FROM TimeTask WHERE id = %s"
            value = id
            cursor.execute(query, value)
            updated_row = cursor.fetchone()

            # 关闭游标
            cursor.close()

            self.reusest = "任务更新成功\n" + title + f"{updated_row[0]}   {updated_row[1]}   {updated_row[2]}"
            return self.reusest

        except pymysql.Error as error:
            self.reusest = "执行更新操作时发生错误:" + str(error)
            return self.reusest

    # 删除定时任务
    def del_task(self, username, id):
        global result_string
        try:
            # 创建游标对象
            cursor = self.connect_mysql()
            title = "id       日期         事件\n"
            deleted_data = ""

            if isinstance(id, list):
                for task_id in id:
                    query = "SELECT COUNT(*) FROM TimeTask WHERE id = %s AND UserName = %s"
                    values = (task_id, username)
                    cursor.execute(query, values)
                    count = cursor.fetchone()[0]

                    if count == 0:
                        self.reusest = f"未查询到任务Id {task_id} 或任务Id不属于当前用户"
                        return self.reusest

                    query = "SELECT id,sleep_time,event FROM TimeTask WHERE id = %s"
                    value = task_id
                    cursor.execute(query, value)
                    deleted_row = cursor.fetchone()

                    query = "DELETE FROM TimeTask WHERE id = %s"
                    value = task_id
                    cursor.execute(query, value)
                    cursor.connection.commit()

                    deleted_data += f"{deleted_row[0]}   {deleted_row[1]}   {deleted_row[2]}\n"

                self.reusest = "删除成功\n" + title + deleted_data
                cursor.close()
                return self.reusest

            else:
                query = "SELECT COUNT(*) FROM TimeTask WHERE id = %s AND UserName = %s"
                values = (id, username)
                cursor.execute(query, values)
                count = cursor.fetchone()[0]

                if count == 0:
                    self.reusest = f"未查询到任务Id或任务Id不属于当前用户"
                    return self.reusest

                # 获取被删除的数据
                query = "SELECT * FROM TimeTask WHERE id = %s"
                value = id
                cursor.execute(query, value)
                deleted_row = cursor.fetchone()

                # 执行删除操作
                query = "DELETE FROM TimeTask WHERE id = %s"
                value = id
                cursor.execute(query, value)
                cursor.connection.commit()
                cursor.close()

                self.reusest = f"删除成功\n" + title + f"{deleted_row[0]}   {deleted_row[1]}   {deleted_row[2]}"
                return self.reusest

        except pymysql.Error as error:
            self.reusest = "执行删除操作时发生错误：" + str(error)
            return self.reusest

    # 获取课程时间
    def return_time(self, course_id):

        # 创建游标对象

        # 拿到课程的星期信息
        result = self.select('schedule', f'course_id = {course_id}', 'start_time,end_time')
        for row in result:
            time_row = datetime.datetime.today() - datetime.timedelta(minutes=-15)  # 提前十五分钟

            # 保留开始时间时分
            row_time = datetime.datetime.strptime(str(row[0]), "%H:%M:%S")
            row_minutes = row_time.strftime("%H:%M")

            # 保留结束时间时分
            end_time = datetime.datetime.strptime(str(row[1]), "%H:%M:%S")
            end_time = end_time - datetime.timedelta(minutes=-1)  # 将结束时间提前一分钟
            end_minutes = end_time.strftime("%H:%M")

            if time_row.strftime("%H:%M") == row_minutes:
                logger.info('时间匹配成功' + row_minutes)
                # 关闭游标
                return 1

            elif time_row.strftime("%H:%M") == end_minutes:
                logger.info('时间匹配成功' + end_minutes)
                # 关闭游标
                return 2

        return 0

    # 通过userid获取username
    def return_username(self, userid):
        # 创建游标对象
        cursor = self.connect_mysql()

        # 执行查询操作
        query = "SELECT username FROM user where user_id = {}".format(userid)
        cursor.execute(query)
        result = cursor.fetchone()
        # 关闭游标
        cursor.close()
        return result

    # 通过username获取userid
    def return_user_id(self, username):
        # 创建游标对象
        cursor = self.connect_mysql()

        # 执行查询操作
        query = "SELECT user_id FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        logger.info(result)
        # 关闭游标
        cursor.close()

        return result

    # 通过userid获取用户的开始周数，计算现在是第几周
    def return_week(self, user_id):
        # 创建游标对象

        week_time = self.select('user', f'user_id = {user_id}', "start_week_time")

        # 检查是否有查询结果
        if week_time:
            we = week_time[0][0]

            today = datetime.datetime.today().strftime("%Y-%m-%d")

            # 将字符串类型的日期转换为 datetime 对象
            we_date = datetime.datetime.strptime(str(we), "%Y-%m-%d")
            today_date = datetime.datetime.strptime(today, "%Y-%m-%d")

            # 计算日期差值
            delta = today_date - we_date

            # 判断差值是否小于一周
            if delta.days < 7:
                diff = 1
            else:
                diff = delta.days // 7
                # 关闭游标

            # 打印结果
            return diff

        else:
            logger.error("No start_week_time found for the user.")


            return None

    # 获取今天是星期几并和每一个课程进行对比匹配
    def return_day_of_week(self, course_id):
        # 创建游标对象

        # 拿到课程的星期信息
        result = self.select('schedule', f'course_id = {course_id}', 'day_of_week')

        for row in result:

            today = datetime.datetime.today().weekday() + 1
            if today == 7:
                today = 0

            if today == row[0]:
                # 匹配成功
                return True

            else:
                # 没有匹配到
                return False

    # 获取每一门课程的星期几
    def return_today_week(self, user_id):

        # 拿到课程的星期信息
        result = self.select('schedule', f'user_id = {user_id}', 'day_of_week')

        for row in result:

            today = datetime.datetime.today().weekday() + 1


            if today == row[0]:



                return today

            else:



                return today

    # 通用查询方法
    def select(self,table, where=None, *args):
        try:
            # 创建连接对象
            connection = pymysql.connect(
                host=self.mysql_host,  # 数据库主机地址
                user=self.mysql_username,  # 数据库用户名
                password=self.mysql_password,  # 数据库密码
                database=self.mysql_databases,  # 数据库名称
                charset='utf8'
            )

            # 创建游标对象
            cursor = connection.cursor()


            if args:
                columns = ", ".join(args)  # 将列名连接成字符串
            else:
                columns = "*"

            if where:
                query = f"SELECT {columns} FROM {table} WHERE {where}"
            else:
                query = f"SELECT {columns} FROM {table}"


            cursor.execute(query)
            results = cursor.fetchall()
            # 关闭游标
            cursor.close()
            connection.close()

            # 提交事务

            return results
        except Exception as e:
            logger.info('查询失败{}'.format(e))

    # 获取每一条课程数据的单双周模式进行解析
    def return_list(self, course_id):


        # 数据
        user_week = self.select( 'schedule', f'course_id = {course_id}', 'week_pattern')

        output_list = []  # 初始化一个空列表
        for row in user_week:
            week = row[0].split('、')

            for item in week:
                if '-' in item:
                    start, end_info = item.split('-')
                    start = int(start)
                    if '单' in end_info:
                        end = int(end_info.replace('单', ''))
                        if end % 2 == 0:
                            end -= 1
                    elif '双' in end_info:
                        end = int(end_info.replace('双', ''))
                        if end % 2 != 0:
                            end -= 1
                    else:
                        end = int(end_info)
                    output_list.extend(range(start, end + 1))
                else:
                    output_list.append(int(item))


        return output_list

    # 检测当前时间是否与课程时间匹配，匹配就发送
    def check_calendar_time(self):
        logger.info('------------->check_calendar_time')
        while True:

            # 更新日历数据
            self.all_calendar = self.select(table='schedule')

            for cal in self.all_calendar:
                # course_id | user_id | course_name | day_of_week | start_time | end_time | teacher | location  | week_pattern
                course_id = cal[0]
                user_id = cal[1]
                course_name = cal[2]
                day_of_week = cal[3]
                start_time = cal[4]
                end_time = cal[5]
                teacher = cal[6]
                location = cal[7]
                week_pattern = cal[8]
                # 获取当前日期和开始日期是第几周

                week_num = self.return_week(user_id)


                week = self.return_list(course_id)

                if week_num in week:
                    flag = self.return_day_of_week(course_id)
                    if flag:
                        # 上课提醒
                        if self.return_time(course_id) == 1:
                            tool_msgs = [
                                "还有15分钟就要上课啦同学！🎒📚✏️",
                                "快点准备好，15分钟后上课开始啦！⏰📝🎉",
                                "小可爱，15分钟后上课，别忘了上课哦！👯‍♀️🎶📚",
                                "时间快到了，让我们一起去上课吧\n"
                                "15分钟后！🏃‍♀️📝🎒",
                                "上课时间快到啦！记得带上笑容和好心情哦\n"
                                "15分钟后！😄📚🎉",
                            ]
                            too = random.choice(tool_msgs)  # 随机选择一个消息返回

                            schedule_str = f"{too}\n" \
                                           f"课表ID：{user_id}\n" \
                                           f"课程：{course_name}\n" \
                                           f"星期：{day_of_week}\n" \
                                           f"教师：{teacher}\n" \
                                           f"地点：{location}\n" \
                                           f"周数：{week_pattern}\n" \
                                           f"上课时间：{start_time}\n" \
                                           f"下课时间：{end_time}\n"
                            nick_name = self.return_username(user_id)
                            logger.info('上课------------->触发')

                            self.send_clandar(schedule_str, nick_name[0])
                        elif self.return_time(course_id) == 2:
                            # 下课提醒

                            tool_msgs = [
                                "下课啦同学！🎉🎒🏠",
                                "课程结束啦~ 🎓🎉🌟",
                                "放学咯，开心回家！🚶‍♀️🌈🏡",
                                "下课时间到，休息一下吧~ ☕️🛋️😴",
                                "课程结束，可以休息一下眼睛啦~ 👀💤🌙",
                                "下课啦，记得整理好书包哦~ 🎒📚🧹",
                                "下课啦，可以和朋友们聊聊天啦~ 🗣️👯‍♀️😃",
                                "课程结束，可以放松一下身心啦~ 🧘‍♀️💆‍♂️🌸",
                            ]
                            too = random.choice(tool_msgs)  # 随机选择一个消息返回
                            end_schedule_str = f'{too}\n' \
                                               f'课程ID：{course_id}\n' \
                                               f'课程：{course_name}\n' \
                                               f'下课时间：{end_time}'
                            nick_name = self.return_username(user_id)
                            logger.info('下课------------->触发')
                            self.send_clandar(end_schedule_str, nick_name[0])
                        else:
                            pass

                else:

                    continue



            time.sleep(40)

    # 发送方法，匹配就发送
    def send_clandar(self, message, nickname):
        chat.wechat_server.WechatServer.send_calendar(message, nickname)

    # 通过下载后的excel会在这里进行读取解析并存入数据库
    def read_excel(self, user_id,filename):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()

            # 读取Excel文件
            df = pd.read_excel(filename)
            # 遍历每一行数据
            for index, row in df.iterrows():
                course_name = row['课程名称']
                day_of_week = row['星期']

                start_time_str = row['开始时间']  # Assuming row['开始时间'] is a string
                start_time = datetime.datetime.strptime(start_time_str, '%H:%M').strftime('%H:%M')

                end_time_str = row['结束时间']
                end_time = datetime.datetime.strptime(end_time_str, '%H:%M').strftime('%H:%M')

                teacher = row['老师']
                location = row['地点']
                week_pattern = row['单双周']

                # 将数据插入到schedule表格中
                sql = "INSERT INTO schedule (user_id, course_name, day_of_week, start_time, end_time, teacher, location, week_pattern) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (user_id, course_name, day_of_week, start_time, end_time, teacher, location, week_pattern)
                # 执行SQL语句，将数据插入数据库
                cursor.execute(sql, values)
                # 提交事务
                cursor.connection.commit()
                logger.info('保存成功')

            cursor.connection.commit()

            # 关闭游标和数据库连接
            cursor.close()

            return '保存成功！'
        except Exception as e:

            return '保存失败，请检查格式是否错误\n错误原因:' + str(e)


    # 创建课表用户
    def mkdir_user(self, nickname, wechat_id, start_week_time):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()

            # 检查是否存在相同的记录
            query = "SELECT COUNT(*) FROM user WHERE username = %s AND wechat_id = %s AND start_week_time = %s"
            values = (nickname, wechat_id, start_week_time)
            cursor.execute(query, values)
            count = cursor.fetchone()[0]

            if count > 0:
                self.reusest = "已经有相同的课程了哦，请勿重复创建"

                return self.reusest

            # 执行写入操作
            query = "INSERT INTO user (username, wechat_id, start_week_time) VALUES (%s, %s, %s)"
            values = (nickname, wechat_id, start_week_time)
            cursor.execute(query, values)


            # 提交事务
            cursor.connection.commit()

            reusest = (self.select( 'user', f"username = '{nickname}'", 'user_id'))



            cursor.close()
            return reusest

        except pymysql.Error as error:
            self.reusest = "执行写入操作时发生错误：\n" + str(error)
            return self.reusest

    # 指定群成员
    def use_users(self, users, user_id):
        try:
            cursor = self.connect_mysql()
            query = "UPDATE schedule SET isgroup = %s WHERE user_id = %s"

            values = (users, user_id)
            cursor.execute(query, values)

            # 提交更改
            cursor.connection.commit()
            return '指定成功，需要@的成员：\n' \
                   f'{users}'
        except Exception as e:
            return '指定失败，请重试！\n' \
                   f'{e}'

    # 获取被指定@的群成员
    def get_group_users(self,user_id):
        try:

            cursor = self.connect_mysql()
            query = f"SELECT isgroup FROM schedule WHERE user_id = '{user_id}' LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            logger.info(result)

            if result:
                result_str = str(result[0])
                return result_str
            else:
                return '没有指定成员'


        except Exception as e:
            return f'发生错误：{e}'


    #  删除课程表和用户
    def del_user_and_calendar(self, username):
        try:
            # 创建游标对象
            cursor = self.connect_mysql()

            select_user_id_sql = "SELECT user_id FROM user WHERE username = %s"
            cursor.execute(select_user_id_sql, (username,))
            user_id = cursor.fetchone()[0]

            # 删除schedule表中指定用户ID的数据
            delete_schedule_sql = "DELETE FROM schedule WHERE user_id = %s"
            cursor.execute(delete_schedule_sql, (user_id,))

            # 删除user表中指定用户name的数据
            delete_user_sql = "DELETE FROM user WHERE username = %s"
            cursor.execute(delete_user_sql, (username,))

            # 提交事务
            cursor.connection.commit()

            # 关闭游标
            cursor.close()

            return "用户和课程数据删除成功！"
        except Exception as e:
            return "删除用户和课程数据时发生错误：" + str(e)


    # 查询当前周某一天的课程
    def get_user_courses(self, username, day_of_week=None):
        try:
             # 创建游标对象
            cursor = self.connect_mysql()

            # 查询指定用户名的用户ID
            select_user_id_sql = "SELECT user_id FROM user WHERE username = %s"
            cursor.execute(select_user_id_sql, (username,))
            user_id = cursor.fetchone()

            if not user_id:
                return "找不到指定用户名的用户"

            # 构建查询条件
            if day_of_week is None:
                # 使用默认查询条件
                default_day_of_week = self.return_today_week(user_id[0])
                # 假设存在名为 return_today_week 的方法来获取当前星期几
                day_of_week = default_day_of_week

            # 查询用户指定星期的课程信息
            select_courses_sql = "SELECT course_name, day_of_week, start_time, end_time, teacher, location, week_pattern FROM schedule WHERE user_id = %s AND day_of_week = %s"
            cursor.execute(select_courses_sql, (user_id[0], day_of_week))
            courses = cursor.fetchall()



            if not courses:
                return f"星期{day_of_week}没有课程！"

            # 拼接课程信息字符串
            course_info = ""
            for course in courses:
                course_info += f"课程名称: {course[0]}\n"
                course_info += f"星期: {course[1]}\n"
                course_info += f"开始时间: {course[2]}\n"
                course_info += f"结束时间: {course[3]}\n"
                course_info += f"老师: {course[4]}\n"
                course_info += f"地点: {course[5]}\n"
                course_info += f"单双周: {course[6]}\n\n"

            # 关闭游标和连接
            cursor.close()
            return course_info
        except Exception as e:
            return "查询课程信息时发生错误：" + str(e)

    # 读取单词excel
    def read_word(self):
        cousor = self.connect_mysql()
        # 读取Excel文件
        df = pd.read_excel('专升本英语词汇40天一本通.xlsx')
        df = df.fillna('')  # 将所有的nan值替换为空字符串

        values = df.values
        values = [tuple(row) for row in values]


        insert_query = "INSERT INTO words (word, british_pronunciation, american_pronunciation, definition) VALUES (%s, %s, %s, %s)"
        for row in values:
            cousor.execute(insert_query, row)
        cousor.connection.commit()

    # 创建单词用户
    def word_user(self, username):
        try:
            cursor = self.connect_mysql()

            # 检查是否存在相同的用户名
            select_query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(select_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return existing_user[0]

            # 插入新用户
            insert_query = "INSERT INTO users (username) VALUES (%s)"
            values = (username,)
            cursor.execute(insert_query, values)
            cursor.connection.commit()

            return '创建成功'
        except Exception as e:
            return '创建失败，请重试或联系管理员\n' + str(e)

    # 获取10个单词
    def get_words(self, username):
        try:
            cursor = self.connect_mysql()
            user_query = f"SELECT current_word FROM users WHERE username = '{username}'"
            cursor.execute(user_query)
            user_result = cursor.fetchall()

            if user_result:
                current_word = user_result[0][0]

                word_query = f"SELECT * FROM words WHERE word = '{current_word}'"
                cursor.execute(word_query)
                word_result = cursor.fetchall()

                if word_result:
                    word_l = word_result[0][1]


                    # 获取符合条件的后面十条数据
                    ten_words_query = "SELECT * FROM words WHERE word >= %s LIMIT 10"
                    cursor.execute(ten_words_query, (word_l,))


                    ten_words = cursor.fetchall()
                    print(ten_words)
                    return ten_words
        except Exception as e:
            print(f"Error: {e}")
            return '获取失败，请重试或联系管理员\n' + str(e)

    # 保存用户分数
    def save_user_scoures(self,ten_words,user_id,score = 0,is_pass = 0):
       try:
           cursor = self.connect_mysql()
           query = "INSERT INTO user_word_scores (user_id,word_id,score,is_pass) VALUES (%s,%s,%s,%s)"
           for word in ten_words:
               word_id = word[0]
               values = (user_id, word_id, score, is_pass)
               cursor.execute(query, values)
               cursor.connection.commit()
           else:
               print('保存成功')
       except Exception as e:
           print('保存失败',e)



    # 随机单词
    def memorize_words(self, username):
        try:
            words = self.get_words(username)
            random_word = random.choice(words)
            # 返回给 check_words
            return random_word
        except Exception as e:
            print(f"Error: {e}")
            return '背单词失败，请重试或联系管理员\n' + str(e)

    # 检查单词是否通过
    def check_words(self):

        cursor = self.connect_mysql()
        query = "SELECT score FROM user_word_scores WHERE word_id = %s"


        random_word = self.memorize_words('早睡不早起')
        word_id = random_word[0]
        print('随机单词---->',random_word)
        cursor.execute(query,word_id)
        score = cursor.fetchone()[0]

        print('分数------>', score)
        if  4 > score <= 0:
            print('没有学会这个单词')








if __name__ == '__main__':
    m = MysqlRw()
    # m.read_word()
    print(m.word_user('早睡不早起'))
    m.check_words()

    print(m.return_user_id('白金瀚董事会')[0])

    # word_list = m.get_words('早睡不早起')
    # result = '\n'.join([f'{word[1]} {word[4]}' for word in word_list])
    #
    # lines = result.split('\n')
    # lines = [line.strip() for line in lines if line.strip()]
    #
    # result = '\n'.join(lines)
    #
    # print(result)
    # random_word = m.memorize_words('早睡不早起')
    # print(random_word)
    #
    # print(m.save_user_scoures(word_list,1))
    # m.read_task('早睡不早起')
    # m.write_task('早睡不早起','EveryDay 12:33','躺尸')
    # m.write_task('server','09:30','睡觉')
    # msg = m.update_task('早睡不早起',2,'打豆豆','2023-06-09 09:30')
    # print(msg)
    #
    # msg = m.del_task('早睡不早起',4)
    # print(msg)
    #

    # m.close_mysql()
    # msg = m.del_task('早睡不早起',["23" ,"31"])
    # print(msg)
    #
    # m.del_task('早睡不早起',21)
    # msg = m.read_task('早睡不早起')
    # print(msg)
    # m.write_task('早睡不早起','EveryDay 21:28','躺尸')
    #
    # m.check_time_tasks()

