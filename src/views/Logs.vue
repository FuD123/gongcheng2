<template>
  <div class="logs container">
    <div class="section" id="logs-section">
      <h3>日志管理</h3>
      <div class="log-controls">
        <div class="filters">
          <select v-model="selectedLevel" @change="filterLogs">
            <option value="all">所有级别</option>
            <option value="info">信息</option>
            <option value="warning">警告</option>
            <option value="error">错误</option>
          </select>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索日志..."
            @input="filterLogs"
          />
        </div>
        <button class="btn btn-secondary" @click="refreshLogs">
          刷新
        </button>
      </div>

      <div class="log-list">
        <div v-for="log in filteredLogs" :key="log.id" class="log-item">
          <div class="log-header">
            <span class="log-level" :class="log.level">{{ log.level }}</span>
            <span class="log-timestamp">{{ formatTimestamp(log.timestamp) }}</span>
          </div>
          <div class="log-content">
            <p class="log-message">{{ log.message }}</p>
            <button
              v-if="log.details"
              class="btn btn-sm"
              @click="toggleDetails(log)"
            >
              {{ log.showDetails ? '隐藏详情' : '查看详情' }}
            </button>
            <div v-if="log.showDetails" class="log-details">
              <pre>{{ log.details }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:5000/api/v1';

export default {
  name: 'Logs',
  data() {
    return {
      logs: [],
      filteredLogs: [],
      selectedLevel: 'all',
      searchQuery: '',
    };
  },
  methods: {
    async getLogs() {
      try {
        const response = await axios.get('/logs');
        this.logs = response.data.map(log => ({
          ...log,
          showDetails: false
        }));
        this.filterLogs();
      } catch (error) {
        console.error('Failed to fetch logs:', error);
      }
    },
    filterLogs() {
      this.filteredLogs = this.logs.filter(log => {
        const matchesLevel = this.selectedLevel === 'all' || 
          log.level.toLowerCase() === this.selectedLevel;
        const matchesQuery = log.message.toLowerCase().includes(
          this.searchQuery.toLowerCase()
        );
        return matchesLevel && matchesQuery;
      });
    },
    toggleDetails(log) {
      log.showDetails = !log.showDetails;
    },
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString();
    },
    refreshLogs() {
      this.getLogs();
    }
  },
  mounted() {
    this.getLogs();
  }
}
</script>

<style scoped>
/* 样式与Home.vue中的相同 */
</style>
