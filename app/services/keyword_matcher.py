from typing import List, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import keyword_crud, detected_item_crud, alert_crud
from app.schemas.detected_item import DetectedItemCreate
from app.schemas.alert import AlertCreate


class KeywordMatcher:
    """키워드 매칭 서비스"""
    
    def __init__(self):
        pass
    
    async def process_crawled_items(self, db: AsyncSession, crawled_items: List[Dict]) -> Dict:
        """크롤링된 물건들을 처리하고 키워드 매칭 수행"""
        results = {
            'total_items': len(crawled_items),
            'new_items': 0,
            'duplicate_items': 0,
            'matched_items': 0,
            'alerts_sent': 0
        }
        
        for item_data in crawled_items:
            try:
                # 중복 체크
                existing_item = await detected_item_crud.get_by_url(db, item_data['url'])
                if existing_item:
                    results['duplicate_items'] += 1
                    continue
                
                # 새 물건 저장
                item_create = DetectedItemCreate(**item_data)
                new_item = await detected_item_crud.create(db, item_create)
                results['new_items'] += 1
                
                # 키워드 매칭 수행
                matched_users = await self._find_matching_users(db, item_data)
                if matched_users:
                    results['matched_items'] += 1
                    
                    # 매칭된 사용자들에게 알림 생성
                    for user_id in matched_users:
                        await self._create_alert(db, user_id, new_item.id, item_data)
                        results['alerts_sent'] += 1
                
            except Exception as e:
                print(f"❌ 물건 처리 실패: {e}")
                continue
        
        return results
    
    async def _find_matching_users(self, db: AsyncSession, item_data: Dict) -> List[str]:
        """물건과 매칭되는 사용자들 찾기"""
        matching_users = set()
        
        # 모든 키워드 조회
        all_keywords = await keyword_crud.get_all_keywords(db)
        
        # 물건 제목과 키워드 비교
        title = item_data.get('title', '').lower()
        item_keywords = item_data.get('keywords', [])
        
        for keyword in all_keywords:
            keyword_lower = keyword.lower()
            
            # 제목에 키워드가 포함되거나, 추출된 키워드에 일치하는 것이 있는지 확인
            if keyword_lower in title or keyword in item_keywords:
                # 해당 키워드를 등록한 사용자들 찾기
                keyword_records = await keyword_crud.get_by_user_id(db, keyword)
                for record in keyword_records:
                    if record.keyword.lower() == keyword_lower:
                        matching_users.add(record.user_id)
        
        return list(matching_users)
    
    async def _create_alert(self, db: AsyncSession, user_id: str, item_id: int, item_data: Dict):
        """알림 생성"""
        try:
            # 중복 알림 체크
            if await alert_crud.check_duplicate_alert(db, user_id, item_id):
                return
            
            # 알림 메시지 생성
            message = f"새로운 경매 물건이 발견되었습니다: {item_data.get('title', '')[:50]}..."
            
            alert_create = AlertCreate(
                user_id=user_id,
                item_id=item_id,
                message=message
            )
            
            await alert_crud.create(db, alert_create)
            
        except Exception as e:
            print(f"❌ 알림 생성 실패: {e}")
    
    def calculate_match_score(self, item_data: Dict, user_keywords: List[str]) -> float:
        """매칭 점수 계산 (향후 확장용)"""
        score = 0.0
        title = item_data.get('title', '').lower()
        item_keywords = item_data.get('keywords', [])
        
        for keyword in user_keywords:
            keyword_lower = keyword.lower()
            
            # 정확한 매칭
            if keyword in item_keywords:
                score += 1.0
            # 부분 매칭
            elif keyword_lower in title:
                score += 0.5
        
        return score 