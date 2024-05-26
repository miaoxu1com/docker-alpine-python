ARG APP_VERSION=latest
FROM alpine:${APP_VERSION} AS builder-image
# 测试构建使用的命令
# docker buildx build --no-cache -t python-3-test -f Dockerfile .
# 新版本的Docker不支持--squash参数需要使用多阶段构建 会发出警告WARNING: experimental flag squash is removed with BuildKit.
# You should squash inside build using a multi-stage Dockerfile for efficiency.

#docker buildx build                                             \
#        --platform linux/amd64,linux/arm64                      \
#        --build-arg GOCACHE=${GOCACHE}                          \
#        --build-arg GOMODCACHE=${GOMODCACHE}                    \
#        -t ${CONTAINER_REGISTRY}/${CONTAINER_IMAGE_NAME}:latest \
#        --push                                                  \
#        .
# 命令行传参覆盖Docfile中定义的arg参数
# 使用pip show beautifulsoup4 查看模块存储路径
# MOUDLECACHE=/home/myapp/venv/lib/python3.11/site-packages
# docker buildx build --build-arg MOUDLECACHE=${MOUDLECACHE} -t ${CONTAINER_REGISTRY}/${CONTAINER_IMAGE_NAME}:latest --push .
# 重要：这里可以减少镜像大小
# docker buildx build --no-cache --build-arg MOUDLECACHE=${MOUDLECACHE} -t python-alpine -f Dockerfile .
# 重要：这里可以减少镜像大小
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

#在基于 Alpine Linux 的系统中，`python3` 和 `python3-dev` 是两个不同的包，它们服务于不同的目的：
#1. **python3**:
#   - 这个包包含了 Python 解释器和标准库。
#   - 它提供了运行 Python 代码所需的基本环境。
#   - 这个包不包含编译 Python 模块所需的头文件和静态库。
#2. **python3-dev**:
#   - 这个包包含了 Python 的开发工具，如头文件和静态库。
#   - 它用于编译和安装那些需要从源代码编译的 Python 扩展模块。
#   - 如果你在安装某些 Python 库时遇到缺少头文件或库的提示，那么你可能需要安装 `python3-dev` 包。
# pip cache dir 查看缓存目录路径
# 使用apk cache -h  查看缓存参数

#在 Docker 中，构建镜像时，Docker 会检查每一行指令，并决定是否可以复用之前的缓存。如果某行指令与之前构建时相同，Docker 将会使用缓存。
#但是，如果指令发生变化，Docker 将会执行新的指令并创建新的缓存层。
#在你提供的 Dockerfile 中，你使用了 docker pull 来尝试拉取最新的基础镜像。这个步骤实际上并不影响 Dockerfile 的构建缓存，因为 docker pull 是一个独立的操作，
#它不会检查 Dockerfile 的内容。然而，确保基础镜像是最新的确实可以避免使用过时的缓存。
#为了确保 Docker 在构建过程中尽可能地复用缓存，你可以采取以下措施：
#优化 Dockerfile：将不容易变化的指令（如 RUN 指令下载依赖或创建用户）放在 Dockerfile 的前面。这样，只有当这些指令发生变化时，Docker 才会重新执行这些指令。
#使用缓存标签：在构建镜像时，你可以使用标签来控制 Docker 何时使用缓存。例如，如果你知道某个层可能经常变化，你可以在这个层之前添加一个 --no-cache 标志来禁用缓存。
#避免不必要的层：尽量减少 Dockerfile 中的层数，可以通过合并多个 RUN 指令来实现。较少的层数可以提高构建效率，并增加缓存复用的机会。
#利用多阶段构建：如果可能，使用多阶段构建来减少最终镜像的大小，并且只在需要时下载依赖或运行构建脚本。

ARG DEBIAN_FRONTEND=noninteractive
ARG MOUDLECACHE
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN \
    #--mount=type=cache,target=/usr/local/bin,id=python_cache \
    #--mount=type=cache,target=/usr/local/bin,id=python_cache,sharing=locked \
    #--mount=type=cache,target="$MOUDLECACHE",id=moudle_cache \
    #--mount=type=cache,target=/home/myuser/venv,id=python_moudle,sharing=locked \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update  \
    && apk upgrade \
    && apk add --no-cache --update python3 \
    && python3 -m venv /home/myuser/venv \
    && rm -rf /root/.cache/pip \
    && rm -rf /var/cache/apk/* \
    && apk cache clean
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
    && rm -rf /var/cache/apk/* \
    && apk cache clean \

ENV TZ Asia/Shanghai
#/home/myuser/venv需要用时就挂载，但是COPY时已经被卸载失败，因为RUN执行执行完目录被卸载了，COPY失败
COPY --from=builder-image /home/myuser/venv /home/myuser/venv
#EXPOSE 5000
# make sure all messages always reach console

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv/bin
ENV PATH="$VIRTUAL_ENV:$PATH"
WORKDIR /home/app
COPY . /home/app/


# ENTRYPOINT ["/home/app"]
#CMD ["python3", "main.py"]
