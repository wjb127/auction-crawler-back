#!/bin/bash

# ===============================================
# 경매 알림 SaaS API 테스트 스크립트
# ===============================================

API_BASE="http://localhost:8001"
USER_ID="test-user-$(date +%s)"

echo "🚀 경매 알림 SaaS API 테스트 시작"
echo "📍 API Base URL: $API_BASE"
echo "👤 Test User ID: $USER_ID"
echo ""

# 1. 헬스 체크
echo "1️⃣ 헬스 체크 테스트"
curl -s "$API_BASE/health" | jq '.'
echo ""

# 2. 키워드 등록
echo "2️⃣ 키워드 등록 테스트"
echo "   송파구 키워드 등록..."
KEYWORD1=$(curl -s -X POST "$API_BASE/keywords" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"keyword\": \"송파구\"}")
echo $KEYWORD1 | jq '.'

echo "   아파트 키워드 등록..."
KEYWORD2=$(curl -s -X POST "$API_BASE/keywords" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"keyword\": \"아파트\"}")
echo $KEYWORD2 | jq '.'
echo ""

# 3. 키워드 조회
echo "3️⃣ 키워드 조회 테스트"
curl -s "$API_BASE/keywords?user_id=$USER_ID" | jq '.'
echo ""

# 4. 크롤링 실행
echo "4️⃣ 크롤링 실행 테스트"
curl -s -X POST "$API_BASE/crawler/run?pages=1" | jq '.'
echo ""

# 5. 감지된 물건 조회
echo "5️⃣ 감지된 경매 물건 조회 테스트"
echo "   전체 물건 조회..."
curl -s "$API_BASE/detected?limit=5" | jq '.'
echo ""

echo "   송파구로 검색..."
curl -s "$API_BASE/detected?keyword=송파구&limit=3" | jq '.'
echo ""

# 6. 크롤러 상태 확인
echo "6️⃣ 크롤러 상태 확인"
curl -s "$API_BASE/crawler/status" | jq '.'
echo ""

# 7. 알림 조회 (현재는 빈 데이터)
echo "7️⃣ 알림 기록 조회 테스트"
curl -s "$API_BASE/alerts?user_id=$USER_ID" | jq '.'
echo ""

echo "✅ 모든 테스트 완료!"
echo ""
echo "📖 Swagger 문서: $API_BASE/docs"
echo "📚 ReDoc 문서: $API_BASE/redoc" 