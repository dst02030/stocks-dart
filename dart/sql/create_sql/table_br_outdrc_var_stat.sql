CREATE TABLE IF NOT EXISTS dart.br_outdrc_var_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    이사수 SMALLINT,
    사외이사수 SMALLINT,
    사외_선임수 SMALLINT,
    사외_해임수 SMALLINT,
    사외_중도퇴임수 SMALLINT,
    PRIMARY KEY ("접수번호")
);