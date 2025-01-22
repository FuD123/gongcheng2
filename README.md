# 工程项目管理系统

这是一个基于Python和Vue.js的工程项目管理系统，采用前后端分离架构。

## 项目结构

```
.
├── app/                  # Flask应用核心
│   ├── __init__.py       # 应用初始化
│   ├── models.py         # 数据库模型
│   └── routes.py         # API路由
├── src/                  # 前端Vue.js代码
│   ├── api/              # API接口
│   ├── assets/           # 静态资源
│   ├── components/       # Vue组件
│   ├── modules/          # 业务模块
│   ├── router/           # 路由配置
│   ├── store/            # Vuex状态管理
│   ├── views/            # 页面视图
│   └── main.ts           # 前端入口
├── tests/                # 测试代码
│   ├── unit/             # 单元测试
│   └── test_app.py       # 应用测试
├── migrations/           # 数据库迁移
├── static/               # 静态文件
├── requirements.txt      # Python依赖
├── package.json          # 前端依赖
├── main.py               # 后端入口
├── utils.py              # 工具函数
└── README.md             # 项目说明
```

## 主要功能模块

- 用户管理
- 任务管理
- 日志管理
- 部署管理
- 系统设置

## 技术栈

- 前端：Vue 3 + TypeScript + Vite
- 后端：Python + Flask
- 数据库：SQLite
- 测试：Pytest + Vitest

## 开发环境配置

1. 克隆项目
   ```bash
   git clone https://github.com/FuD123/gongcheng2.git
   ```

2. 安装依赖
   ```bash
   # 后端
   pip install -r requirements.txt

   # 前端
   npm install
   ```

3. 初始化数据库
   ```bash
   python init_db.py
   ```

4. 启动开发服务器
   ```bash
   # 后端
   python main.py

   # 前端
   npm run dev
   ```

## 测试

运行所有测试：
```bash
# 后端测试
pytest

# 前端测试
npm test
```

## 贡献指南

欢迎提交Pull Request。请确保：
- 代码风格一致
- 包含必要的测试
- 更新相关文档

## 许可证

MIT License
