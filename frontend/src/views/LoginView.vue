<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h1 class="login-title">CRM Chatter</h1>
      <p class="login-subtitle">Войдите в систему</p>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Логин</label>
          <input
            v-model="username"
            type="text"
            placeholder="username"
            autocomplete="username"
            :disabled="loading"
          />
        </div>

        <div class="field">
          <label>Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
            :disabled="loading"
          />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" :disabled="loading || !username || !password">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (loading.value) return
  loading.value = true
  error.value = ''

  try {
    const role = await auth.login(username.value, password.value)
    if (role === 'teamlead') {
      await router.push('/monitor')
    } else {
      await router.push('/chat')
    }
  } catch (e) {
    error.value = 'Неверный логин или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f0f0f;
}

.login-card {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 380px;
}

.login-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 6px;
}

.login-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 32px;
}

.field {
  margin-bottom: 16px;
}

.field label {
  display: block;
  font-size: 13px;
  color: #999;
  margin-bottom: 6px;
}

.field input {
  width: 100%;
  padding: 10px 14px;
  background: #111;
  border: 1px solid #2a2a2a;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.field input:focus {
  border-color: #444;
}

.field input:disabled {
  opacity: 0.5;
}

.error {
  font-size: 13px;
  color: #ff4d4d;
  margin-bottom: 12px;
}

button {
  width: 100%;
  padding: 11px;
  background: #fff;
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

button:hover:not(:disabled) {
  opacity: 0.9;
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>