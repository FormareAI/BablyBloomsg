"""
智能推荐引擎 - 根据用户画像推荐适合的政策
"""
from typing import Dict, List, Any


class RecommendationEngine:
    """智能推荐引擎"""
    
    def __init__(self, policy_kb: Dict[str, Any]):
        """
        初始化推荐引擎
        
        Args:
            policy_kb: 政策知识库字典
        """
        self.policy_kb = policy_kb
    
    def get_recommendations(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根据用户画像生成个性化推荐
        
        Args:
            user_profile: 用户信息
                - citizenship: 公民身份
                - marital_status: 婚姻状态
                - income: 月收入
                - children: 子女数
                - age: 年龄
        
        Returns:
            推荐列表，按优先级排序
        """
        recommendations = []
        
        citizenship = user_profile.get('citizenship', '外国人')
        marital_status = user_profile.get('marital_status', '未婚')
        income = user_profile.get('income', 0)
        children = user_profile.get('children', 0)
        age = user_profile.get('age', 30)
        
        is_citizen = (citizenship == "新加坡公民")
        is_pr = (citizenship == "PR")
        is_married = (marital_status == "已婚")
        
        # 1. 结婚注册推荐
        if not is_married and age >= 21:
            recommendations.append({
                'title': '结婚注册',
                'category': 'marriage',
                'priority': 5,
                'description': '在新加坡注册结婚，开启美好家庭生活',
                'eligibility': '年满21岁',
                'benefits': f"费用仅需S$26-42，流程简单快捷",
                'website': self.policy_kb['marriage']['website']
            })
        
        # 2. 生育津贴推荐
        if is_citizen and (is_married or children > 0):
            next_child = children + 1
            cash = self._get_baby_bonus_cash(next_child)
            cda = self._get_cda_matching(next_child)
            
            recommendations.append({
                'title': f'生育津贴计划（第{next_child}胎）',
                'category': 'fertility',
                'priority': 5 if children == 0 else 4,
                'description': '政府提供现金奖励和CDA配对，减轻育儿负担',
                'eligibility': '孩子必须是新加坡公民',
                'benefits': f"现金奖励S${cash:,} + CDA配对S${cda:,} + Medisave补助S$4,000",
                'website': self.policy_kb['fertility']['website']
            })
        
        # 3. 产假/陪产假推荐
        if is_citizen and is_married and children < 10:
            recommendations.append({
                'title': '产假与陪产假',
                'category': 'fertility',
                'priority': 4,
                'description': '享受政府支付的带薪假期',
                'eligibility': '在职员工',
                'benefits': '产假16周 + 陪产假2周（政府支付）',
                'website': self.policy_kb['fertility']['website']
            })
        
        # 4. 住房津贴推荐
        if (is_citizen or is_pr) and age >= 21:
            if income <= 14000:
                max_grants = self._calculate_max_housing_grants(income, is_citizen)
                
                recommendations.append({
                    'title': 'HDB住房津贴',
                    'category': 'housing',
                    'priority': 5 if is_married else 3,
                    'description': '申请BTO组屋，享受高额购房津贴',
                    'eligibility': f"家庭月收入≤S$14,000（您的收入S${income:,}符合条件✅）",
                    'benefits': f"最高可获津贴S${max_grants:,}",
                    'website': self.policy_kb['housing']['website']
                })
            elif income > 14000:
                recommendations.append({
                    'title': 'HDB组屋购买',
                    'category': 'housing',
                    'priority': 3,
                    'description': '虽超过津贴收入上限，仍可申请BTO',
                    'eligibility': f"您的收入S${income:,}超过津贴上限S$14,000",
                    'benefits': '可申请组屋，但无法享受津贴',
                    'website': self.policy_kb['housing']['website']
                })
        
        # 5. 幼儿托管补贴
        if is_citizen and children > 0 and income <= 12000:
            childcare_subsidy = self.policy_kb['education']['kindergarten']['subsidy']['max_subsidy']
            
            recommendations.append({
                'title': '幼儿托管补贴',
                'category': 'education',
                'priority': 4,
                'description': '政府补贴幼儿托管费用',
                'eligibility': f"家庭月收入≤S$12,000（您符合✅）",
                'benefits': f"最高补贴S${childcare_subsidy}/月",
                'website': self.policy_kb['education']['website']
            })
        
        # 6. 孕产医疗支持
        if is_citizen and is_married and children < 10:
            recommendations.append({
                'title': '孕产医疗支持',
                'category': 'healthcare',
                'priority': 4,
                'description': '产检和分娩享受政府补贴和Medisave支付',
                'eligibility': '新加坡公民',
                'benefits': '公立医院分娩S$700-1,500，可使用Medisave',
                'website': self.policy_kb['healthcare']['website']
            })
        
        # 7. 儿童疫苗接种
        if is_citizen and children > 0:
            recommendations.append({
                'title': '儿童疫苗接种',
                'category': 'healthcare',
                'priority': 3,
                'description': '在公立诊所免费为儿童接种疫苗',
                'eligibility': '新加坡公民儿童',
                'benefits': '免费疫苗接种',
                'website': self.policy_kb['healthcare']['website']
            })
        
        # 按优先级排序
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations
    
    def _get_baby_bonus_cash(self, child_order: int) -> int:
        """获取生育现金奖励"""
        cash_gifts = self.policy_kb['fertility']['baby_bonus']['cash_gifts']
        
        if child_order == 1:
            return cash_gifts['1st_child']
        elif child_order == 2:
            return cash_gifts['2nd_child']
        elif child_order == 3:
            return cash_gifts['3rd_child']
        elif child_order == 4:
            return cash_gifts['4th_child']
        else:
            return cash_gifts['5th_and_above']
    
    def _get_cda_matching(self, child_order: int) -> int:
        """获取CDA配对金额"""
        cda = self.policy_kb['fertility']['baby_bonus']['cda_matching']
        
        if child_order <= 2:
            return cda['1st_2nd']
        else:
            return cda['3rd_to_6th']
    
    def _calculate_max_housing_grants(self, income: int, is_citizen: bool) -> int:
        """计算最大住房津贴"""
        if not is_citizen:
            return 0
        
        grants = self.policy_kb['housing']['grants']
        total = 0
        
        # Enhanced Housing Grant
        if income <= 9000:
            total += grants['enhanced_housing_grant']['max_amount']
        
        # Family Grant
        if income <= 14000:
            total += grants['family_grant']['max_amount']
        
        # Proximity Housing Grant (假设符合条件)
        total += grants['proximity_housing_grant']['max_amount']
        
        return total
    
    def calculate_fertility_benefits(self, current_children: int, planned_children: int, 
                                     is_citizen: bool) -> int:
        """
        计算生育津贴总额
        
        Args:
            current_children: 现有子女数
            planned_children: 计划生育数
            is_citizen: 是否公民
            
        Returns:
            总津贴金额
        """
        if not is_citizen:
            return 0
        
        total = 0
        
        for i in range(current_children + 1, current_children + planned_children + 1):
            # 现金奖励
            total += self._get_baby_bonus_cash(i)
            # CDA配对
            total += self._get_cda_matching(i)
            # Medisave补助
            total += self.policy_kb['fertility']['medisave_grant']
        
        return total
    
    def calculate_housing_grants(self, income: int, is_citizen: bool, 
                                 first_timer: bool = True, proximity: bool = False) -> int:
        """
        计算住房津贴总额
        
        Args:
            income: 家庭月收入
            is_citizen: 是否公民
            first_timer: 是否首次购房
            proximity: 是否与父母同住/附近
            
        Returns:
            总津贴金额
        """
        if not is_citizen or not first_timer:
            return 0
        
        grants = self.policy_kb['housing']['grants']
        total = 0
        
        # Enhanced Housing Grant
        if income <= grants['enhanced_housing_grant']['income_ceiling']:
            total += grants['enhanced_housing_grant']['max_amount']
        
        # Family Grant
        if income <= grants['family_grant']['income_ceiling']:
            total += grants['family_grant']['max_amount']
        
        # Proximity Housing Grant
        if proximity:
            total += grants['proximity_housing_grant']['max_amount']
        
        return total


# 测试代码
if __name__ == "__main__":
    # 简单的测试知识库
    test_kb = {
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
            'medisave_grant': 4000,
            'website': 'https://www.babybonus.msf.gov.sg'
        },
        'housing': {
            'grants': {
                'enhanced_housing_grant': {'max_amount': 80000, 'income_ceiling': 9000},
                'family_grant': {'max_amount': 50000, 'income_ceiling': 14000},
                'proximity_housing_grant': {'max_amount': 30000}
            },
            'website': 'https://www.hdb.gov.sg'
        },
        'marriage': {
            'website': 'https://www.rom.gov.sg'
        },
        'healthcare': {
            'website': 'https://www.healthhub.sg'
        },
        'education': {
            'kindergarten': {
                'subsidy': {'max_subsidy': 467, 'income_ceiling': 12000}
            },
            'website': 'https://www.moe.gov.sg'
        }
    }
    
    print("初始化推荐引擎...")
    engine = RecommendationEngine(test_kb)
    
    print("\n测试推荐...")
    user_profile = {
        'citizenship': '新加坡公民',
        'marital_status': '已婚',
        'income': 8000,
        'children': 1,
        'age': 30
    }
    
    recommendations = engine.get_recommendations(user_profile)
    
    print(f"\n用户画像: {user_profile}")
    print(f"\n获得 {len(recommendations)} 条推荐:\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} (优先级: {rec['priority']})")
        print(f"   {rec['description']}")
        print(f"   福利: {rec['benefits']}\n")