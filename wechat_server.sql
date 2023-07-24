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

-- wechat_server.schedule definition

CREATE TABLE `schedule` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `day_of_week` int(11) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `teacher` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `week_pattern` varchar(255) DEFAULT NULL,
  `isgroup` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=utf8;

-- wechat_server.`user` definition

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `wechat_id` varchar(255) DEFAULT NULL,
  `start_week_time` date DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;

-- wechat_server.user_word_scores definition

CREATE TABLE `user_word_scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `word_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `is_pass` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `word_id` (`word_id`),
  CONSTRAINT `user_word_scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_word_scores_ibfk_2` FOREIGN KEY (`word_id`) REFERENCES `words` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;

-- wechat_server.users definition

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `current_word` varchar(255) DEFAULT 'abandon',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


-- wechat_server.words definition

CREATE TABLE `words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(255) DEFAULT NULL,
  `british_pronunciation` varchar(255) DEFAULT NULL,
  `american_pronunciation` varchar(255) DEFAULT NULL,
  `definition` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15229 DEFAULT CHARSET=utf8;



