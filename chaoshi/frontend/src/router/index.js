import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Home from '../components/Home.vue'
import Shouye from '../components/Shouye.vue'
import Favorites from '../components/Favorites.vue'; // 新增收藏页面组件
import Cart from '../components/Cart.vue'; // 新增购物车页面组件
import ItemDetail from '../components/ItemDetail.vue'; // 新增商品详情页面组件
import Purchase from '../components/purchase-history.vue'; // 新增购买历史页面组件
import PurchaseDetail from '../components/purchase-detail.vue';
import PurchaseComment from '../components/purchase-comment.vue'; // 新增购买评论页面组件
import MyComments from '../components/MyComments.vue';
import AddProduct from '../components/AddProduct.vue'; // 新增添加商品页面组件
import ViewStock from '../components/ViewStock.vue'; // 新增查看库存页面组件
import EditProduct from '../components/EditProduct.vue'; // 新增修改商品页面组件
import SoldOut from '../components/SoldOut.vue'; // 新增商品售罄页面组件
import ViewComments from '../components/ViewComments.vue'; // 新增查看评论页面组件
import CommentDetails from '../components/CommentDetails.vue'; // 新增评论详情页面组件
import AddAdmin from '../components/AddAdmin.vue'; // 新增添加管理员页面组件
import Page1 from '../components/Page1.vue';
import Page2 from '../components/Page2.vue';
import Page3 from '../components/Page3.vue';
import Page4 from '../components/Page4.vue';
import AdminInfo from '../components/AdminInfo.vue';
import EditAdmin from '../components/EditAdmin.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/shouye',
    name: 'Shouye',
    component: Shouye
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: Favorites // 新增收藏页面路由
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart // 新增购物车页面路由
  },
  {
    path: '/item/:name',
    name: 'ItemDetail',
    component: ItemDetail
  },
  {
    path: '/purchase-history',
    name: 'Purchase',
    component: Purchase // 新增购买历史页面路由
  },
  {
    path: '/purchase-detail/:name/:purchase_time',
    name: 'PurchaseDetail',
    component: PurchaseDetail, // 新增购买历史详情页面路由
    props: true
  },
  {
    path: '/purchase-comment/:name/:purchase_time',
    name: 'PurchaseComment',
    component: PurchaseComment, // 新增购买评论页面路由
    props: true
  },
  {
    path: '/my-comments',
    name: 'MyComments',
    component: MyComments
  },
  {
    path: '/add-product',
    name: 'AddProduct',
    component: AddProduct // 新增添加商品页面路由
  },
  {
    path: '/view-stock',
    name: 'ViewStock',
    component: ViewStock // 新增查看库存页面路由
  },
  {
    path: '/edit-product/:name',
    name: 'EditProduct',
    component: EditProduct,
    props: true
  },
  {
    path: '/sold-out',
    name: 'SoldOut',
    component: SoldOut // 新增商品售罄页面路由
  },
  {
    path: '/view-comments',
    name: 'ViewComments',
    component: ViewComments // 新增查看评论页面路由
  },
  {
    path: '/comment-details',
    name: 'CommentDetails',
    component: CommentDetails,
    props: true
  },
  {
    path: '/add-admin',
    name: 'AddAdmin',
    component: AddAdmin // 新增添加管理员页面路由
  },
  {
    path: '/page1',
    name: 'Page1',
    component: Page1
  },
  {
    path: '/page2',
    name: 'Page2',
    component: Page2
  },
  {
    path: '/page3',
    name: 'Page3',
    component: Page3
  },
  {
    path: '/page4',
    name: 'Page4',
    component: Page4
  },
  {
    path: '/admin-info',
    name: 'AdminInfo',
    component: AdminInfo
  },
  {
    path: '/edit-admin/:username',
    name: 'EditAdmin',
    component: EditAdmin,
    props: true
  }


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 