CREATE TABLE IF NOT EXISTS dart.br_exec_payroll (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    회사명 VARCHAR(255),
    구분 VARCHAR(20),
    인원수 INT,
    연간급여총액 BIGINT,
    평균급여액 BIGINT,
    비고 VARCHAR(255),
    PRIMARY KEY ("접수번호")
);