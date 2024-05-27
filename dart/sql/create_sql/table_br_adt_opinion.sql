CREATE TABLE IF NOT EXISTS dart.br_adt_opinion (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    사업연도_시기 VARCHAR(255),
    감사인 VARCHAR(255),
    감사의견 TEXT,
    특기사항 TEXT,
    강조사항등 TEXT,
    핵심감사사항 TEXT,
    PRIMARY KEY ("접수번호")
);