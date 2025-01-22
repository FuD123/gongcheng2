<template>
  <div class="overview container">
    <div class="section" id="overview-section">
      <h3>系统概览</h3>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-title">系统状态</div>
          <div class="metric-value" :class="systemStatusClass">{{ systemStatus }}</div>
        </div>
        <div class="metric-card">
          <div class="metric-title">活跃任务</div>
          <div class="metric-value">{{ activeTasks }}</div>
        </div>
        <div class="metric-card">
          <div class="metric-title">日志条目</div>
          <div class="metric-value">{{ logCount }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:5000/api/v1';

export default {
  name: 'Overview',
  data() {
    return {
      systemStatus: '加载中...',
      activeTasks: 0,
      logCount: 0,
    };
  },
  computed: {
    systemStatusClass() {
      return {
        'status-ok': this.systemStatus === 'Normal',
        'status-warning': this.systemStatus === 'Warning',
        'status-error': this.systemStatus === 'Error'
      };
    }
  },
  methods: {
    async getSystemOverview() {
      try {
        const response = await axios.get('/system/overview');
        this.systemStatus = response.data.status;
        this.activeTasks = response.data.activeTasks;
        this.logCount = response.data.logCount;
      } catch (error) {
        console.error('Failed to fetch system overview:', error);
      }
    }
  },
  mounted() {
    this.getSystemOverview();
  }
}
</script>

<style scoped>
/* 样式与Home.vue中的相同 */
</style>
