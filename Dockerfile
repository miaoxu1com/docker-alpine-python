FROM alpine:latest AS builder-image
# avoid stuck build due to user prompt
# 不再建议使用 ENV DEBUG 0 环境变量，没必要。
# --no-cache: 这个选项告诉apk在安装软件包时不将软件包的元数据缓存到系统中。这意味着不会将下载的软件包索引存储在本地，
# 有助于减小镜像的大小，特别适合于Docker容器这类空间有限的环境。
ARG DEBIAN_FRONTEND=noninteractive
# ENV PYTHONDONTWRITEBYTECODE 1: 建议构建 Docker 镜像时一直为 1, 防止 python 将 pyc 文件写入硬盘
ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED 1: 建议构建 Docker 镜像时一直为 1, 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
ENV PYTHONUNBUFFERED=1
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update  \
    && apk upgrade \
    && apk add --no-cache python3 \
    && apk add --no-cache python3-dev \
    && rm -rf /root/.cache/pip \
    && rm -rf /var/cache/apk/* # 等价apk add --no-cache
# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3 -m venv /home/myapp/venv
ENV PATH="/home/myapp/venv/bin:$PATH"
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

FROM alpine:latest AS runner-image
ENV TZ Asia/Shanghai
COPY --from=builder-image /home/myapp/venv /home/myapp/venv
#EXPOSE 5000
# activate virtual environment
ENV VIRTUAL_ENV=/home/myapp/venv/bin
ENV PATH="$VIRTUAL_ENV:$PATH"
WORKDIR /home/myapp
COPY ./main.py .
# ENTRYPOINT ["/home/app"]
CMD ["python","main.py"]
