import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { reactive } from 'vue';
import routes from './routes';
import guards from './guards';

const ReactiveRoutes = reactive<RouteRecordRaw[]>(routes);

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

// 注册导航守卫
guards.before.forEach(router.beforeEach);
guards.after.forEach(router.afterEach);

export default router;
