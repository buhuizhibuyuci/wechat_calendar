import configparser
# 指定需要@的人
def write_config_file(group_name, at_users):
    config = configparser.ConfigParser()
    config[group_name] = {'at_users': ','.join(at_users)}

    with open('config.config', 'w' ,encoding='utf-8') as configfile:
        config.write(configfile)
write_config_file('白金瀚董事会',('早睡不早起',' ㅤ ㅤ ㅤ ㅤ ','轻触琴弦 '))

def read_config_file():
    config = configparser.ConfigParser()
    config.read('config.config',encoding='utf-8')

    groups = []
    for section in config.sections():
        group_name = section
        at_users = config.get(section, 'at_users').split(',')
        groups.append((group_name, at_users))

    return groups