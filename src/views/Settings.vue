<template>
  <div class="settings container">
    <div class="section" id="settings-section">
      <h3>系统设置</h3>
      <div class="settings-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab-button', { active: currentTab === tab.id }]"
          @click="currentTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="settings-content">
        <div v-if="currentTab === 'general'" class="general-settings">
          <h4>常规设置</h4>
          <div class="form-group">
            <label>系统名称</label>
            <input
              type="text"
              v-model="systemSettings.systemName"
              @change="saveSettings"
            />
          </div>
          <div class="form-group">
            <label>时区设置</label>
            <select v-model="systemSettings.timezone" @change="saveSettings">
              <option
                v-for="tz in timezones"
                :key="tz"
                :value="tz"
              >
                {{ tz }}
              </option>
            </select>
          </div>
        </div>

        <div v-if="currentTab === 'notifications'" class="notification-settings">
          <h4>通知设置</h4>
          <div class="form-group">
            <label>启用邮件通知</label>
            <input
              type="checkbox"
              v-model="systemSettings.notifications.emailEnabled"
              @change="saveSettings"
            />
          </div>
          <div class="form-group">
            <label>邮件通知频率</label>
            <select
              v-model="systemSettings.notifications.emailFrequency"
              @change="saveSettings"
            >
              <option value="immediate">即时</option>
              <option value="daily">每日</option>
              <option value="weekly">每周</option>
            </select>
          </div>
        </div>

        <div v-if="currentTab === 'security'" class="security-settings">
          <h4>安全设置</h4>
          <div class="form-group">
            <label>密码策略</label>
            <select
              v-model="systemSettings.security.passwordPolicy"
              @change="saveSettings"
            >
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
            </select>
          </div>
          <div class="form-group">
            <label>启用双因素认证</label>
            <input
              type="checkbox"
              v-model="systemSettings.security.twoFactorEnabled"
              @change="saveSettings"
            />
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
  name: 'Settings',
  data() {
    return {
      currentTab: 'general',
      tabs: [
        { id: 'general', label: '常规设置' },
        { id: 'notifications', label: '通知设置' },
        { id: 'security', label: '安全设置' },
      ],
      systemSettings: {
        systemName: '',
        timezone: 'UTC',
        notifications: {
          emailEnabled: false,
          emailFrequency: 'daily'
        },
        security: {
          passwordPolicy: 'medium',
          twoFactorEnabled: false
        }
      },
      timezones: [
        'UTC',
        'Asia/Shanghai',
        'America/New_York',
        'Europe/London'
      ]
    };
  },
  methods: {
    async getSettings() {
      try {
        const response = await axios.get('/settings');
        this.systemSettings = response.data;
      } catch (error) {
        console.error('Failed to fetch settings:', error);
      }
    },
    async saveSettings() {
      try {
        await axios.put('/settings', this.systemSettings);
      } catch (error) {
        console.error('Failed to save settings:', error);
      }
    }
  },
  mounted() {
    this.getSettings();
  }
}
</script>

<style scoped>
/* 样式与Home.vue中的相同 */
</style>
