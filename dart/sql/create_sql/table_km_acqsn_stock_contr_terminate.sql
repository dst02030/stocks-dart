CREATE TABLE IF NOT EXISTS dart.km_acqsn_stock_contr_terminate (
    _ts timestamptz NOT NULL,
    접수번호 CHAR(14) NOT NULL,
    법인구분 CHAR(1) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(300) NOT NULL,
    해지전계약금 BIGINT,
    해지후계약금 BIGINT, 
    해지전계약시작일 DATE,
    해지전계약종료일 DATE,
    해지목적 VARCHAR(300),
    해지기관 VARCHAR(300),
    해지예정일자 DATE,
    해지후신탁재산반환방법 VARCHAR(300),
    해지전보통주식취득량_배당가능범위내 BIGINT,
    해지전보통주식취득비율_배당가능범위내 DECIMAL(5,2),
    해지전기타주식취득량_배당가능범위내 BIGINT,
    해지전기타주식취득비율_배당가능범위내 DECIMAL(5,2),
    해지전보통주식취득량_기타취득 BIGINT,
    해지전보통주식취득비율_기타취득 DECIMAL(5,2),
    해지전기타주식취득량_기타취득 BIGINT,
    해지전기타주식취득비율_기타취득 DECIMAL(5,2),
    이사회결의일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(300),
    PRIMARY KEY (접수번호) 
);