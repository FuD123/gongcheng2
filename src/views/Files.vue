<template>
  <div class="files container">
    <div class="section" id="file-operations-section">
      <h3>文件操作</h3>
      <div class="file-controls">
        <div class="upload-area">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileUpload"
            multiple
            style="display: none"
          />
          <button class="btn btn-primary" @click="triggerFileInput">
            上传文件
          </button>
          <button class="btn btn-secondary" @click="refreshFiles">
            刷新
          </button>
        </div>
      </div>

      <div class="file-list">
        <div v-for="file in files" :key="file.id" class="file-item">
          <div class="file-info">
            <span class="file-name">{{ file.name }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
            <span class="file-date">{{ formatDate(file.uploadDate) }}</span>
          </div>
          <div class="file-actions">
            <button class="btn btn-sm" @click="downloadFile(file)">
              下载
            </button>
            <button
              class="btn btn-sm btn-danger"
              @click="deleteFile(file)"
            >
              删除
            </button>
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
  name: 'Files',
  data() {
    return {
      files: [],
      uploadProgress: 0,
      isUploading: false,
    };
  },
  methods: {
    async getFiles() {
      try {
        const response = await axios.get('/files');
        this.files = response.data;
      } catch (error) {
        console.error('Failed to fetch files:', error);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async handleFileUpload(event) {
      const files = event.target.files;
      if (!files.length) return;

      this.isUploading = true;
      try {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
          formData.append('files', files[i]);
        }

        await axios.post('/files', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            this.uploadProgress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
          }
        });

        this.getFiles();
      } catch (error) {
        console.error('Failed to upload files:', error);
      } finally {
        this.isUploading = false;
        this.uploadProgress = 0;
        event.target.value = ''; // 清除文件选择
      }
    },
    async downloadFile(file) {
      try {
        const response = await axios.get(`/files/${file.id}`, {
          responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.name);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('Failed to download file:', error);
      }
    },
    async deleteFile(file) {
      try {
        await axios.delete(`/files/${file.id}`);
        this.getFiles();
      } catch (error) {
        console.error('Failed to delete file:', error);
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    refreshFiles() {
      this.getFiles();
    }
  },
  mounted() {
    this.getFiles();
  }
}
</script>

<style scoped>
/* 样式与Home.vue中的相同 */
</style>
