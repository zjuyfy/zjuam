# zjuam
浙江大学统一身份认证登录

## 使用方法

1. 将jscode.py和zjuam.py放入工作目录下

2. 使用zjuam.py 中的 login class创建一个login实例

3. 使用login.session后续操作

##  example
- 登录统一身份认证后获取健康打卡页面

`import zjuam
username = '3000000000'
password = '123456789'
login1 = zjuam.login(username, password)
content=login1.session.get('https://healthreport.zju.edu.cn/ncov/wap/default/index')
print(content)`
