import time
import requests
from calendar_wechat.mj.dowanload import download_image
from calendar_wechat.wechat_server import WechatServer
from lib.itchat.utils import logger

def send_to_msg(msg,nickname):
    if 'output.png' in msg:

        WechatServer.send_image(nickname)
        logger.info(nickname)
        logger.info(msg)
    else:
        WechatServer.send_msg(msg,nickname=nickname)


def mj(prompt,nickname):
    # 请求URL
    url = "https://api.zxx.im/v1/request"

    # 请求参数
    params = {
        "token": "26b7bfd9-98ab-4081-b743-4fc32d4d8b45",
        "fast": True,
        "action": "CREATE_IMAGE",
        "prompt": f"{prompt}"
    }

    # 发送POST请求
    response = requests.post(url, json=params)
    data = response.json()

    # 检查请求是否成功
    if response.status_code == 200 and data["success"]:
        # 获取任务ID
        task_id = data["result"]["taskId"]
        msg = "任务已创建，任务ID为:"+ task_id
        send_to_msg(msg,nickname)
        logger.info(msg)

        # 等待任务完成
        while True:
            # 请求任务结果
            result_url = f"https://api.zxx.im/v1/webhook/{task_id}"
            result_response = requests.get(result_url)
            result_data = result_response.json()

            if result_response.status_code == 200 and result_data["success"]:
                # 检查任务是否完成
                if result_data["result"]["status"] == 2:
                    # 获取图片URL
                    image_url = result_data["result"]["imageUrl"]
                    msg = "任务已完成，图片URL为:"+ image_url
                    logger.info(msg)
                    send_to_msg(msg,nickname)

                    # 下载图片
                    if download_image(image_url):

                        send_to_msg('output.png',nickname)

                        send_to_msg('绘画结束',nickname)
                        return


            # 等待一段时间后再次请求任务结果
            time.sleep(1)

    else:
        # 请求失败
        error_message = data["message"]
        msg = ("请求失败:", error_message)
        send_to_msg(msg,nickname)
        logger.info(msg)
