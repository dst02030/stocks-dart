CREATE TABLE IF NOT EXISTS dart.km_apa_option (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    보고사유 TEXT,
    자산양수도가액 BIGINT,
    PRIMARY KEY (접수번호) 
);