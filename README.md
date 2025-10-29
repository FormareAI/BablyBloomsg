## BabyBloomSG

AI 助手用于新加坡家庭政策问答、推荐与计算，基于 Streamlit。

### 支持的 Python 版本
- 支持: Python 3.10
- 其他版本不保证兼容性（请务必使用 3.10）

### 快速开始
1) 克隆或下载本项目代码

2) 创建并激活虚拟环境（可选但推荐）
```bash
# Windows (PowerShell) — 请确保系统默认 python 指向 3.10，或用 python3.10
python -m venv venv  # 或 python3.10 -m venv venv
venv\Scripts\Activate.ps1

# macOS / Linux — 建议明确使用 python3.10
python3.10 -m venv venv  # 若无命令，可用 pyenv/包管理安装 3.10
source venv/bin/activate
```

3) 安装依赖（确保当前环境 Python 为 3.10）
```bash
pip install --upgrade pip
pip install -r requirement.txt
```

**注意**: 如果遇到 RAG 系统初始化失败，请确保已安装以下依赖：
```bash
pip install sentence-transformers faiss-cpu scikit-learn
```

4) 运行应用
```bash
conda activate python310
streamlit run app.py
```

访问: http://localhost:8501

### API Key 配置
在页面左侧边栏按所选模型输入对应的 Key：
- 通义千问: 在 `阿里云 DashScope` 获取 Key
- Gemini: 在 `Google AI Studio` 获取 Key
- Llama-3: 在 `HuggingFace` 获取 Token

无需通过 PowerShell 或 Shell 脚本启动，直接在项目中执行上述命令即可。

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
  1. Python 版本为 3.10
  2. 已激活正确的虚拟环境（conda 或 venv）
  3. 已运行 `pip install -r requirement.txt`

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
