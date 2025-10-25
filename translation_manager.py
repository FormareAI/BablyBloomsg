"""
多语言翻译管理器
支持中文、英文、马来语
"""

class TranslationManager:
    """管理应用程序的多语言翻译"""
    
    def __init__(self):
        self.translations = {
            # 应用标题和导航
            'app_title': {
                'zh': '🇸🇬 BabyBloomSG AI智能家庭政策助手',
                'en': '🇸🇬 BabyBloomSG AI Smart Family Policy Assistant',
                'ms': '🇸🇬 Pembantu Dasar Keluarga Pintar BabyBloomSG AI'
            },
            'tab_chat': {
                'zh': '💬 智能问答',
                'en': '💬 Smart Q&A',
                'ms': '💬 Soal Jawab Pintar'
            },
            'tab_recommendation': {
                'zh': '🎯 政策推荐',
                'en': '🎯 Policy Recommendations',
                'ms': '🎯 Cadangan Dasar'
            },
            'tab_calculator': {
                'zh': '📊 津贴计算',
                'en': '📊 Benefits Calculator',
                'ms': '📊 Kalkulator Faedah'
            },
            'tab_timeline': {
                'zh': '📅 时间规划',
                'en': '📅 Timeline Planner',
                'ms': '📅 Perancang Garis Masa'
            },
            
            # 侧边栏
            'sidebar_api_config': {
                'zh': '🔑 API配置',
                'en': '🔑 API Configuration',
                'ms': '🔑 Konfigurasi API'
            },
            'sidebar_select_model': {
                'zh': '选择AI模型',
                'en': 'Select AI Model',
                'ms': 'Pilih Model AI'
            },
            'sidebar_user_info': {
                'zh': '👤 个人信息',
                'en': '👤 Personal Information',
                'ms': '👤 Maklumat Peribadi'
            },
            'sidebar_citizenship': {
                'zh': '公民身份',
                'en': 'Citizenship Status',
                'ms': 'Status Kewarganegaraan'
            },
            'sidebar_marital_status': {
                'zh': '婚姻状态',
                'en': 'Marital Status',
                'ms': 'Status Perkahwinan'
            },
            'sidebar_income': {
                'zh': '家庭月收入 (SGD)',
                'en': 'Monthly Household Income (SGD)',
                'ms': 'Pendapatan Bulanan Isi Rumah (SGD)'
            },
            'sidebar_children': {
                'zh': '已有子女数',
                'en': 'Number of Children',
                'ms': 'Bilangan Anak'
            },
            'sidebar_age': {
                'zh': '年龄',
                'en': 'Age',
                'ms': 'Umur'
            },
            'sidebar_language': {
                'zh': '🌍 语言设置',
                'en': '🌍 Language Settings',
                'ms': '🌍 Tetapan Bahasa'
            },
            'sidebar_advanced': {
                'zh': '⚙️ 高级设置',
                'en': '⚙️ Advanced Settings',
                'ms': '⚙️ Tetapan Lanjutan'
            },
            'sidebar_enable_rag': {
                'zh': '启用RAG增强检索',
                'en': 'Enable RAG Enhanced Search',
                'ms': 'Aktifkan Carian Dipertingkat RAG'
            },
            
            # 公民身份选项
            'citizen': {
                'zh': '新加坡公民',
                'en': 'Singapore Citizen',
                'ms': 'Warganegara Singapura'
            },
            'pr': {
                'zh': 'PR',
                'en': 'PR',
                'ms': 'PR'
            },
            'foreigner': {
                'zh': '外国人',
                'en': 'Foreigner',
                'ms': 'Warga Asing'
            },
            
            # 婚姻状态选项
            'single': {
                'zh': '未婚',
                'en': 'Single',
                'ms': 'Bujang'
            },
            'married': {
                'zh': '已婚',
                'en': 'Married',
                'ms': 'Berkahwin'
            },
            'divorced': {
                'zh': '离异',
                'en': 'Divorced',
                'ms': 'Bercerai'
            },
            
            # 智能问答页面
            'chat_description': {
                'zh': '**💬 向AI助手提问，获取专业的政策解答**',
                'en': '**💬 Ask the AI assistant for professional policy answers**',
                'ms': '**💬 Tanya pembantu AI untuk jawapan dasar profesional**'
            },
            'chat_welcome': {
                'zh': '您好！我是BabyBloomSG AI助手。您可以问我关于生育津贴、住房申请、结婚注册、医疗和教育政策的问题。',
                'en': 'Hello! I am BabyBloomSG AI assistant. You can ask me about baby bonus, housing applications, marriage registration, healthcare, and education policies.',
                'ms': 'Hello! Saya adalah pembantu AI BabyBloomSG. Anda boleh bertanya tentang bonus bayi, permohonan perumahan, pendaftaran perkahwinan, penjagaan kesihatan, dan dasar pendidikan.'
            },
            'chat_input_placeholder': {
                'zh': '请输入您的问题...',
                'en': 'Enter your question...',
                'ms': 'Masukkan soalan anda...'
            },
            'chat_thinking': {
                'zh': '思考中...',
                'en': 'Thinking...',
                'ms': 'Berfikir...'
            },
            'chat_api_hint': {
                'zh': '配置 API密钥获得AI增强回答',
                'en': 'Configure API key for AI-enhanced answers',
                'ms': 'Konfigurasikan kunci API untuk jawapan dipertingkat AI'
            },
            
            # 政策推荐页面
            'rec_description': {
                'zh': '**🎯 根据您的情况，为您推荐适合的政策**',
                'en': '**🎯 Personalized policy recommendations based on your profile**',
                'ms': '**🎯 Cadangan dasar diperibadikan berdasarkan profil anda**'
            },
            'rec_button': {
                'zh': '🔍 生成个性化推荐',
                'en': '🔍 Generate Recommendations',
                'ms': '🔍 Jana Cadangan'
            },
            'rec_analyzing': {
                'zh': '分析您的情况...',
                'en': 'Analyzing your profile...',
                'ms': 'Menganalisis profil anda...'
            },
            'rec_success': {
                'zh': '✅ 推荐生成完成！',
                'en': '✅ Recommendations generated!',
                'ms': '✅ Cadangan dijana!'
            },
            'rec_category': {
                'zh': '类别',
                'en': 'Category',
                'ms': 'Kategori'
            },
            'rec_priority': {
                'zh': '优先级',
                'en': 'Priority',
                'ms': 'Keutamaan'
            },
            'rec_description_label': {
                'zh': '描述',
                'en': 'Description',
                'ms': 'Penerangan'
            },
            'rec_eligibility': {
                'zh': '资格',
                'en': 'Eligibility',
                'ms': 'Kelayakan'
            },
            'rec_benefits': {
                'zh': '福利',
                'en': 'Benefits',
                'ms': 'Faedah'
            },
            'rec_website': {
                'zh': '官网',
                'en': 'Official Website',
                'ms': 'Laman Web Rasmi'
            },
            
            # 津贴计算页面
            'calc_description': {
                'zh': '**📊 计算您可以获得的总津贴金额**',
                'en': '**📊 Calculate your total benefits amount**',
                'ms': '**📊 Kira jumlah faedah anda**'
            },
            'calc_fertility_title': {
                'zh': '💰 生育津贴',
                'en': '💰 Baby Bonus',
                'ms': '💰 Bonus Bayi'
            },
            'calc_housing_title': {
                'zh': '🏠 住房津贴',
                'en': '🏠 Housing Grants',
                'ms': '🏠 Geran Perumahan'
            },
            'calc_children_plan': {
                'zh': '计划生育子女数',
                'en': 'Planned Number of Children',
                'ms': 'Bilangan Anak yang Dirancang'
            },
            'calc_button_fertility': {
                'zh': '计算生育津贴',
                'en': 'Calculate Baby Bonus',
                'ms': 'Kira Bonus Bayi'
            },
            'calc_button_housing': {
                'zh': '计算住房津贴',
                'en': 'Calculate Housing Grants',
                'ms': 'Kira Geran Perumahan'
            },
            'calc_flat_type': {
                'zh': '房型',
                'en': 'Flat Type',
                'ms': 'Jenis Flat'
            },
            'calc_proximity': {
                'zh': '与父母同住或附近',
                'en': 'Living with or near parents',
                'ms': 'Tinggal dengan atau berhampiran ibu bapa'
            },
            'calc_total_fertility': {
                'zh': '总生育津贴',
                'en': 'Total Baby Bonus',
                'ms': 'Jumlah Bonus Bayi'
            },
            'calc_total_housing': {
                'zh': '总住房津贴',
                'en': 'Total Housing Grants',
                'ms': 'Jumlah Geran Perumahan'
            },
            
            # 时间线规划页面
            'timeline_description': {
                'zh': '**📅 从结婚到生娃的完整时间规划**',
                'en': '**📅 Complete timeline from marriage to baby**',
                'ms': '**📅 Garis masa lengkap dari perkahwinan hingga bayi**'
            },
            'timeline_start_date': {
                'zh': '计划开始日期',
                'en': 'Planning Start Date',
                'ms': 'Tarikh Mula Perancangan'
            },
            'timeline_milestones': {
                'zh': '选择里程碑',
                'en': 'Select Milestones',
                'ms': 'Pilih Peristiwa Penting'
            },
            'timeline_marriage': {
                'zh': '💒 结婚注册',
                'en': '💒 Marriage Registration',
                'ms': '💒 Pendaftaran Perkahwinan'
            },
            'timeline_housing': {
                'zh': '🏠 住房申请',
                'en': '🏠 Housing Application',
                'ms': '🏠 Permohonan Perumahan'
            },
            'timeline_pregnancy': {
                'zh': '🤰 怀孕计划',
                'en': '🤰 Pregnancy Planning',
                'ms': '🤰 Perancangan Kehamilan'
            },
            'timeline_baby_admin': {
                'zh': '👶 宝宝手续',
                'en': '👶 Baby Administration',
                'ms': '👶 Pentadbiran Bayi'
            },
            'timeline_generate': {
                'zh': '🎯 生成时间线',
                'en': '🎯 Generate Timeline',
                'ms': '🎯 Jana Garis Masa'
            },
            'timeline_generating': {
                'zh': '生成时间线中...',
                'en': 'Generating timeline...',
                'ms': 'Menjana garis masa...'
            },
            'timeline_reminders_title': {
                'zh': '📌 即将到来的提醒',
                'en': '📌 Upcoming Reminders',
                'ms': '📌 Peringatan Akan Datang'
            },
            'timeline_days_until': {
                'zh': '天后',
                'en': 'days',
                'ms': 'hari'
            },
            'timeline_summary_title': {
                'zh': '📋 里程碑摘要',
                'en': '📋 Milestone Summary',
                'ms': '📋 Ringkasan Peristiwa Penting'
            },
            'timeline_task_count': {
                'zh': '任务数',
                'en': 'Tasks',
                'ms': 'Tugas'
            },
            'timeline_duration': {
                'zh': '持续时间',
                'en': 'Duration',
                'ms': 'Tempoh'
            },
            'timeline_days': {
                'zh': '天',
                'en': 'days',
                'ms': 'hari'
            },
            
            # 底部说明
            'guide_title': {
                'zh': '🚀 快速开始指南',
                'en': '🚀 Quick Start Guide',
                'ms': '🚀 Panduan Mula Pantas'
            },
            'guide_step1': {
                'zh': '**选择AI模型**: 在左侧边栏选择一个模型',
                'en': '**Select AI Model**: Choose a model in the left sidebar',
                'ms': '**Pilih Model AI**: Pilih model di bar sisi kiri'
            },
            'guide_step2': {
                'zh': '**获取API密钥**:',
                'en': '**Get API Key**:',
                'ms': '**Dapatkan Kunci API**:'
            },
            'guide_step3': {
                'zh': '**填写个人信息**: 获得更精准的推荐',
                'en': '**Fill Personal Info**: Get more accurate recommendations',
                'ms': '**Isi Maklumat Peribadi**: Dapatkan cadangan yang lebih tepat'
            },
            'guide_step4': {
                'zh': '**探索功能**:',
                'en': '**Explore Features**:',
                'ms': '**Terokai Ciri-ciri**:'
            },
            'feature_chat': {
                'zh': '💬 智能问答：与AI对话获取政策解答',
                'en': '💬 Smart Q&A: Chat with AI for policy answers',
                'ms': '💬 Soal Jawab Pintar: Berbual dengan AI untuk jawapan dasar'
            },
            'feature_rec': {
                'zh': '🎯 政策推荐：获得个性化政策推荐列表',
                'en': '🎯 Policy Recommendations: Get personalized policy suggestions',
                'ms': '🎯 Cadangan Dasar: Dapatkan cadangan dasar diperibadikan'
            },
            'feature_calc': {
                'zh': '📊 津贴计算：计算可获得的总金额',
                'en': '📊 Benefits Calculator: Calculate total benefits amount',
                'ms': '📊 Kalkulator Faedah: Kira jumlah faedah'
            },
            'feature_timeline': {
                'zh': '📅 时间规划：生成从结婚到生娃的完整时间线',
                'en': '📅 Timeline Planner: Generate complete marriage-to-baby timeline',
                'ms': '📅 Perancang Garis Masa: Jana garis masa lengkap dari perkahwinan hingga bayi'
            },
            'new_features_title': {
                'zh': '✨ 新功能',
                'en': '✨ New Features',
                'ms': '✨ Ciri Baharu'
            },
            'feature_rag': {
                'zh': '✅ **RAG增强检索**: 自动检索最相关的政策信息',
                'en': '✅ **RAG Enhanced Search**: Auto-retrieve most relevant policy info',
                'ms': '✅ **Carian Dipertingkat RAG**: Auto-dapatkan maklumat dasar yang paling relevan'
            },
            'feature_rec_engine': {
                'zh': '✅ **智能推荐引擎**: 根据您的情况主动推荐政策',
                'en': '✅ **Smart Recommendation Engine**: Proactive policy suggestions based on your profile',
                'ms': '✅ **Enjin Cadangan Pintar**: Cadangan dasar proaktif berdasarkan profil anda'
            },
            'feature_calculator': {
                'zh': '✅ **津贴计算器**: 精确计算生育和住房津贴',
                'en': '✅ **Benefits Calculator**: Accurate baby bonus and housing grants calculation',
                'ms': '✅ **Kalkulator Faedah**: Pengiraan bonus bayi dan geran perumahan yang tepat'
            },
            'feature_timeline_gen': {
                'zh': '✅ **时间线生成器**: 可视化您的家庭规划路线图',
                'en': '✅ **Timeline Generator**: Visualize your family planning roadmap',
                'ms': '✅ **Penjana Garis Masa**: Visualkan peta jalan perancangan keluarga anda'
            },
            'feature_multilang': {
                'zh': '✅ **多语言支持**: 中文、英文、马来语无缝切换',
                'en': '✅ **Multi-language Support**: Seamless switching between Chinese, English, Malay',
                'ms': '✅ **Sokongan Berbilang Bahasa**: Pertukaran lancar antara Cina, Inggeris, Melayu'
            },
            'disclaimer_title': {
                'zh': '⚠️ 重要提醒',
                'en': '⚠️ Important Notice',
                'ms': '⚠️ Notis Penting'
            },
            'disclaimer_text': {
                'zh': '所有政策信息仅供参考，请以新加坡政府官方最新公告为准。',
                'en': 'All policy information is for reference only. Please refer to official Singapore government announcements.',
                'ms': 'Semua maklumat dasar adalah untuk rujukan sahaja. Sila rujuk pengumuman rasmi kerajaan Singapura.'
            },
            
            # 错误和警告消息
            'error_no_api_key': {
                'zh': '请先配置API密钥',
                'en': 'Please configure API key first',
                'ms': 'Sila konfigurasikan kunci API dahulu'
            },
            'error_engine_not_loaded': {
                'zh': '引擎未加载',
                'en': 'Engine not loaded',
                'ms': 'Enjin tidak dimuatkan'
            },
            'warning_rag_not_loaded': {
                'zh': '⚠️ RAG系统未加载，部分功能受限',
                'en': '⚠️ RAG system not loaded, some features limited',
                'ms': '⚠️ Sistem RAG tidak dimuatkan, beberapa ciri terhad'
            },
            'warning_rec_not_loaded': {
                'zh': '⚠️ 推荐引擎未加载，部分功能受限',
                'en': '⚠️ Recommendation engine not loaded, some features limited',
                'ms': '⚠️ Enjin cadangan tidak dimuatkan, beberapa ciri terhad'
            },
            
            # 政策类别翻译
            'policy_fertility': {
                'zh': '生育津贴',
                'en': 'Baby Bonus',
                'ms': 'Bonus Bayi'
            },
            'policy_housing': {
                'zh': '住房政策',
                'en': 'Housing Policy',
                'ms': 'Dasar Perumahan'
            },
            'policy_marriage': {
                'zh': '结婚注册',
                'en': 'Marriage Registration',
                'ms': 'Pendaftaran Perkahwinan'
            },
            'policy_healthcare': {
                'zh': '医疗保健',
                'en': 'Healthcare',
                'ms': 'Penjagaan Kesihatan'
            },
            'policy_education': {
                'zh': '教育政策',
                'en': 'Education Policy',
                'ms': 'Dasar Pendidikan'
            }
        }
    
    def get(self, key: str, language: str = 'zh') -> str:
        """
        获取翻译文本
        
        Args:
            key: 翻译键
            language: 语言代码 ('zh', 'en', 'ms')
            
        Returns:
            翻译后的文本
        """
        if key not in self.translations:
            return key
        
        return self.translations[key].get(language, self.translations[key].get('zh', key))
    
    def get_language_name(self, code: str) -> str:
        """获取语言名称"""
        names = {
            'zh': '中文',
            'en': 'English',
            'ms': 'Bahasa Melayu'
        }
        return names.get(code, code)
    
    def get_available_languages(self) -> list:
        """获取可用语言列表"""
        return [
            {'code': 'zh', 'name': '中文', 'flag': '🇨🇳'},
            {'code': 'en', 'name': 'English', 'flag': '🇬🇧'},
            {'code': 'ms', 'name': 'Bahasa Melayu', 'flag': '🇲🇾'}
        ]
    
    def translate_policy_response(self, response: str, from_lang: str, to_lang: str) -> str:
        """
        翻译政策回答（简单的关键词替换）
        更完整的实现需要集成翻译API
        
        Args:
            response: 原始回答
            from_lang: 源语言
            to_lang: 目标语言
            
        Returns:
            翻译后的回答
        """
        if from_lang == to_lang:
            return response
        
        # 简单的关键词替换映射
        keyword_map = {
            ('zh', 'en'): {
                '生育津贴': 'Baby Bonus',
                '现金奖励': 'Cash Gift',
                '产假': 'Maternity Leave',
                '陪产假': 'Paternity Leave',
                '住房津贴': 'Housing Grant',
                '申请条件': 'Eligibility',
                '官方网站': 'Official Website',
                '公民身份': 'Citizenship',
                '新加坡公民': 'Singapore Citizen'
            },
            ('zh', 'ms'): {
                '生育津贴': 'Bonus Bayi',
                '现金奖励': 'Hadiah Tunai',
                '产假': 'Cuti Bersalin',
                '陪产假': 'Cuti Paterniti',
                '住房津贴': 'Geran Perumahan',
                '申请条件': 'Kelayakan',
                '官方网站': 'Laman Web Rasmi',
                '公民身份': 'Kewarganegaraan',
                '新加坡公民': 'Warganegara Singapura'
            }
        }
        
        # 执行关键词替换
        translated = response
        if (from_lang, to_lang) in keyword_map:
            for original, translation in keyword_map[(from_lang, to_lang)].items():
                translated = translated.replace(original, translation)
        
        return translated