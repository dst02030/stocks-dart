CREATE TABLE IF NOT EXISTS dart.fn_xbrl_taxo (
    _ts timestamptz NOT NULL,
    재무제표구분 VARCHAR(255),
    계정id VARCHAR(255),
    계정명 VARCHAR(255),
    적용기준일 DATE,
    한글출력명 VARCHAR(255),
    영문출력명 VARCHAR(255),
    데이터유형 VARCHAR(20),
    ifrs_reference VARCHAR(255),
    PRIMARY KEY (재무제표구분, 계정ID)
);