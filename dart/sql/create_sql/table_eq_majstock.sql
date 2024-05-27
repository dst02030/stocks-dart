CREATE TABLE IF NOT EXISTS dart.eq_majstock (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    접수일자 DATE,
    회사명 VARCHAR(255),
    보고구분 VARCHAR(50),
    대표보고자 VARCHAR(255),
    보유주식수 BIGINT,
    보유주식증감 BIGINT,
    보유비율 DECIMAL(5, 2),
    보유비율증감 BIGINT,
    주요체결주식수 BIGINT,
    주요체결보유비율 DECIMAL(5, 2),
    보고사유 TEXT,
    PRIMARY KEY (접수번호) 
);

