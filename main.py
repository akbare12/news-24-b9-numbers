import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024
OUT=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
CREAM=(250,246,235); INK=(18,18,20); RED=(176,32,32); NAVY=(24,42,78); GREY=(96,96,100); LGREY=(228,223,212); MID=(200,194,182)
GREEN=(32,118,58); BLUE=(30,88,168); ORANGE=(198,108,18); PURPLE=(108,58,158); GOLD=(176,138,0); SKY=(168,205,230); SEA=(146,190,205); LAND=(178,196,150); LAND2=(150,178,132)
def F(s,b=False,serif=False):
    n='DejaVuSerif-Bold.ttf' if serif and b else 'DejaVuSerif.ttf' if serif else 'DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+n,s)
    except Exception: return ImageFont.load_default()
def wrap(d,t,f,mw):
    ls=[];cur=''
    for w in t.split():
        s=(cur+' '+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else:
            if cur: ls.append(cur)
            cur=w
    if cur: ls.append(cur)
    return ls
def para(d,x,y,t,f,mw,lh,fill=INK,maxl=None):
    ls=wrap(d,t,f,mw)
    if maxl: ls=ls[:maxl]
    for i,l in enumerate(ls): d.text((x,y+i*lh),l,font=f,fill=fill)
    return y+len(ls)*lh
CHIP={'CONFIRMED':GREEN,'OFFICIAL':BLUE,'REPORTED':(72,92,122),'CLAIM':ORANGE,'FORECAST':PURPLE,'ONGOING':GOLD}
def chip(d,x,y,s):
    f=F(8,True); w=int(d.textlength(s,font=f))+9
    d.rounded_rectangle([x,y,x+w,y+12],2,fill=CHIP[s]); d.text((x+4.5,y+1),s,font=f,fill=(255,255,255)); return x+w+5
def sky(d,x,y,w,h,top,bot):
    for i in range(h):
        c=tuple(int(top[j]+(bot[j]-top[j])*i/h) for j in range(3)); d.line([(x,y+i),(x+w,y+i)],fill=c)
def scene(d,k,x,y,w,h):
    sky(d,x,y,w,h,(16,24,54),(64,84,128)) if k in ('tower','drone','blast') else sky(d,x,y,w,h,(214,228,240),(238,240,236)) if k in ('gate','court','trophy') else sky(d,x,y,w,h,(30,60,90),(90,130,170)) if k in ('ship','rocket') else sky(d,x,y,w,h,(240,226,200),(250,244,232))
    if k=='tower':
        d.rectangle([x,y+h-14,x+w,y+h],fill=(10,12,20))
        for bx,bw,bh in [(0,26,44),(30,20,60),(56,16,34),(w-72,22,52),(w-40,18,38)]:
            d.rectangle([x+bx,y+h-14-bh,x+bx+bw,y+h-14],fill=(38,46,70))
            for wy in range(y+h-12-bh,y+h-16,9):
                for wx in range(x+bx+3,x+bx+bw-3,7): d.point((wx,wy),fill=(255,214,110))
        d.polygon([(x+w*0.52,y+h-14),(x+w*0.60,y+h-14),(x+w*0.56,y+8)],fill=(52,64,96)); d.rectangle([x+w*0.545,y+8,x+w*0.575,y+h-14],fill=(66,80,116))
        for wy in range(y+16,y+h-16,11):
            d.point((x+w*0.56,wy),fill=(255,214,110))
        d.ellipse([x+w*0.66,y+18,x+w*0.78,y+30],fill=(255,150,40)); d.ellipse([x+w*0.70,y+22,x+w*0.82,y+34],fill=(255,190,90))
        d.ellipse([x+w*0.40,y+26,x+w*0.47,y+33],fill=(220,220,220)); d.line([(x+w*0.40,y+30),(x+w*0.36,y+30)],fill=(220,220,220),width=2)
    elif k=='gate':
        d.rectangle([x,y+h-16,x+w,y+h],fill=(120,110,96)); d.rectangle([x+w*0.08,y+22,x+w*0.92,y+h-16],fill=(150,32,28))
        d.rectangle([x+w*0.08,y+22,x+w*0.92,y+34],fill=(212,170,60)); d.rectangle([x+w*0.44,y+44,x+w*0.56,y+h-16],fill=(90,20,18))
        for cx in (0.20,0.32,0.68,0.80):
            d.rectangle([x+w*cx,y+44,x+w*cx+0.06*w,y+h-16],fill=(96,22,20))
        d.ellipse([x+w*0.47,y+26,x+w*0.53,y+32],fill=(212,170,60))
        d.rectangle([x+w*0.60,y+52,x+w*0.86,y+86],fill=(248,246,240)); d.rectangle([x+w*0.60,y+52,x+w*0.86,y+60],fill=(176,32,32))
        for i,ln in enumerate(['SERIOUS','VIOLATIONS','PROBE']): d.text((x+w*0.63,y+63+i*9),ln,font=F(8,True),fill=INK)
    elif k=='court':
        d.rectangle([x,y+h-14,x+w,y+h],fill=(96,92,84)); d.polygon([(x+8,y+34),(x+w-8,y+34),(x+w/2,y+8)],fill=(70,80,110))
        d.ellipse([x+w/2-7,y+16,x+w/2+7,y+30],fill=(212,170,60))
        for cx in (0.14,0.32,0.50,0.68,0.86):
            d.rectangle([x+w*cx-5,y+36,x+w*cx+5,y+h-14],fill=(220,216,206))
        d.rectangle([x+w*0.62,y+52,x+w*0.90,y+82],fill=(150,32,28)); d.text((x+w*0.66,y+60),'HUAWEI',font=F(11,True),fill=(255,255,255))
        d.rectangle([x+w*0.10,y+58,x+w*0.34,y+62],fill=(120,80,40)); d.rectangle([x+w*0.20,y+46,x+w*0.24,y+58],fill=(120,80,40))
    elif k=='drone':
        d.ellipse([x+w*0.72,y+12,x+w*0.88,y+26],fill=(255,196,90))
        for bx,bw,bh in [(0,30,34),(36,22,50),(64,18,28),(w-58,24,40),(w-28,20,30)]:
            d.rectangle([x+bx,y+h-12-bh,x+bx+bw,y+h-12],fill=(30,34,48))
        d.rectangle([x,y+h-12,x+w,y+h],fill=(12,14,22))
        d.ellipse([x+w*0.42,y+30,x+w*0.58,y+44],fill=(200,200,200)); d.line([(x+w*0.36,y+37),(x+w*0.64,y+37)],fill=(200,200,200),width=2)
        for dx,dy in [(0.30,0.55),(0.55,0.62),(0.70,0.50)]:
            d.ellipse([x+w*dx,y+h*dy,x+w*dx+7,y+h*dy+7],fill=(255,120,40))
    elif k=='trophy':
        d.ellipse([x+w/2-16,y+10,x+w/2+16,y+44],fill=(212,170,60)); d.rectangle([x+w/2-5,y+44,x+w/2+5,y+58],fill=(180,140,40)); d.rectangle([x+w/2-14,y+58,x+w/2+14,y+64],fill=(150,110,30))
        d.arc([x+w/2-30,y+12,x+w/2-12,y+36],90,270,fill=(212,170,60),width=4); d.arc([x+w/2+12,y+12,x+w/2+30,y+36],270,90,fill=(212,170,60),width=4)
        d.rectangle([x+8,y+h-16,x+w*0.42,y+h-6],fill=(0,120,70)); d.rectangle([x+w*0.58,y+h-16,x+w-8,y+h-6],fill=(200,40,40))
        d.text((x+12,y+h-15),'SEN 1-0',font=F(9,True),fill=(255,255,255)); d.text((x+w*0.62,y+h-15),'MAR 0-3',font=F(9,True),fill=(255,255,255))
    elif k=='ship':
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(40,90,140))
        d.rectangle([x+w*0.15,y+h*0.42,x+w*0.85,y+h*0.58],fill=(180,50,40)); d.rectangle([x+w*0.15,y+h*0.42,x+w*0.85,y+h*0.47],fill=(220,220,220))
        for cx in (0.22,0.34,0.46,0.58,0.70): d.rectangle([x+w*cx,y+h*0.48,x+w*cx+0.07*w,y+h*0.56],fill=(240,200,60))
        d.rectangle([x+w*0.78,y+h*0.28,x+w*0.86,y+h*0.44],fill=(240,240,240))
        d.polygon([(x+w*0.55,y+10),(x+w*0.62,y+26),(x+w*0.48,y+26)],fill=(120,120,120)); d.ellipse([x+w*0.60,y+8,x+w*0.70,y+20],fill=(255,150,40))
    elif k=='chart':
        d.rectangle([x+10,y+14,x+w-10,y+h-12],fill=(255,255,255)); d.line([(x+14,y+h-16),(x+w-14,y+h-16)],fill=INK,width=2); d.line([(x+14,y+18),(x+14,y+h-16)],fill=INK,width=2)
        d.line([(x+16,y+h-30),(x+w*0.35,y+h-44),(x+w*0.55,y+h-38),(x+w*0.75,y+h-58),(x+w-16,y+h-66)],fill=(32,118,58),width=3)
        d.line([(x+16,y+22),(x+w-16,y+22)],fill=(176,32,32),width=1); d.text((x+16,y+24),'50,000',font=F(9,True),fill=RED)
        d.text((x+w*0.62,y+h-30),'50,018',font=F(11,True),fill=GREEN)
    elif k=='server':
        for i in range(3):
            y0=y+6+i*(h-12)//3; y1=y0+(h-12)//3-3
            d.rectangle([x+12,y0,x+w-12,y1],fill=(30,40,60))
            for j in range(3): d.ellipse([x+18+j*12,y0+3,x+24+j*12,y0+9],fill=(255,80,60) if j==0 else (80,200,120))
        d.text((x+w*0.55,y+8),'CODE RED',font=F(11,True),fill=(255,80,60))
    elif k=='heli':
        d.ellipse([x+w*0.30,y+22,x+w*0.62,y+44],fill=(90,90,96)); d.line([(x+w*0.12,y+30),(x+w*0.88,y+30)],fill=(60,60,66),width=3)
        d.line([(x+w*0.62,y+32),(x+w*0.92,y+20)],fill=(60,60,66),width=3); d.rectangle([x+w*0.38,y+44,x+w*0.46,y+56],fill=(60,60,66)); d.rectangle([x+w*0.52,y+44,x+w*0.60,y+56],fill=(60,60,66))
        d.polygon([(x+w*0.10,y+h-10),(x+w*0.45,y+h-34),(x+w*0.75,y+h-10)],fill=(120,130,110)); d.polygon([(x+w*0.55,y+h-10),(x+w*0.85,y+h-26),(x+w*0.98,y+h-10)],fill=(100,112,96))
    elif k=='market':
        d.rectangle([x,y+h-18,x+w,y+h],fill=(150,140,120)); d.rectangle([x+w*0.10,y+16,x+w*0.90,y+h-18],fill=(240,230,210))
        d.rectangle([x+w*0.10,y+16,x+w*0.90,y+28],fill=(176,32,32)); d.rectangle([x+w*0.44,y+30,x+w*0.56,y+h-18],fill=(120,90,60))
        for i in range(3): d.ellipse([x+w*(0.2+i*0.24),y+38,x+w*(0.2+i*0.24)+8,y+46],fill=(200,80,60))
    elif k=='arrow':
        d.line([(x+10,y+h-14),(x+w-10,y+12)],fill=(176,32,32),width=4); d.polygon([(x+w-10,y+12),(x+w-26,y+12),(x+w-10,y+28)],fill=RED)
        d.ellipse([x+12,y+14,x+34,y+36],fill=(0,120,70)); d.text((x+17,y+19),'60',font=F(11,True),fill=(255,255,255)); d.text((x+40,y+20),'km to Aden',font=F(10,True),fill=INK)
    elif k=='blast':
        d.ellipse([x+w*0.30,y+10,x+w*0.55,y+36],fill=(255,150,40)); d.ellipse([x+w*0.42,y+18,x+w*0.66,y+44],fill=(255,90,30))
        for bx,bw,bh in [(0,26,30),(32,20,40),(w-50,22,34),(w-24,18,26)]:
            d.rectangle([x+bx,y+h-10-bh,x+bx+bw,y+h-10],fill=(34,36,44))
        d.rectangle([x,y+h-10,x+w,y+h],fill=(14,16,24))
    elif k=='rocket':
        d.polygon([(x+w/2,y+2),(x+w/2-12,y+h*0.34),(x+w/2+12,y+h*0.34)],fill=(220,220,220)); d.rectangle([x+w/2-12,y+h*0.34,x+w/2+12,y+h*0.58],fill=(240,240,240))
        d.polygon([(x+w/2-12,y+h*0.40),(x+w/2-22,y+h*0.56),(x+w/2-12,y+h*0.52)],fill=(176,32,32)); d.polygon([(x+w/2+12,y+h*0.40),(x+w/2+22,y+h*0.56),(x+w/2+12,y+h*0.52)],fill=(176,32,32))
        d.ellipse([x+w/2-6,y+h*0.58,x+w/2+6,y+h*0.78],fill=(255,150,40)); d.ellipse([x+w/2-14,y+h*0.58,x+w/2+14,y+h*0.70],fill=(255,220,120))
        d.ellipse([x+w*0.80,y+4,x+w*0.92,y+16],fill=(230,230,210)); d.ellipse([x+w*0.10,y+12,x+w*0.16,y+18],fill=(255,255,255))

