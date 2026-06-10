<template>
  <div class="chatter-card" :class="{ offline: !chatter.is_online, overdue: chatter.overdue_count > 0 }">
    <div class="card-header">
      <div class="chatter-info">
        <span class="status-dot" :class="chatter.is_online ? 'online' : 'offline'" />
        <span class="chatter-name">{{ chatter.username }}</span>
      </div>
      <span class="last-seen" v-if="!chatter.is_online && chatter.last_seen">
        {{ formatLastSeen(chatter.last_seen) }}
      </span>
    </div>

    <div class="card-stats">
      <div class="stat">
        <span class="stat-value">{{ chatter.dialogs_count }}</span>
        <span class="stat-label">диалогов</span>
      </div>
      <div class="stat" :class="{ danger: chatter.overdue_count > 0 }">
        <span class="stat-value">{{ chatter.overdue_count }}</span>
        <span class="stat-label">просрочено</span>
      </div>
    </div>

    <div v-if="chatter.overdue_dialogs?.length > 0" class="overdue-list">
      <div
          v-for="dialog in chatter.overdue_dialogs"
          :key="dialog.id"
          class="overdue-item"
      >
        <span class="overdue-fan">{{ dialog.fan_name }}</span>
        <span class="overdue-time">⏰ {{ dialog.waiting_minutes }}м</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  chatter: Object,
})

function formatLastSeen(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return 'только что'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}м назад`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}ч назад`
  return date.toLocaleDateString('ru')
}
</script>

<style scoped>
.chatter-card {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 16px;
  transition: border-color 0.2s;
}

.chatter-card.overdue {
  border-color: #ff4d4d;
}

.chatter-card.offline {
  opacity: 0.6;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.chatter-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.online { background: #22c55e; }
.status-dot.offline { background: #555; }

.chatter-name {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
}

.last-seen {
  font-size: 11px;
  color: #555;
}

.card-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #111;
  border-radius: 8px;
  padding: 8px 16px;
  flex: 1;
}

.stat.danger .stat-value {
  color: #ff4d4d;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

.stat-label {
  font-size: 11px;
  color: #555;
  margin-top: 2px;
}

.overdue-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.overdue-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.2);
  border-radius: 8px;
  padding: 6px 10px;
}

.overdue-fan {
  font-size: 13px;
  color: #fff;
}

.overdue-time {
  font-size: 12px;
  color: #ff4d4d;
  font-weight: 600;
}
</style>