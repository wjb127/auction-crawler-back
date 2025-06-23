import re
from typing import List, Optional


def format_currency(amount: int) -> str:
    """숫자를 통화 형태로 포맷"""
    if amount is None:
        return "미정"
    return f"{amount:,}원"


def clean_text(text: str) -> str:
    """텍스트 정리"""
    if not text:
        return ""
    # 여러 공백을 하나로, 줄바꿈 제거
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()


def extract_keywords(text: str) -> List[str]:
    """텍스트에서 키워드 추출"""
    if not text:
        return []
    
    keywords = []
    text_lower = text.lower()
    
    # 지역 키워드
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
    districts = [
        '강남구', '강서구', '송파구', '서초구', '강동구', '마포구', 
        '용산구', '중구', '종로구', '성동구', '동작구', '관악구',
        '영등포구', '금천구', '구로구', '양천구', '노원구', '도봉구',
        '강북구', '성북구', '중랑구', '동대문구', '광진구', '서대문구',
        '은평구'
    ]
    
    # 물건 유형 키워드
    property_types = [
        '아파트', '오피스텔', '상가', '주택', '빌라', '연립주택', 
        '단독주택', '토지', '건물', '사무실', '점포', '공장',
        '창고', '펜션', '리조트'
    ]
    
    # 모든 키워드 리스트 통합
    all_keywords = regions + districts + property_types
    
    for keyword in all_keywords:
        if keyword in text:
            keywords.append(keyword)
    
    return list(set(keywords))  # 중복 제거


def extract_numbers(text: str) -> Optional[int]:
    """텍스트에서 숫자 추출"""
    if not text:
        return None
    
    # 콤마 제거 후 숫자만 추출
    numbers = re.findall(r'\d+', text.replace(',', ''))
    if numbers:
        return int(''.join(numbers))
    return None


def is_valid_url(url: str) -> bool:
    """URL 유효성 검사"""
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


def truncate_text(text: str, max_length: int = 100) -> str:
    """텍스트 길이 제한"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..." 