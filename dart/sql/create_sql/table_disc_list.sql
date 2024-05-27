CREATE TABLE IF NOT EXISTS dart.disc_list (
	_ts timestamptz NOT NULL,
    법인구분 CHAR(1) NOT NULL,
    종목명 VARCHAR(255) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    종목코드 CHAR(6),
    보고서명 VARCHAR(255) NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    공시제출인명 VARCHAR(255) NOT NULL,
    접수일자 Date NOT NULL,
    비고 VARCHAR(255),
	PRIMARY KEY ("고유번호", "접수번호", "접수일자")
);