CONT=[ [(-168,66),(-165,60),(-158,58),(-152,60),(-140,60),(-135,58),(-130,54),(-125,49),(-124,42),(-120,34),(-114,29),(-110,24),(-105,20),(-97,16),(-94,17),(-90,14),(-86,12),(-83,9),(-79,9),(-81,13),(-83,15),(-87,16),(-90,21),(-91,19),(-97,26),(-93,30),(-89,30),(-84,30),(-81,26),(-80,32),(-76,35),(-74,40),(-70,42),(-68,45),(-65,44),(-60,47),(-55,47),(-60,52),(-64,58),(-68,58),(-75,62),(-80,66),(-85,66),(-90,69),(-95,69),(-110,68),(-125,70),(-140,70),(-155,71),(-165,68)], [(-58,64),(-52,60),(-43,60),(-40,64),(-32,68),(-22,70),(-20,74),(-25,78),(-35,80),(-50,80),(-58,76),(-60,70)], [(-79,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-74,-50),(-70,-54),(-66,-55),(-65,-45),(-62,-41),(-58,-35),(-52,-33),(-48,-28),(-41,-23),(-39,-17),(-35,-9),(-35,-6),(-40,-3),(-44,-2),(-50,0),(-53,4),(-58,6),(-62,9),(-68,11),(-72,12),(-75,10)], [(-17,15),(-17,21),(-15,27),(-10,31),(-5,35),(0,36),(10,37),(11,34),(19,32),(25,32),(30,31),(32,31),(35,28),(37,22),(39,18),(43,12),(48,11),(51,11),(51,2),(48,-2),(42,-8),(40,-15),(36,-20),(33,-26),(28,-33),(20,-35),(17,-32),(15,-27),(13,-18),(12,-8),(9,4),(4,6),(-8,5),(-13,8)], [(-10,36),(-9,43),(-2,44),(0,46),(-4,48),(-1,50),(2,51),(5,53),(8,57),(10,59),(5,60),(5,62),(10,64),(12,66),(18,69),(25,71),(30,70),(40,68),(50,69),(60,69),(70,72),(80,73),(90,75),(100,77),(110,74),(120,73),(130,72),(140,72),(150,70),(160,70),(170,67),(178,65),(178,62),(170,60),(162,56),(158,52),(156,50),(150,59),(142,55),(140,50),(135,43),(130,42),(127,40),(126,38),(122,38),(120,32),(122,28),(118,25),(110,20),(108,18),(105,10),(103,8),(100,7),(98,10),(95,16),(92,21),(89,22),(86,20),(80,15),(77,8),(75,12),(72,20),(68,23),(66,25),(62,25),(58,26),(56,27),(52,28),(50,30),(48,30),(44,29),(40,30),(36,36),(33,36),(30,36),(27,37),(23,36),(20,40),(19,42),(16,44),(13,45),(10,44),(8,44),(4,43),(0,40),(-2,37),(-6,36),(-9,37)], [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-3,50)], [(130,31),(132,33),(135,34),(137,35),(139,36),(141,39),(141,42),(143,44),(145,44),(142,42),(140,38),(139,35),(136,33),(132,31)], [(109,1),(113,4),(117,6),(119,1),(117,-3),(113,-3),(110,-2)], [(95,5),(100,0),(104,-3),(106,-6),(103,-5),(99,-1)], [(105,-6),(110,-7),(114,-7),(114,-8),(108,-7)], [(131,-1),(136,-2),(141,-3),(146,-6),(150,-9),(147,-9),(143,-8),(138,-8),(134,-4)], [(113,-22),(114,-30),(115,-35),(120,-34),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-23),(146,-19),(142,-11),(142,-15),(137,-12),(135,-12),(132,-11),(130,-13),(126,-14),(122,-17),(118,-20)] ]
PINS=[(1,24.7,46.7),(2,31.2,121.5),(3,40.7,-74.0),(4,47.8,35.2),(5,14.7,-17.4),(6,26.6,56.3),(7,40.7,-74.0),(8,47.7,-122.1),(9,39.8,30.5),(10,10.4,-75.5),(11,12.8,45.0),(12,13.0,44.9),(13,39.8,98.5)]
def draw_map(d,x,y,w,h):
    d.rectangle([x,y,x+w,y+h],fill=SEA,outline=INK,width=1)
    def px(lon,lat): return (x+(lon+170)/360*w, y+(85-lat)/145*h)
    for poly in CONT:
        d.polygon([px(lo,la) for lo,la in poly],fill=LAND,outline=(110,130,95))
    for n,la,lo in PINS:
        cx,cy=px(lo,la)
        if n==7: cx+=14; cy-=8
        if n==12: cx-=13; cy+=9
        d.ellipse([cx-8,cy-8,cx+8,cy+8],fill=RED,outline=(255,255,255),width=1)
        d.text((cx-3,cy-6),str(n),font=F(8,True),fill=(255,255,255))
