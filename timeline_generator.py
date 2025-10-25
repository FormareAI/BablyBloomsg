"""
个性化时间线生成器
生成从结婚到生娃的完整规划时间轴
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd


class TimelineGenerator:
    """生成个性化家庭规划时间线"""
    
    def __init__(self):
        self.milestones = {
            'marriage': {
                'duration': 0,
                'tasks': [
                    {'name': 'Submit Notice of Marriage', 'days_before': 21, 'duration': 1},
                    {'name': 'Pay Fees', 'days_before': 20, 'duration': 1},
                    {'name': 'Book ROM Appointment', 'days_before': 15, 'duration': 1},
                    {'name': 'Marriage Solemnization', 'days_before': 0, 'duration': 1}
                ]
            },
            'housing': {
                'duration': 180,  # ~6 months for BTO application
                'tasks': [
                    {'name': 'HDB BTO Application', 'days_before': 180, 'duration': 7},
                    {'name': 'Ballot Results', 'days_before': 150, 'duration': 1},
                    {'name': 'Book Flat', 'days_before': 140, 'duration': 30},
                    {'name': 'Apply Housing Grants', 'days_before': 100, 'duration': 14},
                    {'name': 'Sign Agreement', 'days_before': 80, 'duration': 1},
                    {'name': 'Wait for Completion', 'days_before': 0, 'duration': 1095}  # ~3 years
                ]
            },
            'pregnancy': {
                'duration': 280,  # 40 weeks
                'tasks': [
                    {'name': 'Pre-pregnancy Health Check', 'days_before': 90, 'duration': 1},
                    {'name': 'Conception', 'days_before': 0, 'duration': 1},
                    {'name': 'First Trimester Checkup', 'days_before': -30, 'duration': 1},
                    {'name': 'Second Trimester Scan', 'days_before': -120, 'duration': 1},
                    {'name': 'Third Trimester Prep', 'days_before': -210, 'duration': 1},
                    {'name': 'Apply Maternity Leave', 'days_before': -240, 'duration': 7},
                    {'name': 'Baby Due Date', 'days_before': -280, 'duration': 1}
                ]
            },
            'baby_admin': {
                'duration': 180,
                'tasks': [
                    {'name': 'Birth Registration (14 days)', 'days_before': 0, 'duration': 14},
                    {'name': 'Apply Baby Bonus (18 months)', 'days_before': 7, 'duration': 7},
                    {'name': 'Open CDA Account', 'days_before': 14, 'duration': 7},
                    {'name': 'First Vaccination', 'days_before': 30, 'duration': 1},
                    {'name': 'Apply Childcare Subsidy', 'days_before': 90, 'duration': 14}
                ]
            }
        }
    
    def generate_timeline(self, start_date: datetime, milestones: List[str], 
                         language: str = 'zh') -> Dict[str, Any]:
        """
        生成时间线
        
        Args:
            start_date: 起始日期
            milestones: 要包含的里程碑列表 ['marriage', 'housing', 'pregnancy', 'baby_admin']
            language: 语言代码
            
        Returns:
            包含时间线数据和图表的字典
        """
        events = []
        current_date = start_date
        
        for milestone in milestones:
            if milestone not in self.milestones:
                continue
                
            milestone_data = self.milestones[milestone]
            
            for task in milestone_data['tasks']:
                event_date = current_date + timedelta(days=task['days_before'])
                end_date = event_date + timedelta(days=task['duration'])
                
                events.append({
                    'Task': self._translate_task(task['name'], language),
                    'Start': event_date,
                    'End': end_date,
                    'Category': self._translate_category(milestone, language),
                    'Duration': task['duration'],
                    'Description': self._get_task_description(task['name'], language)
                })
            
            # 更新当前日期为下一个里程碑的起点
            if milestone == 'marriage':
                current_date = current_date + timedelta(days=30)  # 婚后1个月开始下一步
            elif milestone == 'housing':
                pass  # 可以与其他里程碑并行
            elif milestone == 'pregnancy':
                current_date = events[-1]['End']  # 从怀孕结束后开始
        
        df = pd.DataFrame(events)
        
        return {
            'dataframe': df,
            'events': events,
            'start_date': start_date,
            'end_date': max([e['End'] for e in events]) if events else start_date
        }
    
    def create_gantt_chart(self, timeline_data: Dict, language: str = 'zh') -> go.Figure:
        """创建甘特图"""
        df = timeline_data['dataframe']
        
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data to display", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # 创建颜色映射
        color_map = {
            self._translate_category('marriage', language): '#FF69B4',
            self._translate_category('housing', language): '#4169E1',
            self._translate_category('pregnancy', language): '#32CD32',
            self._translate_category('baby_admin', language): '#FFD700'
        }
        
        fig = px.timeline(df, x_start="Start", x_end="End", y="Task", 
                         color="Category", 
                         color_discrete_map=color_map,
                         hover_data=["Description", "Duration"])
        
        fig.update_yaxes(categoryorder="total ascending")
        
        titles = {
            'zh': '🗓️ 您的家庭规划时间线',
            'en': '🗓️ Your Family Planning Timeline',
            'ms': '🗓️ Garis Masa Perancangan Keluarga Anda'
        }
        
        fig.update_layout(
            title=titles.get(language, titles['zh']),
            xaxis_title=self._translate('Date', language),
            yaxis_title=self._translate('Milestone', language),
            height=600,
            showlegend=True,
            hovermode='closest'
        )
        
        return fig
    
    def create_milestone_summary(self, timeline_data: Dict, language: str = 'zh') -> List[Dict]:
        """创建里程碑摘要"""
        df = timeline_data['dataframe']
        
        summary = []
        for category in df['Category'].unique():
            category_df = df[df['Category'] == category]
            
            summary.append({
                'category': category,
                'start': category_df['Start'].min(),
                'end': category_df['End'].max(),
                'task_count': len(category_df),
                'total_days': (category_df['End'].max() - category_df['Start'].min()).days
            })
        
        return sorted(summary, key=lambda x: x['start'])
    
    def get_upcoming_reminders(self, timeline_data: Dict, days_ahead: int = 30,
                              language: str = 'zh') -> List[Dict]:
        """获取即将到来的提醒"""
        today = datetime.now()
        upcoming = []
        
        for event in timeline_data['events']:
            days_until = (event['Start'] - today).days
            
            if 0 <= days_until <= days_ahead:
                urgency = '🔴' if days_until <= 7 else '🟡' if days_until <= 14 else '🟢'
                
                upcoming.append({
                    'task': event['Task'],
                    'date': event['Start'],
                    'days_until': days_until,
                    'urgency': urgency,
                    'category': event['Category'],
                    'description': event['Description']
                })
        
        return sorted(upcoming, key=lambda x: x['days_until'])
    
    def _translate_task(self, task: str, language: str) -> str:
        """翻译任务名称"""
        translations = {
            'Submit Notice of Marriage': {
                'zh': '提交结婚通知',
                'en': 'Submit Notice of Marriage',
                'ms': 'Hantar Notis Perkahwinan'
            },
            'Pay Fees': {
                'zh': '支付费用',
                'en': 'Pay Fees',
                'ms': 'Bayar Yuran'
            },
            'Book ROM Appointment': {
                'zh': '预约注册日期',
                'en': 'Book ROM Appointment',
                'ms': 'Tempah Temu Janji ROM'
            },
            'Marriage Solemnization': {
                'zh': '结婚仪式',
                'en': 'Marriage Solemnization',
                'ms': 'Majlis Perkahwinan'
            },
            'HDB BTO Application': {
                'zh': 'HDB BTO申请',
                'en': 'HDB BTO Application',
                'ms': 'Permohonan HDB BTO'
            },
            'Ballot Results': {
                'zh': '抽签结果',
                'en': 'Ballot Results',
                'ms': 'Keputusan Undian'
            },
            'Book Flat': {
                'zh': '选房',
                'en': 'Book Flat',
                'ms': 'Tempah Flat'
            },
            'Apply Housing Grants': {
                'zh': '申请住房津贴',
                'en': 'Apply Housing Grants',
                'ms': 'Mohon Geran Perumahan'
            },
            'Sign Agreement': {
                'zh': '签署协议',
                'en': 'Sign Agreement',
                'ms': 'Tandatangan Perjanjian'
            },
            'Wait for Completion': {
                'zh': '等待建成',
                'en': 'Wait for Completion',
                'ms': 'Tunggu Siap'
            },
            'Pre-pregnancy Health Check': {
                'zh': '孕前健康检查',
                'en': 'Pre-pregnancy Health Check',
                'ms': 'Pemeriksaan Kesihatan Pra-Kehamilan'
            },
            'Conception': {
                'zh': '受孕',
                'en': 'Conception',
                'ms': 'Pembuahan'
            },
            'First Trimester Checkup': {
                'zh': '第一孕期检查',
                'en': 'First Trimester Checkup',
                'ms': 'Pemeriksaan Trimester Pertama'
            },
            'Second Trimester Scan': {
                'zh': '第二孕期扫描',
                'en': 'Second Trimester Scan',
                'ms': 'Imbasan Trimester Kedua'
            },
            'Third Trimester Prep': {
                'zh': '第三孕期准备',
                'en': 'Third Trimester Prep',
                'ms': 'Persediaan Trimester Ketiga'
            },
            'Apply Maternity Leave': {
                'zh': '申请产假',
                'en': 'Apply Maternity Leave',
                'ms': 'Mohon Cuti Bersalin'
            },
            'Baby Due Date': {
                'zh': '预产期',
                'en': 'Baby Due Date',
                'ms': 'Tarikh Jangka Lahir'
            },
            'Birth Registration (14 days)': {
                'zh': '出生登记(14天内)',
                'en': 'Birth Registration (14 days)',
                'ms': 'Pendaftaran Kelahiran (14 hari)'
            },
            'Apply Baby Bonus (18 months)': {
                'zh': '申请婴儿津贴(18个月内)',
                'en': 'Apply Baby Bonus (18 months)',
                'ms': 'Mohon Bonus Bayi (18 bulan)'
            },
            'Open CDA Account': {
                'zh': '开设CDA账户',
                'en': 'Open CDA Account',
                'ms': 'Buka Akaun CDA'
            },
            'First Vaccination': {
                'zh': '首次疫苗接种',
                'en': 'First Vaccination',
                'ms': 'Vaksinasi Pertama'
            },
            'Apply Childcare Subsidy': {
                'zh': '申请托儿补贴',
                'en': 'Apply Childcare Subsidy',
                'ms': 'Mohon Subsidi Jagaan Kanak-kanak'
            }
        }
        
        return translations.get(task, {}).get(language, task)
    
    def _translate_category(self, category: str, language: str) -> str:
        """翻译类别"""
        translations = {
            'marriage': {'zh': '💒 结婚', 'en': '💒 Marriage', 'ms': '💒 Perkahwinan'},
            'housing': {'zh': '🏠 住房', 'en': '🏠 Housing', 'ms': '🏠 Perumahan'},
            'pregnancy': {'zh': '🤰 怀孕', 'en': '🤰 Pregnancy', 'ms': '🤰 Kehamilan'},
            'baby_admin': {'zh': '👶 宝宝手续', 'en': '👶 Baby Admin', 'ms': '👶 Pentadbiran Bayi'}
        }
        
        return translations.get(category, {}).get(language, category)
    
    def _translate(self, text: str, language: str) -> str:
        """通用翻译"""
        translations = {
            'Date': {'zh': '日期', 'en': 'Date', 'ms': 'Tarikh'},
            'Milestone': {'zh': '里程碑', 'en': 'Milestone', 'ms': 'Peristiwa Penting'}
        }
        
        return translations.get(text, {}).get(language, text)
    
    def _get_task_description(self, task: str, language: str) -> str:
        """获取任务描述"""
        descriptions = {
            'Submit Notice of Marriage': {
                'zh': '在线提交结婚通知，需提前21天',
                'en': 'Submit marriage notice online, 21 days in advance',
                'ms': 'Hantar notis perkahwinan dalam talian, 21 hari lebih awal'
            },
            'HDB BTO Application': {
                'zh': '申请建屋发展局预购组屋',
                'en': 'Apply for HDB Build-To-Order flat',
                'ms': 'Mohon flat HDB Build-To-Order'
            },
            'Baby Due Date': {
                'zh': '宝宝预计出生日期',
                'en': 'Expected baby delivery date',
                'ms': 'Tarikh jangka kelahiran bayi'
            }
        }
        
        return descriptions.get(task, {}).get(language, '')