CREATE TABLE IF NOT EXISTS dart.br_dbtsec_isu (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1) NOT NULL,
    회사명 VARCHAR(255),
    발행회사 VARCHAR(255),
    증권종류 VARCHAR(255),
    발행방법 VARCHAR(255),
    발행일자 DATE,
    권면총액 BIGINT,
    이자율 VARCHAR(255),
    평가등급기관 VARCHAR(255),
    만기일 Date,
    상환여부 VARCHAR(1000),
    주관회사 VARCHAR(255)
);