import os
import re

import wget
from qiniu import Auth, put_file, etag

import config

# 加载配置
access_key = config.access_key
secret_key = config.secret_key
bucket_name = config.bucket_name
ROOT_DIR_PATH = config.ROOT_DIR_PATH
OLD_IMG_URL_PREFIX = config.OLD_IMG_URL_PREFIX
OLD_IMG_URL_REPLACE_PREFIX = config.OLD_IMG_URL_REPLACE_PREFIX
NEW_IMG_URL_PREFIX = config.NEW_IMG_URL_PREFIX


def upload(local_path, upload_path):
    """
    上传方法
    :param local_path:
    :param upload_path:
    :return:
    """
    print("正在上传 {} ，上传到 {}".format(local_path, upload_path))
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    key = upload_path
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = local_path
    ret, info = put_file(token, key, localfile, version='v2')
    print(info)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


def subdir_list(dirname):
    """获取目录下所有子目录名
    @param dirname: str 目录的完整路径
    @return: list(str) 所有子目录完整路径组成的列表
    """
    return list(filter(os.path.isdir, map(lambda filename: os.path.join(dirname, filename), os.listdir(dirname))))


def file_list(dirname, ext='.csv'):
    """获取目录下所有特定后缀的文件
    @param dirname: str 目录的完整路径
    @param ext: str 后缀名, 以点号开头
    @return: list(str) 所有子文件名(不包含路径)组成的列表
    """
    return list(filter(lambda filename: os.path.splitext(filename)[1] == ext, os.listdir(dirname)))


def list_file_path(root_dirname, ext='.md'):
    """
    获取文件路径列表
    :param root_dirname:
    :param ext:
    :return:
    """
    file_path_list = []
    dirname_list = subdir_list(root_dirname)
    for dirname in dirname_list:
        filename_list = file_list(dirname=dirname, ext='.md')
        for filename in filename_list:
            file_path_list.append(r'{}\{}'.format(dirname, filename))
    return file_path_list


def replace_file_img_url(file_path):
    """
    替换文件中的图床地址，通过下载图片再上传到七牛云实现
    :param file_path:
    :return:
    """
    # 存储读取的文件内容，用于更新文件，从而实现修改的效果
    file_data = ""
    i = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 正则匹配当前行
            # 读内容
            res = re.search(OLD_IMG_URL_PREFIX + r'.+(?=\))', line)
            if res:
                # 提取url
                img_url = line[res.span()[0]: res.span()[1]]

                # 替换成备用的url
                img_url = img_url.replace(OLD_IMG_URL_PREFIX, OLD_IMG_URL_REPLACE_PREFIX)
                print(os.path.dirname(__file__) + os.path.basename(img_url))

                # 通过备用的url下载到本地
                img_path = wget.download(img_url, "temp/" + os.path.basename(img_url))

                # 上传到七牛云
                upload(img_path, img_url[len(OLD_IMG_URL_REPLACE_PREFIX) + 1:])

                # 删除本地图片
                os.remove(img_path)

                # 更新当前行的图床地址
                line = line.replace(OLD_IMG_URL_PREFIX, NEW_IMG_URL_PREFIX)
            file_data += line

    # 写出文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_data)


if __name__ == '__main__':
    for file_path in list_file_path(ROOT_DIR_PATH):
        replace_file_img_url(file_path)
