<template>
  <div class="message" :class="message.sender_type">
    <div class="bubble">
      <div v-if="message.message_type === 'ppv'" class="ppv-badge">
        PPV · {{ message.ppv_price }}$
      </div>
      <p class="content">{{ message.content }}</p>
      <span class="time">{{ formatTime(message.created_at) }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: Object,
})

function formatTime(dateStr) {
  return new Date(dateStr).toLocaleTimeString('ru', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 8px;
}

.bubble {
  max-width: 65%;
  padding: 8px 12px;
  border-radius: 12px;
  position: relative;
}

.message.chatter .bubble {
  background: #2563eb;
  border-bottom-right-radius: 4px;
}

.message.fan .bubble {
  background: #1e1e1e;
  border-bottom-left-radius: 4px;
}

.ppv-badge {
  font-size: 11px;
  font-weight: 600;
  color: #fbbf24;
  margin-bottom: 4px;
}

.content {
  font-size: 14px;
  color: #fff;
  line-height: 1.4;
  word-break: break-word;
}

.time {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  display: block;
  text-align: right;
  margin-top: 4px;
}
</style>