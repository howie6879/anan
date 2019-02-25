## anan

> 愿世界上所有的宝贝们都健康长大～

初当父母，将互联网上关于孩子一些身体疾病方面的相关问答爬取下来，然后利用机器学习构建问答模型

如果能做到防微杜渐，那这就是一个有价值的项目

### 使用

项目说明：

- 开发语言基于 `Python3.6+`
- 数据库采用 `MongoDB`
- Web 服务采用 [aiohttp](https://github.com/aio-libs/aiohttp)
- 数据集爬虫框架选取 [Ruia](https://github.com/howie6879/ruia)

**安装**

```shell
git clone https://github.com/howie6879/anan.git
# Python 3.6+
pip install pipenv
cd anan
pipenv install --dev
cd anan
python run app.py
```

### 关于数据集

数据集来源于互联网，目前收录来源如下：

- [快速问医生](https://m.120ask.com/jibing/class/c3/)：数据集[文件](./datasets/type_of_disease.csv)

更多来源欢迎提Issue