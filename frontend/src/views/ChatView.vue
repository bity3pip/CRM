<template>
  <div class="chat-layout">
    <DialogList
        :dialogs="chat.dialogs"
        :active-id="chat.activeDialog?.id"
        :loading="chat.loadingDialogs"
        @select="onSelectDialog"
    />

    <div class="chat-main">
      <ChatWindow
          v-if="chat.activeDialog"
          :dialog="chat.activeDialog"
          :messages="chat.messages"
          :has-more="chat.hasMore"
          :loading="chat.loadingMessages"
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
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import DialogList from '@/components/chat/DialogList.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const chat = useChatStore()

onMounted(() => {
  chat.fetchDialogs()
})

async function onSelectDialog(dialog) {
  await chat.selectDialog(dialog)
}

async function onSend({ content, message_type, ppv_price }) {
  if (!chat.activeDialog) return
  const message = await chat.sendMessage(
      chat.activeDialog.id,
      content,
      message_type,
      ppv_price,
  )
  chat.addMessage(message)
}
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