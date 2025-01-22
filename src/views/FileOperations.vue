<template>
  <div class="file-operations">
    <h2>文件操作</h2>

    <!-- Task Queue Section -->
    <div class="task-queue">
      <h3>任务队列</h3>
      <div class="task-controls">
        <button @click="refreshTasks" :disabled="loading">
          刷新
          <span v-if="loading" class="spinner"></span>
        </button>
        <button @click="showCreateTaskModal = true">新建任务</button>
      </div>

      <div class="task-list">
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-info">
            <span class="task-name">{{ task.name }}</span>
            <span class="task-status" :class="task.status">
              {{ taskStatusLabels[task.status] }}
            </span>
            <span class="task-progress">
              进度: {{ task.progress }}%
              <progress :value="task.progress" max="100"></progress>
            </span>
          </div>
          
          <div class="task-actions">
            <button 
              v-if="task.status === 'pending'"
              @click="startTask(task.id)"
            >
              开始
            </button>
            <button
              v-if="task.status === 'running'"
              @click="pauseTask(task.id)"
            >
              暂停
            </button>
            <button
              v-if="task.status === 'paused'"
              @click="resumeTask(task.id)"
            >
              继续
            </button>
            <button
              v-if="['pending', 'paused'].includes(task.status)"
              @click="cancelTask(task.id)"
            >
              取消
            </button>
            <button
              v-if="task.status === 'completed'"
              @click="downloadTaskResult(task.id)"
            >
              下载结果
            </button>
            <button @click="showTaskDetails(task)">
              详情
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateTaskModal" class="modal-overlay">
      <div class="modal-content">
        <h3>新建任务</h3>
        <form @submit.prevent="createTask">
          <div class="form-group">
            <label>任务名称</label>
            <input v-model="newTask.name" required>
          </div>

          <div class="form-group">
            <label>任务类型</label>
            <select v-model="newTask.type" required>
              <option value="download">文件下载</option>
              <option value="upload">文件上传</option>
              <option value="delete">文件删除</option>
            </select>
          </div>

          <div class="form-group">
            <label>目标路径</label>
            <input v-model="newTask.targetPath" required>
          </div>

          <div class="form-group">
            <label>源路径</label>
            <input v-model="newTask.sourcePath">
          </div>

          <div class="form-group">
            <label>优先级</label>
            <select v-model="newTask.priority">
              <option value="1">高</option>
              <option value="2">中</option>
              <option value="3">低</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="button" @click="showCreateTaskModal = false">
              取消
            </button>
            <button type="submit" :disabled="creatingTask">
              创建
              <span v-if="creatingTask" class="spinner"></span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Task Details Modal -->
    <div v-if="selectedTask" class="modal-overlay">
      <div class="modal-content">
        <h3>任务详情</h3>
        <div class="task-details">
          <div class="detail-item">
            <label>ID:</label>
            <span>{{ selectedTask.id }}</span>
          </div>
          <div class="detail-item">
            <label>名称:</label>
            <span>{{ selectedTask.name }}</span>
          </div>
          <div class="detail-item">
            <label>状态:</label>
            <span :class="selectedTask.status">
              {{ taskStatusLabels[selectedTask.status] }}
            </span>
          </div>
          <div class="detail-item">
            <label>进度:</label>
            <span>{{ selectedTask.progress }}%</span>
          </div>
          <div class="detail-item">
            <label>创建时间:</label>
            <span>{{ formatDate(selectedTask.createdAt) }}</span>
          </div>
          <div class="detail-item">
            <label>开始时间:</label>
            <span>{{ formatDate(selectedTask.startedAt) }}</span>
          </div>
          <div class="detail-item">
            <label>结束时间:</label>
            <span>{{ formatDate(selectedTask.finishedAt) }}</span>
          </div>
          <div class="detail-item">
            <label>错误信息:</label>
            <span class="error-message">{{ selectedTask.error }}</span>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="selectedTask = null">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tasks: [],
      loading: false,
      showCreateTaskModal: false,
      creatingTask: false,
      selectedTask: null,
      newTask: {
        name: '',
        type: 'download',
        targetPath: '',
        sourcePath: '',
        priority: '2'
      },
      taskStatusLabels: {
        pending: '等待中',
        running: '运行中',
        paused: '已暂停',
        completed: '已完成',
        failed: '失败',
        cancelled: '已取消'
      },
      taskUpdateInterval: null
    }
  },
  methods: {
    async refreshTasks() {
      this.loading = true
      try {
        const response = await this.$http.get('/tasks')
        this.tasks = response.data
      } catch (error) {
        console.error('获取任务列表失败:', error)
      } finally {
        this.loading = false
      }
    },
    async createTask() {
      this.creatingTask = true
      try {
        await this.$http.post('/tasks', this.newTask)
        this.showCreateTaskModal = false
        this.refreshTasks()
      } catch (error) {
        console.error('创建任务失败:', error)
      } finally {
        this.creatingTask = false
      }
    },
    async startTask(taskId) {
      try {
        const response = await this.$http.post(`/tasks/${taskId}/start`, {
          executor: 'threadpool',
          max_workers: 4
        })
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'running' } : task
        )
      } catch (error) {
        console.error('启动任务失败:', error)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'failed', error: error.message } : task
        )
      }
    },
    async pauseTask(taskId) {
      try {
        await this.$http.post(`/tasks/${taskId}/pause`)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'paused' } : task
        )
      } catch (error) {
        console.error('暂停任务失败:', error)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'failed', error: error.message } : task
        )
      }
    },
    async resumeTask(taskId) {
      try {
        await this.$http.post(`/tasks/${taskId}/resume`)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'running' } : task
        )
      } catch (error) {
        console.error('继续任务失败:', error)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'failed', error: error.message } : task
        )
      }
    },
    async cancelTask(taskId) {
      try {
        await this.$http.post(`/tasks/${taskId}/cancel`)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'cancelled' } : task
        )
      } catch (error) {
        console.error('取消任务失败:', error)
        this.tasks = this.tasks.map(task => 
          task.id === taskId ? { ...task, status: 'failed', error: error.message } : task
        )
      }
    },
    async downloadTaskResult(taskId) {
      try {
        const response = await this.$http.get(`/tasks/${taskId}/result`, {
          responseType: 'blob'
        })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `task_${taskId}_result.zip`)
        document.body.appendChild(link)
        link.click()
      } catch (error) {
        console.error('下载任务结果失败:', error)
      }
    },
    showTaskDetails(task) {
      this.selectedTask = task
    },
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString()
    },
    setupTaskUpdates() {
      this.taskUpdateInterval = setInterval(() => {
        this.refreshTasks()
      }, 5000)
    }
  },
  mounted() {
    this.refreshTasks()
    this.setupTaskUpdates()
  },
  beforeDestroy() {
    if (this.taskUpdateInterval) {
      clearInterval(this.taskUpdateInterval)
    }
  }
}
</script>

<style scoped>
.file-operations {
  padding: 20px;
}

.task-queue {
  margin-top: 20px;
}

.task-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.task-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.task-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.task-status.pending {
  background-color: #f0f0f0;
  color: #666;
}

.task-status.running {
  background-color: #e6f4ff;
  color: #1677ff;
}

.task-status.completed {
  background-color: #f6ffed;
  color: #52c41a;
}

.task-status.failed {
  background-color: #fff2f0;
  color: #ff4d4f;
}

.task-status.cancelled {
  background-color: #fafafa;
  color: #8c8c8c;
}

.task-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-progress progress {
  width: 200px;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.task-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.error-message {
  color: #ff4d4f;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #1677ff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
