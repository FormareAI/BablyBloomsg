@echo off
setlocal ENABLEDELAYEDEXPANSION

REM BabyBloomSG Windows 启动脚本（CMD/PowerShell 双击可用）
REM 功能：自动创建并激活 conda 环境（Python 3.10）、安装依赖并启动应用

chcp 65001 >nul
echo ========================================
echo   BabyBloomSG AI 助手启动脚本 (Windows)
echo ========================================

REM 1) 检查 conda 是否可用
where conda >nul 2>&1
if errorlevel 1 (
  echo [错误] 未检测到 conda。请先安装 Miniconda/Anaconda 并重试。
  echo       下载地址: https://docs.conda.io/en/latest/miniconda.html
  pause
  exit /b 1
)

REM 2) 创建/检测环境 python310（Python 3.10）
set ENV_NAME=python310
call conda env list | findstr /C:"%ENV_NAME%" >nul 2>&1
if errorlevel 1 (
  echo [创建] conda 环境: %ENV_NAME% (python=3.10)
  call conda create -y -n %ENV_NAME% python=3.10
) else (
  echo [存在] 已检测到环境: %ENV_NAME%
)

REM 3) 激活环境
call conda activate %ENV_NAME%
if errorlevel 1 (
  echo [错误] conda 环境激活失败。请手动执行: conda activate %ENV_NAME%
  pause
  exit /b 1
)

REM 4) 安装依赖
echo [依赖] 升级 pip
python -m pip install --upgrade pip

if exist requirement.txt (
  echo [依赖] 安装 requirement.txt
  pip install -r requirement.txt
) else (
  echo [警告] 未找到 requirement.txt，跳过通用依赖安装
)

echo [依赖] 安装/校验 RAG 依赖 (sentence-transformers, faiss-cpu, scikit-learn)
pip install sentence-transformers faiss-cpu scikit-learn
if errorlevel 1 (
  echo [警告] RAG 依赖安装可能失败，稍后应用内会给出提示。
)

REM 5) 启动应用
echo ========================================
echo   启动 BabyBloomSG 应用...
echo ========================================
echo 访问地址: http://localhost:8501
echo 关闭窗口或按 Ctrl+C 可停止服务

streamlit run app.py

endlocal

