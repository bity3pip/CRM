import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import router from '@/router'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
    const accessToken = ref(localStorage.getItem('access_token'))
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

    const isAuthenticated = computed(() => !!accessToken.value)
    const isChatter = computed(() => user.value?.role === 'chatter')
    const isTeamlead = computed(() => user.value?.role === 'teamlead')

    async function login(username, password) {
        const response = await api.post('api/auth/login/', { username, password })
        const { access, refresh, role, user_id, username: uname } = response.data

        accessToken.value = access
        user.value = { id: user_id, username: uname, role }

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user.value))

        return role
    }
    function logout() {
        accessToken.value = null
        user.value = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        router.push('/login')
    }
    return { accessToken, user, isAuthenticated, isChatter, isTeamlead, login, logout}
})