CREATE TABLE IF NOT EXISTS dart.km_wrt_down (
    _ts timestamptz NOT NULL,
    접수번호 VARCHAR(14),
    법인구분 CHAR(1),
    고유번호 VARCHAR(8),
    회사명 VARCHAR(100),
    보통주수 BIGINT,
    기타주수 BIGINT,
    주당액면가 INT,
    감자전자본금 BIGINT,
    감자후자본금 BIGINT,
    감자전보통주수 BIGINT,
    감자후보통주수 BIGINT,
    감자전기타주수 BIGINT,
    감자후기타주수 BIGINT,
    감자비율_보통주 VARCHAR(100),
    감자비율_기타주 VARCHAR(100),
    감자기준일 DATE,
    감자방법 TEXT,
    감자사유 TEXT,
    주주총회예정일 DATE,
    명의개서정지기간 VARCHAR(100),
    구주권제출기간 VARCHAR(100),
    매매정지예정기간 VARCHAR(100),
    구주권제출시작일 DATE,
    구주권제출종료일 DATE,
    매매정지예정시작일 DATE,
    매매정지예정종료일 DATE,
    신주권교부예정일 DATE,
    신주상장예정일 DATE,
    채권자이의제출시작일 DATE,
    채권자이의제출종료일 DATE,
    구주권제출및신주권교부장소 TEXT,
    이사회결의일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(100),
    공정위신고대상여부 VARCHAR(100),
    PRIMARY KEY (접수번호) 
);