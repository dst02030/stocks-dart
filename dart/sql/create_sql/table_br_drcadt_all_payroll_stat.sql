CREATE TABLE IF NOT EXISTS dart.br_drcadt_all_payroll_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    인원수 INT,
    보수총액 BIGINT,
    인당평균보수액 BIGINT,
    비고 TEXT,
    PRIMARY KEY ("접수번호")
);