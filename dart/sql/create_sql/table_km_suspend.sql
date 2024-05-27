CREATE TABLE IF NOT EXISTS dart.km_suspend (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    영업정지분야 TEXT,
    영업정지금액 BIGINT,
    최근매출총액 BIGINT,
    매출액대비 TEXT,
    대규모법인여부 VARCHAR(255),
    거래소의무공시해당여부 VARCHAR(255),
    영업정지내용 TEXT,
    영업정지사유 TEXT,
    향후대책 TEXT,
    영업정지영향 TEXT,
    영업정지일자 Date,
    이사회결의일 VARCHAR(100),
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(200),
    PRIMARY KEY (접수번호) 
);