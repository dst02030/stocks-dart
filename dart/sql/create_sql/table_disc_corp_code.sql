CREATE TABLE IF NOT EXISTS dart.disc_corp_code (
    _ts TIMESTAMPTZ NOT NULL,
	고유번호 VARCHAR(8) NOT NULL,
	정식명칭 VARCHAR(255) NOT NULL,
	종목코드 VARCHAR(6),
	최종변경일자 DATE NOT NULL,
	PRIMARY KEY (고유번호, 최종변경일자)
);