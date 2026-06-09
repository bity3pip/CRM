import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useChatStore = defineStore('chat', () => {
    const dialogs = ref([])
    const activeDialog = ref(null)
    const messages = ref([])
    const loadingDialogs = ref(false)
    const loadingMessages = ref(false)
    const nextCursor = ref(null)
    const hasMore = ref(false)

    async function fetchDialogs() {
        loadingDialogs.value = true
        try {
            const response = await api.get('/api/dialogs/')
            dialogs.value = response.data
        } finally {
            loadingDialogs.value = false
        }
    }

    async function selectDialog(dialog) {
        activeDialog.value = dialog
        messages.value = []
        nextCursor.value = null
        hasMore.value = false
        await fetchMessages(dialog.id)
        await markAsRead(dialog.id)

        const d = dialogs.value.find(d => d.id === dialog.id)
        if (d) d.unread_count = 0
    }

    async function fetchMessages(dialogId, cursor = null) {
        loadingMessages.value = true
        try {
            const params = cursor ? { cursor } : {}
            const response = await api.get(`/api/dialogs/${dialogId}/messages/`, { params })
            const { results, next } = response.data

            if (cursor) {
                messages.value = [...results.reverse(), ...messages.value]
            } else {
                messages.value = results.reverse()
            }

            nextCursor.value = next ? new URL(next).searchParams.get('cursor') : null
            hasMore.value = !!next
        } finally {
            loadingMessages.value = false
        }
    }

    async function loadMoreMessages() {
        if (!hasMore.value || !activeDialog.value) return
        await fetchMessages(activeDialog.value.id, nextCursor.value)
    }

    async function markAsRead(dialogId) {
        await api.post(`/api/dialogs/${dialogId}/read/`)
    }

    async function sendMessage(dialogId, content, messageType = 'text', ppvPrice = null) {
        const payload = { content, message_type: messageType }
        if (messageType === 'ppv' && ppvPrice) {
            payload.ppv_price = ppvPrice
        }
        const response = await api.post(`/api/dialogs/${dialogId}/messages/send/`, payload)
        return response.data
    }

    function addMessage(message) {
        messages.value.push(message)
    }

    function updateDialog(updatedDialog) {
        const index = dialogs.value.findIndex(d => d.id === updatedDialog.id)
        if (index !== -1) {
            dialogs.value[index] = { ...dialogs.value[index], ...updatedDialog }
        }
    }

    function upsertDialogFromMessage(message, dialogId) {
        const dialog = dialogs.value.find(d => d.id === dialogId)
        if (dialog) {
            dialog.last_message = message
            dialog.updated_at = message.created_at
            if (message.sender_type === 'fan' && activeDialog.value?.id !== dialogId) {
                dialog.unread_count = (dialog.unread_count || 0) + 1
            }
        }
        dialogs.value.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
    }

    return {
        dialogs,
        activeDialog,
        messages,
        loadingDialogs,
        loadingMessages,
        hasMore,
        fetchDialogs,
        selectDialog,
        fetchMessages,
        loadMoreMessages,
        markAsRead,
        sendMessage,
        addMessage,
        updateDialog,
        upsertDialogFromMessage,
    }
})