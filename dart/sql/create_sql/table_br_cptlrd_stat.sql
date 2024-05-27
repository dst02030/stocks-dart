CREATE TABLE IF NOT EXISTS dart.br_cptlrd_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    감소일 DATE,
    감소형태 VARCHAR(255),
    감소주식종류 VARCHAR(255),
    감소수량 BIGINT,
    감소주당액면가 BIGINT,
    발행감소주가 BIGINT,
    PRIMARY KEY ("보고서코드")
);