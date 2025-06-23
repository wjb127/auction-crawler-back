from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import random
from app.config import settings


class BaseCrawler(ABC):
    """크롤러 베이스 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.user_agent
        })
        
    @abstractmethod
    async def crawl_items(self) -> List[Dict]:
        """경매 물건 크롤링 (하위 클래스에서 구현)"""
        pass
    
    def get_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """웹페이지 요청 및 파싱"""
        try:
            # 요청 간격 조절 (1-3초 랜덤)
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # 인코딩 설정
            response.encoding = response.apparent_encoding
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.RequestException as e:
            print(f"❌ 페이지 요청 실패: {url}, 오류: {e}")
            return None
    
    def extract_number(self, text: str) -> Optional[int]:
        """텍스트에서 숫자만 추출"""
        import re
        numbers = re.findall(r'\d+', text.replace(',', ''))
        if numbers:
            return int(''.join(numbers))
        return None
    
    def clean_text(self, text: str) -> str:
        """텍스트 정리"""
        if not text:
            return ""
        return text.strip().replace('\n', ' ').replace('\t', ' ')
    
    def close(self):
        """세션 종료"""
        self.session.close() 