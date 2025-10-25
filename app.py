import streamlit as st
import os
import requests
from datetime import datetime, timedelta
import json
import time

# 新增：导入模块
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    from rag_system import RAGSystem
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

try:
    from recommendation_engine import RecommendationEngine
    REC_AVAILABLE = True
except ImportError:
    REC_AVAILABLE = False

# 新增：导入时间线生成器和翻译管理器
try:
    from timeline_generator import TimelineGenerator
    TIMELINE_AVAILABLE = True
except ImportError:
    TIMELINE_AVAILABLE = False
    st.warning("⚠️ 时间线生成器未加载")

try:
    from translation_manager import TranslationManager
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("⚠️ 翻译管理器未加载")

# 页面配置
st.set_page_config(
    page_title="BabyBloomSG AI助手",
    page_icon="🇸🇬",
    layout="wide"
)

# 初始化翻译管理器
if 'translator' not in st.session_state:
    if TRANSLATION_AVAILABLE:
        st.session_state.translator = TranslationManager()
    else:
        st.session_state.translator = None

# 初始化语言设置
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 获取翻译文本的辅助函数
def t(key):
    """获取翻译文本"""
    if st.session_state.translator:
        return st.session_state.translator.get(key, st.session_state.language)
    return key

# 模型配置
MODEL_CONFIG = {
    "通义千问": {
        "name": "Qwen-Max",
        "provider": "Alibaba Cloud",
        "speed": "快速",
        "cost": "中等"
    },
    "Gemini": {
        "name": "Gemini-1.5-Flash",
        "provider": "Google",
        "speed": "极快",
        "cost": "免费"
    },
    "Llama-3": {
        "name": "Llama-3-8B",
        "provider": "Meta (HuggingFace)",
        "speed": "较慢",
        "cost": "免费"
    }
}

# 政策知识库
POLICY_KB = {
    'fertility': {
        'baby_bonus': {
            'cash_gifts': {
                '1st_child': 8000,
                '2nd_child': 8000,
                '3rd_child': 10000,
                '4th_child': 10000,
                '5th_and_above': 10000
            },
            'cda_matching': {
                '1st_2nd': 3000,
                '3rd_to_6th': 9000
            }
        },
        'maternity_leave': {
            'government_paid': 16,
            'employer_paid': 0,
            'total': 16
        },
        'paternity_leave': {
            'government_paid': 2,
            'employer_paid': 0,
            'total': 2
        },
        'childcare_subsidy': {
            'infant_care': {'max_subsidy': 600, 'income_ceiling': 12000},
            'childcare': {'max_subsidy': 467, 'income_ceiling': 12000}
        },
        'medisave_grant': 4000,
        'website': 'https://www.babybonus.msf.gov.sg',
        'description': '生育津贴计划帮助新加坡家庭应对抚养孩子的费用'
    },
    'housing': {
        'bto_requirements': {
            'age': 21,
            'income_ceiling': {
                '2room': 7000,
                '3room_to_5room': 14000
            },
            'citizenship': 'At least one applicant must be Singapore Citizen'
        },
        'grants': {
            'enhanced_housing_grant': {
                'max_amount': 80000,
                'income_ceiling': 9000
            },
            'family_grant': {
                'max_amount': 50000,
                'income_ceiling': 14000
            },
            'proximity_housing_grant': {
                'max_amount': 30000,
                'condition': 'Living with or near parents'
            }
        },
        'price_ranges': {
            '2room': [150000, 250000],
            '3room': [250000, 400000],
            '4room': [350000, 550000],
            '5room': [450000, 700000]
        },
        'website': 'https://www.hdb.gov.sg',
        'description': '建屋发展局(HDB)组屋是新加坡大多数家庭的首选住房'
    },
    'marriage': {
        'age_requirement': 21,
        'cost_range': [26, 42],
        'documents': ['身份证(NRIC/FIN)', '出生证明', '单身证明'],
        'procedures': [
            '在线提交结婚通知(21天前)',
            '支付费用',
            '预约注册日期',
            '携带文件到婚姻注册局',
            '宣誓并签署结婚证书'
        ],
        'website': 'https://www.rom.gov.sg',
        'description': '在新加坡注册结婚是一个简单快捷的过程'
    },
    'healthcare': {
        'pregnancy_support': {
            'antenatal_care': '定期产检由政府诊所提供补贴',
            'delivery_costs': {
                'public_hospital': [700, 1500],
                'private_hospital': [5000, 15000]
            },
            'medisave_usage': '可使用Medisave支付产检和分娩费用'
        },
        'child_immunization': {
            'cost': 'Free at polyclinics',
            'schedule': '出生至18个月需完成多次接种'
        },
        'website': 'https://www.healthhub.sg'
    },
    'education': {
        'kindergarten': {
            'age': '18个月起可申请',
            'subsidy': {
                'income_ceiling': 12000,
                'max_subsidy': 467
            }
        },
        'primary_school': {
            'age': 6,
            'registration': '分阶段报名系统',
            'cost': 'Heavily subsidized for citizens'
        },
        'website': 'https://www.moe.gov.sg'
    }
}

