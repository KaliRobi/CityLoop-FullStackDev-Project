<template>
  <main>
    <div class="login-container">
      <h2 class="login-title">Cityloop the tracking app</h2>
      <h2 class="login-title">Login</h2>
      <form @submit.prevent="SendLoginCredentials" class="new-shipment-form">
        <div class="input-field">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="userData.username" required>
        </div>
        <div class="input-field">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="userData.password" required>
        </div>
        <div class="create-new-button-container">
          <button  type="submit" class="login-button">Login</button>
        </div>
        <p v-if="loginError" class="error-message">Login failed. Please check your username and password.</p>
      </form>
    </div>
  </main>
</template>

<script setup>
import {ref, watch} from "vue"
import { useRouter } from 'vue-router'

const router = useRouter()

const userData = ref({
  username : '',
  password : ''
})

const loginError = ref(0)

const headers = {
  'Content-type': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem('access')}`
}

const domain = 'http://127.0.0.1:8000/'

watch(loginError, (newValue) => {
  if (newValue !== 0) {
    setTimeout(() => {
      loginError.value = 0
    }, 3000) 
  }
})


const SendLoginCredentials = async () => {
  try {
    const response = await fetch(`${domain}api-token-auth/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(userData.value)
    })
    if (response.ok)
      {
        const data = await response.json()
      localStorage.setItem('access', data['access'])
      router.push({name : 'ShipmentsTab'})
      }
    else {
      loginError.value = 1
    }
  } catch (error) {
    console.error( error)
  }
}
</script>



<style scoped>

main {
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
}

.login-container {
  display: inline;
  width: 50vw;
  max-width: 500px;
  padding: 50px;
  background-color: white;
  border-radius: 10px;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
}


.input-field label {
  display: block;
  margin: 5px;
}

.input-field input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.login-button {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #d5d5d5;
}

.error-message {
  color: red;
  text-align: center;
}

.logged-out {
  color: green;
  text-align: center;
}

</style>