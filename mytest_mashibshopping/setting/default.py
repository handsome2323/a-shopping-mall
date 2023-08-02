#负责整个项目的配置信息


class Config():
    #配置数据库和sqlachime
    HOSTNAME = '127.0.0.1'
    PORT     = '3306'
    DATABASE = 'mytest'
    USERNAME = 'root'
    PASSWORD = 'root'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    # 把链接数据库的参数设置到app中
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False



 # 日志的配置
    LOGGING_LEVEL = 'INFO'
    LOGGING_FILE_DIR = 'logs/'
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024
    LOGGING_FILE_BACKUP = 100

    # 限流器采用Redis保存数据，默认是内存，需要安装flask-redis
    RATELIMIT_STORAGE_URL = 'redis://127.0.0.1:6379/1'
    # 限制策略：移动窗口：时间窗口会自动变化
    RATELIMIT_STRATEGY = 'moving-window'

    # redis数据库的连接地址,使用数据库1来存放缓存数据包括短信验证码
    REDIS_URL = "redis://127.0.0.1:6379/1"


#开发环境下的配置信息
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO =True #打印sql语句的


#生产环境中的配置信息

class ProductConfig(Config):
    pass


#把两个生产环境不同的配置和字符串映射起来

# map_config={
#     'develop':DevelopmentConfig,
#     'product':ProductConfig
# }