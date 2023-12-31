# 学习通作业提醒
## 简介

本程序会在每天21：30推送当前所有未完成的作业

在每天6：30到21：30之间每隔三小时推送24小时内截止的作业，若无24小时内截止的作业则不做提醒

本项目无需填写课程ID，默认检测所有未完成的作业

## 运行原理
本程序基于python运行，使用学习通登录以及作业列表api获取作业信息，通过[wxpusher](https://wxpusher.zjiecode.com/docs/#/)平台进行微信推送


## 如何使用
### 依赖安装
python安装过程不再赘述，版本需>3.10

安装完成后在CMD或终端依次执行以下代码;

	pip install BeautifulSoup4
	pip install schedule
    pip install requests
	
### 启动程序
1、将本项目所有文件下载到同一文件夹下，按照提示修改config.json的内容，有关wxpusher的配置请查阅[wxpusher](https://wxpusher.zjiecode.com/docs/#/)官方文档

2、cmd或终端定位到该文件夹

3、执行`python/python3 main.py`即可自动定时运行

## 注意事项
1、本程序所使用的学习通api由作者本人抓取而来，不能保证此api可持续使用

2、Linux环境下推荐通过Screen使用本程序，方便后台留存以及查看日志

## 常见异常处理
### 提示`cannot import name 'Mapping' from 'collections'`
编辑报错的文件

	#将
	from collections import Mapping 
	from collections import MutableMapping 
	#这些导入全部替换以下这些，如没有这两行，在文件开头加上即可
	from collections.abc import Mapping
	from collections.abc import MutableMapping
	#即用collections.abc代替collections调用方法Mapping、MutableMapping

 ### 提示`AttributeError: module ‘collections‘ has no attribute`

 编辑报错的文件

更改`collections.attr` 为 `collections.abc.attr`即可
