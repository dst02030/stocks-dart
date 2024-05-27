CREATE TABLE IF NOT EXISTS dart.br_cptlbnd_out_blce (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    잔여만기1 VARCHAR(20),
    잔여만기2 VARCHAR(20),
    년1이하 BIGINT,
    년1초과5이하 BIGINT,
    년5초과10이하 BIGINT,
    년10초과15이하 BIGINT,
    년15초과20이하 BIGINT,
    년20초과30이하 BIGINT,
    년30초과 BIGINT,
    합계 BIGINT,
    PRIMARY KEY ("접수번호", "잔여만기1", "잔여만기2")
);
