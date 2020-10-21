# _*_ coding:utf-8 _*_
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request,jsonify
from app.admin.forms import LoginForm,GoodsForm
from app.models import Admin,Goods,SuperCat,SubCat,User,Orders,OrdersDetail
from sqlalchemy import or_
from functools import wraps
from decimal import *


def admin_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@admin.route("/")
@admin_login
def index():
    page = request.args.get('page', 1, type=int) # 获取page参数值
    page_data = Goods.query.order_by(
        Goods.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/index.html",page_data=page_data)

@admin.route("/goods/add/", methods=["GET", "POST"])
@admin_login
def goods_add():
    """
    添加商品
    """
    form = GoodsForm()               # 实例化form表单
    supercat_list = [(v.id, v.cat_name) for v in SuperCat.query.all()]  # 为super_cat_id添加属性
    form.supercat_id.choices = supercat_list  # 为super_cat_id添加属性
    form.subcat_id.choices = [(v.id, v.cat_name) for v in SubCat.query.filter_by(super_cat_id=supercat_list[0][0]).all()]  # 为super_cat_id添加属性
    form.current_price.data = form.data['original_price'] # 为current_pirce 赋值
    if form.validate_on_submit():    # 添加商品情况
        data = form.data
        goods = Goods(
            name = data["name"],
            supercat_id = int(data['supercat_id']),
            subcat_id = int(data['subcat_id']),
            picture= data["picture"],
            original_price = Decimal(data["original_price"]).quantize(Decimal('0.00')), # 转化为包含2位小数的形式
            current_price = Decimal(data["original_price"]).quantize(Decimal('0.00')),  # 转化为包含2位小数的形式
            is_new = int(data["is_new"]),
            is_sale = int(data["is_sale"]),
            introduction=data["introduction"],
        )
        db.session.add(goods)  # 添加数据
        db.session.commit()     # 提交数据
        return redirect(url_for('admin.index')) # 页面跳转
    return render_template("admin/goods_add.html", form=form) # 渲染模板


@admin.route("/goods/detail/", methods=["GET", "POST"])
@admin_login
def goods_detail():
    goods_id = request.args.get('goods_id')
    goods = Goods.query.filter_by(id=goods_id).first_or_404()
    return render_template('admin/goods_detail.html',goods=goods)

@admin.route("/goods/edit/<int:id>", methods=["GET", "POST"])
@admin_login
def goods_edit(id=None):
    """
    编辑商品
    """
    goods = Goods.query.get_or_404(id)
    form = GoodsForm() # 实例化form表单
    form.supercat_id.choices = [(v.id, v.cat_name) for v in SuperCat.query.all()]  # 为super_cat_id添加属性
    form.subcat_id.choices = [(v.id, v.cat_name) for v in SubCat.query.filter_by(super_cat_id=goods.supercat_id).all()]  # 为super_cat_id添加属性

    if request.method == "GET":
        form.name.data = goods.name
        form.picture.data = goods.picture
        form.current_price.data = goods.current_price
        form.original_price.data = goods.original_price
        form.supercat_id.data = goods.supercat_id
        form.subcat_id.data = goods.subcat_id
        form.is_new.data = goods.is_new
        form.is_sale.data = goods.is_sale
        form.introduction.data = goods.introduction
    elif form.validate_on_submit():
        goods.name = form.data["name"]
        goods.supercat_id = int(form.data['supercat_id'])
        goods.subcat_id = int(form.data['subcat_id'])
        goods.picture= form.data["picture"]
        goods.original_price = Decimal(form.data["original_price"]).quantize(Decimal('0.00'))
        goods.current_price = Decimal(form.data["current_price"]).quantize(Decimal('0.00'))
        goods.is_new = int(form.data["is_new"])
        goods.is_sale = int(form.data["is_sale"])
        goods.introduction=form.data["introduction"]
        db.session.add(goods)  # 添加数据
        db.session.commit()     # 提交数据
        return redirect(url_for('admin.index')) # 页面跳转

    return render_template("admin/goods_edit.html", form=form) # 渲染模板

@admin.route("/goods/select_sub_cat/", methods=["GET"])
@admin_login
def select_sub_cat():
    """
    查找子分类
    """
    super_id = request.args.get("super_id", "")  # 接收传递的参数super_id
    subcat = SubCat.query.filter_by(super_cat_id = super_id).all()
    result = {}
    if subcat:
        data = []
        for item in subcat:
            data.append({'id':item.id,'cat_name':item.cat_name})
        result['status'] = 1
        result['message'] = 'ok'
        result['data'] = data
    else:
        result['status'] = 0
        result['message'] = 'error'
    return jsonify(result)   # 返回json数据

@admin.route("/goods/del_confirm/")
@admin_login
def goods_del_confirm():
    '''确认删除商品'''
    goods_id = request.args.get('goods_id')
    goods = Goods.query.filter_by(id=goods_id).first_or_404()
    return render_template('admin/goods_del_confirm.html',goods=goods)

@admin.route("/goods/del/<int:id>/", methods=["GET"])
@admin_login
def goods_del(id=None):
    """
    删除商品
    """
    goods = Goods.query.get_or_404(id)  # 根据景区ID查找数据
    db.session.delete(goods)             # 删除数据
    db.session.commit()                   # 提交数据
    return redirect(url_for('admin.index', page=1)) # 渲染模板


@admin.route("/login/", methods=["GET","POST"])
def login():
    """
    登录功能
    """
    # 判断是否已经登录
    if "admin" in session:
        return redirect(url_for("admin.index"))
    form = LoginForm()   # 实例化登录表单
    if form.validate_on_submit():   # 验证提交表单
        data = form.data    # 接收数据
        admin = Admin.query.filter_by(manager=data["manager"]).first() # 查找Admin表数据
        # 密码错误时，check_password,则此时not check_password(data["pwd"])为真。
        if not admin.check_password(data["password"]):
            flash("密码错误!", "err")   # 闪存错误信息
            return redirect(url_for("admin.login")) # 跳转到后台登录页
        # 如果是正确的，就要定义session的会话进行保存。
        session["admin"] = data["manager"]  # 存入session
        session["admin_id"] = admin.id # 存入session
        return redirect(url_for("admin.index")) # 返回后台主页
    return render_template("admin/login.html",form=form)

@admin.route('/logout/')
@admin_login
def logout():
    """
    后台注销登录
    """
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))

