import { ref, onUnmounted } from 'vue'

export function useWebSocket(url, handlers) {
    const ws = ref(null)
    const connected = ref(false)
    let reconnectTimer = null
    let lastMessageId = ref(null)
    let manualClose = false

    function connect() {
        manualClose = false
        const fullUrl = lastMessageId.value
            ? `${url}&last_message_id=${lastMessageId.value}`
            : url

        ws.value = new WebSocket(fullUrl)

        ws.value.onopen = () => {
            connected.value = true
            if (reconnectTimer) {
                clearTimeout(reconnectTimer)
                reconnectTimer = null
            }
            handlers.onOpen?.()
        }

        ws.value.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                handlers.onMessage?.(data)
            } catch (e) {
                console.error('WS parse error', e)
            }
        }

        ws.value.onclose = (event) => {
            connected.value = false
            handlers.onClose?.(event)
            if (!manualClose) {
                if (event.code === 4401 || event.code === 4403) {
                    handlers.onAuthError?.()
                    return
                }
                reconnectTimer = setTimeout(() => connect(), 3000)
            }
        }

        ws.value.onerror = (e) => {
            console.error('WS error', e)
        }
    }

    function send(data) {
        if (ws.value?.readyState === WebSocket.OPEN) {
            ws.value.send(JSON.stringify(data))
        }
    }

    function disconnect() {
        manualClose = true
        if (reconnectTimer) {
            clearTimeout(reconnectTimer)
            reconnectTimer = null
        }
        ws.value?.close()
        ws.value = null
        connected.value = false
    }

    function setLastMessageId(id) {
        lastMessageId.value = id
    }

    onUnmounted(() => disconnect())

    return { connected, connect, send, disconnect, setLastMessageId }
}