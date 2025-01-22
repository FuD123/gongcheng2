import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { NavLink } from '@/types'

export const useHomeStore = defineStore('home', () => {
  // 状态管理
  const loading = ref(false)
  const error = ref(false)
  const errorMessage = ref<string>('')

  // 导航链接
  const navLinks = ref<NavLink[]>([
    { name: '系统概览', path: '/overview', component: 'SystemOverview' },
    { name: '任务管理', path: '/tasks', component: 'TaskManagement' },
    { name: '日志管理', path: '/logs', component: 'LogManagement' },
    { name: '文件操作', path: '/files', component: 'FileOperations' },
    { name: '部署管理', path: '/deployment', component: 'DeploymentManagement' },
    { name: '系统设置', path: '/settings', component: 'SettingsManagement' }
  ])

  // 初始化数据
  const initializeData = async () => {
    try {
      loading.value = true
      error.value = false
      // 这里可以添加实际的初始化逻辑
      await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟异步操作
    } catch (err: unknown) {
      error.value = true
      errorMessage.value = err instanceof Error ? err.message : '初始化数据失败'
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    errorMessage,
    navLinks,
    initializeData
  }
})
