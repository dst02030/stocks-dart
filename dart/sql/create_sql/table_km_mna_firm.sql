CREATE TABLE IF NOT EXISTS dart.km_mna_firm (
    _ts timestamptz NOT NULL,
    접수번호 CHAR(14) NOT NULL,
    법인구분 CHAR(1) NOT NULL,
    고유번호 CHAR(8) NOT NULL,
    회사명 VARCHAR(300) NOT NULL,
    분할합병방법 TEXT,
    분할합병중요영향및효과 TEXT,
    이전사업및재산내용 TEXT,
    존속회사명 VARCHAR(300),
    존속회사_자산총계 BIGINT,
    존속회사_부채총계 BIGINT,
    존속회사_자본총계 BIGINT,
    존속회사_자본금 BIGINT,
    존속회사_재무기준일 DATE,
    존속회사_최근사업연도매출액 BIGINT,
    존속회사_주요사업 VARCHAR(300),
    존속회사_상장유지여부 VARCHAR(10),
    분할회사명 VARCHAR(300),
    분할회사_자산총계 BIGINT,
    분할회사_부채총계 BIGINT,
    분할회사_자본총계 BIGINT,
    분할회사_자본금 BIGINT,
    분할회사_재무기준일 DATE,
    분할회사_최근사업연도매출액 BIGINT,
    분할회사_주요사업 VARCHAR(300),
    분할회사_상장유지여부 VARCHAR(10),
    감자비율 VARCHAR(100),
    구주권제출시작일 DATE,
    구주권제출종료일 DATE,
    매매거래정지예정시작일 DATE,
    매매거래정지예정종료일 DATE,
    신주배정조건 TEXT,
    주주주식수비례여부및사유 TEXT,
    신주배정기준일 DATE,
    신주권교부예정일 DATE,
    신주상장예정일 DATE,
    합병형태 VARCHAR(300),
    합병상대회사명 VARCHAR(300),
    상대회사주요사업 VARCHAR(300),
    상대회사와관계 VARCHAR(300),
    상대회사_자산총계 BIGINT,
    상대회사_부채총계 BIGINT,
    상대회사_자본총계 BIGINT,
    상대회사_자본금 BIGINT,
    상대회사_매출액 BIGINT,
    상대회사_당기순이익 BIGINT,
    상대회사_외부감사기관명 VARCHAR(300),
    상대회사_외부감사의견 VARCHAR(300),
    합병시_보통주수 BIGINT,
    합병시_종류주수 BIGINT,
    합병신설회사명 VARCHAR(300),
    합병신설_자본금 BIGINT,
    합병신설_주요사업 VARCHAR(300),
    합병신설_재상장신청여부 VARCHAR(10),
    분할합병비율 VARCHAR(300),
    분할합병비율산출근거 TEXT,
    외부평가여부 VARCHAR(10),
    외부평가근거및사유 VARCHAR(300),
    외부평가기관명칭 VARCHAR(300),
    외부평가기간 VARCHAR(300),
    외부평가의견 TEXT,
    분할합병계약일 DATE,
    주주확정기준일 DATE,
    주주명부폐쇄시작일 DATE,
    주주명부폐쇄종료일 DATE,
    분할합병반대의사통지접수시작일 DATE,
    분할합병반대의사통지접수종료일 DATE,
    주총예정일 DATE,
    주식매수청구권행사시작일 DATE,
    주식매수청구권행사종료일 DATE,
    채권자이의제출시작일 DATE,
    채권자이의제출종료일 DATE,
    분할합병기일 DATE,
    종료보고총회일 DATE,
    분할합병등기예정일 DATE,
    우회상장여부 VARCHAR(10),
    타법인우회상장요건충족여부 VARCHAR(10),
    주식매수청구권매수예정가 BIGINT,
    주식매수청구권행사요건 TEXT,
    주식매수청구권행사관련사항 TEXT,
    주식매수청구권지급관련사항 TEXT,
    주식매수청구권제한관련 TEXT,
    주식매수청구권계약에미치는효력 TEXT,
    이사회결의일 DATE,
    사외이사참석수 SMALLINT,
    사외이사불참수 SMALLINT,
    감사위원참석여부 VARCHAR(10),
    풋옵션등계약체결여부 VARCHAR(10),
    계약내용 VARCHAR(300),
    증권신고서제출대상여부 VARCHAR(10),
    제출면제사유 VARCHAR(300),
    PRIMARY KEY (접수번호) 
);