import hashlib
import time,re
from datetime import datetime
from random import randint

from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect
from faker import Faker

# 加密 md5进行加密 -->> 不可逆的  123 --> md5 -->abc
#  使用md5进行加密 ： 固定的密码生成固定的加密内容 123 --->> abc
from catering import models


# 定义一个 加密函数pwd_encrypt，对用户的密码进行md5加密
def pwd_encrypt(password):
    md5 = hashlib.md5()  # 获取md5对象
    md5.update(password.encode())  # 进行更新注意需要使用 字符串的二进制格式
    result = md5.hexdigest()  # 获取加密后的内容
    return result


# 注册视图
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        number = request.POST.get('number')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        # password = pwd_encrypt(password)
        models.User.objects.create(name=username, password=password, number=number, telephone=telephone)
        return redirect('/catering/login/')
    return render(request, 'register.html')


# 登录视图
def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        # pwd = pwd_encrypt(pwd)
        # select * from user where name=username and password =pwd
        ret = models.User.objects.filter(name=username, password=pwd)
        # print(ret) # 如果用户不存在 返回空 QuerySet对象,转换成False
        if ret:
            # 有此用户 -->> 跳转到首页
            # 登录成功后，将用户名和昵称保存到session 中，
            request.session['username'] = username
            user_obj = ret.last()  # 获取user对象
            request.session['id'] = user_obj.id

            return redirect('/catering/index/')

        else:
            # 没有此用户-->> 用户名或者密码错误
            error_msg = '用户名或者密码错误请重新输入'
    return render(request, 'login.html', {'error_msg': error_msg})


# 退出(登出)
def logout(request):
    request.session.flush()
    return redirect('/catering/login/')


# 权限错误
def error(request):
    error_msg = "请使用管理员身份登录"
    return render(request, "error.html", locals())

def addresserror(request):
    return render(request, "addresserror.html")

# 更多信息
def more(request):
    return render(request, "more.html")


# 装饰器
def user_decorator(func):
    def inner(request, *args, **kwargs):
        username = request.session.get('username')
        if username:
            """用户登录过"""
            return func(request, *args, **kwargs)
        else:
            """用户没有登录，重定向到登录页面"""
            return redirect('/catering/login/')
    return inner


# 装饰器
def admin_decorator(func):
    def inner(request, *args, **kwargs):
        obj_id = request.session.get('id')
        if obj_id == 1:
            """管理员"""
            return func(request, *args, **kwargs)
        else:
            """普通用户"""
            return redirect('/catering/error/')
    return inner


# 增加供应商
@user_decorator
@admin_decorator
def add_provider(request):
    if request.method == 'POST':
        provider_name = request.POST.get('provider_name')
        provider_address = request.POST.get('provider_address')
        provider_telephone = request.POST.get('provider_telephone')
        models.Provider.objects.create(name=provider_name, address=provider_address, telephone=provider_telephone)
        return redirect('/catering/provider_list/')
    return render(request, 'provider_add.html')


# 供应商列表
@user_decorator
def provider_list(request, page=1):
    if request.method == "GET":
        provider_obj_list = models.Provider.objects.all()
        paginator = Paginator(provider_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page if page else request.GET.get("page", 1)  # 当前页，默认显示第一页
        provider_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)
        else:
            page_range = page_range
        return render(request, "provider_list.html", locals())


# 更新供应商
@user_decorator
@admin_decorator
def update_provider(request):
    if request.method == "GET":
        obj_id = request.GET.get("id")
        provider = models.Provider.objects.get(id=obj_id)
        return render(request, "provider_update.html", locals())
    else:
        obj_id = request.POST.get("id")
        names = request.POST.get("name")
        address = request.POST.get("address")
        telephone = request.POST.get("telephone")
        models.Provider.objects.filter(id=obj_id).update(name=names, address=address, telephone=telephone)
        return redirect("/catering/provider_list/")


# 删除供应商
@user_decorator
@admin_decorator
def delete_provider(request):
    obj_id = request.GET.get("id")
    provider = models.Provider.objects.get(id=obj_id)
    provider.delete()
    return redirect("/catering/provider_list/")


