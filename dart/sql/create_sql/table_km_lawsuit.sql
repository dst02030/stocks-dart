CREATE TABLE IF NOT EXISTS dart.km_lawsuit (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    사건명칭 TEXT,
    원고신청인 TEXT,
    청구내용 TEXT,
    관할법원 TEXT,
    향후대책 TEXT,
    제기일자 DATE,
    확인일자 DATE,
    PRIMARY KEY (접수번호) 
);