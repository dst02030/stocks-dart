CREATE TABLE IF NOT EXISTS dart.br_all_ctrs_stat (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    사업연도_시기 VARCHAR(255),
    계약체결일 VARCHAR(255),
    용역내용 TEXT,
    용역수행기간 VARCHAR(500),
    용역보수 VARCHAR(255),
    비고 TEXT
);