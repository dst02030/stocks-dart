CREATE TABLE IF NOT EXISTS dart.rs_extr (
    _ts timestamptz NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    접수일자 DATE NOT NULL,
    일반사항 JSON, 
    발행증권 JSON, 
    당사회사에관한사항 JSON,
    PRIMARY KEY (고유번호, 접수일자) 
);