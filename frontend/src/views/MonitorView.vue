<template>
  <div class="monitor-layout">
    <div class="monitor-header">
      <div class="header-left">
        <h1>Монитор</h1>
        <span class="ws-status">
          <span class="dot" :class="wsConnected ? 'online' : 'offline'" />
          {{ wsConnected ? 'Live' : 'Reconnecting...' }}
        </span>
      </div>
      <div class="header-right">
        <span class="online-count">
          Онлайн: {{ onlineCount }} / {{ monitor.chatters.length }}
        </span>
        <button class="logout-btn" @click="handleLogout">Выйти</button>
      </div>
    </div>

    <div class="monitor-body">
      <div v-if="monitor.loading" class="loading">Загрузка...</div>

      <div v-else-if="monitor.chatters.length === 0" class="empty">
        Нет чатеров
      </div>

      <div v-else class="chatters-grid">
        <ChatterCard
            v-for="chatter in sortedChatters"
            :key="chatter.id"
            :chatter="chatter"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useMonitorStore } from '@/stores/monitor'
import { useAuthStore } from '@/stores/auth'
import { useWebSocket } from '@/composables/useWebSocket'
import ChatterCard from '@/components/monitor/ChatterCard.vue'

const monitor = useMonitorStore()
const auth = useAuthStore()

const wsConnected = ref(false)
let ws = null

const onlineCount = computed(() =>
    monitor.chatters.filter(c => c.is_online).length
)

const sortedChatters = computed(() => {
  return [...monitor.chatters].sort((a, b) => {
    if (a.is_online !== b.is_online) return b.is_online - a.is_online
    if (a.overdue_count !== b.overdue_count) return b.overdue_count - a.overdue_count
    return 0
  })
})

onMounted(() => {
  monitor.fetchChatters()
  connectWs()
})

onUnmounted(() => {
  ws?.disconnect()
})

function connectWs() {
  const token = auth.accessToken
  const wsBase = import.meta.env.VITE_WS_URL || ''
  const url = `${wsBase}/ws/monitor/?token=${token}`

  ws = useWebSocket(url, {
    onOpen: () => {
      wsConnected.value = true
    },
    onMessage: (data) => {
      if (data.type === 'snapshot' || data.type === 'update') {
        monitor.applySnapshot(data.data)
      }
    },
    onClose: () => {
      wsConnected.value = false
    },
  })

  ws.connect()
}

function handleLogout() {
  ws?.disconnect()
  auth.logout()
}
</script>

<style scoped>
.monitor-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0d0d0d;
}

.monitor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #1e1e1e;
  background: #111;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.monitor-header h1 {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.ws-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #555;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.online { background: #22c55e; }
.dot.offline { background: #ef4444; }

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.online-count {
  font-size: 13px;
  color: #666;
}

.logout-btn {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  color: #999;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.logout-btn:hover {
  border-color: #444;
  color: #fff;
}

.monitor-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.loading,
.empty {
  text-align: center;
  color: #555;
  font-size: 14px;
  padding: 40px;
}

.chatters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
</style>