# 配置项基类
class Config(object):
    # flask-sqlalchemy配置项
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True


# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = ''


# 测试环境配置
class TestingConfig(Config):
    TESTING = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = ''


# 生产环境配置
class ProductionConfig(Config):
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
