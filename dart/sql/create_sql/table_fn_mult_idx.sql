CREATE TABLE IF NOT EXISTS dart.fn_mult_idx (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    종목코드 VARCHAR(6),
    지표분류코드 VARCHAR(8),
    지표분류명 VARCHAR(50),
    지표코드 VARCHAR(10),
    지표명 VARCHAR(255),
    지표값 DECIMAL(20, 3),
    PRIMARY KEY (고유번호, 사업연도, 보고서코드, 지표분류코드, 지표코드)
);