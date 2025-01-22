import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  },
  transformRequest: [(data, headers) => {
    // 确保路径以 / 开头
    if (headers.url && !headers.url.startsWith('/')) {
      headers.url = '/' + headers.url;
    }
    return data;
  }],
  transformResponse: [(data) => {
    try {
      return JSON.parse(data);
    } catch (error) {
      return data;
    }
  }]
});

// 响应拦截器
instance.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 处理未授权
          break;
        case 404:
          // 处理未找到
          break;
        default:
          break;
      }
    }
    return Promise.reject(error);
  }
);

export default instance;