@admin.route("/user/list/", methods=["GET"])
@admin_login
def user_list():
    """
    会员列表
    """
    page = request.args.get('page', 1, type=int) # 获取page参数值 
    keyword = request.args.get('keyword', '', type=str)
    if keyword:
        # 根据姓名或者邮箱查询
        filters = or_(User.username == keyword, User.email == keyword)
        page_data = User.query.filter(filters).order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:
        page_data = User.query.order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)

    return render_template("admin/user_list.html", page_data=page_data)


@admin.route("/user/view/<int:id>/", methods=["GET"])
@admin_login
def user_view(id=None):
    """
    查看会员详情
    """
    from_page = request.args.get('fp')
    if not from_page:
        from_page = 1
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user, from_page=from_page)


@admin.route('/supercat/add/',methods=["GET","POST"])
@admin_login
def supercat_add():
    """
    添加大分类
    """
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        supercat = SuperCat.query.filter_by(cat_name=cat_name).count()
        if supercat :
            flash("大分类已存在", "err")
            return redirect(url_for("admin.supercat_add"))
        data = SuperCat(
            cat_name = cat_name,
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("admin.supercat_list"))
    return render_template("admin/supercat_add.html")

@admin.route("/supercat/list/", methods=["GET"])
@admin_login
def supercat_list():
    """
    大分类列表
    """
    data = SuperCat.query.order_by(
        SuperCat.addtime.desc()
    ).all()
    return render_template("admin/supercat.html", data=data) # 渲染模板

