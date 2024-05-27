CREATE TABLE IF NOT EXISTS dart.br_ind_payroll (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    이름 VARCHAR(255),
    직위 VARCHAR(255),
    보수총액 BIGINT,
    총액비포함보수 TEXT
);