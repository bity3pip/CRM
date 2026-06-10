<template>
  <div class="chat-window">
    <div class="chat-header">
      <div class="chat-header-info">
        <span class="fan-name">{{ dialog.fan_name }}</span>
        <span class="model-name">{{ dialog.model_username }}</span>
      </div>
      <div class="connection-status">
        <span class="dot" :class="connected ? 'online' : 'offline'" />
        {{ connected ? 'Online' : 'Reconnecting...'}}
      </div>
      <div v-if="dialog.is_overdue" class="overdue-alert">
        ⏰ Ждёт {{ dialog.waiting_minutes }}м
      </div>
    </div>

    <div class="messages-wrap" ref="messagesEl" @scroll="onScroll">
      <div v-if="hasMore" class="load-more">
        <button @click="loadMore" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Загрузить ещё' }}
        </button>
      </div>

      <MessageItem
          v-for="message in messages"
          :key="message.id"
          :message="message"
      />

      <div ref="bottomEl" />
    </div>

    <div class="chat-input">
      <div v-if="showPpv" class="ppv-row">
        <input
            v-model="ppvPrice"
            type="number"
            placeholder="Цена PPV"
            class="ppv-input"
        />
        <button class="cancel-ppv" @click="showPpv = false">✕</button>
      </div>

      <div class="input-row">
        <button class="ppv-btn" @click="showPpv = !showPpv" title="PPV">$</button>
        <input
            v-model="inputText"
            type="text"
            placeholder="Сообщение..."
            @keydown.enter.prevent="send"
            :disabled="sending"
        />
        <button class="send-btn" @click="send" :disabled="!canSend">
          ➤
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import MessageItem from './MessageItem.vue'
import { useChatStore } from '@/stores/chat'

const props = defineProps({
  dialog: Object,
  messages: Array,
  hasMore: Boolean,
  loading: Boolean,
  connected: Boolean,
})

const emit = defineEmits(['send', 'load-more', 'logout'])

const chat = useChatStore()
const messagesEl = ref(null)
const bottomEl = ref(null)
const inputText = ref('')
const ppvPrice = ref('')
const showPpv = ref(false)
const sending = ref(false)

const canSend = computed(() => {
  if (!inputText.value.trim()) return false
  if (showPpv.value && !ppvPrice.value) return false
  return !sending.value
})

async function send() {
  if (!canSend.value) return
  sending.value = true
  try {
    emit('send', {
      content: inputText.value.trim(),
      message_type: showPpv.value ? 'ppv' : 'text',
      ppv_price: showPpv.value ? ppvPrice.value : null,
    })
    inputText.value = ''
    ppvPrice.value = ''
    showPpv.value = false
  } finally {
    sending.value = false
  }
}

async function loadMore() {
  emit('load-more')
}

function scrollToBottom() {
  nextTick(() => {
    bottomEl.value?.scrollIntoView({ behavior: 'smooth' })
  })
}

watch(() => props.messages?.length, () => {
  scrollToBottom()
})

watch(() => props.dialog?.id, () => {
  nextTick(() => scrollToBottom())
})
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #0d0d0d;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #1e1e1e;
  background: #111;
}

.chat-header-info {
  display: flex;
  flex-direction: column;
}

.fan-name {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
}

.model-name {
  font-size: 12px;
  color: #555;
}

.overdue-alert {
  font-size: 12px;
  color: #ff4d4d;
  background: rgba(255, 77, 77, 0.1);
  padding: 4px 10px;
  border-radius: 20px;
}

.messages-wrap {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
}

.load-more {
  text-align: center;
  margin-bottom: 12px;
}

.load-more button {
  background: #1e1e1e;
  color: #999;
  border: none;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
}

.chat-input {
  padding: 12px 16px;
  border-top: 1px solid #1e1e1e;
  background: #111;
}

.ppv-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.ppv-input {
  flex: 1;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 8px;
  color: #fff;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;
}

.cancel-ppv {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  color: #666;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.input-row input {
  flex: 1;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 8px;
  color: #fff;
  padding: 10px 14px;
  font-size: 14px;
  outline: none;
}

.input-row input:focus {
  border-color: #444;
}

.ppv-btn {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  color: #fbbf24;
  border-radius: 8px;
  width: 38px;
  height: 38px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn {
  background: #2563eb;
  border: none;
  color: #fff;
  border-radius: 8px;
  width: 38px;
  height: 38px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s;
}

.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.connection-status {
  font-size: 12px;
  color: #555;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.online { background: #22c55e; }
.dot.offline { background: #ef4444; }
</style>