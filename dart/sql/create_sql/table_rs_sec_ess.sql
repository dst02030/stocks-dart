CREATE TABLE IF NOT EXISTS dart.rs_sec_ess (
    _ts timestamptz NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    접수일자 DATE NOT NULL,
    일반사항 JSON, 
    증권의종류 JSON, 
    인수인정보 JSON,
    자금의사용목적 JSON,
    매출인에관한사항 JSON,
    일반청약자환매청구권 JSON,
    PRIMARY KEY (고유번호, 접수일자) 
);