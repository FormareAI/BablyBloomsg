"""
RAG检索系统 - 使用FAISS向量数据库进行语义检索
"""
import json
import numpy as np
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("⚠️ 请安装依赖: pip install sentence-transformers faiss-cpu")


class RAGSystem:
    """RAG检索系统"""
    
    def __init__(self, policy_kb: Dict[str, Any]):
        """
        初始化RAG系统
        
        Args:
            policy_kb: 政策知识库字典
        """
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("缺少必要的依赖库")
        
        self.policy_kb = policy_kb
        self.documents = []
        self.index = None
        
        # 使用轻量级的多语言模型
        print("正在加载embedding模型...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ Embedding模型加载完成")
    
    def _extract_documents(self) -> List[Dict[str, str]]:
        """
        从知识库中提取文档
        
        Returns:
            文档列表，每个文档包含text和metadata
        """
        docs = []
        
        for category, content in self.policy_kb.items():
            # 为每个政策类别创建文档
            if isinstance(content, dict):
                # 主文档
                main_text = f"类别: {category}\n"
                if 'description' in content:
                    main_text += f"描述: {content['description']}\n"
                if 'website' in content:
                    main_text += f"官网: {content['website']}\n"
                
                docs.append({
                    'text': main_text,
                    'metadata': {
                        'category': category,
                        'type': 'overview'
                    }
                })
                
                # 详细子项
                for key, value in content.items():
                    if key not in ['description', 'website'] and isinstance(value, (dict, list, str, int, float)):
                        sub_text = f"类别: {category} - {key}\n内容: {json.dumps(value, ensure_ascii=False, indent=2)}"
                        docs.append({
                            'text': sub_text,
                            'metadata': {
                                'category': category,
                                'type': 'detail',
                                'key': key
                            }
                        })
        
        return docs
    
    def build_index(self):
        """构建FAISS向量索引"""
        print("正在构建向量索引...")
        
        # 提取文档
        self.documents = self._extract_documents()
        
        if not self.documents:
            print("⚠️ 没有可索引的文档")
            return
        
        # 生成embeddings
        texts = [doc['text'] for doc in self.documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # 转换为numpy数组
        embeddings = np.array(embeddings).astype('float32')
        
        # 创建FAISS索引
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        print(f"✅ 向量索引构建完成，共 {len(self.documents)} 个文档")
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        语义检索
        
        Args:
            query: 查询文本
            top_k: 返回前k个最相关文档
            
        Returns:
            最相关的文档文本列表
        """
        if self.index is None:
            print("⚠️ 索引未构建，请先调用build_index()")
            return []
        
        # 查询向量化
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        # 搜索
        distances, indices = self.index.search(query_embedding, top_k)
        
        # 返回结果
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx]['text'])
        
        return results
    
    def search_with_metadata(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        语义检索（包含元数据）
        
        Args:
            query: 查询文本
            top_k: 返回前k个最相关文档
            
        Returns:
            包含文本、元数据和相似度分数的字典列表
        """
        if self.index is None:
            return []
        
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append({
                    'text': self.documents[idx]['text'],
                    'metadata': self.documents[idx]['metadata'],
                    'score': float(distance)  # L2距离，越小越相似
                })
        
        return results
    
    def get_category_documents(self, category: str) -> List[str]:
        """
        获取特定类别的所有文档
        
        Args:
            category: 政策类别（如'fertility', 'housing'等）
            
        Returns:
            该类别的所有文档文本
        """
        results = []
        for doc in self.documents:
            if doc['metadata'].get('category') == category:
                results.append(doc['text'])
        return results


# 测试代码
if __name__ == "__main__":
    # 简单的测试知识库
    test_kb = {
        'fertility': {
            'description': '生育津贴计划帮助家庭',
            'cash_gifts': {'1st_child': 8000, '2nd_child': 8000},
            'website': 'https://www.babybonus.msf.gov.sg'
        },
        'housing': {
            'description': 'HDB组屋政策',
            'grants': {'enhanced_housing_grant': {'max_amount': 80000}},
            'website': 'https://www.hdb.gov.sg'
        }
    }
    
    print("初始化RAG系统...")
    rag = RAGSystem(test_kb)
    
    print("\n构建索引...")
    rag.build_index()
    
    print("\n测试检索...")
    query = "生育津贴多少钱？"
    results = rag.search(query, top_k=2)
    
    print(f"\n查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result[:100]}...")