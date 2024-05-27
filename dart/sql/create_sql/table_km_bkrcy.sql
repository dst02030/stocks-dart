CREATE TABLE IF NOT EXISTS dart.km_bkrcy (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    부도내용 TEXT,
    부도금액 BIGINT,
    부도발생은행 VARCHAR(100),
    최종부도일자 DATE,
    부도사유및경위 TEXT,
    PRIMARY KEY (접수번호) 
);