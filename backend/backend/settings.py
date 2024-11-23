# settings.py

import os

# 添加媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 安全性配置
ALLOWED_HOSTS = ['*']  # 开发阶段使用，生产环境请设置具体域名
