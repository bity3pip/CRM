<template>
  <div class="dialog-list">
    <div class="dialog-list-header">
      <h2>Диалоги</h2>
      <span class="dialog-count">{{ dialogs.length }}</span>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="dialogs.length === 0" class="empty">
      Нет диалогов
    </div>

    <div v-else class="dialogs">
      <DialogItem
          v-for="dialog in dialogs"
          :key="dialog.id"
          :dialog="dialog"
          :is-active="activeId === dialog.id"
          @select="$emit('select', dialog)"
      />
    </div>
  </div>
</template>

<script setup>
import DialogItem from './DialogItem.vue'

defineProps({
  dialogs: Array,
  activeId: Number,
  loading: Boolean,
})
defineEmits(['select'])
</script>

<style scoped>
.dialog-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #111;
  border-right: 1px solid #1e1e1e;
}

.dialog-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 16px;
  border-bottom: 1px solid #1e1e1e;
}

.dialog-list-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.dialog-count {
  font-size: 12px;
  color: #555;
  background: #1e1e1e;
  padding: 2px 8px;
  border-radius: 10px;
}

.loading,
.empty {
  padding: 24px 16px;
  font-size: 13px;
  color: #555;
  text-align: center;
}

.dialogs {
  flex: 1;
  overflow-y: auto;
}
</style>