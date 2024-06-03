踩坑记录：
1.Drone SETTINGS 页面没有 Trusted
a：可以在地址栏看到登录的用户名http://192.168.31.137:8080/miaoxu1com/alpine-python，需要在docker-compose.ymal中添加
env=DRONE_USER_CREATE=username:yourUsername,admin:true

2.搭建gitea+drone使用ip地址
参考：https://blog.csdn.net/qq_46039856/article/details/135749459

3.搭建gitea+drone使用域名
参考：https://soulteary.com/2021/02/25/lightweight-code-warehouse-and-ci-usage-plan-in-docker-with-gitea-and-drone-part-1.html

4.drone不支持docker buildx命令构建只支持docker build，所以也不支持buildx特性比如mount-cache

