CREATE TABLE IF NOT EXISTS dart.km_cvbd_issue (
    _ts timestamptz NOT NULL,
    접수번호 CHAR(14) NOT NULL, 
    법인구분 CHAR(1) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(100) NOT NULL,
    회차 VARCHAR(255),
    종류 VARCHAR(255),
    권면총액 BIGINT,
    잔여발행한도 BIGINT,
    해외권면총액 BIGINT,
    해외통화단위 VARCHAR(10),
    해외기준환율등 VARCHAR(50),
    해외발행지역 VARCHAR(50),
    해외시장명칭 VARCHAR(300),
    시설자금 BIGINT,
    영업양수자금 BIGINT,
    운영자금 BIGINT, 
    채무상환자금 BIGINT,
    타법인증권취득자금 BIGINT,
    기타자금 BIGINT,
    표면이자율 DECIMAL(5,2),
    만기이자율 DECIMAL(5,2),
    사채만기일 DATE,
    사채발행방법 VARCHAR(300),
    전환비율 DECIMAL(5,2),
    전환가액 BIGINT,
    전환발행주식종류 VARCHAR(300),
    전환발행주식수 BIGINT,
    주식총수대비전환발행비율 DECIMAL(5,2),
    전환청구기간시작일 DATE,
    전환청구기간종료일 DATE,
    최저조정가액 BIGINT,
    최저조정가액근거 TEXT,
    전환가액70퍼센트미만조정가능잔여발행한도 BIGINT,
    합병관련사항 TEXT,
    청약일 DATE,
    납입일 DATE, 
    대표주관회사 VARCHAR(300),
    보증기관 VARCHAR(300),
    이사회결의일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(200),
    증권신고서제출대상여부 VARCHAR(200),
    제출면제사유 VARCHAR(500),
    당해사채해외발행연계대차거래내역 VARCHAR(500),
    공정위신고대상여부 VARCHAR(200),
    PRIMARY KEY (접수번호)
);