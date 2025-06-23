-- =====================================================
-- 경매 알림 SaaS 데이터베이스 설정
-- Supabase SQL Editor에서 실행하세요
-- =====================================================

-- 1. auction_keywords 테이블 생성
CREATE TABLE auction_keywords (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    keyword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. auction_detected_items 테이블 생성
CREATE TABLE auction_detected_items (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    appraisal_value BIGINT,
    bid_date DATE,
    url TEXT NOT NULL,
    keywords JSONB,
    source_site VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. auction_alerts 테이블 생성
CREATE TABLE auction_alerts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    item_id INT NOT NULL,
    message TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_auction_alerts_item FOREIGN KEY (item_id) REFERENCES auction_detected_items(id)
);

-- 4. 인덱스 생성 (성능 최적화)
CREATE INDEX idx_auction_keywords_user_id ON auction_keywords(user_id);
CREATE INDEX idx_auction_keywords_keyword ON auction_keywords(keyword);
CREATE INDEX idx_auction_detected_items_created_at ON auction_detected_items(created_at);
CREATE INDEX idx_auction_detected_items_bid_date ON auction_detected_items(bid_date);
CREATE INDEX idx_auction_detected_items_keywords ON auction_detected_items USING GIN(keywords);
CREATE INDEX idx_auction_detected_items_url ON auction_detected_items(url);
CREATE INDEX idx_auction_alerts_user_id ON auction_alerts(user_id);
CREATE INDEX idx_auction_alerts_item_id ON auction_alerts(item_id);
CREATE INDEX idx_auction_alerts_sent_at ON auction_alerts(sent_at);

-- 5. RLS (Row Level Security) 설정 (선택사항)
-- 현재는 임시 사용자 ID를 사용하므로 비활성화
-- ALTER TABLE auction_keywords ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE auction_detected_items ENABLE ROW LEVEL SECURITY;  
-- ALTER TABLE auction_alerts ENABLE ROW LEVEL SECURITY;

-- 6. 테스트 데이터 삽입
INSERT INTO auction_detected_items (title, appraisal_value, bid_date, url, keywords, source_site) VALUES
('서울특별시 송파구 잠실동 123-45 아파트', 850000000, '2024-02-15', 'https://example.com/item/1', '["송파구", "아파트"]', '대법원 경매정보'),
('부산광역시 강서구 명지동 567-89 오피스텔', 450000000, '2024-02-20', 'https://example.com/item/2', '["부산", "강서구", "오피스텔"]', '대법원 경매정보'),
('대구광역시 수성구 범어동 901-23 상가', 320000000, '2024-02-25', 'https://example.com/item/3', '["대구", "수성구", "상가"]', '대법원 경매정보');

-- 7. 테이블 확인
SELECT 'auction_keywords' as table_name, count(*) as row_count FROM auction_keywords
UNION ALL
SELECT 'auction_detected_items', count(*) FROM auction_detected_items  
UNION ALL
SELECT 'auction_alerts', count(*) FROM auction_alerts;

-- 8. 스키마 확인
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
    AND table_name IN ('auction_keywords', 'auction_detected_items', 'auction_alerts')
ORDER BY table_name, ordinal_position; 