<p align="center">  
  <a href="https://github.com/cary997/fastapi-naive-admin">
    <image src="https://github.com/cary997/fastapi-naive-web/blob/main/src/assets/image/darkLogo.svg" height="50" width="100" />
</a> 
</p>

<h2 align="center">FastAPI Naive Admin</h1>
<p align="left" >
  fastapi-naive-admin 是一个基于python3+fastapi框架的权限控制系统，集合了常见的权限控制示例。前端使用了最新的 Vue3、Vite、Naive UI、TypeScript、Pinia、Tailwindcss 等主流技术开发。
  后端使用python3、fastapi、tortoise-orm等主流技术开发，拥有完整的API文档。 您可基于此项目基础上专注开发您的业务模块，希望此项目对您有帮助!
</p>

### 功能列表
- 前端国际化
- 前端多主题
- 动态路由(支持内嵌、外链)
- 按钮权限控制
- JWT无感刷新
- RBAC权限控制
- LDAP集成
- MFA登录
- IP黑白名单校验
- 邮件通知
- ......

### 前端代码
[fastapi-naive-web](https://github.com/cary997/fastapi-naive-web)

### 预览地址
[fastapi-naive-admin](http://121.196.209.165:8080)

### 后端开发环境安装
#### 本地开发环境

- python 3.12.2
- poetry 1.8.2
- mysql 8.3.0 (docker image mysql:latest)
- redis 7.2.4 (docker image redis:latest)

#### 安装依赖

```shell
- 使用poetry

poetry install

- 使用pip

pip install -r requirements.txt
```

#### 配置文件 && 初始化sql
```shell
- 配置文件

将config-template.yaml copy未config.yaml 按照里面配置的注释修改即可
或者可以使用环境变量添加 具体请查看 utils/config.py

- 初始化数据库(项目根目录base.sql)

mysql -uroot -proot123 < base.sql

- 默认账户密码
admin/Admin@123

```

#### 启动

```shell
uvicorn main:app --reload

or

poetry run uvicorn main:app --reload
```

### 前端部署开发环境安装
#### 本地开发环境

- node.js v20.11.1
- npm 10.4.0

#### 安装依赖

```shell
npm i
```

#### 启动

```shell
npm run dev
```

#### 打包

```shell
npm run build
```

### 预览截图
![image](https://github.com/cary997/fastapi-naive-admin/assets/106720683/6683dc14-8328-4dc1-8aea-cc8795d64a62)
![image](https://github.com/cary997/fastapi-naive-admin/assets/106720683/76ab260a-9341-4058-9c69-4cfe2e4076de)
![image](https://github.com/cary997/fastapi-naive-admin/assets/106720683/6da463ff-87c5-4099-8779-da4d7de89859)

