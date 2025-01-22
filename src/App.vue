<template>
  <div id="app">
    <AppNavigation :links="navLinks" />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import AppNavigation from './components/AppNavigation.vue'

const navLinks = [
  { name: '任务', path: '/tasks' },
  { name: '文件', path: '/files' },
  { name: '日志', path: '/logs' },
  { name: '概览', path: '/overview' },
  { name: '设置', path: '/settings' }
]
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.navbar {
  background: #f5f5f5;
  padding: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-link {
  margin-right: 1rem;
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: #e9e9e9;
}

.router-link-exact-active {
  background: #007bff;
  color: white;
}
</style>
