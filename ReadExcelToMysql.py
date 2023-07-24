import datetime
import time

import pymysql

from lib.itchat.utils import logger


def shared_connection(func):
    def wrapper(self, *args, **kwargs):
        if self.connection is None:
            self.connect_mysql()
        return func(self, *args, **kwargs)

    return wrapper


class MysqlRw:
    def __init__(self):
        self.connection = None
        self.outcome = []
        self.reusest = None
        self.all_calendar = None

    def connect_mysql(self):
        try:
            # 建立数据库连接
            self.connection = pymysql.connect(
                host="localhost",  # 数据库主机地址
                user="root",  # 数据库用户名
                password="root",  # 数据库密码
                database="wechat_server"  # 数据库名称
            )

            if self.connection:
                logger.info('已连接数据库')

        except pymysql.Error as error:
            logger.info("连接到 MySQL 数据库时发生错误：", error)

    def close_mysql(self):
        if self.connection:
            # 关闭连接
            self.connection.close()
            logger.info('关闭数据库连接')

    @shared_connection
    def check_calendar(self):

        # 创建游标对象
        cursor = self.connection.cursor()

        # 执行查询操作
        query = "SELECT week_pattern,user_id FROM schedule"
        cursor.execute(query)
        result = cursor.fetchall()

        # 拿到所有用户开始周数

        for row in result:
            week = row[0].split('、')
            userid = row[1]
            print('userid:')
            print(userid)

            weeks = int(self.return_week(userid))

            print('第几周：' + str(weeks))

            output_list = []
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
                    output_list.append(item)
            print('转换结果')
            print(output_list)

            if weeks in output_list:
                print('包含')

                msg, id = self.return_day_of_week(userid)
                if msg and id != None:
                    print('msg--->', msg)
                    nickname = self.return_username(id)
                    print('nickname--->', nickname)

            else:
                print('不包含')

    # @shared_connection
    # def return_day_of_week(self, userid):
    #     # 创建游标对象
    #     cursor = self.connection.cursor()
    #     # 查询当前userid所有的星期数
    #     query = "SELECT course_name, day_of_week, start_time, end_time, teacher, location, week_pattern, user_id FROM schedule where user_id = {}".format(
    #         userid)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     ret = []
    #     for row in result:
    #         print(row[1])
    #         today = datetime.datetime.today().weekday() + 1
    #         if today == 7:
    #             today = 0
    #
    #         print('今天是：' + str(today))
    #         if today == row[1]:
    #             print('成功匹配星期', row[1])
    #             time_row = datetime.datetime.today() - datetime.timedelta(minutes=-15)  # 提前十五分钟
    #             print('当前时间' + time_row.strftime("%H:%M"))
    #
    #             row_time = datetime.datetime.strptime(str(row[2]), "%H:%M:%S")
    #             row_minutes = row_time.strftime("%H:%M")
    #
    #             print('课程时间（小时和分钟）:', row_minutes)
    #
    #
    #             if time_row.strftime("%H:%M") == row_minutes:
    #                 print('时间匹配成功' + row_minutes)
    #                 # 拼接结果
    #                 result_str = "课程：{}，时间：{}，地点：{}，教师：{}".format(row[0], row_minutes, row[5], row[4])
    #                 print('匹配成功后的结果：', result_str)
    #                 ret.append(result_str)
    #                 return result_str,str(row[7])
    #
    #
    #
    #             else:
    #                 return None,None

    @shared_connection
    def return_time(self, course_id):

        # 创建游标对象
        cursor = self.connection.cursor()
        # 拿到课程的星期信息
        result = self.select(cursor, 'schedule', f'course_id = {course_id}', 'start_time,end_time')
        for row in result:

            time_row = datetime.datetime.today() - datetime.timedelta(minutes=-15)  # 提前十五分钟
            print('当前时间' + time_row.strftime("%H:%M"))

            row_time = datetime.datetime.strptime(str(row[0]), "%H:%M:%S")
            row_minutes = row_time.strftime("%H:%M")

            print('课程时间（小时和分钟）:', row_minutes)

            if time_row.strftime("%H:%M") == row_minutes:
                print('时间匹配成功' + row_minutes)

                return True
            else:

                return False


    @shared_connection
    def return_username(self, userid):
        # 创建游标对象
        cursor = self.connection.cursor()

        # 执行查询操作
        query = "SELECT username FROM user where user_id = {}".format(userid)
        cursor.execute(query)
        result = cursor.fetchone()

        return result


    @shared_connection
    def return_week(self, user_id):
        # 创建游标对象
        cursor = self.connection.cursor()
        week_time = self.select(cursor, 'user', f'user_id = {user_id}', "start_week_time")

        # 检查是否有查询结果
        if week_time:
            we = week_time[0][0]
            print(we)
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

            # 打印结果
            return diff
        else:
            logger.error("No start_week_time found for the user.")

            return None


    @shared_connection
    def return_day_of_week(self, course_id):
        # 创建游标对象
        cursor = self.connection.cursor()
        # 拿到课程的星期信息
        result = self.select(cursor, 'schedule', f'course_id = {course_id}', 'day_of_week')

        for row in result:
            print(row[0])
            today = datetime.datetime.today().weekday() + 1
            if today == 7:
                today = 0

            if today == row[0]:
                print('成功匹配星期', row[0])

                return True

            else:

                return False




    def select(self, cursor, table, where=None, *args):
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

        return results


    @shared_connection
    def return_list(self, course_id):
        cursor = self.connection.cursor()

        # 数据
        user_week = self.select(cursor, 'schedule', f'course_id = {course_id}', 'week_pattern')

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

        print('转换结果')
        print(output_list)
        return output_list

    @shared_connection
    def check_calendar_time(self):
        while True:
            # 创建游标对象
            cursor = self.connection.cursor()
            # 所有数据
            self.all_calendar = self.select(cursor=cursor, table='schedule')
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
                print("-----------------------------------------------------------")
                week_num = self.return_week(user_id)
                print(week_num)

                week = self.return_list(course_id)

                if week_num in week:
                    print('课表包含当前周', week_num)
                    if self.return_day_of_week(course_id):
                        if self.return_time(course_id):
                            self.send(course_name)

                else:
                    print('课表不包含当前周', week_num)
                    continue

            cursor.close()

            time.sleep(10)

    def send(self,msg):
        print(msg)

if __name__ == '__main__':
    m = MysqlRw()
    m.check_calendar_time()
