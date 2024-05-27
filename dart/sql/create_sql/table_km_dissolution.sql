CREATE TABLE IF NOT EXISTS dart.km_dissolution (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    해산사유 TEXT,
    해산사유발생일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(100),
    PRIMARY KEY (접수번호) 
);