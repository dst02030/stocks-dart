CREATE TABLE IF NOT EXISTS dart.km_acqsn_othr (
    _ts timestamptz NOT NULL,
    접수번호 CHAR(14) NOT NULL,
    법인구분 CHAR(1) NOT NULL, 
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(300) NOT NULL,
    발행회사명 TEXT,
    발행회사국적 VARCHAR(300),
    발행회사대표자 VARCHAR(300),
    발행회사자본금 BIGINT,
    발행회사와회사관계 VARCHAR(300),
    발행회사주식총수 BIGINT,
    발행회사주요사업 VARCHAR(300),
    최근6m_3자배정신주취득여부 VARCHAR(10),
    양수주식수 BIGINT,
    양수금액 BIGINT,
    총자산 BIGINT,
    총자산대비비율 DECIMAL(7,2),
    자기자본 BIGINT,
    자기자본대비비율 DECIMAL(7,2),
    양수후소유주식수 BIGINT,
    양수후지분비율 DECIMAL(7,2),
    양수목적 VARCHAR(300),
    양수예정일자 DATE,
    거래상대회사명 TEXT,
    거래상대자본금 BIGINT,
    거래상대주요사업 VARCHAR(300),
    거래상대주소 TEXT,
    거래상대와관계 VARCHAR(300),
    거래대금지급 TEXT,
    외부평가여부 VARCHAR(10),
    외부평가근거및사유 TEXT,
    외부평가기관명칭 VARCHAR(300),
    외부평가기간 VARCHAR(300),
    외부평가의견 TEXT,
    이사회결의일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(10),
    우회상장해당여부 VARCHAR(10),
    향후6m_제3자배정증자등계획 VARCHAR(100),
    발행회사우회상장요건충족여부 VARCHAR(10),
    공정위신고대상여부 VARCHAR(10),
    풋옵션등계약체결여부 VARCHAR(10),
    계약내용 TEXT,
    PRIMARY KEY (접수번호)
);