# 初始化系统
@st.cache_resource
def initialize_systems():
    """初始化RAG、推荐和时间线系统"""
    systems = {}
    
    if RAG_AVAILABLE:
        try:
            systems['rag'] = RAGSystem(POLICY_KB)
            systems['rag'].build_index()
        except Exception as e:
            st.warning(f"RAG系统初始化失败: {e}")
    
    if REC_AVAILABLE:
        try:
            systems['rec'] = RecommendationEngine(POLICY_KB)
        except Exception as e:
            st.warning(f"推荐引擎初始化失败: {e}")
    
    if TIMELINE_AVAILABLE:
        try:
            systems['timeline'] = TimelineGenerator()
        except Exception as e:
            st.warning(f"时间线生成器初始化失败: {e}")
    
    return systems

if 'systems' not in st.session_state:
    st.session_state.systems = initialize_systems()

# 标题
st.title(t('app_title'))

# 侧边栏：语言选择
st.sidebar.header(t('sidebar_language'))
if TRANSLATION_AVAILABLE and st.session_state.translator:
    languages = st.session_state.translator.get_available_languages()
    
    # 创建语言选择器
    lang_options = [f"{lang['flag']} {lang['name']}" for lang in languages]
    lang_codes = [lang['code'] for lang in languages]
    
    current_index = lang_codes.index(st.session_state.language)
    
    selected_lang = st.sidebar.selectbox(
        "Language / 语言 / Bahasa",
        lang_options,
        index=current_index
    )
    
    # 更新语言设置
    new_lang_code = lang_codes[lang_options.index(selected_lang)]
    if new_lang_code != st.session_state.language:
        st.session_state.language = new_lang_code
        st.rerun()

# 侧边栏：API配置
st.sidebar.header(t('sidebar_api_config'))

selected_model = st.sidebar.selectbox(
    t('sidebar_select_model'),
    list(MODEL_CONFIG.keys()),
    help="不同模型有不同特点，建议都试试！"
)

with st.sidebar.expander("📊 模型信息", expanded=False):
    info = MODEL_CONFIG[selected_model]
    st.write(f"**名称**: {info['name']}")
    st.write(f"**提供商**: {info['provider']}")
    st.write(f"**速度**: {info['speed']}")
    st.write(f"**成本**: {info['cost']}")

if selected_model == "通义千问":
    api_key = st.sidebar.text_input("通义千问API Key", type="password")
elif selected_model == "Gemini":
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
else:
    api_key = st.sidebar.text_input("HuggingFace Token", type="password")

# 用户信息
st.sidebar.header(t('sidebar_user_info'))

# 翻译选项
citizen_options = [t('citizen'), t('pr'), t('foreigner')]
marital_options = [t('single'), t('married'), t('divorced')]

