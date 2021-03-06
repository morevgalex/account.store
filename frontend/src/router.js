import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Home',
            meta: {layout: 'main'},
            component: () => import('./components/view/Home.vue')
        },
        {
            path: '/login',
            name: 'Login',
            meta: {layout: 'empty'},
            component: () => import('./components/view/Login.vue')
        },
        {
            path: '/register',
            name: 'Register',
            meta: {layout: 'empty'},
            component: () => import('./components/view/Register.vue')
        },
        {
            path: '/page',
            name: 'Page',
            meta: {layout: 'main'},
            component: () => import('./components/view/Page.vue')
        },
        {
            path: '*',
            redirect: '/'
        },
    ]
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('user-token')
    const requireAuth = to.matched.some(record => record.meta.auth)

    if (requireAuth && !token) {
        next('/login?message=login')
    } else {
        next()
    }
})

export default router
