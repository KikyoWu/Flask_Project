- [1.需求分析：](#1-----)
- [2.系统功能设计](#2------)
  * [1.系统结构功能](#1------)
  * [2.系统业务流程](#2------)
  * [3.文件夹组织架构](#3-------)
- [3.系统各部分文件分析](#3---------)
  * [**1.初始化文件`__init__.py`:**](#--1--------init--py----)
      - [1——导入模块：](#1-------)
      - [2——实例化SQLAlchemy对象：`db = SQLAlchemy()`](#2-----sqlalchemy----db---sqlalchemy---)
      - [3——创建工厂函数app_create(config_name)实现程序实例初始化,以便扩展对象不最初绑定到应用程序app上：](#3--------app-create-config-name---------------------------app--)
  * [2.配置文件`config.py`：](#2-----configpy--)
    + [1——创建一个基类Config来保存通用配置](#1--------config-------)
    + [2——创建一个类继承定义的Config类配置DevelopmenttConfig环境下配置](#2------------config---developmenttconfig-----)
    + [3——用一个字典config提供选择](#3-------config----)
  * [3.模型文件`models.py`:](#3-----modelspy--)
    + [1——导入模块：](#1--------1)
    + [2——数据模型类：](#2--------)
  * [4.`shop.sql`文件：](#4-shopsql----)
  * [5.`home`文件](#5-home---)
    + [1——初始化文件`__init__.py`:](#1----------init--py--)
    + [2——**前台表单文件`forms.py`：**](#2-----------formspy----)
    + [3——前台路由文件`views.py`：](#3---------viewspy--)
      - [1.导入模块函数：](#1-------)
      - [2.注册页面：](#2-----)
      - [3.登陆页面：](#3-----)
      - [4.首页模块：](#4-----)
      - [5.购物车模块：](#5------)

------



# 1.需求分析：

- 具备首页商品轮播功能
- 具备首页商品展示功能，包括展示最新上架商品、打折商品和热门商品等功能
- 具备查看商品详情功能，可以用于展示商品的详细信息
- 具备加入购物车功能，用户可以将商品添加至购物车
- 具备查看购物车功能，用户可以查看购物车中的所有商品，可以更改购买商品的数量，情况购物车等
- 具备填写订单功能，用户可以填写地址信息，用于接收商品
- 具备提交订单功能，用户提史订单后，可以显现支付宝收款的二维码
- 具备查看订单功能，用户提交订单后可以查看订隼详情
- 具备会员管理功能，包括用户注册、登录和退出等
- 具备后台管理商品功能，包括新増商品、编辑商品、删除商品和查看商品排行等
- 具备后台管理会员功能，包括查看会员信息等
- 具备后台管理订单功能，包括查看订单信息等

# 2.系统功能设计

## 1.系统结构功能

**系统结构功能图：**

![系统结构功能图](https://github.com/KikyoWu/Python/blob/master/image/%E7%B3%BB%E7%BB%9F%E7%BB%93%E6%9E%84%E5%8A%9F%E8%83%BD%E5%9B%BE.png)

## 2.系统业务流程

**购物商场业务流程图：**

![商场业务流程图](https://github.com/KikyoWu/Python/blob/master/image/%E5%95%86%E5%9C%BA%E4%B8%9A%E5%8A%A1%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

## 3.文件夹组织架构

**采用模块和包的方式组织程序，文件夹组织架构如下所示：**

![文件夹组织架构图](https://images.cnblogs.com/cnblogs_com/yffxwyy/1858223/o_201008071448%E6%96%87%E4%BB%B6%E5%A4%B9%E7%BB%84%E7%BB%87%E6%9E%B6%E6%9E%84%E5%9B%BE.png)

- 有3个顶层文件夹：

  - **app:**Flask程序的包名。该文件夹下还有4个包：`home`（前台），`admin`（后台），`static`（静态文件），`template`（模板文件）；app初始化文件`__init__.py`,模型文件`models.py`

    - **home(前台):**

      - **初始化文件`__init__.py`:**用`home = Blueprint("home",__name__)`定义蓝图，用`import app.home.views`导入前台路由文件

      - **前台表单文件`forms.py`：**验证用户注册表单类RegisterForm，用户登录表单类LoginForm，修改密码表单类PasswordForm。继承自FlaskForm类，定义各个表单中每个字段类型和验证规则，以及字段的相关属性等信息。

      - **路由文件`vews.py`**:

        1. 设置登录路由`"/login/"`,注册路由`("/register/",`退出登录路由`"/logout/"`,修改密码路由`"/modify_password/"`,首页路由`"/"`，商品列表路由`"/goods_list/<int:supercat_id>/"`，商品详情路由`"/goods_detail/<int:id>/"`,搜索功能路由`"/search/"`,添加购物车路由`"/cart_add/"`,清空购物车路由`"/cart_clear/"`,删除购物车中某个商品路由`"/cart_delete/<int:id>/"`,购物车路由`"/shopping_cart/"`,购物车提交订单路由`"/cart_order/"`,删除某个订单路由`"/order_delete/<int:id>/"`,订单详情路由`"/order_list/"`。<!--路由具体地址不定的地方：需要把一些特定的字段标记成 <variable_name> ，将这些特定的字段将作为参数传入到函数中-->

        2. 使用方法render_template('hello.html', name=name)  来渲染模板，在 Python 中生成 HTML,显示网页页面

        3.  使用redirect(url_for('目录.函数名'))函数在某些路由下执行一些操作后重定向用户到其它地方，构建一个 URL 来匹配一个特定的函数可以使用 from flask import url_for方法。它接受函数名作为第一个参数，以及一些关键字参数,每一个关键字参数对应于 URL 规则的变量部分。未知变量部分被插入到 URL 中作为查询参数

        4. 调用`home.__init__.py`（初始化文件）中定义好的蓝图：

           ```python
           from . improt home
           @home.route("/")
           ```

    - **static（静态文件):**

      - **404:**错误页面
      - **home：**前台页面排版css,字体fonts,相关图片images,支付插件js
      - **Images:**所有商品图片

    - **template（模板文件)：**

      - 用来响应各个页面的HTML文件

    - **`__init__.py`（初始化文件）：**

      - 实例化SQLAlchemy对象做数据库映射，对数据库进行操作
      - 定义app工厂函数create_app（）：实例化Flask对象，载入并初始化配置文件config，注册前后台蓝图`app.register_blueprint(home_blueprint)`，这样app才能激活蓝图中的路径

    - **models.py模型文件：**使用SQLAlchemy进行数据库操作，将所有模型放到一个单独的models模块中，所以需要导入`__init__.py`中实例化的SQLAlchemy对象db，用SQLAlchemy扩展定义会员数据模型`User(db.Model)`，大分类`SuperCat`，子分类`SubCat`，商品`Goods`，购物车`Cart`，订单`Orders`，订单详情`OrdersDetail`.

  - **`migrations`数据库迁移文件:**使用

    [^Flask-Script]: Manage启动文件中定义的Manager实例调用命令

    扩展以命名行的形式生成数据表和启动文件后生成的文件，其命令如下：

    ```python
    python mamage.py db init      #创建迁移仓库，首次使用
    python mamage.py db migrate   #创建迁移脚本
    python mamage.py db upgrade   #把迁移应用到数据库中
    ```

  - **`venv`虚拟环境：**python运行的虚拟环境，创建并启动虚拟环境后产生，其命令如下：

    ```python
    virtualenv venv #创建venv虚拟环境
    source venv/bin/activate #启动venv虚拟环境
    ```

  - **`Requirments.txt:`**列出所有依赖包，便于在其他电脑中重新生成相同的虚拟环境

  - **`config.py`配置文件：**定义配置:设置密钥保证会话安全，进行数据库修改跟踪，连接数据库，打开环境调试端口

  - **`manage.py`启动文件：**用于启动程序以及其他程序任务：

    - 实例化应用对象create_app
    - 添加Manager实例调用的命令Python shell，make_shell_context()函数在命令行获取上下文，和所有和数据库相关的命令MigrateComman，将实例对象传入Manager追踪所有的在命令中调用的命令和处理过程的调用运行情况
    - 定义应用404找不到内容时的路由
    - 启动Manger实例接受命令行中的命令

  - **`shop.sql`:**创建数据库表的数据内容，方便进行数据表迁移

# 3.系统各部分文件分析

## **1.初始化文件`__init__.py`:**

#### 1——导入模块：

1. **Flask:**实现了一个WSGI应用`from flask import Flask`
2. **SQLAlchemy:**进行数据库操作`from flask_sqlalchemy import SQLAlchemy`
3. **config:**导入`config.py`里的config函数配置各种环境`from config import config`

#### 2——实例化SQLAlchemy对象：`db = SQLAlchemy()`

#### 3——创建工厂函数app_create(config_name)实现程序实例初始化,以便扩展对象不最初绑定到应用程序app上：

1. **实例化Flask对象**`app = Flask(__name__)`，让flask.helpers.get_root_path函数通过传入这个名字确定程序的根目录， 以便获得静态文件和模板文件的目录。
2. **载入配置文件**`app.config.from_object(config[config_name])`引用`config.py`里的config函数后传入模块对象
3. **使用`config.py`的静态方法init_app用于支持创建应用拓展的工厂模式：**配置`config[config_name].init_app(app)`,数据库`db.init_app(app)`，使一个扩展对象可以用于多个应用程序。
4. **在应用对象上注册前台和后台蓝图对象：**先导入前后台模块：`from app.home import home as home_blueprint`,再通过register_blueprint（）函数注册蓝图[^1]`app.register_blueprint(admin_blueprint,url_prefix="/admin")`
5. **返回应用对象：**`return app`

## 2.配置文件`config.py`：

### 1——创建一个基类Config来保存通用配置

1. **设置密钥，保证会话安全**：`SECRET_KEY = 'str'`

2. **设置数据库可被修改跟踪**：`SQLALCHEMY_TRACK_MODIFICATIONS = True`

3. 定义一个静态方法init_app，并且函数体为空,用于支持创建拓展对象的工厂模式

   ```python
   @staticmethod
       def init_app(app):
           pass
   ```

### 2——创建一个类继承定义的Config类配置DevelopmenttConfig环境下配置

1. **连接数据库：**

   ```python
   #root用户名，123密码，127.0.0.1主机IP，shop数据库名
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@127.0.0.1:3306/shop'
   ```

2. **打开环境调试端口：**`DEBUG = True`

### 3——用一个字典config提供选择

- 默认配置是DevelopmentConfig:`config = {'default': DevelopmentConfig}`

## 3.模型文件`models.py`:

### 1——导入模块：

1. **初始化文件`__init__.py`中的SQLAlchemy实例化对象db:**`from . import db`
2. **时间模块datetime：**`from datetime import datetime`有些表单类需要添加的当前时间

### 2——数据模型类：

> - SQLAlchemy对象关系映射器（ORM)是在我们的数据库中执行的原始的 SQL 查询的之上的抽象层。它为一个长长的列表的数据库引擎提供一致的 API,提供了一种将用户定义的Python类与数据库表以及这些类（对象）的实例与相应表中的行关联起来的方法。
> - 使用ORM时，配置过程首先描述将要处理的数据库表，然后定义将映射到这些表的自己的类，在SQLAlchemy中，这两个任务通常一起执行，使用的系统称为声明的，这允许我们创建包含指令的类来描述它们将映射到的实际数据库表。
> - 使用声明性系统映射的类是根据一个基类定义的，根据基类定义任意数量的映射类。

1. **数据表名称及作用：**<img src="https://images.cnblogs.com/cnblogs_com/yffxwyy/1858223/o_201008071424%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%93%E6%9E%84.png" alt="数据表结构" style="zoom:67%;" />
2. **数据表关系ER图：**![数据表关系图](https://images.cnblogs.com/cnblogs_com/yffxwyy/1858223/o_201008071400%E6%95%B0%E6%8D%AE%E8%A1%A8%E5%85%B3%E7%B3%BB%E5%9B%BE.png)
3. **会员数据模型类User(db.Model)：**
   - **db.Model基类定义映射类User**
   - **使用SQLAlchemy对象关系映射器（ORM**)，将会员数据模型类User与数据库表`shop.sql`中的`user`表关联起来，类的属性和数据库中表的字段一一对应
     - User的表名要与用户数据表名相同：`__tablename__ = "user"`
     -  **编号id：**设为大整形数据Integer，设为主键primary_key，自动增加
     - **用户名username：**字符串
     - **密码password：**字符串
     - **邮箱email：**字符串，且unique
     - **手机号phone：**11位字符串，且unique
     - **消费额consumption：**DECIMAL（10，2）十进制小数类型，两个小数点，整体长度不超过10，默认为0
     - **注册时间addtime：**db.DateTime，index=True使可被索引，default=datetime.now使默认添加时间是当前时间
     - **订单外键关系关联orders（`db.relationship`与`db.ForeignKey`的区别[^2]）：**`db.relationship('Orders', backref='user')`通过用户user可以找到对于用户的所有订单Orders
   - **重构repr方法，直接输出对象按方法中定义的格式显示:**当在python shell中调用模型类的对象时，repr()方法会返回一条类似”<模型类名主键值>”的字符串,重新定义__repr__()方法，返回一些更有用的信息,`return '<User %r>' % self.name`%r是用repr()方法处理对象，返回类型本身，而不进行类型转化
   - **定义检查密码的函数`check_password(self, password)`:**需要传入密码password，导入`werkzeug.security`模块的`check_password_hash`函数，通过`check_password_hash`函数返回用户密码`self.password`与传入的密码`password`对比的布尔值来判断密码是否正确

## 4.`shop.sql`文件：

1. **设置 禁用外键关联约束：**MySQL中设置了foreign key关联，造成无法更新或删除数据`SET FOREIGN_KEY_CHECKS=0;`
2. **创建各个数据表，并插入数据：**

- **创建数据表：**先判断表是否存在`DROP TABLE IF EXISTS 'cart';
  再用CREATE TABLE '表名' ('列名' 数据类型`

  ```mysql
  /*
  NOT NULL表名购物车ID不能不存在，AUTO_INCREMENT自动增长
  DEFAULT NULL默认是无
  购物车主键是id,AUTO_INCREMENT=81设置默认增加数据时id是81
  KEY键可以用来确定表中具体的一行记录，通过goods_id，user_id，ix_cart_addtime键来确定购物车
  CONSTRAINT应用完整性规定，防止不合法的数据写入数据库，
  FOREIGN KEY所引用的数据必须存在，REFERENCES外键goods_id的取值参照范围是goods表的id，没有goods就不会有cart
  所有的外键FOREIGN KEY对应models.py里.relationship()外键关系关联
  */
  DROP TABLE IF EXISTS `cart`;
  CREATE TABLE `cart` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `goods_id` int(11) DEFAULT NULL,
    `user_id` int(11) DEFAULT NULL,
    `number` int(11) DEFAULT NULL,
    `addtime` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `goods_id` (`goods_id`),
    KEY `user_id` (`user_id`),
    KEY `ix_cart_addtime` (`addtime`),
    CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`goods_id`) REFERENCES `goods` (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
  ```

- **插入数据：**`INSERT INTO '表名' VALUES ('1', '59', '1', '1', '2018-10-31 14:29:40');`

```mysql
INSERT INTO `cart` VALUES ('1', '59', '1', '1', '2018-10-31 14:29:40');
INSERT INTO `cart` VALUES ('2', '59', '0', '1', '2018-10-31 14:30:46');
INSERT INTO `cart` VALUES ('3', '59', '0', '1', '2018-10-31 14:31:48');
```

## 5.`home`文件

### 1——初始化文件`__init__.py`:

1. **导入模块：**`from flask import Blueprint`用来创建蓝图，导入前台路由文件`import app.home.views`
2. **创建蓝图：**`home = Blueprint("home",__name__)`

### 2——**前台表单文件`forms.py`：**

> 需要用户输入数据提交的表单类

1. **导入模块函数：**

   - **`FlaskForm`验证表单：**`from flask_wtf import FlaskForm`
   - **`StringField, PasswordField, SubmitField, TextAreaField`定义表单的HTML标准字段类型:**`from wtforms import StringField, PasswordField, SubmitField, TextAreaField`
   - **`DataRequired, Email, Regexp, EqualTo, ValidationError,Length`定义字段的验证规则：**`from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError,Length`
   - **模型文件`models.py`中的`User`类:**有些验证需要通过SQLAlchemy对用户模型类User映射的user表进行过滤

2. **验证用户注册表单类RegisterForm：**

   - **username用户名：**

     - 继承FlaskForm类

     - 账户名字段类型字符串StringField：

       - **标签label=’ ‘：**渲染后显示在输入字段前的文字

       - **验证器列表validators=[]:**在表单提交后逐一调用,DataRequired("str")输入为空时显示，Length(min=, max=5, message=" ")输入长度不符合时使用

       - **文本字段描述：**`description=" "`讲解文本用途

       - **render_kw字段**：设置对应的HTML\<input>标签属性

         ```python
         render_kw={
                     "type": "text",                 #输入类型，文本
                     "placeholder": "请输入用户名！",  #规定帮助用户填写输入字段的提示
                     "class":"validate-username",    
                     "size" : 38,                 
                 }
         ```

   - **phone电话：**

     - 电话字段类型字符串StringField：

     - 其他类似，验证器列表validators=[]中的Length变为Regexp正则表达式验证

       ```python
       #第一个数字是1，第二个是34578其中一个，后9位是0-9中的数字
       Regexp("1[34578][0-9]{9}", message="手机号码格式不正确")
       ```

   - **email邮箱：**

     - 邮箱段类型字符串StringField：
     - 验证器列表validators=[]中使用Email函数验证

   - **password密码：**

     - 密码字段类型字符串PasswordField：
     - 验证器列表validators=[]中由Regexp正则表达式验证

     ```python
     #^匹配字符串的开头，？=表示当前位置的后面没有换行且匹配一个字母，.*匹配除了换行的任意字符 []匹配在[]中的字符，{}匹配 n 到 m 次由前面的正则表达式定义的片段,$匹配字符串的结尾
     Regexp("^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[?/*&^$#@!]).{6,18}$", message="密码长度为6-18，必须包含字母、数字和特殊符号")
     ```

   - **repassword重新输入密码：**

     - 重新输入密码字段类型字符串PasswordField：
     - 验证器列表validators=[]中用EqualTo函数比较两个字段的值`EqualTo('password', message="两次密码不一致！")`

   - **submit提交表单：**

     - 提交表单字段类型字符串SubmitField

   - **自定义validate_email函数检测注册邮箱是否已经存在：**

     - 通过`<模型类名>.query.filter_by(email=传入数据).count()`在数据库中查找当前邮箱的数目是否已经为1来判断邮箱是否已经存在
     - 已经存在引发error`raise ValidationError("邮箱已经存在！")`

   - **自定义validate_phone函数检测手机号是否已经存在：**与邮箱类似

3. **用户登录表单类LoginForm：**

4. **修改密码表单类PasswordForm：**

   - **自定义validate_old_password函数检测输入的原始密码是否正确：**

     - 导入session会话查找存储的用户id
     - 利用SQLAlchemy查询执行函数get()找该用户id所在行`user = User.query.get(int(user_id))

     - 利用`app.models.py`中User类的check_password函数检查旧密码是否正确`user.check_password(old_password)`

     - 不正确引发error`raise ValidationError(" ")`

     - SQLAlchemy查询过滤器和执行函数

       **SQLAlchemy查询过滤器**

       | 过滤器      | 说明                                                 |
       | ----------- | ---------------------------------------------------- |
       | filter()    | 把过滤器添加到原查询上，返回一个新查询               |
       | filter_by() | 把等值过滤器添加到原查询上，返回一个新查询           |
       | limit()     | 使用指定的值限制原查询返回的结果数量，返回一个新查询 |
       | offset()    | 偏移原查询返回的结果，返回一个新查询                 |
       | order_by()  | 根据指定条件对原查询结果进行排序，返回一个新查询     |
       | group_by()  | 根据指定条件对原查询结果进行分组，返回一个新查询     |

       **SQLAlchemy查询执行函数**

       | 方法           | 说明                                                         |
       | -------------- | ------------------------------------------------------------ |
       | all()          | 以列表形式返回查询的所有结果                                 |
       | first()        | 返回查询的第一个结果，如果没有结果，则返回None               |
       | first_or_484() | 返回查询的第一个结果，如果没有结果，则终止请求，返回404错误响应 |
       | get()          | 返回指定主键对应的行，如果没有对应的行，则返回None           |
       | get_or_484     | 返回指定主键对应的行，如果没有找到指定的主键，则终止请求，返回404错误响应 |
       | count()        | 返回查询结果的数量                                           |
       | paginate()     | 返回一个Paginate对象，它包含指定范围内的结果                 |

### 3——前台路由文件`views.py`：

#### 1.导入模块函数：

- **`home`前台文件调用蓝图，定义视图函数：**`from . import home`
- **初始化文件`__init__.py`中的SQLAlchemy实例化对象db:**`from . import db`,利用SQLAlchemy对数据库的数据进行添加和提交
- **前台表单文件`app.home.forms`里的登陆、注册、修改密码类获取提交的表单信息：**`from app.home.forms import LoginForm,RegisterForm,PasswordForm`
- **模型`app.models`里的数据模型查询过滤器和执行函数查询数据库相应数据：**`from app.models import User,Goods,Orders,Cart,OrdersDetail`
- **`render_template`渲染模板,`url_for`构建URLs,`redirect`重定向,`flash`闪现消息,`session`会话）数据存储在服务器上,`request`处理客户端发送到服务器的数据,`make_response`获取在视图中得到的响应对象（二维码的二进制数据）并修改返回（动态gif）：**`from flask import render_template, url_for, redirect, flash, session, request,make_response`
- **`generate_password_hash`对输入的表单密码加密：**`from werkzeug.security import generate_password_hash`
- **`wraps`装饰器，给登陆函数添加用户是否已登陆功能：**`from functools import wraps`
- **`random`生成随机的验证码颜色：**`import random`
- **`string`生成随机的验证码数字和字母：**`import string`
- **`PIL`图像处理库创建验证码图像：**`from PIL import Image, ImageFont, ImageDraw`
- **`BytesIO`在内存中读写验证码二进制数据：**`from io import BytesIO`

#### 2.注册页面：

#### 3.登陆页面：

1. **生成验证码：**

   - **定义rndColor函数用`random.randint`生成随机颜色的三个值：**`return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))`

   - **定义gene_text函数用`random.simple`生成随机验证码的四个值：**`return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))`

   - **定义生成验证码函数get_verify_code：**

     - 调用gene_text函数生成随机验证码的值
     - 用PIL图像库的Image函数的new方法创建验证码的白底图，ImageFont函数的truetype方法设置验证码字体，ImageDraw的draw方法在白底图上绘制验证码：绘制时使用for语句生成随机位置，颜色用定义的rndColor函数，字体用先前设置的字体

     ```python
     def get_verify_code():
         '''生成验证码图形'''
         code = gene_text()
         # 图片大小120×50
         width, height = 120, 50
         # 创建新图片对象（mode（L,RGB,RGBA),size,color)
         im = Image.new('RGB',(width, height),'white')
         # 字体，使用app/static/fonts下的arial.ttf字体，字体大小为40
         font = ImageFont.truetype('app/static/fonts/arial.ttf', 40)
         # 创建一个可以在给定白底图片上绘图的对象
         draw = ImageDraw.Draw(im)
         # 绘制字符串
         for item in range(4):
             #在给定位置绘制随机验证码的字符，分别用随机颜色填充，设置字体
             draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                       text=code[item], fill=rndColor(),font=font )
         #返回绘制后的图片对象和验证码字符
         return im, code
     ```

2. **显示验证码：**

   - 将验证码图片显示在验证码路由`@home.route('/code')`下
   - 调用生成验证码的函数get_verify_code生成验证码
   - 利用`BytesIO`将验证码以二进制的形式写入保存成jpeg静态图片格式，再通过`BytesIO().getvalue()`获取写入的图片的二进制数据,用`make_response().headers['X-Something'] = 'A value'`把获得的图片的二进制数据改为动态gif验证码图片作为响应体返回前端显示
   - 将验证码字符串储存在session中

   ```python
   @home.route('/code')
   def get_code():
       """
       验证码
       """
       #生成二进制图片
       image, code = get_verify_code()
       # 图片以二进制形式写入
       buf = BytesIO()
       #保存成jpeg静态图片格式
       image.save(buf, 'jpeg')
       #获取写入的图片的二进制数据
       buf_str = buf.getvalue()
       # 把二进制数据作为响应体返回前端
       response = make_response(buf_str)
       #设置前段首部字段是动态gif验证码图片
       response.headers['Content-Type'] = 'image/gif'
       # 将验证码字符串储存在session中
       session['image'] = code
       return response
   ```

3. **将验证码显示在登陆页面：**

   - 将登陆页面`login.html`验证码图片的\<img>标签的scr属性，通过url_for()构建到home.get_code验证码的URL下
   - 单击验证码可更新通过javascr的onclick事件：URL重定向到home.views里的验证码路由下，用？执行1次，Math.random()生成随机数

   ```html
   <div class="col-sm-8" style="clear: none;">
   										<!-- 验证码文本框 -->
   										{{form.verify_code}}
   											<!-- 显示验证码在登陆页面：src规定显示图像的 URL重定向到home.views里的验证码路由下 -->
                                               <!-- 单击验证码更新：onclick事件：URL重定向到home.views里的验证码路由下，？执行1次，Math.random()生成随机数 -->
   											<img class="img_checkcode" src="{{url_for('home.get_code')}}" width="116"
   	 											height="43" onclick="this.src='{{url_for('home.get_code')}}'+'?'+ Math.random()">
   </div>
   ```

4. **检测验证码是否正确：**

   - 将生成验证码函数get_verify_code时存在session里的验证码与home.forms表单里用户提交的数据verify_code.data全部转换成英文小数作对比
   - 不对用`flash`闪现错误消息，用`render_template()`重新渲染登陆页面

   ```python
   # 判断验证码(将存在session里的验证码与表单里用户提交的数据作对比
           if session.get('image').lower() != form.verify_code.data.lower():
               #不同时用flash闪现消息：验证码错误
               flash('验证码错误',"err")
               #重新渲染登陆页，表单中输入验证不变
               return render_template("home/login.html", form=form)  # 返回登录页
   ```

5. **保存会员登陆状态：**

   - 实例化`home.forms`里的`LoginForm`类,生成登陆表单：`form = LoginForm()`
   - 表单提交时：
     - 通过`form.data`接收表单里的数据
     - 将存储在session中的username与提交到表单里的data.username通过`filter_by()`过滤器等值查询，用户名和密码是否存在，不在用`render_template()`重新渲染登陆页面
     - 将user_id写入session, 判断用户是否登录，将username写入session, 判断用户是否存在
     - 登陆成功，用`redirect()`重定向到首页
   - 用`render_template()`渲染登陆页面

   ```python
   @home.route("/login/", methods=["GET", "POST"])
   def login():
       """
       登录
       """
       #if "user_id" in session:        # 如果已经登录，则直接跳转到首页
           #return redirect(url_for("home.index"))
       form = LoginForm()              # 实例化LoginForm类,生成表单（home.forms里的）
       if form.validate_on_submit():   # 如果提交
           data = form.data            # 接收表单数据
           # 判断验证码(将存在session里的验证码与表单里用户提交的数据作对比
           if session.get('image').lower() != form.verify_code.data.lower():
               #不同时用flash闪现消息：验证码错误
               flash('验证码错误',"err")
               #重新渲染登陆页，表单中输入验证不变
               return render_template("home/login.html", form=form)  # 返回登录页
           # 判断用户名是否存在(
           user = User.query.filter_by(username=data["username"]).first()    # 获取用户信息
           if not user :
               flash("用户名不存在！", "err")           # 输出错误信息
               return render_template("home/login.html", form=form)  # 返回登录页
           # 判断用户名和密码是否匹配
           if not user.check_password(data["password"]):     # 调用check_password()方法，检测用户名密码是否匹配
               flash("密码错误！", "err")           # 输出错误信息
               return render_template("home/login.html", form=form)  # 返回登录页
   
           session["user_id"] = user.id                # 将user_id写入session, 后面判断用户是否登录
           session["username"] = user.username         # 将username写入session, 判断用户是否存在
           return redirect(url_for("home.index"))      # 登录成功，跳转到首页
   
       return render_template("home/login.html",form=form) # 渲染登录页面模板
   ```

6. **退出会员登陆状态：**

   - 定义新的视图函数
   - 利用`session.pop`删除服务器中的user_id和username
   - 退出成功，用`redirect()`重定向到登陆页面

   ```python
   @home.route("/logout/")
   def logout():
       """
       退出登录
       """
       # 重定向到home模块下的登录页面。
       session.pop("user_id", None)#删除服务器中的user_id
       session.pop("username", None)
       return redirect(url_for('home.login'))
   ```

7. **给登陆页面添加商城标志图：**

   - ```html
     <!--通过在 <a> 标签中嵌套 <img> 标签，给51商城图像添加到返回首页的链接-->
     <!--src规定显示图像的 URL，给静态文件生成 URL ，使用url_for('static', filename='')-->
     <a href="index.html" title="点击返回首页"><img src="{{url_for('static',filename='home/images/51logo.png')}}"></a>
     ```

#### 4.首页模块：

#### 5.购物车模块：

**route装饰器** ：可以使用Flask应用实例的route装饰器将一个URL规则绑定到 一个视图函数上

[^1]: 使用蓝图可以分为三个步骤:  1,在前台`home.init.py`初始化文件中创建一个蓝图对象`admin``=``Blueprint(``'admin'``,__name__)　`  2,在`init.py`的应用对象上注册这个蓝图对象`app.register_blueprint(admin,url\_prefix``=``'/admin'``)`   3,在前台`home.views.py`路由文件这个蓝图对象上进行操作,注册路由,指定静态文件夹,注册模版过滤器`@admin``.route(``'/'``)``def` `admin_home():``  ``return` `'admin_home'`
[^2]:1、 `db.ForeignKey('supercat.id')`添加外键，所属关系,可以通过一个子分类查找到对应的大分类（supercat）      2、`db.relationship("Goods", backref='subcat')`添加外键关系关联，包含关系，可以通过子分类找到子分类对应的所有商品

