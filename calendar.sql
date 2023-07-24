# 1. 设计表结构：根据需求，可以创建两个表，一个用于存储用户信息，另一个用于存储日程信息。用户表可以包含字段如用户ID（主键）
# ，用户名，用户微信ID；日程表包含字段如日程ID（主键），用户ID（外键），开始时间，结束时间，地点，标题，描述。
USE wechat_server;
drop table schedule;
drop table user;
CREATE TABLE user (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255),
  wechat_id VARCHAR(255),
  start_week_time date
);


CREATE TABLE schedule (
  course_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  course_name VARCHAR(255),
  day_of_week INT,
  start_time TIME,
  end_time TIME,
  teacher VARCHAR(255),
  location VARCHAR(255),
  week_pattern VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

INSERT INTO schedule (course_id, user_id, course_name, day_of_week, start_time, end_time, teacher, location, week_pattern) VALUES (4, 2, '新课程', 4, '15:38', '16:35', '小李', '某地点', '3');
# 2. 设计表关系：在日程表中，将用户ID作为外键与用户表关联，这样可以方便地找到与某个用户相关的所有日程信息。

# 3. 设计索引：为了提高查询性能，可以为需要经常查询的字段创建索引，例如用户ID和开始时间等。

# 4. 设计约束：可以定义一些约束条件来确保数据的完整性和一致性，例如在用户表中设置用户名唯一约束，以防止重复用户名的出现。

# 5. 设计触发器：可以创建触发器来处理一些特定的业务逻辑，例如在插入或更新日程信息时，检查开始时间和结束时间的合法性等。

# 6. 设计视图：根据需求，可以创建一些视图来简化复杂的查询操作，例如一个视图可以显示某个用户的所有日程信息。