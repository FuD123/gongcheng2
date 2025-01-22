<template>
  <div class="home-container">
    <!-- 骨架屏加载效果 -->
    <template v-if="isLoading">
      <DashboardSkeleton />
    </template>

    <!-- 错误提示 -->
    <template v-else-if="error">
      <ErrorDisplay :message="error" @retry="retryLoading" />
    </template>

    <template v-else>
      <!-- 独立导航组件 -->
      <AppNavigation :links="navLinks" />

      <!-- 主内容区域 -->
      <main class="main-content">
        <DashboardLayout>
          <!-- 系统概览 -->
          <template #overview>
            <SystemOverview />
          </template>
        </DashboardLayout>
      </main>

      <!-- 底部信息 -->
      <AppFooter />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useHomeStore } from '@/stores/home'
import AppNavigation from '@/components/AppNavigation.vue'
import DashboardLayout from '@/components/DashboardLayout.vue'
import SystemOverview from '@/components/SystemOverview.vue'
import AppFooter from '@/components/AppFooter.vue'
import DashboardSkeleton from '@/components/DashboardSkeleton.vue'
import ErrorDisplay from '@/components/ErrorDisplay.vue'
import type { NavLink } from '@/types/navigation'

const homeStore = useHomeStore()
const { navLinks } = homeStore
const isLoading = ref(true)
const error = ref<string | null>(null)

const retryLoading = async () => {
  isLoading.value = true
  error.value = null
  try {
    await homeStore.initializeData()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load data'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  retryLoading()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;

  @include respond-to('medium') {
    padding: 1rem;
  }

  @include respond-to('small') {
    padding: 0.5rem;
  }
}
</style>
