CREATE TABLE IF NOT EXISTS dart.br_lgstsh_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    성명 VARCHAR(255),
    관계 VARCHAR(50),
    주식종류 VARCHAR(50),
    기초소유수 BIGINT,
    기초소유지분율 DECIMAL(5, 2),
    기말소유수 BIGINT,
    기말소유지분율 DECIMAL(5, 2),
    비고 TEXT
);