HERO=[('tower','1 RIYADH · MIDDLE EAST','CONFIRMED','Houthi drone hits Riyadh\u2019s tallest tower again, 11 hurt','A Houthi drone struck the PIF tower \u2014 Riyadh\u2019s tallest \u2014 the second hit on the same tower in a week. 11 hurt: 2 Saudi, 2 India, 3 Nepal, 4 Egypt. (Saudi officials)'),('gate','2 SHANGHAI · ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, is probed for \u201cserious violations\u201d \u2014 the fourth Politburo member to fall in a probe this year, the biggest shock to the Party elite in 2026. (CCDI)'),('court','3 NEW YORK · US / TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US federal jury found Huawei guilty on 10 of 12 counts \u2014 trade-secret theft and bank fraud \u2014 and cleared it of racketeering. Sentencing Sep 2027; Huawei will appeal. (US court)')]
CARDS=[('drone','4 ZAPORIZHZHIA · EUROPE','REPORTED','Russian attacks kill 9 across Ukraine in a day','9 killed, 81 hurt; 96 drones launched, 73 shot down or jammed. (Ukrainian officials)'),('trophy','5 CAS · AFRICA / SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','Morocco forfeit 3\u20130, so Senegal win 1\u20130 and take the Africa Cup back. (CAS)'),('ship','6 HORMUZ · MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','Ship hit 18:58 UTC; navigation off, exclusion zone north of Khasab, Oman. (UKMTO)'),('chart','7 NEW YORK · MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','Dow 50,018. Nasdaq \u22121.5%; Taiex +8.99% record 40,122; Kospi +6.3%. (Market close)'),('server','8 REDMOND · TECH','REPORTED','Microsoft declares \u2018Code Red\u2019 after historic outage','24h outage, worst ever for Exchange Online. Recovery in 1h; 11,000+ messages. (Reuters)'),('heli','9 ESKISEHIR · EUROPE','REPORTED','Turkish military helicopter crash kills 5','An AS-532 military helicopter came down in Eskisehir; 5 killed. 19:52 UTC. (Turkish officials)'),('market','10 CARTAGENA · AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','25 held; 5 elderly women freed; airport landings paused ~45 min. (Colombia officials)'),('arrow','11 ADEN · MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces push to 60 km from Aden, Yemen. 16:51 UTC. (Wires)'),('blast','12 LAHJ · MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Wadi Maabaq, Lahj: 25 killed or missing, 6 wounded. 10:42 UTC. (Yemen officials)'),('rocket','13 JIUQUAN · SPACE','OFFICIAL','China names first foreign astronaut for Tiangong','Crew: Tang Hongbo, Wu Yi, Zeeshan Ali (Pakistan) \u2014 first foreigner on Tiangong. (CMSA)')]
ALSO=[('Ankara','Haftar visits Turkey for the first time'),('London','UK sanctions Houthis + 4 officials'),('Villavicencio','Car bomb injures 23'),('Gaza','Israel kills Hamas internal security chief'),('Baghdad','Iraq orders federal control of Kurdish oilfields'),('Gaza','Meningitis alert: 272 cases in October, 15 dead in 2026'),('DR Congo','Missing Cessna 208; rebels claim shootdown, 4 aboard'),('Hanoi','Hot-pot blast kills \u22656, \u226510 hurt'),('Gulf of Finland','Ukraine hits Russian ship Sparta II; 16 evacuated'),('Kuala Lumpur','Malaysia to return thousands of migrants to Myanmar'),('Ulleungdo','S. Korea shelter order as Russian jets enter ADIZ'),('Dhaka','Hasina plans return 16 Dec'),('The Hague','14 nations endorse ICJ Myanmar ruling (9\u20136)'),('Jakarta','Indonesia nominates 2 VP candidates'),('Beijing','China sentences official Ma to death for spying'),('Brussels','NATO vows defence against space threat'),('Mexico City','El Chapo Isidro: US drone aided weekend capture'),('San Salvador','Bukele names 3 soldiers killed in Haiti'),('Ottawa','Pentagon rebukes Canada: only 41.9% of air fleet ready'),('Washington','US adds Megaspeed to trade blacklist'),('Kyiv','Zelensky urges Ukraine-Russia-US-Europe talks soon'),('Ras Al Khaimah','UAE bus-truck crash kills 13; bus carried 41'),('London','England record 5,258 heat deaths, summer 2026'),('Kourou','Ariane 6 lofts 36 Amazon satellites'),('Cikande','Factory-fire toll rises to 26')]
UTC=[('02:15','NATO vows space defence'),('08:16','Hanoi hot-pot blast'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
NUMS=[('11','hurt in Riyadh'),('9','killed in Ukraine'),('50,018','Dow, first over 50k'),('+8.99%','Taiex record'),('25','killed or missing, Yemen'),('26','Cikande fire toll'),('10/12','Huawei guilty counts'),('96','drones at Ukraine')]

img=Image.new('RGB',(W,H),CREAM); d=ImageDraw.Draw(img)
d.rectangle([0,0,W,18],fill=RED); d.text((10,3),'THE WORLD ON ONE PAGE',font=F(11,True),fill=(255,255,255)); d.text((W-10,3),'38 STORIES \u00b7 7 REGIONS \u00b7 13 FIELDS \u00b7 ALL FROM TUESDAY 24 NOVEMBER 2026',font=F(10,True),fill=(255,255,255),anchor='ra')
d.text((W//2,24),'Tuesday 24 November 2026',font=F(34,True,True),fill=INK,anchor='ma')
d.text((W//2,62),'Houthi drone hits Riyadh\u2019s tallest tower  \u00b7  China probes Shanghai party chief Chen Jining  \u00b7  Huawei guilty on 10 of 12 counts',font=F(12,False,True),fill=RED,anchor='ma')
REG=[('Europe',7,(30,88,168)),('Middle East',8,(176,32,32)),('Asia',9,(32,118,58)),('Africa',5,(198,108,18)),('Americas',5,(108,58,158)),('Oceania',0,(90,90,90)),('World / Space',4,(24,42,78))]
x=10; unit=(W-20-30)/38
for name,n,c in REG:
    w=30 if n==0 else int(n*unit)
    d.rectangle([x,84,x+w,102],fill=c)
    if n: d.text((x+w//2,87),f'{name} {n}',font=F(9,True),fill=(255,255,255),anchor='ma')
    x+=w
d.rectangle([10,106,W-10,134],fill=(255,255,255),outline=MID); d.text((16,110),'THE DAY IN UTC',font=F(10,True),fill=RED)
ux=150
for t,ev in UTC:
    d.text((ux,110),t,font=F(10,True),fill=INK); d.text((ux,121),ev,font=F(8),fill=GREY); ux+=(W-160)//7
d.rectangle([10,138,W-10,182],fill=NAVY)
d.text((16,142),'THE DAY IN NUMBERS',font=F(10,True),fill=(255,214,110))
nx=170; cw=(W-180)//8
for v,lab in NUMS:
    d.text((nx+cw//2,142),v,font=F(17,True),fill=(255,255,255),anchor='ma'); d.text((nx+cw//2,164),lab,font=F(8),fill=(200,210,230),anchor='ma'); nx+=cw
hy=188; hw=328; hx=[10,348,686]
for i,(k,kick,chp,hl,deck) in enumerate(HERO):
    X=hx[i]; d.rectangle([X,hy,X+hw,hy+212],fill=(255,255,255),outline=INK,width=1)
    scene(d,k,X+1,hy+1,hw-2,100)
    d.text((X+8,hy+108),kick,font=F(9,True),fill=RED)
    cx=chip(d,X+8,hy+124,chp)
    para(d,X+8,hy+140,hl,F(14,True),hw-16,17,INK,2)
    para(d,X+8,hy+176,deck,F(9),hw-16,12,GREY,3)
cy=408; cw2=198; ch2=142
for r in range(2):
    for c in range(5):
        i=r*5+c; k,kick,chp,hl,deck=CARDS[i]; X=10+c*203; Y=cy+r*147
        d.rectangle([X,Y,X+cw2,Y+ch2],fill=(255,255,255),outline=INK,width=1)
        scene(d,k,X+1,Y+1,cw2-2,50)
        d.text((X+6,Y+56),kick,font=F(8,True),fill=RED)
        chip(d,X+6,Y+70,chp)
        para(d,X+6,Y+86,hl,F(10,True),cw2-12,12,INK,2)
        para(d,X+6,Y+112,deck,F(8),cw2-12,10,GREY,2)

my=702
d.text((10,my),'THE WORLD \u2014 WHERE IT HAPPENED',font=F(11,True),fill=INK)
draw_map(d,10,my+16,690,120)
lx=716; d.text((lx,my+16),'PIN  =  STORY NUMBER',font=F(9,True),fill=INK)
d.text((lx,my+32),'1 Riyadh tower hit   2 Shanghai probe',font=F(9),fill=INK)
d.text((lx,my+44),'3 Huawei verdict   4 Ukraine strikes',font=F(9),fill=INK)
d.text((lx,my+56),'5 Senegal AFCON   6 Hormuz ship',font=F(9),fill=INK)
d.text((lx,my+68),'7 Dow 50,018   8 Microsoft Code Red',font=F(9),fill=INK)
d.text((lx,my+80),'9 Eskisehir crash   10 Cartagena siege',font=F(9),fill=INK)
d.text((lx,my+92),'11 Aden advance   12 Lahj strikes',font=F(9),fill=INK)
d.text((lx,my+104),'13 Tiangong crew named',font=F(9),fill=INK)
d.text((lx,my+122),'CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record',font=F(8),fill=GREY)
d.text((lx,my+133),'REPORTED = one outlet \u00b7 CLAIM = one side',font=F(8),fill=GREY)
ay=842; d.text((10,ay),'ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES',font=F(11,True),fill=RED)
for i,(city,hl) in enumerate(ALSO):
    col=i//9; row=i%9; X=10+col*338; Y=ay+16+row*10
    d.text((X,Y),f'{14+i}',font=F(8,True),fill=RED); d.text((X+20,Y),f'{city}: {hl}',font=F(8),fill=INK)
dy=950; d.rectangle([10,dy,W-10,1008],fill=(255,235,235),outline=RED,width=1)
d.text((16,dy+4),'DATE CHECK',font=F(10,True),fill=RED)
para(d,16,dy+16,'Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC.',F(9),W-32,12,INK,1)
para(d,16,dy+28,'LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov) \u00b7 Nvidia Huang returns as CEO (23 Nov) \u00b7 EU sanctions package 22 (23 Nov) \u00b7 COP31 ends with no deal (22 Nov) \u00b7 corvette Merkury sinks (22 Nov) \u00b7 El Chapo Isidro captured (20 Nov) \u00b7 Cikande factory fire starts (21 Nov) \u00b7 Shenzhou-24 launch (25 Nov) \u00b7 Trump hush-money appeal ruling (23 Nov) \u00b7 ATP Finals (22 Nov) \u00b7 F1 Las Vegas GP (21 Nov) \u00b7 ICJ Myanmar ruling (last week).',F(8),W-32,10,GREY,2)
para(d,16,dy+48,'NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC) \u00b7 MPR vote for VP (11 Dec) \u00b7 Huawei sentencing (Sep 2027) \u00b7 Hasina returns to Bangladesh (16 Dec).',F(8),W-32,10,GREY,1)
d.text((10,1010),'Sources: Saudi officials \u00b7 CCDI \u00b7 US court \u00b7 Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CMSA \u00b7 wires. Scenes are drawn illustrations, not photographs.',font=F(8),fill=GREY)
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True); img.save(OUT,optimize=True)
print('saved',OUT,img.size,os.path.getsize(OUT))
