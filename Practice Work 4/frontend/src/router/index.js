import { createRouter, createWebHistory } from 'vue-router';
import Admin from '../views/AdminView.vue';
import RegisterView from "@/views/RegisterView.vue";
import store from '../store';
import LoginView from "@/views/LoginView.vue";
import ItemList from "@/components/ItemList.vue";

const routes = [
    { path: '/', component: ItemList },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    {
        path: '/admin',
        component: Admin,
        meta: { requiresAdmin: true },
    },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        await store.dispatch('fetchUser');
        if (store.state.user?.role === 'admin') {
            next();
        } else {
            next('/login');
        }
    } else {
        next();
    }
});

export default router;