# def search(request):
#     pass


# 增加商品
@user_decorator
@admin_decorator
def add_dish(request):
    if request.method == "GET":
        window_list = models.Window.objects.all()
        return render(request, "dish_add.html", locals())
    elif request.method == "POST":
        # 获取dish_add.html表单提交过来的数据
        dish_name = request.POST.get("dish_name")
        window_id = request.POST.get("window")
        dish_price = request.POST.get("dish_price")
        # dish_star = request.POST.get("dish_star")
        # dish_sale = request.POST.get("dish_sale")

        window_obj = models.Window.objects.get(id=window_id)  # 窗口对象
        # 将表单获取到的数据保存到数据库中
        dish_obj = models.Dish.objects.create(
            name=dish_name,
            price=dish_price,
            win_id=window_obj
        )
        # 保存图片
        # 注意上传字段使用 FILES.getlist() 来获取 多张图片
        userfiles = request.FILES.getlist('dish_image')  # 图书缩略图
        # 循环遍历读取每一张图片保存到images下  -->>枚举 （0,'<InMemoryUploadedFile: 3.jpg (image/jpeg)>'）
        for index, image_obj in enumerate(userfiles):
            name = image_obj.name.rsplit('.', 1)[1]  # 图书格式
            path = 'catering/static/images/dish/{}_{}.{}'.format(dish_name, index, name)  # 图片路径
            # 保存图片
            with open(path, mode='wb') as f:
                for content in image_obj.chunks():
                    f.write(content)
            # 保存图片路径到数据库
            obj_image = models.Image()
            path1 = 'images/dish/{}_{}.{}'.format(dish_name, index, name)
            obj_image.img_address = path1
            obj_image.img_label = image_obj.name  # 图片原名称
            obj_image.dish = dish_obj  # 设置图片和商品的关系
            obj_image.save()
            # 重定向到商品列表
        return redirect("/catering/dish_list/")


@user_decorator
def dish_list(request, page=1):
    if request.method == "GET":
        dish_obj_list = models.Dish.objects.all()
        paginator = Paginator(dish_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page  # 当前页，默认显示第一页
        dish_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 确定页码范围
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)

        return render(request, "dish_list.html", locals())


@user_decorator
@admin_decorator
def update_dish(request):
    if request.method == "GET":
        obj_id = request.GET.get("id")
        dish_obj = models.Dish.objects.get(id=obj_id)
        window_list = models.Window.objects.all()
        return render(request, "dish_update.html", locals())
    else:
        obj_id = request.POST.get("id")
        dish_name = request.POST.get("dish_name")
        dish_price = request.POST.get("dish_price")
        window_id = request.POST.get("window")  # 窗口id
        window_obj = models.Window.objects.get(id=window_id)  # 窗口对象

        dish_obj = models.Dish.objects.filter(id=obj_id).update(
            name=dish_name,
            price=dish_price,
            win_id=window_obj
        )
        # 重定向到商品列表
        return redirect("/catering/dish_list/")


@user_decorator
@admin_decorator
def delete_dish(request):
    obj_id = request.GET.get("id")
    models.Dish.objects.get(id=obj_id).delete()
    return redirect("/catering/dish_list/")


@user_decorator
@admin_decorator
def add_window(request):
    if request.method == "GET":
        provider_obj_list = models.Provider.objects.all()
        return render(request, "window_add.html", locals())
    elif request.method == "POST":
        name = request.POST.get("name")
        place = request.POST.get("place")
        provider_id = request.POST.get("provider")
        provider_obj = models.Provider.objects.get(id=provider_id)
        window_obj = models.Window.objects.create(name=name, place=place, pro_id=provider_obj)

        return redirect("/catering/window_list/")


@user_decorator
def window_list(request, page=1):
    if request.method == "GET":
        window_obj_list = models.Window.objects.all()
        paginator = Paginator(window_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page  # 当前页，默认显示第一页
        window_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 确定页码范围
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)

        return render(request, "window_list.html", locals())


