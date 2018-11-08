from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),
    url(r'^registe/$', views.registe, name='registe'),
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^addcart/$', views.addcart, name='addcart'),  # 添加购物车，发起ajax请求的路由
    url(r'^subcart/$', views.subcart, name='subcart'),  # 购物车减操作
    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'),  # 修改选中状态
    url(r'changecartselect/$', views.changecartselect, name='changecartselect'),  # 全选/取消全选
    url(r'^generateorder/$', views.generateorder, name='generateorder'),  # 下单
    url(r'^orderinfo/(\d+)/$', views.orderinfo, name='orderinfo'),

    url(r'^pay/$', views.pay, name='pay'),  # 支付
    url(r'^notifyurl/$', views.notifyurl, name='notifyurl'),  # 支付完成后的通知
    url(r'^returnurl/$', views.returnurl, name='returnurl'),  # 支付完成后的跳转

]
