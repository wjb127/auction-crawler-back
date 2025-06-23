-- =====================================================
-- 경매 알림 SaaS 데이터베이스 설정
-- Supabase SQL Editor에서 실행하세요
-- =====================================================

-- 1. keywords 테이블 생성
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    keyword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. detected_items 테이블 생성
CREATE TABLE detected_items (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    appraisal_value BIGINT,
    bid_date DATE,
    url TEXT NOT NULL,
    keywords JSONB,
    source_site VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. alerts 테이블 생성
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    item_id INT NOT NULL,
    message TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerts_item FOREIGN KEY (item_id) REFERENCES detected_items(id)
);

-- 4. 인덱스 생성 (성능 최적화)
CREATE INDEX idx_keywords_user_id ON keywords(user_id);
CREATE INDEX idx_keywords_keyword ON keywords(keyword);
CREATE INDEX idx_detected_items_created_at ON detected_items(created_at);
CREATE INDEX idx_detected_items_bid_date ON detected_items(bid_date);
CREATE INDEX idx_detected_items_keywords ON detected_items USING GIN(keywords);
CREATE INDEX idx_detected_items_url ON detected_items(url);
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_item_id ON alerts(item_id);
CREATE INDEX idx_alerts_sent_at ON alerts(sent_at);

-- 5. RLS (Row Level Security) 설정 (선택사항)
-- 현재는 임시 사용자 ID를 사용하므로 비활성화
-- ALTER TABLE keywords ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE detected_items ENABLE ROW LEVEL SECURITY;  
-- ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- 6. 테스트 데이터 삽입
INSERT INTO detected_items (title, appraisal_value, bid_date, url, keywords, source_site) VALUES
('서울특별시 송파구 잠실동 123-45 아파트', 850000000, '2024-02-15', 'https://example.com/item/1', '["송파구", "아파트"]', '대법원 경매정보'),
('부산광역시 강서구 명지동 567-89 오피스텔', 450000000, '2024-02-20', 'https://example.com/item/2', '["부산", "강서구", "오피스텔"]', '대법원 경매정보'),
('대구광역시 수성구 범어동 901-23 상가', 320000000, '2024-02-25', 'https://example.com/item/3', '["대구", "수성구", "상가"]', '대법원 경매정보');

-- 7. 테이블 확인
SELECT 'keywords' as table_name, count(*) as row_count FROM keywords
UNION ALL
SELECT 'detected_items', count(*) FROM detected_items  
UNION ALL
SELECT 'alerts', count(*) FROM alerts;

-- 8. 스키마 확인
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
    AND table_name IN ('keywords', 'detected_items', 'alerts')
ORDER BY table_name, ordinal_position; 