CREATE TABLE IF NOT EXISTS dart.fn_xbrl (
	_ts timestamptz NOT NULL,
    접수번호 VARCHAR(14) NOT NULL,
    파일이름 VARCHAR(255) NOT NULL,
    파일내용 xml,
	PRIMARY KEY (접수번호, 파일이름)
);