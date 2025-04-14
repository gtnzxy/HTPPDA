

<h1 align="center">心理健康检测系统</h1>

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English">
  </a>
  <a href="README_CN.md">
    <img src="https://img.shields.io/badge/语言-中文-blue?style=for-the-badge" alt="中文">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/许可证-GPL%203.0-green?style=for-the-badge" alt="许可证">
  </a>
</p>



## 项目概述
在中国，超过6600万留守儿童由于父母外出务工面临严重的心理健康挑战。早期筛查和识别高风险留守儿童至关重要，但由于心理健康专业人员严重短缺（尤其是在农村地区），这项工作面临巨大困难。房树人测验（HTP）作为一种参与度较高的心理评估工具，因其对专业解释的需求限制了在资源匮乏地区的应用。为解决这一问题，我们提出了HTPPDA，一个基于多模态大语言模型的多智能体系统，用于协助心理健康专业人员分析HTP绘画。该系统通过特征提取和心理解释两个阶段运作，能够生成专业报告，为心理健康筛查提供支持。


## ✨ 主要特点

<p align="center">
  <img src="https://img.shields.io/badge/HTP分析-专业级辅助-blue?style=for-the-badge" alt="HTP分析">
  <img src="https://img.shields.io/badge/语言支持-EN%20%7C%20中文-blue?style=for-the-badge" alt="语言">
</p>

## 🚀 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/LYiHub/psydraw.git
cd HTPPDA
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
- 复制 `.env_example` 文件并重命名为 `.env`
- 填写您的API密钥和基础URL

### 使用方法

<p align="center">
  <img src="https://img.shields.io/badge/1-直接调用-orange?style=for-the-badge" alt="直接调用">
  <img src="https://img.shields.io/badge/2-API集成-orange?style=for-the-badge" alt="API">
  <img src="https://img.shields.io/badge/3-网页演示-orange?style=for-the-badge" alt="网页">
</p>

#### 1. 直接调用
```bash
bash run.sh
# 或
mple/epython run.py --image_file exaxample1.png --save_path example/example1_result.json --language zh
```

#### 2. API集成
```bash
python deploy.py --port 9557
```
服务运行于 `http://127.0.0.1:9557`

#### 3. 网页演示
```bash
bash web_demo.sh
# 或
streamlit run src/main.py
```


## ⚖️ 许可证

本项目采用GPL-3.0许可证。详情请参见[LICENSE](LICENSE)文件。

## ⚠️ 免责声明

本项目严格作为专业筛查辅助工具。它不得作为独立的诊断工具或替代专业医疗评估。该系统旨在支持而非取代合格心理健康专业人员的专业知识。任何系统的实施或使用都必须在专业监督下进行。 