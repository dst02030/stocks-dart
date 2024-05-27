CREATE TABLE IF NOT EXISTS dart.record_history (
    _ts timestamptz NOT NULL,
    테이블이름 VARCHAR(100) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    latest_ins_date Date NOT NULL,
    PRIMARY KEY ("테이블이름", "고유번호")
);