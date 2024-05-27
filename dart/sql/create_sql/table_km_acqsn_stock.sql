CREATE TABLE IF NOT EXISTS dart.km_acqsn_stock (
  _ts timestamptz NOT NULL,
  접수번호 VARCHAR(14) NOT NULL,
  법인구분 CHAR(1) NOT NULL,
  고유번호 VARCHAR(8) NOT NULL,
  회사명 VARCHAR(100) NOT NULL,
  취득예정보통주수 BIGINT,
  취득예정기타주수 BIGINT,
  취득대상보통주총액 BIGINT,
  취득대상기타주총액 BIGINT,
  취득예상시작일 DATE,
  취득예상종료일 DATE,
  보유예상시작일 DATE,
  보유예상종료일 DATE,
  취득목적 TEXT,
  취득방법 VARCHAR(300),
  위탁투자중개업자 VARCHAR(300),
  취득전보통주식취득량_배당가능범위내 BIGINT,
  취득전보통주식취득비율_배당가능범위내 DECIMAL(10,2),
  취득전기타주식취득량_배당가능범위내 BIGINT,
  취득전기타주식취득비율_배당가능범위내 DECIMAL(10,2),
  취득전보통주식취득량_기타취득 BIGINT,
  취득전보통주식취득비율_기타취득 DECIMAL(10,2),
  취득전기타주식취득량_기타취득 BIGINT,
  취득전기타주식취득비율_기타취득 DECIMAL(10,2),
  취득결정일 DATE,
  사외이사참석수 SMALLINT,
  사외이사불참수 SMALLINT,
  감사위원참석여부 VARCHAR(10),
  일보통주매수한도량 INT,
  일기타주매수한도량 INT,
    PRIMARY KEY (접수번호) 
);