from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import math

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *

from funcat.data.tushare_backend import TushareDataBackend
from funcat.data.rqalpha_data_backend import RQAlphaDataBackend


set_data_backend(TushareDataBackend())

set_start_date("2015-01-01")
S("000001.XSHG")  # 设置当前关注股票
T("2016-06-01")   # 设置当前观察日期


print(O, H, L, C, V)

# # 短期1:=EMA(C,10);
# # duanQi1 = EMA(C, 10)

# # 短期2:=EMA(短期1,3);
# # 短期3:=EMA(短期2,3);
# # 短期4:=EMA(短期3,3);
# # 短期5:=EMA(短期4,3);
# # 长期1:=EMA(C,45);
# # 长期2:=EMA(长期1,3);
# # 长期3:=EMA(长期2,3);
# # 长期4:=EMA(长期3,3);
# # 长期5:=EMA(长期4,3);
# # 一买托:=短期1>短期2 AND 短期2>短期3 AND ((MIN(长期1,长期5)>短期1 AND (CROSS(短期1,短期5) OR (O<MA(C,9) AND C>MA(C,5) AND MA(C,5)>MA(C,9)) OR (REF(长期1,1)<REF(长期1,2) AND 长期1>REF(长期1,1)))) OR (CROSS(短期1,长期1) AND 长期1>长期2 AND 长期2>长期3 AND 长期3>长期4 AND 长期4>长期5) );
# # 二买托:=短期1>短期2 AND 短期2>短期3 AND 短期3>长期1 AND 长期1>长期2 AND 长期2>长期3 AND 长期3>长期4 AND 长期4>长期5 AND 短期5/长期1<1.13;

#cross
duanqi1 = EMA(C, 10)
duanqi2 = EMA(duanqi1, 3)
duanqi3 = EMA(duanqi2, 3)
duanqi4 = EMA(duanqi3, 3)
duanqi5 = EMA(duanqi4, 3)

changqi1 = EMA(C, 45)
changqi2 = EMA(changqi1, 3)
changqi3 = EMA(changqi2, 3)
changqi4 = EMA(changqi3, 3)
changqi5 = EMA(changqi4, 3)

maituo1 = duanqi1 > duanqi2 and duanqi2 > duanqi3 and \
    ((MIN(changqi1, changqi5)>duanqi1 and (CROSS(duanqi1, duanqi5) or (O<MA(C,9) and C>MA(C,5) and MA(C,5)>MA(C,9)) \
        or (REF(changqi1, 1)<REF(changqi1,2) and changqi1>REF(changqi1,1)))) or (CROSS(duanqi1, changqi1) and changqi1>changqi2 and changqi2>changqi3 and changqi3>changqi4 \
            and changqi4>changqi5))

maituo2 = duanqi1 > duanqi2 and duanqi2>duanqi3 and duanqi3>changqi1 and changqi1>changqi2 and changqi2>changqi3 and changqi3>changqi4 and changqi4>changqi5 and duanqi5/duanqi1<1.13
print(maituo2)


#
VOL1 = 6
DC = (2*C+H+L+O) / 5
EMDC = EMA(EMA(EMA(DC,4),4),4)
BBB = (EMDC-REF(EMDC,1))/REF(EMDC,1)*10
BA = MA(BBB,VOL1)
simu = (BBB-BA)*100

FF = EMA(CLOSE,3)
MA15 = EMA(CLOSE,21)
guaidian = CROSS(FF,MA15)

VAR11 = HHV(HIGH,25)
VAR22 = LLV(LOW,25)
VAR33 = EMA((CLOSE-VAR22)/(VAR11-VAR22)*100,20)
VAR44 = EMA((CLOSE-VAR22)/(VAR11-VAR22)*100,5)
duanqimai = CROSS(VAR44,VAR33)

ZJ = (C+H+L)/3
VAR1 = MA(ZJ,30)
zhongxianqushi = VAR1+2.2*STD(ZJ,30)
KS = (C-MA(C,13))/MA(C,13)*(-100)
RKS = REF(KS,1)
MLS = RKS/KS>=1.23 AND RKS>=8 AND C/REF(C,1)>=1.02
FENG:=EMA(C,10);
YUN:=EMA(KS/10+EMA(C,10),3);
风云买:=CROSS(FENG,YUN);

主力:=EMA( (CLOSE-MA(CLOSE,7))/MA(CLOSE,7)*480,2)*5;
散户:=EMA( (CLOSE-MA(CLOSE,11))/MA(CLOSE,11)*480,7)*5;
主力底:=CROSS(主力,散户) AND 主力<-10;

TD:=REF(H,1)>HHV(REF(H,2),20);
TDT:=BARSLAST(TD);

X_4:=MA((2*CLOSE+HIGH+LOW)/4,5);
X_6:=X_4*0.98;
X_25:=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4;
乖离:=REF((X_6-X_25)/X_25*100,1);

