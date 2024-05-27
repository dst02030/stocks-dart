
CREATE TABLE IF NOT EXISTS dart.br_shtsh_stat (
    _ts timestamptz NOT NULL,
    사업연도 SMALLINT NOT NULL,
    보고서코드 SMALLINT NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    법인구분 CHAR(1),
    법인명 VARCHAR(255),
    구분 VARCHAR(255),
    주주수 BIGINT,
    전체주주수 BIGINT,
    주주비율 VARCHAR(100),
    보유주식수 BIGINT,
    총발행주식수 BIGINT,
    보유주식비율 VARCHAR(100),
    PRIMARY KEY (접수번호, 구분) 
);