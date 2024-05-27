CREATE TABLE IF NOT EXISTS dart.km_overseas_sec_delist_dec (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    상장폐지보통주수 BIGINT,
    상장폐지기타주수 BIGINT,
    상장거래소 VARCHAR(100),
    해외상장목적 TEXT,
    폐지신청예정일자 DATE,
    상장예정일자 DATE,
    폐지사유 TEXT,
    이사회결의일 DATE,
    사외이사참석수 INT,
    사외이사불참수 INT,
    감사위원참석여부 VARCAHR(255),
    PRIMARY KEY (접수번호) 
);