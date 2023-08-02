#把两个生产环境不同的配置和字符串映射起来

from .default import DevelopmentConfig,ProductConfig
map_config={
    'develop':DevelopmentConfig,
    'product':ProductConfig
}


