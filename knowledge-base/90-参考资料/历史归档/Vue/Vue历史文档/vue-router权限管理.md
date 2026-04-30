#### 一、方案一：路由权限数据通过接口获取
完整路由配置由通用路由配置及接口返回的权限路由配置组成。



```javascript
import router from "./router";
import store from "./store";
import Cookies from "js-cookie";

//根据id请求接口获取规则
let whiteList = ["/about", "/login"];

router.beforeEach(async (to, from, next) => {
  const token = Cookies.get("token");
  // 判断用户是否登录
  if (token) {
    if (to.path == "/login") {
      next("/");
    } else {
      //判断是不是已经请求拿了路由规则了
      if (store.state.asyncRoute.length == 0) {
        // 路由权限数据为空时, 获取路由权限数据
        const _asyncRoutes = await store.dispatch("getRouter");
        _asyncRoutes.forEach((item) => {
          router.addRoute(item);
        });
        //继续跳转
        next(to.path);
      } else {
        if (to.matched.length != 0) {
          next();
        } else {
          alert("无页面权限");
          next(from.path);
        }
      }
    }
  } else {
    // 未登录时, 判断访问页面是否需要登录才能访问(白名单), 在白名单内的页面可以直接访问, 否则跳转到登录页
    if (whiteList.indexOf(to.path) != -1) {
      next();
    } else {
      next("/login");
    }
  }
});

```



```javascript

import Vue from "vue";
import Vuex from "vuex";
import Cookies from "js-cookie";
import { initRoutes, resetRouter } from "../router";
import axios from "axios";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    asyncRoute: [],
    routes: [],
  },
  mutations: {
    SET_ROUTES: (state, routes) => {
      state.asyncRoute = routes;
      state.routes = initRoutes.concat(routes);
    },
    RESET_ROUTES: (state) => {
      state.asyncRoute = [];
      state.routes = [];
    },
  },
  actions: {
    getRouter({ commit }) {
      function parseRouter(routeArr) {
        let _newArr = [];
        routeArr.forEach((item) => {
          let _newItem = Object.assign({}, item);
          let _str = item.component;
          _newItem.component = () => {
            return import(`@/views${_str}`);
          };
          _newArr.push(_newItem);
        });
        return _newArr;
      }
      let _id = Cookies.get("id");
      if (_id) {
        return new Promise((resolve) => {
          let _local = JSON.parse(localStorage.getItem("menu"));
          if (_local) {
            let _newArr = parseRouter(_local);
            commit("SET_ROUTES", _newArr);
            resolve(_newArr);
          } else {
            axios.get("http://localhost:3000/routes?id=" + _id).then((res) => {
              let _newArr = parseRouter(res.data.data);
              localStorage.setItem("menu", JSON.stringify(res.data.data));
              commit("SET_ROUTES", _newArr);
              resolve(_newArr);
            });
          }
        });
      }
    },
    //按钮
    //登录-拉去一下用户的权限code ["some1","SOMETHING"]
    getCode() {},
    resetRouter({ commit }) {
      resetRouter();
      commit("RESET_ROUTES");
    },
  },
  modules: {},
});

```



```javascript

import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import login from "../views/login.vue";

Vue.use(VueRouter);

export const initRoutes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/About.vue");
    },
  },
  {
    path: "/login",
    name: "login",
    component: login,
  },
];

const router = new VueRouter({
  routes: initRoutes,
});

export function resetRouter() {
  const newRouter = new VueRouter({
    routes: initRoutes,
  });

  router.matcher = newRouter.matcher;
}
export default router;

```