@user_decorator
@admin_decorator
def update_window(request):
    if request.method == "GET":
        obj_id = request.GET.get("id")
        window_obj = models.Window.objects.get(id=obj_id)
        provider_obj_list = models.Provider.objects.all()
        return render(request, "window_update.html", locals())
    else:
        obj_id = request.POST.get("id")
        name = request.POST.get("name")
        place = request.POST.get("place")

        provider_id = request.POST.get("provider")
        provider_obj = models.Provider.objects.get(id=provider_id)

        window_obj = models.Window.objects.filter(id=obj_id).update(
            name=name,
            place=place,
            pro_id=provider_obj
        )
        # 重定向到窗口列表
        return redirect("/catering/window_list/")


@user_decorator
@admin_decorator
def delete_window(request):
    obj_id = request.GET.get("id")
    window = models.Window.objects.get(id=obj_id)
    window.delete()
    return redirect("/catering/window_list/")


# 增加用户
@user_decorator
@admin_decorator
def add_user(request):
    if request.method == "GET":
        return render(request, "user_add.html")
    else:
        name = request.POST.get("name")
        number = request.POST.get("number")
        telephone = request.POST.get("telephone")
        password = request.POST.get("password")
        # password = pwd_encrypt(password)
        user_obj = models.User.objects.create(
            name=name,
            number=number,
            telephone=telephone,
            password=password
        )
        return redirect("/catering/user_list/")


@user_decorator
# @admin_decorator
def user_list(request, page=1):
    if request.method == "GET":
        user_id = request.session.get('id')
        if user_id == 1:
            user_obj_list = models.User.objects.all()
        else:
            user_obj_list = models.User.objects.filter(id=user_id)
        paginator = Paginator(user_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page  # 当前页，默认显示第一页
        user_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 当前页
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)

        return render(request, "user_list.html", locals())


@user_decorator
def update_user(request):
    if request.method == "GET":
        obj_id = request.GET.get("id")
        user_obj = models.User.objects.get(id=obj_id)
        return render(request, "user_update.html", locals())
    else:
        obj_id = request.POST.get("id")
        name = request.POST.get("name")
        number = request.POST.get("number")
        telephone = request.POST.get("telephone")
        password = request.POST.get("password")
        # password = pwd_encrypt(password)
        user_obj = models.User.objects.filter(id=obj_id).update(name=name, password=password, number=number,
                                                                telephone=telephone)

        return redirect("/catering/user_list/")


@user_decorator
@admin_decorator
def delete_user(request):
    obj_id = request.GET.get("id")
    models.User.objects.get(id=obj_id).delete()
    return redirect("/catering/user_list/")


@user_decorator
def add_purchase(request):
    dish_id = request.GET.get('id')
    user_id = request.session.get('id')
    ctime = time.localtime(time.time())
    dish = models.Dish.objects.get(id=dish_id)
    user = models.User.objects.get(id=user_id)
    models.Purchase.objects.create(dish_id=dish, user_id=user, time=ctime)
    return redirect("/catering/purchase_list/")


@user_decorator
def purchase_list(request, page=1):
    if request.method == "GET":
        user_id = request.session.get('id')
        if user_id == 1:
            purchase_obj_list = models.Purchase.objects.all()
        else:
            purchase_obj_list = models.Purchase.objects.filter(user_id=user_id)
        paginator = Paginator(purchase_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page  # 当前页，默认显示第一页
        purchase_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 当前页
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)

        return render(request, "purchase_list.html", locals())


@user_decorator
def update_purchase(request):
    if request.method == "GET":
        obj_id = request.GET.get("id")
        purchase_obj = models.Purchase.objects.get(id=obj_id)
        return render(request, "purchase_update.html", locals())
    else:
        obj_id = request.POST.get("id")
        star = request.POST.get("star")
        # print(star)
        if re.match(r'[0-5]', star, flags=0):
            purchase_obj = models.Purchase.objects.filter(id=obj_id).update(star=star)
            return redirect("/catering/purchase_list/")
        else:
            error_msg = "数据有误，请重新输入"
            return render(request, "error.html", locals())


