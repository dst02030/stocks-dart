CREATE TABLE IF NOT EXISTS dart.km_crdt_mng_terminate (
    _ts timestamptz NOT NULL,
    접수번호 CHAR(14) NOT NULL,
    법인구분 CHAR(1) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(100) NOT NULL,
    결정일자 DATE,
    관리기관 VARCHAR(50),
    중단사유 VARCHAR(500),
    향후대책 VARCHAR(500),
    확인일자 DATE,
    PRIMARY KEY (접수번호)
);