citizen = st.sidebar.selectbox(t('sidebar_citizenship'), citizen_options)
marital_status = st.sidebar.selectbox(t('sidebar_marital_status'), marital_options)
income = st.sidebar.number_input(t('sidebar_income'), min_value=0, value=5000, step=100)
children = st.sidebar.number_input(t('sidebar_children'), min_value=0, value=0)
age = st.sidebar.number_input(t('sidebar_age'), min_value=18, max_value=100, value=30)

# 高级设置
st.sidebar.header(t('sidebar_advanced'))
use_rag = st.sidebar.checkbox(t('sidebar_enable_rag'), value=True)

# 模型统计
if 'model_stats' not in st.session_state:
    st.session_state.model_stats = {
        "通义千问": {"calls": 0, "total_time": 0, "errors": 0},
        "Gemini": {"calls": 0, "total_time": 0, "errors": 0},
        "Llama-3": {"calls": 0, "total_time": 0, "errors": 0}
    }

with st.sidebar.expander("📈 模型性能统计", expanded=False):
    for model_name, stats in st.session_state.model_stats.items():
        if stats['calls'] > 0:
            avg_time = stats['total_time'] / stats['calls']
            st.write(f"**{model_name}**")
            st.write(f"  • 调用次数: {stats['calls']}")
            st.write(f"  • 平均响应: {avg_time:.2f}秒")
            st.write(f"  • 错误次数: {stats['errors']}")
            st.write("---")

