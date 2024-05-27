CREATE TABLE IF NOT EXISTS dart.br_lgstsh_var_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    변동일 VARCHAR(255),
    최대주주명 VARCHAR(255),
    소유주식수 BIGINT,
    지분율 VARCHAR(255),
    변동원인 TEXT,
    비고 TEXT
);