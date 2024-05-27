CREATE TABLE IF NOT EXISTS dart.km_overseas_sec_list (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    상장보통주식총수 BIGINT,
    상장기타주식총수 BIGINT,
    상장거래소 VARCHAR(100),
    종목명 VARCHAR(100),
    상장일자 DATE,
    확인일자 DATE,
    PRIMARY KEY (접수번호) 
);