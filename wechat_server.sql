-- 检查数据库是否存在
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'wechat_server';

-- 如果数据库存在，则删除它
DROP DATABASE IF EXISTS wechat_server;

-- 创建数据库
CREATE DATABASE wechat_server;

-- 如果表存在，则删除它
DROP TABLE IF EXISTS TimeTask;

-- 创建表
CREATE TABLE TimeTask (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    sleep_time VARCHAR(16),
    event VARCHAR(255)
);

INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@Lᴏɴᴇʟʏ. 打飞机');
INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@轻触琴弦 打飞机');
INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@自由鱼. 打飞机');
INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@ㅤ ㅤ ㅤ ㅤ ㅤ 打飞机');
INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@Road killer ￡ 打飞机');
INSERT INTO TimeTask (username, sleep_time, event) VALUES ('白金瀚董事会', 'EveryDay 15:34', '@Healer 打飞机');

