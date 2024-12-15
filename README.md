# 项目名称：AI艺术鉴赏 - 看画猜作者

## 项目概述
“看画猜作者”是一个基于AI的艺术作品识别项目，旨在通过图像识别技术自动识别出艺术作品的创作者。用户可以通过Web界面上传画作图像，系统将返回作者的预测结果，并展示艺术家简介及其代表作。本项目采用敏捷开发方法，以提升软件的开发效率和迭代效果。

## 目标
- 利用深度学习模型识别上传图像的艺术家。
- 提供艺术家的基本信息和代表作推荐，帮助用户更好地了解艺术作品。

## 功能特点
1. **图片上传**：用户可以上传一张画作图片，通过前端界面发送给后端进行处理。
2. **作者识别**：后端调用EfficientNet-B3模型，分析图像内容并返回预测的作者名称。
3. **艺术家简介与推荐**：系统提供艺术家的基本信息和代表作品推荐，帮助用户更深入地了解该作者及其作品。
4. **跨平台支持**：优化的前端界面适配多种设备和浏览器。

## 技术栈
- **前端**：Vue.js - 提供用户界面，支持图像上传及结果展示。
- **后端**：Django - 处理图像分类请求，调用AI模型并返回结果。
- **模型**：EfficientNet-B3 - 基于深度学习的图像分类模型，用于识别艺术作品的作者。
- **数据**：使用来自49位知名艺术家的画作数据集，包括乔托·迪·邦多纳、毕加索、梵高、安德烈·鲁勃廖夫、提香·韦切利奥等。
- **爬虫**：Python爬虫获取艺术家的简介和代表作介绍，增强用户体验。

## 项目结构
```plaintext
ArtworkRecognition
├── backend              # 后端代码（Django框架）
│   ├── api             # API接口
│   ├── models          # 深度学习模型（EfficientNet-B3）
│   ├── utils           # 工具函数及数据处理
├── frontend             # 前端代码（Vue.js框架）
│   ├── components      # Vue组件
│   ├── assets          # 静态资源（图片、样式表等）
├── crawler              # 爬虫模块
│   ├── scripts         # 爬取艺术家信息的脚本
├── data                 # 数据存储与处理
│   ├── raw_data        # 原始数据集
│   ├── processed_data  # 处理后的数据集
├── docs                 # 文档
└── README.md            # 项目说明文件
```

## 使用方法
### 环境要求
- Python 3.8或更高版本
- Node.js 14.x或更高版本
- Django 4.1或更高版本
- Vue CLI 4.x

### 安装步骤
1. **克隆仓库**
```bash
git clone https://github.com/NeuropathyNetwork/artworkRecognition.git
cd artworkRecognition
```

2. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
```

3. **运行后端服务器**
```bash
python manage.py runserver
```

4. **安装前端依赖**
```bash
cd ../frontend
npm install
```

5. **启动前端开发服务器**
```bash
npm run serve
```

6. **爬虫模块运行（可选）**
```bash
cd ../crawler
python run_crawler.py
```

7. **访问应用**
打开浏览器，访问 `http://127.0.0.1:8000`。

## 开发进度
- **项目分工和仓库搭建**：完成
- **前端框架设计与实现**：进行中
- **后端框架设计与API接口**：进行中
- **AI模型选择与训练**：已选定EfficientNet-B3
- **数据采集与预处理**：进行中
- **艺术家信息爬虫**：设计中

## 贡献指南
1. Fork 本仓库。
2. 创建一个分支：`git checkout -b feature-branch-name`。
3. 提交更改：`git commit -m 'Add some feature'`。
4. 推送到分支：`git push origin feature-branch-name`。
5. 创建一个 Pull Request。

## 团队分工
- **王子琳**：项目管理、后端开发、仓库初始化
- **缪纬韬**：前端设计与实现
- **时晓天**：前端设计与实现
- **陈正元**：后端开发与数据处理

## 项目展示
将在项目完成后发布演示视频和图片，以展示项目的最终功能。

## 许可证
本项目基于 [MIT License](LICENSE) 开源。

## 联系方式
- **组长博客：** [可爱就完事了嗷-CSDN博客](https://blog.csdn.net/m0_73588392)
- **项目地址：** [GitHub仓库](https://github.com/NeuropathyNetwork/artworkRecognition)
