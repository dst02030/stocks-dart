CREATE TABLE IF NOT EXISTS dart.br_adt_ctrs_stat (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    사업연도_시기 VARCHAR(255),
    감사인 VARCHAR(255),
    내용 TEXT,
    보수 VARCHAR(255),
    총소요시간 VARCHAR(255),
    감사계약내역_보수 TEXT,
    감사계약내역_시간 TEXT,
    실제수행내역_보수 TEXT,
    실제수행내역_시간 TEXT,
    PRIMARY KEY ("접수번호")
);