# 辅助函数
def get_exchange_rate():
    """获取实时汇率"""
    try:
        r = requests.get('https://api.exchangerate-api.com/v4/latest/SGD', timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {
                'USD': data['rates'].get('USD', 0.74),
                'CNY': data['rates'].get('CNY', 5.3),
                'MYR': data['rates'].get('MYR', 3.3)
            }
    except:
        pass
    return {'USD': 0.74, 'CNY': 5.3, 'MYR': 3.3}

def detect_intent(question):
    """意图识别"""
    q = question.lower()
    if any(word in q for word in ['生育', '津贴', 'baby', '孩子', '怀孕', 'maternity', 'paternity', 'bonus', 'bayi']):
        return 'fertility'
    elif any(word in q for word in ['住房', 'bto', 'hdb', '房子', 'housing', 'perumahan']):
        return 'housing'  
    elif any(word in q for word in ['结婚', '婚姻', 'rom', 'marriage', 'perkahwinan']):
        return 'marriage'
    elif any(word in q for word in ['医疗', '健康', '产检', 'health', 'pregnancy', 'kesihatan']):
        return 'healthcare'
    elif any(word in q for word in ['教育', '幼儿园', '学校', 'education', 'kindergarten', 'pendidikan']):
        return 'education'
    return 'general'

def generate_response(question, intent, user_info):
    """生成政策回答"""
    rates = get_exchange_rate()
    citizen_status = t('citizen') in user_info.get('citizen', '')
    income = user_info.get('income', 0)
    kids = user_info.get('children', 0)
    
    if intent == 'fertility':
        data = POLICY_KB['fertility']['baby_bonus']
        n = kids + 1
        
        child_key = f"{['1st', '2nd', '3rd', '4th', '5th_and_above'][min(n-1, 4)]}_child"
        cash = data['cash_gifts'].get(child_key, 10000)
        cda = data['cda_matching']['1st_2nd' if n <= 2 else '3rd_to_6th']
        
        ml = POLICY_KB['fertility']['maternity_leave']['total']
        pl = POLICY_KB['fertility']['paternity_leave']['total']
        
        return f"""
💰 **新加坡生育津贴详情（第{n}胎）**

🎁 **现金奖励**: S${cash:,} (约¥{int(cash * rates['CNY']):,})
💳 **CDA配对**: S${cda:,}
🏥 **Medisave新生儿补助**: S$4,000
👶 **产假**: {ml}周（政府支付）
👨‍👧 **陪产假**: {pl}周

📋 **申请条件**:
  • 孩子必须是新加坡公民
  • 出生后18个月内申请
  
🌐 **官方网站**: {POLICY_KB['fertility']['website']}

{"✅ 您符合申请条件" if citizen_status else "❌ 需要公民身份才能申请"}
        """
        
    elif intent == 'housing':
        data = POLICY_KB['housing']
        req = data['bto_requirements']
        
        income_ok = income <= req['income_ceiling']['3room_to_5room']
        citizen_ok = citizen_status
        
        grants_text = "\n".join([
            f"  • {name.replace('_', ' ').title()}: S${info['max_amount']:,}"
            for name, info in data['grants'].items()
        ])
        
        return f"""
🏠 **HDB/BTO住房政策指南**

💰 **价格范围**:
  • 3房式: S${data['price_ranges']['3room'][0]:,} - S${data['price_ranges']['3room'][1]:,}
  • 4房式: S${data['price_ranges']['4room'][0]:,} - S${data['price_ranges']['4room'][1]:,}

✅ **资格检查**:
  • 收入: {'✅' if income_ok else '❌'} (S${income:,} vs 上限S$14,000)
  • 公民身份: {'✅' if citizen_ok else '❌'}

💸 **可用津贴**:
{grants_text}

🌐 **官网**: {data['website']}
        """
        
    elif intent == 'marriage':
        data = POLICY_KB['marriage']
        steps = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(data['procedures'])])
        
        return f"""
💒 **新加坡结婚注册指南**

📋 **申请流程**:
{steps}

💰 **费用**: S${data['cost_range'][0]} - S${data['cost_range'][1]}
⏰ **所需时间**: 最少21天通知期
🌐 **官网**: {data['website']}
        """
    
    elif intent == 'healthcare':
        data = POLICY_KB['healthcare']
        delivery_range = data['pregnancy_support']['delivery_costs']['public_hospital']
        
        return f"""
🏥 **新加坡孕产医疗支持**

🤰 **产检护理**: {data['pregnancy_support']['antenatal_care']}
👶 **分娩费用** (公立医院): S${delivery_range[0]:,} - S${delivery_range[1]:,}
💳 **Medisave使用**: {data['pregnancy_support']['medisave_usage']}
💉 **儿童疫苗**: {data['child_immunization']['cost']}

🌐 **官网**: {data['website']}
        """
    
    elif intent == 'education':
        data = POLICY_KB['education']
        kg = data['kindergarten']
        
        return f"""
🎓 **新加坡儿童教育政策**

🏫 **幼儿园**:
  • 入学年龄: {kg['age']}
  • 最高补贴: S${kg['subsidy']['max_subsidy']}/月
  • 收入上限: S${kg['subsidy']['income_ceiling']:,}

📚 **小学**:
  • 入学年龄: {data['primary_school']['age']}岁
  • 注册方式: {data['primary_school']['registration']}

🌐 **官网**: {data['website']}
        """
    
    return "我正在学习更多政策知识，请尝试询问生育津贴、住房申请、结婚注册、医疗或教育相关问题。"

# LLM调用函数
def call_qwen_api(question, context, api_key):
    """调用通义千问API"""
    if not api_key:
        return t('error_no_api_key')
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-max",
        "messages": [
            {"role": "system", "content": "你是BabyBloomSG，新加坡家庭政策专业AI助手。请基于提供的政策信息，用中文回答用户问题，语调温暖专业，使用emoji。"},
            {"role": "user", "content": f"政策背景信息：{context}\n\n用户问题：{question}"}
        ]
    }
    
    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"API调用失败: {response.status_code}"
            
    except Exception as e:
        return f"网络错误: {str(e)}"

def call_gemini_api(question, context, api_key):
    """调用Gemini API"""
    if not GEMINI_AVAILABLE:
        return "❌ Gemini库未安装"
    
    if not api_key:
        return t('error_no_api_key')
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""你是BabyBloomSG，新加坡家庭政策专业AI助手。

政策背景信息：
{context}

