# Markdown文件微博图床转七牛云

## 使用
将`config.py.bak`复制一份命名为`config.py`，并根据实际情况配置，然后就可以run了

```python
# 需要填写你的 Access Key 和 Secret Key；在此处查看 https://portal.qiniu.com/user/key
access_key = 'access_key'
secret_key = 'secret_key'

# 要上传的空间 也就是 https://portal.qiniu.com/kodo/bucket 这里的空间名称
bucket_name = 'bucket_name'

# md文件夹路径
ROOT_DIR_PATH = r"D:\xxxxx\_posts"

# 旧的图床域名前缀
OLD_IMG_URL_PREFIX = 'https://ws1.sinaimg.cn'
# 旧的图床域名的备用域名前缀，处理md文件中的链接已失效的问题
OLD_IMG_URL_REPLACE_PREFIX = 'https://wx1.sinaimg.cn'
# 新的图床域名前缀，用于替换md文件中的旧图床url
NEW_IMG_URL_PREFIX = 'https://xxx.xxx.xxx'
```