import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useMonitorStore = defineStore('monitor', () => {
    const chatters = ref([])
    const loading = ref(false)

    async function fetchChatters() {
        loading.value = true
        try {
            const response = await api.get('/api/monitor/chatters/')
            chatters.value = response.data
        } finally {
            loading.value = false
        }
    }

    function applySnapshot(data) {
        chatters.value = data
    }

    return { chatters, loading, fetchChatters, applySnapshot }
})