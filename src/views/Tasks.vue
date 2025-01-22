<template>
  <div class="tasks container">
    <div class="section" id="task-section">
      <h3>任务管理</h3>
      <div class="task-controls">
        <button class="btn btn-primary" @click="showCreateModal = true">
          新建任务
        </button>
        <button class="btn btn-secondary" @click="refreshTasks">
          刷新
        </button>
      </div>

      <div class="task-list">
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-info">
            <span class="task-name">{{ task.name }}</span>
            <span class="task-status" :class="task.status">{{ task.status }}</span>
          </div>
          <div class="task-actions">
            <button class="btn btn-sm" @click="editTask(task)">编辑</button>
            <button class="btn btn-sm btn-danger" @click="deleteTask(task)">删除</button>
          </div>
        </div>
      </div>

      <!-- 任务创建/编辑模态框 -->
      <div v-if="showCreateModal" class="modal-overlay">
        <div class="modal-content">
          <h4>{{ isEditing ? '编辑任务' : '新建任务' }}</h4>
          <form @submit.prevent="saveTask">
            <div class="form-group">
              <label>任务名称</label>
              <input v-model="currentTask.name" required />
            </div>
            <div class="form-group">
              <label>任务描述</label>
              <textarea v-model="currentTask.description"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                取消
              </button>
              <button type="submit" class="btn btn-primary">
                {{ isEditing ? '保存' : '创建' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from '@/api/axios'
import { useToast } from 'vue-toastification'
import type { AxiosResponse } from 'axios'

interface Task {
  id: number
  name: string
  description: string
  status: 'pending' | 'in-progress' | 'completed'
}

interface TaskResponse {
  data: Task[]
}

const toast = useToast()
const tasks = ref<Task[]>([])
const showCreateModal = ref(false)
const isEditing = ref(false)
const currentTask = ref<Partial<Task>>({
  name: '',
  description: '',
  status: 'pending'
})

const getTasks = async () => {
  try {
    const response: AxiosResponse<Task[]> = await axios.get('/tasks')
    tasks.value = response.data
  } catch (error) {
    if (error instanceof Error) {
      toast.error('获取任务列表失败')
      console.error('Failed to fetch tasks:', error.message)
    }
  }
}

const saveTask = async () => {
  try {
if (isEditing.value) {
      await axios.put<Task>(`/tasks/${currentTask.value.id}`, currentTask.value)
    } else {
      await axios.post<Task>('/tasks', currentTask.value)
    }
    closeModal()
    getTasks()
    toast.success('任务保存成功')
  } catch (error) {
    if (error instanceof Error) {
      toast.error('保存任务失败')
      console.error('Failed to save task:', error.message)
    }
  }
}

const editTask = (task: Task) => {
  currentTask.value = { ...task }
  isEditing.value = true
  showCreateModal.value = true
}

const deleteTask = async (task: Task) => {
  try {
if (task.id !== undefined) {
      await axios.delete(`/tasks/${task.id}`)
      getTasks()
      toast.success('任务删除成功')
    }
  } catch (error) {
    if (error instanceof Error) {
      toast.error('删除任务失败')
      console.error('Failed to delete task:', error.message)
    }
  }
}

const refreshTasks = () => {
  getTasks()
}

const closeModal = () => {
  showCreateModal.value = false
  isEditing.value = false
  resetCurrentTask()
}

const resetCurrentTask = () => {
  currentTask.value = {
    name: '',
    description: '',
    status: 'pending'
  }
}

onMounted(() => {
  getTasks()
})
</script>

<style scoped>
.tasks {
  padding: 2rem;
}

.task-controls {
  margin-bottom: 1rem;
  display: flex;
  gap: 0.5rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.task-name {
  font-weight: bold;
}

.task-status {
  font-size: 0.875rem;
  color: #666;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 4px;
  width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>