用户问题：{question}

请基于上述政策信息，用中文回答用户问题。语调温暖专业，适当使用emoji。"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Gemini调用错误: {str(e)}"

def call_llama_api(question, context, hf_token):
    """调用Llama-3"""
    if not HF_AVAILABLE:
        return "❌ HuggingFace库未安装"
    
    if not hf_token:
        return t('error_no_api_key')
    
    try:
        client = InferenceClient(token=hf_token)
        
        prompt = f"""You are BabyBloomSG, a professional AI assistant for Singapore family policies.

Policy Information:
{context}

User Question: {question}

Please answer in Chinese based on the policy information above. Be warm and professional."""
        
        response = client.text_generation(
            prompt,
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            max_new_tokens=500,
            temperature=0.7
        )
        
        return response
        
    except Exception as e:
        return f"Llama-3调用错误: {str(e)}"

def call_llm_api(question, context, model_type, api_key):
    """统一LLM调用"""
    start_time = time.time()
    
    try:
        if model_type == "通义千问":
            response = call_qwen_api(question, context, api_key)
        elif model_type == "Gemini":
            response = call_gemini_api(question, context, api_key)
        elif model_type == "Llama-3":
            response = call_llama_api(question, context, api_key)
        else:
            response = "未知模型类型"
        
        elapsed_time = time.time() - start_time
        st.session_state.model_stats[model_type]["calls"] += 1
        st.session_state.model_stats[model_type]["total_time"] += elapsed_time
        
        return response
        
    except Exception as e:
        st.session_state.model_stats[model_type]["errors"] += 1
        return f"调用失败: {str(e)}"

# ==================== 导航选择 ====================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "智能问答"

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(t('tab_chat'), use_container_width=True, 
                 type="primary" if st.session_state.current_page == "智能问答" else "secondary"):
        st.session_state.current_page = "智能问答"
with col2:
    if st.button(t('tab_recommendation'), use_container_width=True,
                 type="primary" if st.session_state.current_page == "政策推荐" else "secondary"):
        st.session_state.current_page = "政策推荐"
with col3:
    if st.button(t('tab_calculator'), use_container_width=True,
                 type="primary" if st.session_state.current_page == "津贴计算" else "secondary"):
        st.session_state.current_page = "津贴计算"
with col4:
    if st.button(t('tab_timeline'), use_container_width=True,
                 type="primary" if st.session_state.current_page == "时间规划" else "secondary"):
        st.session_state.current_page = "时间规划"

st.markdown("---")

# ==================== 智能问答页面 ====================
if st.session_state.current_page == "智能问答":
    st.markdown(t('chat_description'))
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": t('chat_welcome')}
        ]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input(t('chat_input_placeholder')):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner(f"{selected_model} {t('chat_thinking')}"):
                intent = detect_intent(prompt)
                
                user_info = {
                    'citizen': citizen,
                    'income': income,
                    'children': children,
                    'age': age,
                    'marital_status': marital_status
                }
                
                if use_rag and RAG_AVAILABLE and 'rag' in st.session_state.systems:
                    try:
                        retrieved_docs = st.session_state.systems['rag'].search(prompt, top_k=3)
                        rag_context = "\n\n".join([f"相关政策 {i+1}:\n{doc}" for i, doc in enumerate(retrieved_docs)])
                        basic_response = f"{generate_response(prompt, intent, user_info)}\n\n**检索到的相关政策**:\n{rag_context}"
                    except:
                        basic_response = generate_response(prompt, intent, user_info)
                else:
                    basic_response = generate_response(prompt, intent, user_info)
                
                if api_key:
                    ai_response = call_llm_api(prompt, basic_response, selected_model, api_key)
                    final_response = ai_response
                else:
                    final_response = basic_response + f"\n\n💡 {t('chat_api_hint')}"
                
                # 如果需要翻译（非中文）
                if st.session_state.language != 'zh' and st.session_state.translator:
                    final_response = st.session_state.translator.translate_policy_response(
                        final_response, 'zh', st.session_state.language
                    )
                
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})

