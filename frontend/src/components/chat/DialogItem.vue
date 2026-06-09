<template>
  <div
      class="dialog-item"
      :class="{
      active: isActive,
      overdue: dialog.is_overdue,
      unread: dialog.unread_count > 0,
    }"
      @click="$emit('select', dialog)"
  >
    <div class="dialog-avatar">
      {{ dialog.fan_name.charAt(0).toUpperCase() }}
    </div>

    <div class="dialog-info">
      <div class="dialog-header">
        <span class="dialog-name">{{ dialog.fan_name }}</span>
        <span class="dialog-time">{{ formatTime(dialog.updated_at) }}</span>
      </div>

      <div class="dialog-footer">
        <span class="dialog-preview">
          {{ dialog.last_message?.content || 'Нет сообщений' }}
        </span>
        <span v-if="dialog.unread_count > 0" class="unread-badge">
          {{ dialog.unread_count }}
        </span>
        <span v-if="dialog.is_overdue" class="overdue-badge">
          {{ dialog.waiting_minutes }}м
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  dialog: Object,
  isActive: Boolean,
})
defineEmits(['select'])

function formatTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return 'только что'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}м`
  if (diff < 86400000) {
    return date.toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' })
  }
  return date.toLocaleDateString('ru', { day: '2-digit', month: '2-digit' })
}
</script>

<style scoped>
.dialog-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #1e1e1e;
  transition: background 0.15s;
}

.dialog-item:hover {
  background: #1a1a1a;
}

.dialog-item.active {
  background: #1e1e1e;
}

.dialog-item.overdue {
  border-left: 3px solid #ff4d4d;
}

.dialog-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #2a2a2a;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.dialog-info {
  flex: 1;
  min-width: 0;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.dialog-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
}

.dialog-time {
  font-size: 11px;
  color: #555;
  flex-shrink: 0;
}

.dialog-footer {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dialog-preview {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.unread-badge {
  background: #3b82f6;
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  flex-shrink: 0;
}

.overdue-badge {
  background: #ff4d4d;
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  flex-shrink: 0;
}
</style>