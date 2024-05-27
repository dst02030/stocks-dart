CREATE TABLE IF NOT EXISTS dart.eq_execstock (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    접수일자 DATE,
    회사명 VARCHAR(255),
    보고자 VARCHAR(255),
    임원등기여부 VARCHAR(50),
    임원직위 VARCHAR(255),
    주요주주 VARCHAR(255),
    소유수 BIGINT,
    소유증감수 BIGINT,
    소유비율 DECIMAL(5, 2),
    소유증감비율 DECIMAL(5, 2),
    PRIMARY KEY (접수번호, 보고자) 
);