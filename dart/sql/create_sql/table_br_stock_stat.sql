CREATE TABLE IF NOT EXISTS dart.br_stock_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    구분 VARCHAR(255),
    발행예정주식총수 TEXT,
    발행주식총수 TEXT,
    감소주식총수 TEXT,
    감소_감자 TEXT,
    감소_이익소각 TEXT,
    감소_상환 TEXT,
    감소_기타 TEXT,
    현재주식총수 TEXT,
    자기주식수 TEXT
);