@user_decorator
def delete_purchase(request):
    obj_id = request.GET.get("id")
    models.Purchase.objects.get(id=obj_id).delete()
    return redirect("/catering/purchase_list/")


@user_decorator
def search(request):
    # 要前端中获取用户输入的关键字
    search_keywords = request.POST.get("search_keywords", "")
    # print(search_keywords)
    if search_keywords:
        dish_obj_list = models.Dish.objects.filter(
            Q(name__icontains=search_keywords)
        )  # 根据关键词搜索数据库记录，icontains是不区分大小写

        window_obj_list = models.Window.objects.filter(
            Q(name__icontains=search_keywords)
        )

        provider_obj_list = models.Provider.objects.filter(
            Q(name__icontains=search_keywords)
        )

        user_obj_list = models.User.objects.filter(
            Q(name__icontains=search_keywords)
        )
        # 判断查询结果，用来控制前端页面绘制
        if len(dish_obj_list) != 0:  # 如果能查询到，前端显示商品查询结果
            dish_search_result = True
        elif len(window_obj_list) != 0:
            window_search_result = True
        elif len(provider_obj_list) != 0:  # 如果能查到，前端显示供应商查询结果
            provider_search_result = True
        elif len(user_obj_list) != 0:
            user_search_result = True  # 如果能查到，前端显示用户信息
        else:
            error_msg = "没有查询到结果，请重新输入"
    else:
        error_msg = "您输入的信息有误,请重新输入"
    return render(request, "search_result.html", locals())


@user_decorator
def index(request):
    user_id = request.session.get('id')
    # 从数据中获取出版社数据、作者数据、图书数据、用户数据
    provider_num = models.Provider.objects.count()
    window_num = models.Window.objects.count()
    dish_num = models.Dish.objects.count()
    user_num = models.User.objects.count()

    # 统计最近30天用户访问量
    # 当前年，月
    this_year = time.strftime("%Y", time.localtime(time.time()))
    this_month = time.strftime("%m", time.localtime(time.time()))
    res = models.User.objects.filter(last_time__month=this_month)
    # print(res)
    # 按天分组
    select = {'day': connection.ops.date_trunc_sql('day', 'last_time')}
    # 获取当月每天的用户访问数据
    count_data = models.User.objects.filter(last_time__year=this_year, last_time__month=this_month).extra(
        select=select).values('day').annotate(number=Count('id'))

    # TODO：获取前30天的用户访问数量
    # 计算第前30天时间
    # time_30 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    # count_data = models.User.objects.filter(last_time__gte=time_30).extra(
    #     select=select).values('day').annotate(number=Count('id'))

    # 下面来处理数据，让当月的每天用户访问量和日期对应方便绘制折线图
    day_list = []  # 当月时间列表
    user_num_list = []  # 每天用户登录人数列表
    user_list = []
    for i, obj in enumerate(count_data):
        day_list.append(obj['day'].day)
        user_num_list.append(obj['number'])
    # 把当月时间列表和每天用户登录人数列表 转成成字典，方便后面进行数据处理
    user_login_dict = dict(zip(day_list, user_num_list))
    # 统计30天中每天用户登录人数，如果某一天没有人登录就置为0
    for day in range(1, 31):
        if day not in day_list:  # 如果某天不在数据库中的天数中时,说明这天网站没有用户浏览，用户数据为0
            user_login_dict[day] = 0

    # 按照日期顺序的方式，把这个月每天登录人数进行排序，把每天的登录人数放到列表里，方便给前端模板传值
    user_login_list = []
    for day in range(1, 31):
        for k, v in user_login_dict.items():
            if day == k:
                user_login_list.append(v)


    # 选择销量前10的商品并且倒序排列
    dish_obj_list = models.Dish.objects.all().order_by("-mon_sale")
    paginator = Paginator(dish_obj_list, 10)  # 实例化分页对象，每页显示10条数据
    total_page_num = paginator.num_pages  # 总页码
    current_page_num = 1  # 当前页，默认显示第一页
    dish_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示

    return render(request, 'index.html', locals())

