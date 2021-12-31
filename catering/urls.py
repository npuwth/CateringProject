from django.urls import path

from catering import views

app_name = "catering"

urlpatterns = [

    path('register/', views.register),  # 注册功能
    path('login/', views.login),  # 登录功能
    path('logout/', views.logout),  # 登出功能
    path('error/', views.error),  # 权限错误
    path('more/', views.more),  # 更多信息

    path('add_provider/', views.add_provider),
    path("provider_list/", views.provider_list, name="provider_list"),
    path("provider_list/<int:page>", views.provider_list, name="provider_list"),
    path("update_provider/", views.update_provider, name="update_provider"),
    path("delete_provider/", views.delete_provider, name="delete_provider"),

    path("add_dish/", views.add_dish, name="add_dish"),
    path("dish_list/", views.dish_list, name="dish_list"),
    path("dish_list/<int:page>", views.dish_list, name="dish_list"),
    path("update_dish/", views.update_dish, name="update_dish"),
    path("delete_dish/", views.delete_dish, name="delete_dish"),

    path("add_window/", views.add_window, name="add_window"),
    path("window_list/", views.window_list, name="window_list"),
    path("window_list/<int:page>/", views.window_list, name="window_list"),
    path('update_window/', views.update_window, name="update_window"),
    path("delete_window/", views.delete_window, name="delete_window"),

    path("add_user/", views.add_user, name="add_user"),
    path("user_list/", views.user_list, name="user_list"),
    path("user_list/<int:page>", views.user_list, name="user_list"),
    path("update_user/", views.update_user, name="update_user"),
    path("delete_user/", views.delete_user, name="delete_user"),

    path("add_purchase/", views.add_purchase, name="add_purchase"),
    path("purchase_list/", views.purchase_list, name="purchase_list"),
    path("purchase_list/<int:page>", views.purchase_list, name="purchase_list"),
    path("update_purchase/", views.update_purchase, name="update_purchase"),
    path("delete_purchase/", views.delete_purchase, name="delete_purchase"),

    path('index/', views.index),  # 首页
    # path('user_index/', views.user_index),  # 用户首页
    # path('index/<int:page>', views.index, name="index"),  # 首页
    path("search/", views.search, name="search"),  # 全局搜索

]