@admin.route("/supercat/del/", methods=["POST"])
@admin_login
def supercat_del():
    """
    大分类删除
    """
    if request.method == 'POST':
        cat_ids = request.form.getlist("delid") # cat_ids 是一个列表
        # 判断是否有子类
        for id in cat_ids:
            count = SubCat.query.filter_by(super_cat_id=id).count()
            if count:
                return "大分类下有小分类，请先删除小分类"
        # 使用in_ 方式批量删除，需要设置synchronize_session为False,而 in 操作估计还不支持
        # 解决办法就是删除时不进行同步，然后再让 session 里的所有实体都过期
        db.session.query(SuperCat).filter(SuperCat.id.in_(cat_ids)).delete(synchronize_session=False)
        db.session.commit()
        return redirect(url_for("admin.supercat_list"))

@admin.route("/subcat/list/", methods=["GET"])
@admin_login
def subcat_list():
    """
    小分类
    """
    data = SubCat.query.order_by(
        SubCat.addtime.desc()
    ).all()
    return render_template("admin/subcat.html", data=data) # 渲染模板

@admin.route('/subcat/add/',methods=["GET","POST"])
@admin_login
def subcat_add():
    """
    添加小分类
    """
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        super_cat_id = request.form['super_cat_id']
        # 检测名称是否存在
        subcat = SubCat.query.filter_by(cat_name=cat_name).count()
        if subcat :
            return "<script>alert('该小分类已经存在');history.go(-1);</script>"
        # 组织数据
        data = SubCat(
            super_cat_id = super_cat_id,
            cat_name = cat_name,
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("admin.subcat_list"))

    supercat = SuperCat.query.all()  # 获取大分类信息
    return render_template("admin/subcat_add.html",supercat=supercat)

@admin.route("/subcat/del/", methods=["POST"])
@admin_login
def subcat_del():
    """
    删除小分类
    """
    if request.method == 'POST':
        cat_ids = request.form.getlist("delid") # cat_ids 是一个列表
        # 判断子类下是否有商品
        for id in cat_ids:
            count = Goods.query.filter_by(cat_id=id).count()
            if count:
                return "<script>alert('该分类下有商品，请先删除分类下的商品');history.go(-1);</script>"
        # 使用in_ 方式批量删除，需要设置synchronize_session为False,而 in 操作估计还不支持
        # 解决办法就是删除时不进行同步，然后再让 session 里的所有实体都过期
        db.session.query(SubCat).filter(SubCat.id.in_(cat_ids)).delete(synchronize_session=False)
        db.session.commit()
        return redirect(url_for("admin.subcat_list"))


@admin.route("/orders/list/", methods=["GET"])
@admin_login
def orders_list():
    """
    订单列表页面
    """
    keywords = request.args.get('keywords','',type=str) 
    page = request.args.get('page', 1, type=int) # 获取page参数值
    if keywords :
        page_data = Orders.query.filter_by(id=keywords).order_by(
            Orders.addtime.desc()
        ).paginate(page=page, per_page=10)
    else :
        page_data = Orders.query.order_by(
            Orders.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/orders_list.html", page_data=page_data)

@admin.route("/orders/detail/", methods=["GET"])
@admin_login
def orders_detail():
    """
    订单详情
    """
    order_id = request.args.get('order_id')
    orders = OrdersDetail.query.join(Orders).filter(OrdersDetail.order_id==order_id).all()
    return render_template('admin/orders_detail.html',data = orders)

@admin.route('/topgoods/', methods=['GET'])
@admin_login
def topgoods():
    """
    销量排行榜(前10位)
    """
    orders = OrdersDetail.query.order_by(OrdersDetail.number.desc()).limit(10).all()
    return render_template("admin/topgoods.html", data=orders)