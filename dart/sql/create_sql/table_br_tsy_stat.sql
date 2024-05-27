CREATE TABLE IF NOT EXISTS dart.br_tsy_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    대분류 VARCHAR(50),
    중분류 VARCHAR(50),
    소분류 VARCHAR(50),
    주식종류 VARCHAR(50),
    기초수량 BIGINT,
    취득변동수 BIGINT,
    처분변동수 BIGINT,
    소각변동수 BIGINT,
    기말수량 BIGINT,
    비고 TEXT
);