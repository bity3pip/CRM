<template>
  <div class="dialog-list">
    <div class="dialog-list-header">
      <div class="header-top">
        <h2>Диалоги</h2>
        <div class="header-actions">
          <span class="dialog-count">{{ dialogs.length }}</span>
          <button class="logout-btn" @click="$emit('logout')">Выйти</button>
        </div>
      </div>
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}



.logout-btn {
  background: transparent;
  border: 1px solid #2a2a2a;
  color: #555;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  margin-top: 8px;
  width: auto;
  transition: border-color 0.2s;
}

.logout-btn:hover {
  border-color: #444;
  color: #999;
}
</style>