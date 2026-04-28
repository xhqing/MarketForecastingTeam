"""
Longport API 凭证配置模板

=============================================================================
文件功能：
    本文件是 Longport（长桥）API 的凭证配置模板。
    包含连接长桥行情API所需的三要素：
    - App Key
    - App Secret
    - Access Token

=============================================================================
使用方法：
    1. 复制本文件为 config.py
       cp config_example.py config.py

    2. 编辑 config.py，填入真实的API凭证
       LONGPORT_APP_KEY = "your_actual_app_key"
       LONGPORT_APP_SECRET = "your_actual_app_secret"
       LONGPORT_ACCESS_TOKEN = "your_actual_access_token"

    3. 确保 config.py 不被提交到git（已在.gitignore中排除）

=============================================================================
如何获取API凭证：
    1. 访问 Longport 开发者平台：https://open.longportapp.com
    2. 注册/登录账号
    3. 创建应用，获取 App Key 和 App Secret
    4. 申请行情权限，获取 Access Token

=============================================================================
配置项说明：

    LONGPORT_APP_KEY
        类型：字符串
        说明：长桥应用的App Key，用于标识应用身份
        示例：LONGPORT_APP_KEY = "lb_x9xxx"

    LONGPORT_APP_SECRET
        类型：字符串
        说明：长桥应用的App Secret，与App Key配对使用，用于签名验证
        示例：LONGPORT_APP_SECRET = "3Txxxxx"
        注意：App Secret是敏感信息，切勿泄露或提交到代码仓库

    LONGPORT_ACCESS_TOKEN
        类型：字符串
        说明：长桥行情API的访问令牌，用于获取实时行情数据权限
        示例：LONGPORT_ACCESS_TOKEN = "eyJxxxxx"
        注意：Access Token是敏感信息，切勿泄露或提交到代码仓库

=============================================================================
安全提示：
    ⚠️ 本文件（config.py）已通过 .gitignore 排除版本控制
    ⚠️ 切勿将真实的API凭证提交到git仓库
    ⚠️ 建议定期更换Access Token以提高安全性
    ⚠️ 不要在代码中硬编码凭证，应使用环境变量或配置文件

=============================================================================
权限说明：
    本项目需要以下行情数据权限：
    - 港股实时行情（指数、股票、ETF）
    - 美股实时行情（指数、ETF）
    - 日K线历史数据

=============================================================================
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

# Longport API 凭证配置
# 请将以下占位符替换为真实的API凭证

# App Key - 长桥应用标识
LONGPORT_APP_KEY = "your_app_key"

# App Secret - 长桥应用密钥（用于签名验证）
LONGPORT_APP_SECRET = "your_app_secret"

# Access Token - 行情数据访问令牌
LONGPORT_ACCESS_TOKEN = "your_access_token"
