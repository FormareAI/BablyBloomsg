## BabyBloomSG

AI 助手用于新加坡家庭政策问答、推荐与计算，基于 Streamlit。

### 支持的 Python 版本
- 支持: Python 3.10
- 其他版本不保证兼容性（请务必使用 3.10）

### 快速开始

#### 方式一：使用 Conda（推荐）

1) **克隆或下载本项目代码**
```bash
git clone <项目地址>
cd BablyBloomsg
```

2) **创建 Conda 环境（Python 3.10）**
```bash
conda create -n python310 python=3.10
```

3) **激活环境**
```bash
conda activate python310
```

4) **安装依赖**
```bash
# 升级 pip
pip install --upgrade pip

# 安装所有依赖
pip install -r requirement.txt

# 如果 RAG 系统初始化失败，确保安装以下依赖：
pip install sentence-transformers faiss-cpu scikit-learn
```

5) **运行应用**
```bash
streamlit run app.py
```

6) **访问应用**
- 在浏览器中打开：http://localhost:8501
- 应用会自动在浏览器中打开

7) **配置 API Key 并使用**
   - 在页面左侧边栏选择模型（通义千问 / Gemini / Llama-3）
   - 在对应的输入框中输入 API Key：
     - **通义千问**: 访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/) 获取 API Key
     - **Gemini**: 访问 [Google AI Studio](https://aistudio.google.dev/) 获取 API Key
     - **Llama-3**: 访问 [HuggingFace](https://huggingface.co/settings/tokens) 获取 Token
   - 在聊天界面输入问题（如："我想了解生育津贴政策"）
   - 等待 AI 回答（首次使用可能需要几秒加载模型）
   - 查看回答并根据需要继续提问

8) **填写用户信息（可选）**
   - 在左侧边栏可以填写您的身份信息：
     - 公民身份（新加坡公民 / PR / 外国人）
     - 婚姻状况
     - 月收入
     - 子女数量
     - 年龄
   - 填写后可以获得更个性化的政策推荐和计算

#### 方式二：使用 venv（备选）

如果未安装 Conda，可以使用 Python 自带的 venv：

1) **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# macOS / Linux
python3.10 -m venv venv
source venv/bin/activate
```

2) **安装依赖并运行**
```bash
pip install --upgrade pip
pip install -r requirement.txt
pip install sentence-transformers faiss-cpu scikit-learn
streamlit run app.py
```

### 完整使用流程示例

```
1. 创建环境 → conda create -n python310 python=3.10
2. 激活环境 → conda activate python310
3. 安装依赖 → pip install -r requirement.txt
4. 运行程序 → streamlit run app.py
5. 打开浏览器 → http://localhost:8501
6. 输入 API Key → 在左侧边栏选择模型并输入 Key
7. 开始提问 → 在聊天框输入问题，如："生育津贴有多少钱？"
8. 查看回答 → 等待 AI 生成回答并查看结果
9. 继续对话 → 可以继续提问或切换到其他功能（政策推荐、津贴计算等）
```

### 依赖说明

**核心依赖**（必需）:
- `streamlit`, `requests`, `pandas`, `numpy`
- AI 模型库: `google-generativeai`, `huggingface-hub`
- 可视化: `plotly`

**RAG 系统依赖**（必需，用于智能问答）:
- `sentence-transformers>=2.2.0` - 用于文本嵌入
- `faiss-cpu>=1.7.4` - 用于向量检索（CPU 版本）
- `scikit-learn>=1.3.0` - 用于数据处理

⚠️ **重要**: RAG 功能需要上述三个包。如果安装失败，请单独安装：
```bash
pip install sentence-transformers faiss-cpu scikit-learn
```

如未安装 RAG 依赖，应用会显示警告，智能问答功能将不可用。

### 常见问题

**Q: RAG 系统初始化失败，提示"缺少必要的依赖库"**
- A: 请运行以下命令安装 RAG 依赖：
  ```bash
  pip install sentence-transformers faiss-cpu scikit-learn
  ```
  安装完成后重启应用。

**Q: 无法启动或导入失败**
- A: 请确认：
  1. 已创建并激活 Conda 环境：`conda activate python310`
  2. Python 版本为 3.10（运行 `python --version` 检查）
  3. 已运行 `pip install -r requirement.txt`
  4. 已安装 RAG 依赖：`pip install sentence-transformers faiss-cpu scikit-learn`

**Q: 端口被占用**
- A: 修改启动命令：
  ```bash
  streamlit run app.py --server.port 8502
  ```

**Q: faiss 安装失败**
- A: 确保使用 `faiss-cpu`（CPU 版本），而非 `faiss`。在 Windows 上可能需要先安装 Visual C++ 构建工具。

### 后续优化（待办）
- 提升模型回答的专业性与结构化输出
- 结合小规模测试集做准确性评估
- 评估时间规划模块的性价比与准确性