# ==================== 政策推荐页面 ====================
elif st.session_state.current_page == "政策推荐":
    st.markdown(t('rec_description'))
    
    if st.button(t('rec_button'), type="primary"):
        if REC_AVAILABLE and 'rec' in st.session_state.systems:
            with st.spinner(t('rec_analyzing')):
                user_profile = {
                    'citizenship': citizen,
                    'marital_status': marital_status,
                    'income': income,
                    'children': children,
                    'age': age
                }
                
                recommendations = st.session_state.systems['rec'].get_recommendations(user_profile)
                
                st.success(t('rec_success'))
                
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"📌 {t('rec_button')} {i}: {rec['title']}", expanded=(i==1)):
                        st.write(f"**{t('rec_category')}**: {rec['category']}")
                        st.write(f"**{t('rec_priority')}**: {'⭐' * rec['priority']}")
                        st.write(f"**{t('rec_description_label')}**: {rec['description']}")
                        
                        if rec.get('eligibility'):
                            st.write(f"**{t('rec_eligibility')}**: {rec['eligibility']}")
                        
                        if rec.get('benefits'):
                            st.write(f"**{t('rec_benefits')}**: {rec['benefits']}")
                        
                        if rec.get('website'):
                            st.write(f"**{t('rec_website')}**: {rec['website']}")
        else:
            st.error(t('error_engine_not_loaded'))

