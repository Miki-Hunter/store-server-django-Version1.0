# store-server-django V1.0
## 一些说明
### 1、此为根据原 node.js + Koa框架 使用django + drf 重构的方法  

部分接口有所改动，请求逻辑、数据库等有细微变化，对应改动后的前端项目toUser  

由于本人drf属于初学，代码习惯比较差，当然可以有很高效且优雅的写法，有待继续学习改进。  

此为前端用户项目[前端项目 toUser1.0](https://github.com/Miki-Hunter/toUser-vue-store-1.0)  

本项目为后端：[DRF后端1.0](https://github.com/Miki-Hunter/store-server-django-Version1.0)  

与之对应的后台管理项目 [前端项目 toAdmin1.0](https://github.com/Miki-Hunter/toAdmin-vue-store-1.0) 基于Vue3、element-Plus，正在学习和改进  


[原作者-后端](https://github.com/hai-27/store-server) 全部采用post方法实现。  
[原作者-前端](https://github.com/hai-27/vue-store)   

### 2、购物车模块、订单模块、收藏模块  都有登录校验

### 3、使用drf时，前端写网址时最后加上一条斜杠  例如 "/api/product/getPromoProduct/"  ,否则可能无法访问  
[原作者-前端](https://github.com/hai-27/vue-store) 

### 4、关于 order_time 时间戳

	如 	"order_time": 1659522650709,  使用的是毫秒级时间戳
		 "order_id": 11659522650709,  则是 user_id  +  order_time

### 5、 [API文档](https://github.com/Miki-Hunter/store-server-django-Version1.0/blob/main/storeAPI.md) 

### 6、添加了后台管理的功能，API接口尚未编写到文档内，可参考Django项目中url界面的注解

### 7、添加激活校验，需要邮箱校验，返回一个激活链接(功能在用户注册部分)，此为本人验证工作，可根据需要引入


### 8、 关于启动

1） 和一般的django项目没什么区别

2）安装依赖，也就是requirments.txt 列出的内容

3）设置数据库 ，我用的是Mysql， sql文件也准备好了，使用前自定义数据库名

4）数据库迁移

5）启动

6）在正式对接前端前，最好进行api测试
