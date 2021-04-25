from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *

from funcat.data.tushare_backend import TushareDataBackend
from funcat.data.rqalpha_data_backend import RQAlphaDataBackend


set_data_backend(TushareDataBackend())

set_start_date("2015-01-01")
S("000001.XSHG")  # 设置当前关注股票
T("2016-06-01")   # 设置当前观察日期


print(O, H, L, C)

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

# # RSV:=(CLOSE-LLV(LOW,5))/(HHV(HIGH,5)-LLV(LOW,5))*100;
# # K:=SMA(RSV,5,1);
# # D:=SMA(K,5,5);
# # J:=3*K-2*D;
# # VARB2:=(RSV/2+22)*1;
# # 量:=EMA(VOL,13);
# # 资金:=EMA(AMOUNT,13);
# # 过滤:=((资金 /量) / 100);
# # 提纯:=(((CLOSE -过滤) / 过滤) * 100);
# # 黄金:=((提纯 < (0)) AND ZXNH);
# # 低买:=IF(黄金 AND RSV<VARB2-2,50,0);
# # 高卖:=IF(黄金 AND RSV>VARB2,80,120);
# # 上涨分界:=25;
# # KDJ提前金叉:=(CROSS(上涨分界,低买));

# rsv = (C - LLV(L, 5)) / (HHV(H, 5) - LLV(L, 5)) * 100
# K = SMA(rsv, 5, 1)
# D = SMA(K, 5, 5)
# J = 3 * k - 2 * D
# varb2 = (rsv / 2 + 22)
# liang = EMA(V, 13)
# zijin = EMA(A, 13)
# guolv = ((zijin / liang) / 100)
# tichun = (((C -guolv) / guolv) * 100)
# huangjin = ((tichun < 0) and zxnh)
# dimai = if(huangjin and rsv < varb2-2, 50, 0)
# gaomai = if(huangj  and rsv > varb2, 80, 120)
# shangzhangfenjie = 25
# KDJjincha = CROSS(shangzhangfenjie, dimai)

# DDIFF:=100*(EMA(CLOSE,12)-EMA(CLOSE,26));
# DDEA:=EMA(DDIFF,9);
# DMACD:=(DDIFF-DDEA)*2;
# 死叉:=CROSS(DDEA,DDIFF);
# N1:=BARSLAST(死叉);
# N2:=REF(BARSLAST(死叉),N1+1);
# N3:=REF(BARSLAST(死叉),N2+N1+2);
# CL1:=LLV(LOW,N1+1);
# DIFL1:=LLV(DDIFF,N1+1);
# CL2:=REF(CL1,N1+1);
# DIFL2:=REF(DIFL1,N1+1);
# CL3:=REF(CL2,N1+1);
# DIFL3:=REF(DIFL2,N1+1);
# PDIFL2:=IF(DIFL2 > 0,INTPART(LOG(DIFL2))-1,INTPART(LOG(-DIFL2))-1);
# MDIFL2:=INTPART(DIFL2/POW(10,PDIFL2));
# PDIFL3:=IF(DIFL3 > 0,INTPART(LOG(DIFL3))-1,INTPART(LOG(-DIFL3))-1);
# MDIFL3:=INTPART(DIFL3/POW(10,PDIFL3));
# MDIFB2:=INTPART(DDIFF/POW(10,PDIFL2));
# MDIFB3:=INTPART(DDIFF/POW(10,PDIFL3));
# 直接底部结构:=(CL1 < CL2 ) AND (MDIFB2 > MDIFL2) AND DDIFF < 0 AND (DMACD < 0 AND REF(DMACD,1) < 0) AND MDIFB2 <= REF(MDIFB2,0);
# 隔峰底部结构:=(CL1 < CL3 AND CL3 < CL2 ) AND (MDIFB3 > MDIFL3) AND (DMACD < 0 AND REF(DMACD,1) < 0) AND MDIFB3 <= REF(MDIFB3,0);
# BG:=((MDIFB2 > REF(MDIFB2,1))*REF(直接底部结构,2)) OR ((MDIFB3 > REF(MDIFB3,2))*REF(隔峰底部结构,2));
# P:=CROSS(DDIFF,DDEA);
# 一买:=FILTER(BG AND P,DMACD>0);

# ddiff = 100*(EMA(C, 12)-EMA(C, 26))
# ddea = EMA(DDIFF, 9)
# dmacd = (ddiff - ddea)*2
# sicha = CROSS(ddea, ddiff)
