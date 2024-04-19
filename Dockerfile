ARG APP_VERSION=latest
FROM alpine:${APP_VERSION} AS builder-image
# 测试构建使用的命令
# docker buildx build --squash --no-cache -t python-3-test -f Dockerfile .
# 新版本的Docker不支持--squash参数需要使用多阶段构建 会发出警告WARNING: experimental flag squash is removed with BuildKit.
# You should squash inside build using a multi-stage Dockerfile for efficiency.

# avoid stuck build due to user prompt
# ENV PYTHONDONTWRITEBYTECODE 1: 建议构建 Docker 镜像时一直为 1, 防止 python 将 pyc 文件写入硬盘
# ENV PYTHONUNBUFFERED 1: 建议构建 Docker 镜像时一直为 1, 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
# 不再建议使用 ENV DEBUG 0 环境变量，没必要。
#**/__pycache__: python 缓存目录
#**/*venv: Python 虚拟环境目录。很多 Python 开发习惯将虚拟环境目录创建在项目下，一般命名为：.venv 或 venv
#**/.env: Python 环境变量文件
#**/.git **/.gitignore: git 相关目录和文件
#**/.vscode: 编辑器、IDE 相关目录
#**/charts: Helm Chart 相关文件
#**/docker-compose*: docker compose 相关文件
#*.db: 如果使用 sqllite 的相关数据库文件
#.python-version: pyenv 的 .python-version 文件
# --no-cache: 这个选项告诉apk在安装软件包时不将软件包的元数据缓存到系统中。这意味着不会将下载的软件包索引存储在本地，有助于减小镜像的大小，特别适合于Docker容器这类空间有限的环境。
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN --mount=type=cache,target=/usr/local/bin,id=python_cache,sharing=locked \
    #--mount=type=cache,target=/home/myuser/venv,id=python_moudle,sharing=locked \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update  \
    && apk upgrade \
    && apk add --no-cache --update python3 \
    && python3 -m venv /home/myuser/venv \
    && rm -rf /root/.cache/pip
# create and activate virtual environment
# using final folder name to avoid path issues with packages
ENV PATH="/home/myuser/venv/bin:$PATH"
COPY requirements.txt .
RUN \
    #--mount=type=cache,target=/home/myuser/venv,id=python_moudle,sharing=locked \
    pip3 install --upgrade --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

FROM alpine:latest AS runner-image
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update  \
    && apk upgrade \
    && apk add --no-cache --update python3 \
    && rm -rf /root/.cache/pip
ENV TZ Asia/Shanghai
#/home/myuser/venv需要用时就挂载，但是COPY时已经被卸载失败，因为RUN执行执行完目录被卸载了，COPY失败
COPY --from=builder-image /home/myuser/venv /home/myuser/venv
#EXPOSE 5000
# make sure all messages always reach console

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv/bin
ENV PATH="$VIRTUAL_ENV:$PATH"
WORKDIR /home/app
#COPY . /home/app/

# ENTRYPOINT ["/home/app"]
CMD ["python3", "main.py"]
