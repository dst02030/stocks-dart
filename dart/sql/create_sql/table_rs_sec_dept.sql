CREATE TABLE IF NOT EXISTS dart.rs_sec_debt (
    _ts timestamptz NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    접수일자 DATE NOT NULL,
    일반사항 JSON, 
    인수인정보 JSON,
    자금의사용목적 JSON,
    매출인에관한사항 JSON,
    PRIMARY KEY (고유번호, 접수일자) 
);