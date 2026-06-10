<template>
  <div class="chat-layout">
    <DialogList
        :dialogs="chat.dialogs"
        :active-id="chat.activeDialog?.id"
        :loading="chat.loadingDialogs"
        @select="onSelectDialog"
        @logout="handleLogout"
    />

    <div class="chat-main">
      <ChatWindow
          v-if="chat.activeDialog"
          :dialog="chat.activeDialog"
          :messages="chat.messages"
          :has-more="chat.hasMore"
          :loading="chat.loadingMessages"
          :connected="wsConnected"
          @send="onSend"
          @load-more="chat.loadMoreMessages"
      />
      <div v-else class="no-dialog">
        <p>Выберите диалог</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useAuthStore } from '@/stores/auth'
import { useWebSocket } from '@/composables/useWebSocket'
import DialogList from '@/components/chat/DialogList.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const chat = useChatStore()
const auth = useAuthStore()

const wsConnected = ref(false)
let currentWs = null

onMounted(() => {
  chat.fetchDialogs()
})

async function onSelectDialog(dialog) {
  if (currentWs) {
    currentWs.disconnect()
    currentWs = null
  }

  await chat.selectDialog(dialog)

  connectToDialog(dialog.id)
}

function connectToDialog(dialogId) {
  const token = auth.accessToken
  const wsBase = import.meta.env.VITE_WS_URL || ''
  const url = `${wsBase}/ws/dialogs/${dialogId}/?token=${token}`

  const ws = useWebSocket(url, {
    onOpen: () => {
      wsConnected.value = true
    },
    onMessage: (data) => handleWsMessage(data, dialogId),
    onClose: () => {
      wsConnected.value = false
      const lastId = chat.getLastMessageId()
      if (lastId) ws.setLastMessageId(lastId)
    },
    onAuthError: () => {
      auth.logout()
    }
  })

  ws.connect()
  currentWs = ws
}

function handleWsMessage(data, dialogId) {
  if (data.type === 'message' || data.type === 'fan_message') {
    const message = data.message

    if (chat.activeDialog?.id === dialogId) {
      chat.addMessage(message)
    }

    chat.upsertDialogFromMessage(message, dialogId)

    if (data.type === 'message' && message.sender_type === 'chatter') {
      const dialog = chat.dialogs.find(d => d.id === dialogId)
      if (dialog) {
        dialog.fan_waiting_since = null
        dialog.is_overdue = false
        dialog.waiting_minutes = null
      }
      if (chat.activeDialog?.id === dialogId) {
        chat.activeDialog.fan_waiting_since = null
        chat.activeDialog.is_overdue = false
        chat.activeDialog.waiting_minutes = null
      }
    }
  }

  if (data.type === 'missed_messages') {
    data.messages.forEach(msg => {
      const exists = chat.messages.find(m => m.id === msg.id)
      if (!exists) chat.addMessage(msg)
    })
  }
}
function handleLogout() {
  if (currentWs) currentWs.disconnect()
  auth.logout()
}

async function onSend({ content, message_type, ppv_price }) {
  if (!chat.activeDialog || !currentWs) return

  currentWs.send({ content, message_type, ppv_price })
}

onUnmounted(() => {
  if (currentWs) currentWs.disconnect()
})
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  background: #0d0d0d;
}

.chat-layout > :first-child {
  width: 320px;
  flex-shrink: 0;
}

.chat-main {
  flex: 1;
  min-width: 0;
}

.no-dialog {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  font-size: 15px;
}
</style>