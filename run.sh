#!/bin/sh
# 定义应用组名
group_name='auto-test'
# 定义应用名称
app_name='python-test'
# 定义应用版本
app_version='latest'
#docker stop ${app_name}
#echo '----stop container----'
#docker rm ${app_name}
#echo '----rm container----'
docker rmi ${group_name}/${app_name}:${app_version}
echo '----rm image----'

# 并行编译
# docker buildx build -t python-3-test -f Dockerfile .
# 打包编译docker镜像
docker build -t ${group_name}/${app_name}:${app_version} .
# 临时容器
# docker run --rm -it ${group_name}/${app_name}:${app_version} -e TZ="Asia/Shanghai" -v /etc/localtime:/etc/localtime  /app/run_script.sh

#
echo '----build image----'
docker run --name ${app_name} \
-e TZ="Asia/Shanghai" \
-v /etc/localtime:/etc/localtime \
-d ${group_name}/${app_name}:${app_version}
echo '----start container----'