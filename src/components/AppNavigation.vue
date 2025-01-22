<template>
  <nav class="app-nav">
  <router-link
    v-for="link in links.filter(l => l.name !== '部署')"
    :key="link.name"
    :to="link.path"
    class="nav-link"
    active-class="active"
  >
    {{ link.name }}
  </router-link>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  links: Array<{
    name: string
    path: string
  }>
}>()
</script>

<style scoped>
.app-nav {
  display: flex;
  justify-content: center;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link {
  margin: 0 1rem;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: var(--text-color);
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--primary-color);
  border-bottom: 2px solid var(--primary-color);
}

@media (max-width: 768px) {
  .app-nav {
    flex-wrap: wrap;
  }
  
  .nav-link {
    margin: 0.5rem;
    padding: 0.25rem 0.5rem;
  }
}
</style>