# ==================== 津贴计算页面 ====================
elif st.session_state.current_page == "津贴计算":
    st.markdown(t('calc_description'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t('calc_fertility_title'))
        calc_children = st.number_input(t('calc_children_plan'), min_value=1, max_value=10, value=2, key="calc_children")
        
        if st.button(t('calc_button_fertility'), key="calc_fertility"):
            if REC_AVAILABLE and 'rec' in st.session_state.systems:
                total = st.session_state.systems['rec'].calculate_fertility_benefits(
                    current_children=children,
                    planned_children=calc_children,
                    is_citizen=(t('citizen') in citizen)
                )
                
                st.metric(t('calc_total_fertility'), f"S${total:,}")
                
                rates = get_exchange_rate()
                st.write(f"约 ¥{int(total * rates['CNY']):,} 人民币")
                st.write(f"约 ${int(total * rates['USD']):,} 美元")
            else:
                st.error(t('error_engine_not_loaded'))
    
    with col2:
        st.subheader(t('calc_housing_title'))
        calc_flat_type = st.selectbox(t('calc_flat_type'), ["3房", "4房", "5房"], key="calc_flat")
        calc_live_with_parents = st.checkbox(t('calc_proximity'), key="calc_proximity")
        
        if st.button(t('calc_button_housing'), key="calc_housing"):
            if REC_AVAILABLE and 'rec' in st.session_state.systems:
                total = st.session_state.systems['rec'].calculate_housing_grants(
                    income=income,
                    is_citizen=(t('citizen') in citizen),
                    first_timer=True,
                    proximity=calc_live_with_parents
                )
                
                st.metric(t('calc_total_housing'), f"S${total:,}")
                
                grants = POLICY_KB['housing']['grants']
                if income <= 9000:
                    st.write(f"• Enhanced Housing Grant: S${grants['enhanced_housing_grant']['max_amount']:,}")
                if income <= 14000:
                    st.write(f"• Family Grant: S${grants['family_grant']['max_amount']:,}")
                if calc_live_with_parents:
                    st.write(f"• Proximity Housing Grant: S${grants['proximity_housing_grant']['max_amount']:,}")
            else:
                st.error(t('error_engine_not_loaded'))

# ==================== 时间规划页面 ====================
elif st.session_state.current_page == "时间规划":
    st.markdown(t('timeline_description'))
    
    if TIMELINE_AVAILABLE and 'timeline' in st.session_state.systems:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("⚙️ " + t('timeline_milestones'))
            
            start_date = st.date_input(
                t('timeline_start_date'),
                value=datetime.now(),
                min_value=datetime.now() - timedelta(days=365),
                max_value=datetime.now() + timedelta(days=365*5)
            )
            
            milestones = []
            if st.checkbox(t('timeline_marriage'), value=True):
                milestones.append('marriage')
            if st.checkbox(t('timeline_housing'), value=True):
                milestones.append('housing')
            if st.checkbox(t('timeline_pregnancy'), value=True):
                milestones.append('pregnancy')
            if st.checkbox(t('timeline_baby_admin'), value=True):
                milestones.append('baby_admin')
            
            if st.button(t('timeline_generate'), type="primary"):
                if milestones:
                    with st.spinner(t('timeline_generating')):
                        timeline_data = st.session_state.systems['timeline'].generate_timeline(
                            datetime.combine(start_date, datetime.min.time()),
                            milestones,
                            st.session_state.language
                        )
                        
                        st.session_state.timeline_data = timeline_data
                        st.success("✅ " + t('timeline_generate'))
                else:
                    st.warning("请至少选择一个里程碑")
        
        with col2:
            if 'timeline_data' in st.session_state and st.session_state.timeline_data:
                # 显示甘特图
                fig = st.session_state.systems['timeline'].create_gantt_chart(
                    st.session_state.timeline_data,
                    st.session_state.language
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示即将到来的提醒
                st.subheader(t('timeline_reminders_title'))
                reminders = st.session_state.systems['timeline'].get_upcoming_reminders(
                    st.session_state.timeline_data,
                    days_ahead=90,
                    language=st.session_state.language
                )
                
                if reminders:
                    for reminder in reminders[:5]:
                        with st.container():
                            cols = st.columns([1, 4, 2])
                            with cols[0]:
                                st.write(reminder['urgency'])
                            with cols[1]:
                                st.write(f"**{reminder['task']}**")
                                st.caption(reminder['description'])
                            with cols[2]:
                                st.write(f"{reminder['days_until']} {t('timeline_days_until')}")
                                st.caption(reminder['date'].strftime('%Y-%m-%d'))
                            st.markdown("---")
                else:
                    st.info("未来90天内暂无提醒事项")
                
                # 显示里程碑摘要
                st.subheader(t('timeline_summary_title'))
                summary = st.session_state.systems['timeline'].create_milestone_summary(
                    st.session_state.timeline_data,
                    st.session_state.language
                )
                
                for item in summary:
                    with st.expander(f"{item['category']}", expanded=False):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(t('timeline_task_count'), item['task_count'])
                        with col_b:
                            st.metric(t('timeline_duration'), f"{item['total_days']} {t('timeline_days')}")
                        
                        st.write(f"**开始**: {item['start'].strftime('%Y-%m-%d')}")
                        st.write(f"**结束**: {item['end'].strftime('%Y-%m-%d')}")
            else:
                st.info("👈 请在左侧配置并生成时间线")
    else:
        st.error("时间线生成器未加载，请安装所需依赖：pip install plotly pandas")

# 底部说明
st.markdown("---")
st.markdown(f"### {t('guide_title')}")
st.markdown(f"""
1. {t('guide_step1')}
2. {t('guide_step2')}
   - 通义千问: [阿里云DashScope](https://dashscope.console.aliyun.com/)
   - Gemini: [Google AI Studio](https://aistudio.google.dev/)
   - Llama-3: [HuggingFace](https://huggingface.co/settings/tokens)
3. {t('guide_step3')}
4. {t('guide_step4')}
   - {t('feature_chat')}
   - {t('feature_rec')}
   - {t('feature_calc')}
   - {t('feature_timeline')}

### {t('new_features_title')}
- {t('feature_rag')}
- {t('feature_rec_engine')}
- {t('feature_calculator')}
- {t('feature_timeline_gen')}
- {t('feature_multilang')}

### {t('disclaimer_title')}
{t('disclaimer_text')}
""")