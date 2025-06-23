from typing import List, Dict
from datetime import datetime, date
import re
from .base import BaseCrawler


class CourtAuctionCrawler(BaseCrawler):
    """대법원 경매정보 크롤러"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://www.courtauction.go.kr"
        self.search_url = f"{self.base_url}/RetrieveRealEstateDetailList.laf"
    
    async def crawl_items(self, pages: int = 3) -> List[Dict]:
        """대법원 경매정보 크롤링"""
        items = []
        
        try:
            for page in range(1, pages + 1):
                print(f"📄 페이지 {page} 크롤링 중...")
                
                # 검색 파라미터 설정
                params = {
                    'pageIndex': page,
                    'pageSize': 20,
                    'realEstateUsage': '',  # 용도 (빈값 = 전체)
                    'roadNameAddress': '',  # 도로명주소
                    'appraisalValueMin': '',  # 최소 감정가
                    'appraisalValueMax': '',  # 최대 감정가
                }
                
                soup = self.get_page(self.search_url, params)
                if not soup:
                    continue
                
                # 경매 물건 목록 추출
                item_rows = soup.find_all('tr', {'class': ['Ltbllist', 'Ltbllist2']})
                
                for row in item_rows:
                    try:
                        item_data = self._extract_item_data(row)
                        if item_data:
                            items.append(item_data)
                    except Exception as e:
                        print(f"❌ 물건 데이터 추출 실패: {e}")
                        continue
                
                print(f"✅ 페이지 {page}: {len(item_rows)}개 물건 처리")
                
        except Exception as e:
            print(f"❌ 크롤링 실패: {e}")
        
        print(f"🎯 총 {len(items)}개 물건 크롤링 완료")
        return items
    
    def _extract_item_data(self, row) -> Dict:
        """테이블 행에서 물건 데이터 추출"""
        try:
            cells = row.find_all('td')
            if len(cells) < 8:
                return None
            
            # 물건 상세 링크 추출
            detail_link = cells[2].find('a')
            if not detail_link:
                return None
            
            href = detail_link.get('href', '')
            detail_url = f"{self.base_url}/{href}" if href else ""
            
            # 물건명/주소
            title = self.clean_text(detail_link.get_text())
            
            # 감정가 추출
            appraisal_text = self.clean_text(cells[4].get_text())
            appraisal_value = self.extract_number(appraisal_text)
            
            # 입찰일 추출
            bid_date_text = self.clean_text(cells[6].get_text())
            bid_date = self._parse_date(bid_date_text)
            
            # 키워드 추출 (제목에서)
            keywords = self._extract_keywords(title)
            
            return {
                'title': title,
                'appraisal_value': appraisal_value,
                'bid_date': bid_date,
                'url': detail_url,
                'keywords': keywords,
                'source_site': '대법원 경매정보'
            }
            
        except Exception as e:
            print(f"❌ 데이터 추출 오류: {e}")
            return None
    
    def _parse_date(self, date_text: str) -> date:
        """날짜 텍스트를 date 객체로 변환"""
        try:
            # "2024.02.15" 형태로 가정
            date_match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', date_text)
            if date_match:
                year, month, day = map(int, date_match.groups())
                return date(year, month, day)
        except Exception:
            pass
        return None
    
    def _extract_keywords(self, title: str) -> List[str]:
        """제목에서 키워드 추출"""
        keywords = []
        
        # 지역 키워드
        regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
        districts = ['강남구', '강서구', '송파구', '서초구', '강동구', '마포구', 
                    '용산구', '중구', '종로구', '성동구', '동작구', '관악구']
        
        # 물건 유형 키워드
        property_types = ['아파트', '오피스텔', '상가', '주택', '빌라', '연립주택', 
                         '단독주택', '토지', '건물', '사무실']
        
        for keyword_list in [regions, districts, property_types]:
            for keyword in keyword_list:
                if keyword in title:
                    keywords.append(keyword)
        
        return list(set(keywords))  # 중복 제거 