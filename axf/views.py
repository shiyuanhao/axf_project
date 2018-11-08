import hashlib
import os
import random
import time
import uuid


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF项目 import settings
from axf.alipay import alipay_axf
from axf.models import Wheel, Nav, Mustbuy, Shop, Foodtypes, Goods, Mainshow, Cart, User, Order, OrderGoods


def home(request):  # 首页
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shopList = Shop.objects.all()
    shophead = shopList[0]
    shoptab = shopList[1:3]
    shopclass = shopList[3:7]
    shopcommend = shopList[7:11]

    # 商品主体内容
    mainshows = Mainshow.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys': mustbuys,
        'shophead':shophead,
        'shoptab':shoptab,
        'shopclass':shopclass,
        'shopcommend':shopcommend,
        'mainshows':mainshows
    }

    return render(request, 'home/home.html', context=data)

# categoryid 分类ID
# childid 子类ID
# sortid 排序ID
def market(request, categoryid, childid, sortid):    # 闪购超市
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 分类 点击 下标  >>>>  分类ID
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标 获取 对应 分类ID
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    # 将每个子类拆分出来
    childTypleList = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname': arr[0],    # 子类名称
            'childid': arr[1]       # 子类ID
        }
        childTypleList.append(dir)

    # 商品信息 - 根据分类id获取对应数据
    # goodsList = Goods.objects.all()[0:5]
    if childid == '0':  # 全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:   # 分类 下 子类
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)


    # 排序
    if sortid == '1':   # 销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2': # 价格最低
        goodsList = goodsList.order_by('price')
    elif sortid == '3': # 价格最高
        goodsList = goodsList.order_by(('-price'))

    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user= user)

    data = {
        'foodtypes':foodtypes,  # 分类信息
        'goodsList':goodsList,  # 商品信息
        'childTypleList': childTypleList,   # 子类信息
        'categoryid':categoryid,    # 分类ID
        'childid': childid,     # 子类ID
        'carts': carts,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    token = request.session.get('token')
    if token:  # 显示该用户下 购物车信息
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

        return render(request, 'cart/cart.html', context={'carts': carts})
    else:  # 跳转到登录页面
        return redirect('axf:login')


def mine(request):
    # 获取用户信息
    token = request.session.get('token')

    responseData = {}

    if token:  # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['isLogin'] = 1
    else:  # 未登录
        responseData['name'] = '未登录'
        responseData['img'] = '/static/uploads/axf.png'

    return render(request, 'mine/mine.html', context=responseData)

def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()

def registe(request):
    if request.method == 'GET':
        return render(request, 'mine/registe.html')
    elif request.method == 'POST':
        # try:
            user = User()
            user.account = request.POST.get('account')
            user.password = genarate_password(request.POST.get('password'))
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.addr = request.POST.get('addr')
            # user.img = 'axf.png'

            # 头像
            imgName = user.account + '.png'
            imagePath = os.path.join(settings.MEDIA_ROOT, imgName)
            file = request.FILES.get('icon')
            with open(imagePath, 'wb') as fp:
                for data in file.chunks():
                    fp.write(data)
            user.img = imgName

            user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

            user.save()

            # 状态保持
            request.session['token'] = user.token

            # 重定向
            return redirect('axf:mine')
        # except:
        #     return HttpResponse('注册失败(该用户已被注册)')


def checkaccount(request):
    account = request.GET.get('account')

    responseData = {
        'msg': '账号可用',
        'status': 1 # 1标识可用，-1标识不可用
    }

    try:
        user = User.objects.get(account=account)
        responseData['msg'] = '账号已被占用'
        responseData['status'] = -1
        return JsonResponse(responseData)
    except:
        return JsonResponse(responseData)


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password):    # 登录成功

                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:   # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'mine/login.html', context={'acountErr':'账号不存在!'})


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'添加购物车成功',
        'status':1,
    }
    if token:
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number +1
            cart.save()
            responseData['number'] = cart.number
        else:
            cart =Cart()
            cart.user = user
            cart.goods = goods
            cart.number =1
            cart.save()
            responseData['number']= cart.number
        return JsonResponse(responseData)
    else:
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)


def subcart(request):
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg':'购物车删减成功',
        'status':1,
        'number':cart.number
    }
    return JsonResponse(responseData)


def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()
    responseData = {
        'msg':'选中状态改变',
        'status': 1,
        'isselect': cart.isselect
    }
    return JsonResponse(responseData)


def changecartselect(request):
    isselect = request.GET.get('isselect')
    if isselect == 'true':
        isselect = True
    else:
        isselect = False
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = User.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()

    return JsonResponse({'msg':'反选操作成功','status':1})


def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    order = Order()
    order.user = user
    order.identifier = str(int(time.time()))+str(random.randrange(10000,100000))
    order.save()

    carts = Cart.objects.filter(user=user).filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()

        cart.delete()
        responseData = {
            'msg':'订单生成成功',
            'status':1,
            'identifier':order.identifier
        }
    return JsonResponse(responseData)


def orderinfo(request,identifier):
    #一个订单对应多个商品
    order = Order.objects.get(identifier=identifier)

    return render(request,'order/orderinfo.html',context={'order':order})


def pay(request):
    identifier = request.GET.get('identifier')
    #支付url
    url = alipay_axf.direct_pay(
        subject = '测试订单 --- iphone X',#订单名称
        out_trade_no = identifier,#订单号
        total_amount = 9.9,#付款金额
        return_url='http://112.74.55.3/axf/returnurl/',
    )
    #拼接支付网关
    alipay_url = 'https://openapi.alipaydev.com/gateway.do?{data}'.format(data=url)
    return JsonResponse({'alipay_url':alipay_url})


def notifyurl(request):
    print('xxx 订单支付成功，请发货')
    print(request.GET.get('subject'))
    return JsonResponse({'msg':'success'})


def returnurl(request):
    print('xxx 订单支付成功，进行页面跳转')
    return HttpResponse('进行页面跳转，回到axf...')