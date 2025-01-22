<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>关于我们</h4>
        <p>系统版本: 1.0.0</p>
        <p>© 2024 公司名称</p>
      </div>
      
      <div class="footer-section">
        <h4>联系我们</h4>
        <p>电话: 123-456-7890</p>
        <p>邮箱: support@example.com</p>
      </div>
      
      <div class="footer-section">
        <h4>快速链接</h4>
        <router-link to="/privacy">隐私政策</router-link>
        <router-link to="/terms">服务条款</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.app-footer {
  background-color: var(--background-color);
  padding: 2rem 1rem;
  border-top: 1px solid #eaeaea;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.footer-section {
  color: var(--text-color);
}

.footer-section h4 {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.footer-section p {
  margin: 0.5rem 0;
}

.footer-section a {
  display: block;
  color: var(--text-color);
  text-decoration: none;
  margin: 0.5rem 0;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
  }
  
  .footer-section {
    text-align: center;
  }
}
</style>
