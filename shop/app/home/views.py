# _*_ coding: utf-8 _*_
from . import home
from app import db
from app.home.forms import LoginForm,RegisterForm,PasswordForm
from app.models import User ,Goods,Orders,Cart,OrdersDetail
from flask import render_template, url_for, redirect, flash, session, request,make_response
from werkzeug.security import generate_password_hash
from functools import wraps
import random
import string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))

def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB',(width, height),'white')
    # 字体
    font = ImageFont.truetype('app/static/fonts/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                  text=code[item], fill=rndColor(),font=font )
    return im, code


@home.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response

def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)

    return decorated_function

@home.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录
    """
    if "user_id" in session:        # 如果已经登录，则直接跳转到首页
        return redirect(url_for("home.index"))
    form = LoginForm()              # 实例化LoginForm类
    if form.validate_on_submit():   # 如果提交
        data = form.data            # 接收表单数据
        # 判断验证码
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('验证码错误',"err")
            return render_template("home/login.html", form=form)  # 返回登录页
        # 判断用户名是否存在
        user = User.query.filter_by(username=data["username"]).first()    # 获取用户信息
        if not user :
            flash("用户名不存在！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页
        # 判断用户名和密码是否匹配
        if not user.check_password(data["password"]):     # 调用check_password()方法，检测用户名密码是否匹配
            flash("密码错误！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页

        session["user_id"] = user.id                # 将user_id写入session, 后面用户判断用户是否登录
        session["username"] = user.username                # 将user_id写入session, 后面用户判断用户是否登录
        return redirect(url_for("home.index")) # 登录成功，跳转到首页

    return render_template("home/login.html",form=form) # 渲染登录页面模板

@home.route("/register/", methods=["GET", "POST"])
def register():
    """
    注册功能
    """
    if "user_id" in session:
        return redirect(url_for("home.index"))
    form = RegisterForm()           # 导入注册表单
    if form.validate_on_submit():   # 提交注册表单
        data = form.data            # 接收表单数据
        # 为User类属性赋值
        user = User(
            username = data["username"],            # 用户名
            email = data["email"],                  # 邮箱
            password = generate_password_hash(data["password"]),# 对密码加密
            phone = data['phone']
        )
        db.session.add(user) # 添加数据
        db.session.commit()  # 提交数据
        return redirect(url_for("home.login"))  # 登录成功，跳转到首页
    return render_template("home/register.html", form=form) # 渲染模板

@home.route("/logout/")
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for('home.login'))

@home.route("/modify_password/",methods=["GET","POST"])
@user_login
def modify_password():
    """
    修改密码
    """
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=session["username"]).first()
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(data["password"])
        db.session.add(user)
        db.session.commit()
        return "<script>alert('密码修改成功');location.href='/';</script>"
    return render_template("home/modify_password.html", form=form)

@home.route("/")
def index():
    """
    首页
    """
    # 获取2个热门商品
    hot_goods = Goods.query.order_by(Goods.views_count.desc()).limit(2).all()
    # 获取12个新品
    new_goods = Goods.query.filter_by(is_new=1).order_by(
                    Goods.addtime.desc()
                        ).limit(12).all()
    # 获取12个打折商品
    sale_goods = Goods.query.filter_by(is_sale=1).order_by(
                    Goods.addtime.desc()
                        ).limit(12).all()
    return render_template('home/index.html',new_goods=new_goods,sale_goods=sale_goods,hot_goods=hot_goods) # 渲染模板

@home.route("/goods_list/<int:supercat_id>/")
def goods_list(supercat_id=None):  # supercat_id 为商品大分类ID
    """
    商品页
    """
    page = request.args.get('page', 1, type=int)  # 获取page参数值
    page_data = Goods.query.filter_by(supercat_id=supercat_id).paginate(page=page, per_page=12)
    hot_goods = Goods.query.filter_by(supercat_id=supercat_id).order_by(Goods.views_count.desc()).limit(7).all()
    return render_template('home/goods_list.html',page_data=page_data,hot_goods=hot_goods,supercat_id=supercat_id)

@home.route("/goods_detail/<int:id>/")
def goods_detail(id=None):  # id 为商品ID
    """
    详情页
    """
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    goods = Goods.query.get_or_404(id) # 根据景区ID获取景区数据，如果不存在返回404
    # 浏览量加1
    goods.views_count += 1
    db.session.add(goods) # 添加数据
    db.session.commit()   # 提交数据
    # 获取左侧热门商品
    hot_goods = Goods.query.filter_by(subcat_id=goods.subcat_id).order_by(Goods.views_count.desc()).limit(5).all()
    # 获取底部相关商品
    similar_goods = Goods.query.filter_by(subcat_id=goods.subcat_id).order_by(Goods.addtime.desc()).limit(5).all()
    return render_template('home/goods_detail.html',goods=goods,hot_goods=hot_goods,similar_goods=similar_goods,user_id=user_id)   # 渲染模板


@home.route("/search/")
def goods_search():
    """
    搜素功能
    """
    page = request.args.get('page', 1, type=int) # 获取page参数值
    keywords = request.args.get('keywords','',type=str)

    if keywords :
        # 使用like实现模糊查询
        page_data = Goods.query.filter(Goods.name.like("%"+keywords+"%")).order_by(
            Goods.addtime.desc()
        ).paginate(page=page, per_page=12)
    else :
        page_data = Goods.query.order_by(
            Goods.addtime.desc()
        ).paginate(page=page, per_page=12)
    hot_goods = Goods.query.order_by(Goods.views_count.desc()).limit(7).all()
    return render_template("home/goods_search.html", page_data=page_data,keywords=keywords,hot_goods=hot_goods)

@home.route("/cart_add/")
@user_login
def cart_add():
    """
    添加购物车
    """
    cart = Cart(
        goods_id = request.args.get('goods_id'),
        number = request.args.get('number'),
        user_id=session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    )
    db.session.add(cart) # 添加数据
    db.session.commit()   # 提交数据
    return redirect(url_for('home.shopping_cart'))

@home.route("/cart_clear/")
@user_login
def cart_clear():
    """
    清空购物车
    """
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
    db.session.commit()
    return redirect(url_for('home.shopping_cart'))

@home.route("/shopping_cart/")
@user_login
def shopping_cart():
    user_id = session.get('user_id',0)
    cart = Cart.query.filter_by(user_id = int(user_id)).order_by(Cart.addtime.desc()).all()
    if cart:
        return render_template('home/shopping_cart.html',cart=cart)
    else:
        return render_template('home/empty_cart.html')

@home.route("/cart_order/",methods=['GET','POST'])
@user_login
def cart_order():
    if request.method == 'POST':
        user_id = session.get('user_id',0) # 获取用户id
        # 添加订单
        orders = Orders(
            user_id = user_id,
            recevie_name = request.form.get('recevie_name'),
            recevie_tel = request.form.get('recevie_tel'),
            recevie_address = request.form.get('recevie_address'),
            remark = request.form.get('remark')
        )
        db.session.add(orders)  # 添加数据
        db.session.commit()      # 提交数据
        # 添加订单详情
        cart = Cart.query.filter_by(user_id=user_id).all()
        object = []
        for item in cart :
            object.append(
                OrdersDetail(
                    order_id=orders.id,
                    goods_id=item.goods_id,
                    number = item.number,)
            )
        db.session.add_all(object)
        # 更改购物车状态
        Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
        db.session.commit()
    return redirect(url_for('home.index'))

@home.route("/order_list/",methods=['GET','POST'])
@user_login
def order_list():
    """"
    我的订单
    """
    user_id = session.get('user_id',0)
    orders = OrdersDetail.query.join(Orders).filter(Orders.user_id==user_id).order_by(Orders.addtime.desc()).all()
    return render_template('home/order_list.html',orders=orders)


@home.route("/collect_add/")
@user_login
def collect_add():
    """
    收藏景区
    """
    scenic_id = request.args.get("scenic_id", "")   # 接收传递的参数scenic_id
    user_id   = session.get('user_id',0)            # 获取当前用户的ID
    collect = Collect.query.filter_by(              # 根据用户ID和景区ID判断是否该收藏
        user_id =int(user_id),
        scenic_id=int(scenic_id)
    ).count()
    # 已收藏
    if collect == 1:
        data = dict(ok=0)     # 写入字典
    # 未收藏进行收藏
    if collect == 0:
        collect = Collect(
            user_id =int(user_id),
            scenic_id=int(scenic_id)
        )
        db.session.add(collect)  # 添加数据
        db.session.commit()      # 提交数据
        data = dict(ok=1)        # 写入字典
    import json                 # 导入模块
    return json.dumps(data)     # 返回json数据

@home.route("/collect_cancel/")
@user_login
def collect_cancel():
    """
    收藏景区
    """
    id = request.args.get("id", "")    # 获取景区ID
    user_id = session["user_id"]       # 获取当前用户ID
    collect = Collect.query.filter_by(id=id,user_id=user_id).first() # 查找Collect表，查看记录是否存在
    if collect :                      # 如果存在
        db.session.delete(collect)     # 删除数据
        db.session.commit()             # 提交数据
        data = dict(ok=1)               # 写入字典
    else :
        data = dict(ok=-1)           # 写入字典
    import json                     # 引入json模块
    return json.dumps(data)         # 输出json格式


@home.route("/collect_list/")
@user_login
def collect_list():
    page = request.args.get('page', 1, type=int) # 获取page参数值
    # 根据user_id删选Collect表数据
    page_data = Collect.query.filter_by(user_id = session['user_id']).order_by(
        Collect.addtime.desc()
    ).paginate(page=page, per_page=3)                                     # 使用分页方法
    return render_template('home/collect_list.html',page_data=page_data) # 渲染模板

