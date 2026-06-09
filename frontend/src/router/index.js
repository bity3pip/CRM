import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
        path: '/',
        redirect: '/login',
  },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: {guest: true},
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue'),
      meta: {requiresAuth: true, role: 'chatter'},
    },
    {
      path: '/monitor',
      name: 'monitor',
      component: () => import('@/views/MonitorView.vue'),
      meta: {requiresAuth: true, role: 'teamlead'},
    },
  ],
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.guest && auth.isAuthenticated) {
    return next(auth.isTeamlead ? '/monitor' : '/chat')
  }

  if (to.meta.role === 'chatter' && !auth.isChatter) {
    return next('/monitor')
  }

  if (to.meta.role === 'teamlead' && !auth.isTeamlead) {
    return next('/chat')
  }

  next()
})

export default router
