CREATE TABLE IF NOT EXISTS dart.km_crdt_mng (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    관리결정일자 DATE,
    관리기관 VARCHAR(100),
    관리기간 VARCHAR(100),
    관리사유 TEXT,
    확인일자 DATE,
    PRIMARY KEY (접수번호) 
);