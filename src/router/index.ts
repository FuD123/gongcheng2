import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Tasks from '../views/Tasks.vue'
import Logs from '../views/Logs.vue'
import Files from '../views/Files.vue'
import Overview from '../views/Overview.vue'
import Settings from '../views/Settings.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/tasks'
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks
  },
  {
    path: '/logs',
    name: 'Logs',
    component: Logs
  },
  {
    path: '/files',
    name: 'Files',
    component: Files
  },
  {
    path: '/overview',
    name: 'Overview',
    component: Overview
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes
})

export default router
