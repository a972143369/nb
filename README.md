# 亚洲盘口预测模型 Web 版本

## 功能介绍
- 预测比赛赢盘 / 走盘 / 输盘结果
- 支持 AOD盘口水位异常检测
- 提示一致性强信号（情报+模型+交锋）
- 显示最近预测结果回顾

## 使用方法

### 一、本地运行（测试）
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行网页：
   ```bash
   python app.py
   ```
3. 打开浏览器访问：http://localhost:7860

### 二、Render 部署
1. 创建 GitHub 仓库，上传本目录文件和你的 model.joblib 模型文件；
2. 登录 [https://render.com](https://render.com)，选择 New Web Service；
3. 填写部署信息：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Port: 7860
4. 几分钟后获得公网访问链接！

