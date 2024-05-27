CREATE TABLE IF NOT EXISTS dart.br_pubcptl_use (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(255),
    법인구분 CHAR(1),
    구분 VARCHAR(255),
    회차 VARCHAR(255),
    납입일 DATE,
    납입금액 BIGINT,
    자금사용계획 TEXT,
    실제자금사용현황 TEXT,
    자금사용계획_사용용도 TEXT,
    자금사용계획_조달금액 BIGINT,
    실제자금사용내역_내용 TEXT,
    실제자금사용내역_금액 BIGINT,
    차이발생사유등 TEXT
    -- PRIMARY KEY (접수번호, 구분)
);