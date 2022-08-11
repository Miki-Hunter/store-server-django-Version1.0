from django.urls import path, include
from rest_framework import routers
from apps.views import ProductInfoViewSet, OrdersInfoViewSet, \
    ShoppingCartInfoViewSet, UserInfoViewSet, CarouselInfoViewSet, CollectInfoViewSet

router_users = routers.DefaultRouter()
router_users.register('login', UserInfoViewSet.Login)  # 登录
router_users.register('loginAdmin', UserInfoViewSet.LoginAdmin) # 登录-管理员
router_users.register('findUserName', UserInfoViewSet.IsRegister) # 查询用户名是否已经注册
router_users.register('register', UserInfoViewSet.Register) # 注册
router_users.register('getUsers', UserInfoViewSet.GetUserInfo) # 获取用户信息
router_users.register('editUser', UserInfoViewSet.EditUsers)    # 编辑用户信息
router_users.register('changeUserState', UserInfoViewSet.EditUsers)   # 修改用户状态
router_users.register('deleteUser', UserInfoViewSet.DeleteUser)  # 删除用户

router_shoppingCart = routers.DefaultRouter()
router_shoppingCart.register('getShoppingCart', ShoppingCartInfoViewSet.GetShoppingCart) # 获取购物车信息
router_shoppingCart.register('addShoppingCart', ShoppingCartInfoViewSet.AddShoppingCart) # 添加购物车信息
router_shoppingCart.register('deleteShoppingCart', ShoppingCartInfoViewSet.DeleteShoppingCart) # 删除购物车信息
router_shoppingCart.register('updateShoppingCart', ShoppingCartInfoViewSet.UpdateShoppingCart) # 更新购物车信息

router_resources = routers.DefaultRouter()
router_resources.register('carousel', CarouselInfoViewSet.CarouselInfo) # 获取轮播图信息、删除轮播图、添加轮播图

router_product = routers.DefaultRouter()
router_product.register('getPromoProduct', ProductInfoViewSet.GetPromoProduct)  #获取促销商品（首页展示用）
router_product.register('getDetails', ProductInfoViewSet.GetDetails)  #获取商品详情
router_product.register('getDetailsPicture', ProductInfoViewSet.GetDetailsPicture) #获取商品详情图片、添加、删除
router_product.register('getCategory', ProductInfoViewSet.GetCategory)  #获取商品分类列表
router_product.register('getAllProduct', ProductInfoViewSet.GetAllProduct) #获取所有商品
router_product.register('getHotProduct', ProductInfoViewSet.GetHotProduct) #获取热销商品 (多种类中销量最高的前几件)
router_product.register('getProductByCategory', ProductInfoViewSet.GetProductByCategory) #获取指定分类的商品
router_product.register('getProductBySearch', ProductInfoViewSet.GetProductBySearch) #按搜索内容获取商品
router_product.register('deleteProduct', ProductInfoViewSet.DeleteProduct) #删除商品
router_product.register('updateProduct', ProductInfoViewSet.UpdateProduct) #更新商品


router_order = routers.DefaultRouter()
router_order.register('getOrder', OrdersInfoViewSet.GetOrder) #获取订单信息
router_order.register('addOrder', OrdersInfoViewSet.AddOrder) #添加订单信息
router_order.register('getOrderBySearch', OrdersInfoViewSet.GetOrderBySearch) #按搜索内容获取订单信息
router_order.register('deleteOrder', OrdersInfoViewSet.DeleteOrder) #删除订单信息
router_order.register('getOrdersInfo', OrdersInfoViewSet.OrderList) #获取订单统计结果

router_collect = routers.DefaultRouter()
router_collect.register('addCollect', CollectInfoViewSet.AddCollect) #添加收藏信息
router_collect.register('getCollect', CollectInfoViewSet.GetCollect) #获取收藏信息
router_collect.register('deleteCollect', CollectInfoViewSet.DeleteCollect) #删除收藏信息


router_menus = routers.DefaultRouter()
router_menus.register('menusList', UserInfoViewSet.GetMenus) #获取菜单信息
urlpatterns = [
    path('users/', include(router_users.urls)),
    path('resources/', include(router_resources.urls)),
    path('user/shoppingCart/', include(router_shoppingCart.urls)),
    path('user/collect/', include(router_collect.urls)),
    path('user/order/', include(router_order.urls)),
    path('product/', include(router_product.urls)),
    path('menus/', include(router_menus.urls)),
]