强势线1:=HHV(MA((((LOW + HIGH) + CLOSE)/3),8),60);

V11:=3*SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1)-2*SMA(SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1),3,1);
趋势线:=EMA(V11,3);

# RSV:=(CLOSE-LLV(LOW,5))/(HHV(HIGH,5)-LLV(LOW,5))*100;
# K:=SMA(RSV,5,1);
# D:=SMA(K,5,5);
# J:=3*K-2*D;
# VARB2:=(RSV/2+22)*1;
# 量:=EMA(VOL,13);
# 资金:=EMA(AMOUNT,13);
# 过滤:=((资金 /量) / 100);
# 提纯:=(((CLOSE -过滤) / 过滤) * 100);
# 黄金:=((提纯 < (0)) AND ZXNH);
# 低买:=IF(黄金 AND RSV<VARB2-2,50,0);
# 高卖:=IF(黄金 AND RSV>VARB2,80,120);
# 上涨分界:=25;
# KDJ提前金叉:=(CROSS(上涨分界,低买));

rsv = (C - LLV(L, 5)) / (HHV(H, 5) - LLV(L, 5)) * 100
K = SMA(rsv, 5, 1)
D = SMA(K, 5, 5)
J = 3 * K - 2 * D
varb2 = (rsv / 2 + 22)
liang = EMA(V, 13)
zijin = EMA(V, 13)
guolv = ((zijin / liang) / 100)
tichun = (((C -guolv) / guolv) * 100)
huangjin = ((tichun < 0) and zxnh)
dimai = 50 if huangjin and rsv < varb2-2 else 0
gaomai = 80 if huangjin  and rsv > varb2 else 120
shangzhangfenjie = 25
KDJjincha = CROSS(shangzhangfenjie, dimai)
print(KDJjincha)

V1 = (C*2+H+L)/4*10
V2 = EMA(V1,13)-EMA(V1,21)
V3 = EMA(V2,5)
V4 = 2*(V2-V3)*100
choumajin = V4 if V4 >= 0 else 0
choumaxiuzheng = False if choumajin<REF(choumajin,1) and REF(C/O>1,1) else True

X_4 = MA((2*C+H+L)/4,5)
X_6 = X_4*0.98
X_25 = (MA(C,3)+MA(C,6)+MA(C,12)+MA(C,24))/4
guaili = REF((X_6-X_25)/X_25*100,1)

qiangshixian1 = HHV(MA((((L + H) + C) / 3),8),60)
print(qiangshixian1)

V11 = 3*SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1)-2*SMA(SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1),3,1)
qushixian = EMA(V11, 3)

DDIFF = 100*(EMA(C,12)-EMA(C,26))
DDEA = EMA(DDIFF,9)
DMACD = (DDIFF-DDEA)*2
sicha = CROSS(DDEA,DDIFF)

N1 = REF(BARSLAST(sicha), -1)
N2 = REF(BARSLAST(sicha), N1 + 1)
N3 = REF(BARSLAST(sicha), N1 + N2 + 1)

CL1 = LLV(L, N1+1)
DIFL1 = LLV(DDIFF,N1+1)
CL2 = REF(CL1,N1+1)
DIFL2 = REF(DIFL1, N1+1)
CL3 = REF(CL2, N1+1)
DIFL3 = REF(DIFL2, N1+1)
PDIFL2 = INTPART(LOG(DIFL2)) - 1 if DIFL2 > 0 else INTPART(LOG(-1 * DIFL2))-1 #INTPART(LOG(DIFL2))-1 if DIFL2 > 0 else INTPART(LOG(-DIFL2))-1
MDIFL2 = INTPART(DIFL2/POW(10,PDIFL2));
PDIFL3 = INTPART(LOG(DIFL3))-1 if DIFL3 > 0 else INTPART(LOG(-1 * DIFL3))-1
MDIFL3 = INTPART(DIFL3/POW(10,PDIFL3))
MDIFB2 = INTPART(DDIFF/POW(10,PDIFL2))
MDIFB3 = INTPART(DDIFF/POW(10,PDIFL3))
zhijiedibujiegou = (CL1 < CL2 ) and (MDIFB2 > MDIFL2) and DDIFF < 0 and (DMACD < 0 and REF(DMACD,1) < 0) and MDIFB2 <= REF(MDIFB2,0)
gefengdibujiegou = (CL1 < CL3 and CL3 < CL2 ) and (MDIFB3 > MDIFL3) and (DMACD < 0 and REF(DMACD,1) < 0) and MDIFB3 <= REF(MDIFB3,0)
BG = ((MDIFB2 > REF(MDIFB2,1))*REF(zhijiedibujiegou,2)) or ((MDIFB3 > REF(MDIFB3,2))*REF(gefengdibujiegou,2));
P = CROSS(DDIFF,DDEA) and ~(N1>=16 and O/REF(C,1)<1.05)
buy = FILTER(BG and P, DMACD>0)