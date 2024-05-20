
import { createRouter, createWebHistory } from 'vue-router'
import { createApp } from 'vue'
import App from './App.vue'
import auth from './auth'
import LoginTab from '@/views/LoginTab.vue'
import ShipmentsTab from '@/views/ShipmentTab.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: LoginTab, name: "LoginTab" },
        { path: '/shipments', component: ShipmentsTab, name: 'ShipmentsTab', meta: { requiresAuth: true } }
      ]
  })

router.beforeEach((to, from, next) => {
if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!auth.loggedIn()) {
    next({
        path: '/',
        query: { redirect: to.fullPath }
    })
    } else {
    next()
    }
} else {
    next() 
}
})

const app = createApp(App)

createApp(App)
  .use(router)
  .mount('#app')