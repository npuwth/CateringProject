from django.db import models


# Create your models here.

# 用户数据模型
class User(models.Model):
    id = models.AutoField(primary_key=True)  # 用户id
    name = models.CharField(max_length=32, verbose_name="用户名")  # 用户名
    password = models.CharField(max_length=32, verbose_name="密码")  # 密码
    number = models.CharField(max_length=12, verbose_name="学工号", null=True)  # 学工号
    telephone = models.CharField(max_length=12, verbose_name="用户电话", null=True)  # 用户电话
    last_time = models.DateTimeField(auto_now=True, verbose_name="登录时间")  # 登录时间


# 供应商数据模型
class Provider(models.Model):
    id = models.AutoField(primary_key=True)  # 供应商id
    name = models.CharField(max_length=128, verbose_name="供应商名称")  # 供应商名称
    address = models.CharField(max_length=128, verbose_name="供应商地址")  # 供应商地址
    telephone = models.CharField(max_length=12, verbose_name="供应商电话")  # 供应商电话


# 窗口数据模型
class Window(models.Model):
    id = models.AutoField(primary_key=True)  # 窗口id
    name = models.CharField(max_length=128, verbose_name="窗口名称")  # 窗口名称
    place = models.CharField(max_length=128, verbose_name="窗口位置")  # 窗口位置
    avg_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="平均价格", null=True)  # 平均价格
    avg_star = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="平均评分", null=True)  # 平均评分
    mon_sale = models.IntegerField(verbose_name="月销量", null=True, default=0)  # 月销量
    pro_id = models.ForeignKey(to='Provider', on_delete=models.CASCADE, verbose_name="供应商id")  # 供应商id（外键）


# 商品数据模型
class Dish(models.Model):
    id = models.AutoField(primary_key=True)  # 商品id
    # 商品图片
    name = models.CharField(max_length=128, verbose_name="商品名称")  # 商品名称
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品价格")  # 商品价格
    avg_star = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品评分", null=True)  # 商品评分
    mon_sale = models.IntegerField(verbose_name="月销量", null=True, default=0)  # 月销量
    win_id = models.ForeignKey(to='Window', on_delete=models.CASCADE, verbose_name="窗口id")  # 窗口id（外键）


# 图片数据
class Image(models.Model):
    id = models.AutoField(primary_key=True)  # 图片id
    img_address = models.ImageField(verbose_name="图片路径")  # 图片路径 -->> 会将路径封装成一个对象，需要使用模块Pillow,python 3.6 后 使用 PIL 模块
    img_label = models.CharField(max_length=128, verbose_name="图片名称")  # 图片名称
    dish = models.ForeignKey(to='Dish', on_delete=models.CASCADE, default=None, verbose_name="商品")  # 图片对应的商品（外键）


# 购买与评价数据模型
class Purchase(models.Model):
    id = models.AutoField(primary_key=True)  # 购买id
    dish_id = models.ForeignKey(to='Dish', on_delete=models.CASCADE, verbose_name="商品id")  # 商品id
    user_id = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name="用户id")  # 用户id
    time = models.DateTimeField(auto_now=True, verbose_name="购买时间")  # 购买时间
    star = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品评分", null=True)  # 评分
