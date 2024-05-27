CREATE TABLE IF NOT EXISTS dart.km_rehab (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    신청인 TEXT,
    관할법원 TEXT,
    신청사유 TEXT,
    신청일자 DATE,
    향후대책및일정 TEXT,
    PRIMARY KEY (접수번호) 
);

