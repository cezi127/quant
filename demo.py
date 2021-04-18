from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *


from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

set_start_date("2015-01-01")
S("000001.XSHG")  # 设置当前关注股票
T("2016-06-01")   # 设置当前观察日期

#乖离
# X_4 = MA((2 * C + H + L) / 4, 5)
# X_6 = X_4 * 0.98
# X_25 = (MA(C,3)+MA(C,6)+MA(C,12)+MA(C,24))/4
# guaili = REF((X_6-X_25)/X_25*100,1)
# print(guaili)

#强势线
# qiangShiXian_1 = HHV(MA((((L + H) + C) / 3),8),60)
# print(qiangShiXian_1)

#主力
# MAV=(C*2+H+L)/4
# SK=EMA(MAV,13)-EMA(MAV,34)
# SD=EMA(SK,5)
# kongJunZhuLi=(-2*(SK-SD))*3.8
# duoJunZhuLi=(2*(SK-SD))*3.8
# print(duoJunZhuLi)

#长期线、短期线、中期线
# A=MA(-100*(HHV(H,34)-C)/(HHV(H,34)-LLV(L,34)),19)
# B=-100*(HHV(H,15)-C)/(HHV(H,15)-LLV(L,15))
# D=EMA(-100*(HHV(H,34)-C)/(HHV(H,34)-LLV(L,34)),4)
# changQiXian=100+A
# duanQiXian=100+B
# zhongQiXian=100+D
# print(zhongQiXian)

#SSD
# SLOWV=LLV(LOW,36)
# SHIGHV=HHV(HIGH,36)
# SRSV=EMA((CLOSE-SLOWV)/(SHIGHV-SLOWV)*100,5)
# SSK=EMA(SRSV,5)
# SSD=MA(SSK,5)
# print(SSD)

#高抛低吸
# RSV=(C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100
# RK=SMA(RSV,3,1)
# RD=SMA(RK,3,1)
# RJ=3*RK-2*RD
# BDGD= True if HHV(RJ,2)==HHV(RJ,8) and RJ>80 else False
# zhuYi= 1 if CROSS(REF(RJ-0.01,1),RJ)and REF(BDGD,1) else 0
# zhongXin=(2*C+H+L)/4
# SJ=WMA((zhongXin-LLV(L,5))/(HHV(H,5)-LLV(L,5))*100,2)
# ZJ=WMA(0.618*REF(SJ,1)+0.382*SJ,2)
# gaoPao = True if CROSS(ZJ,SJ) and SJ>70 else False
# diXi = True if CROSS(SJ,ZJ) and SJ<30 else False
# MTM = C-REF(C,1)
# ZLGJ = 100*EMA(EMA(MTM,6),6)/EMA(EMA(ABS(MTM),6),6)
# buy_1 = 1 if LLV(ZLGJ,2)==LLV(ZLGJ,7) and COUNT(ZLGJ<0,2) and CROSS(ZLGJ,MA(ZLGJ,2)) else 0
# sell_1 = 1 if HHV(ZLGJ,2)==HHV(ZLGJ,7) and COUNT(ZLGJ>50,2) and CROSS(MA(ZLGJ,2),ZLGJ) else 0

#均线多头排列
# MA7 = MA(C, 7)
# MA14 = MA(C, 14)
# MA21 = MA(C, 21)
# MA34 = MA(C, 34)
# MA8 = MA(C, 55)
# junXianJinCha = CROSS(MA7, MA34)
# junXianDuoTouPaiLie = True if MA7 > MA14 and MA14 > MA21 and MA21 > MA34 else False

#VAR80
# VAR80 = 3*SMA((C-LLV(L,180))/(HHV(H,180)-LLV(L,180))*100,5,1)-2*SMA(SMA((C-LLV(L,180))/(HHV(H,180)-LLV(L,180))*100,180,1),15,1)

# #XA
# XA_1= True if REF(C,1)*1.1-C<0.01 and H==C else False
# XA_2=5
# XA_3=3
# XA_4=(EMA(C,5)*7+EMA(C,10)*3)/10
# XA_6=EMA(EMA(L,21)+6.8*STD(L,2),55)
# XA_7=EMA(C/XA_6*(1.88*C+L+O)/2.75,3)
# XA_8=(XA_7-XA_6)/XA_6/2
# XA_9=EMA(XA_7-XA_8*XA_7,5)
# XA_10=EMA(C,34)-3*STD(C,34)
#
# #喇叭
# laBa_up= XA_4 if XA_4 > XA_9 else XA_9
# laBa_down = EMA(C,34) - 3*STD(C,34) if XA_9 < XA_4 and XA_9 < C * 0.15 else XA_9

#疯牛
fengNiuYaLi = HHV((H+L)/2,120)
jinChaFengNiu = EMA((EMA(C,4)+EMA(C,6)+EMA(C,12)+EMA(C,24))/4,2)


