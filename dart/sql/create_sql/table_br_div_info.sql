CREATE TABLE IF NOT EXISTS dart.br_div_info (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    구분 VARCHAR(50),
    주식종류 VARCHAR(50),
    당기 BIGINT,
    전기 BIGINT,
    전전기 BIGINT
);