# 摘要
- 使用python manage.py runserver 即可运行
## 项目需求：
- 主页
    - 幻灯片显示最新房屋图片，可链接房屋详情页。 
    - 提供登陆/注册入口，登陆后显示用户名，点击可跳转至个人中心
    - 用户可以选择城区、入住时间、离开时间等条件进行搜索
    - 城区的区域信息动态加载
- 注册
    - 账号为手机号
    - 图片验证码正确后才能发送短信验证码，并且验证码只能用一次
    - 短信验证码每60秒才可发送一次
    - 每个条件出错时有相应错误提示
- 登陆
    - 用手机号与密码登陆
    - 错误时有相应提示
    - 错误超过五次封ip10分钟
- 退出
    - 点击用户名，提供退出接口
- 房屋列表页
    - 可根据进行筛选，排序
    - 房屋信息分页加载
    - 区域信息动态加载
    - 条件更新，页面更新
- 房屋详情页
    - 展示房屋所有信息及设施
    - 非房主本人提供预定入口
- 房屋预定
    - 由用户确定入住时间
    - 合计天数及总金额
- 我的爱家页面
    - 显示个人头像、手机号、用户名（未设置时默认为手机号）
    - 提供修改个人信息的入口
    - 提供作为房客下单的查询入口
    - 提供成为房东所需实名认证的入口
    - 提供作为房东发布房源入口
    - 提供作为房东查询客户订单的入口
    - 提供退出的入口
- 个人信息修改
    - 可以修改个人头像、用户名
    - 手机号不可修改
    - 上传头像与用户名分开保存
    - 上传新头像后立即更新显示
- 实名认证
    - 实名认证只可进行一次
    - 提交认证信息后再次进入只能查看信息，不能修改
- 我的房源
    - 未实名认证的用户不能发布新房源信息，需引导到实名认证页面
    - 按时间倒序显示已经发布的房屋信息
    - 点击房屋可以进入详情页面
- 发布新房源
    - 需要用户填写全部房屋信息
    - 房屋的文字信息与图片分开操作
- 客户订单（房东）
    - 按时间倒序显示用户下的订单
    - 对于新订单提供接单与拒单的功能
    - 拒单必须填写拒单原因
    - 若客户进行了订单评价，需显示
- 我的订单（房客）
    - 按时间倒序显示订单信息
    - 订单完成后提供评价功能
    - 已评价的订单能看到评价信息
    - 被拒绝的订单能看到拒单原因
## 项目技术概览
- 前后端分离
- bootstrap框架配合jquery等js插件搭建前端页面
- ajax完成前后端交互
- 路由遵循Restful风格
- 定制转换器，实现路由匹配参数支持正则
- sqlalchemy实现orm
- logging实现log日志记录功能
- 改变默认session存储，令其存入redis中
- redis
    - redis(7):用于验证码的存储；记录第一次获取验证码的时间；登录session存储；登录验证次数；房区信息的缓存;房屋列表页信息缓存（hash）；拒单原因及评论信息的缓存。
    - redis(6):用于存取celery任务队列
    - redis(5):用于存取broker返回的数据
- 验证码验证
    - uuid作为键以达到唯一标识
- celery异步短信验证（容联云）
    - 避免反复使用一个图片验证码进行校验。（在redis中查询之后，就将该值删除）
    - 在后端也要不允许60s内重复发送验证码
- 悲观锁处理订单并发 
- 注册
    - sha256加密密码,csrf验证。
- 装饰器解决登录状态验证问题
- 七牛云存储解决文件存储问题。
- 实名认证
    - 只有一次机会（-。-自己用正则造的实名认证）
- art-template模板引擎 实现模板渲染
- 支付宝实现订单支付（手机网站支付接口）
    - 采用return_url获取订单反馈信息，ajax异步上传信息，后台修改订单状态 
## 项目展示：
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/index.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/register.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/login.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/search.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/home.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/house.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/myhouse.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/personal.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/Realname.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/createnewhouse.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/order.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/pay.png)
![image](https://github.com/luola63702168/ihome/blob/master/obj_images/evaluate.png)












