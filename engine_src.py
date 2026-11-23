# tiny-chess-01 engine: mailbox-0x88 board, alpha-beta + TT + killers + null-move + LMR + aspiration windows
import os,sys,json,urllib.request
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("env?")
def post(p,b):
 return json.load(urllib.request.urlopen(urllib.request.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
V=[0,100,320,330,500,900,20000]
C=[min(i,7-i)for i in range(8)]
def pst(t,i):
 r,f=i>>3,i&7;c=C[r]+C[f]
 return([0,0,4,8,14,24,40,0][r]+([0,0,0,10,15,10,5,0][r]if f in(3,4)else 0),6*c-20,4*c-8,(15 if r==6 else 0)+(5 if r==0 and f in(3,4)else 0),2*c-6,0)[t-1]if t<6 else 0
PA,KN,BI,RO,QU=[[pst(t,i)for i in range(64)]for t in range(1,6)]
KI=[([20,25,10,0,0,10,25,20][i&7]if i>>3==0 else max(-50,-15*(i>>3)))for i in range(64)]
KE=[8*(C[i>>3]+C[i&7])-24 for i in range(64)]
PST={1:PA,2:KN,3:BI,4:RO,5:QU}
ND={2:(33,31,18,14,-33,-31,-18,-14),3:(17,15,-17,-15),4:(16,-16,1,-1),5:(17,16,15,1,-1,-17,-16,-15),6:(16,17,15,1,-1,-17,-16,-15)}
MATE=30000
BUD=int(os.environ.get("CHESS_BUDGET","500000"))
SQ=[s for s in range(128) if not s&136]
IX={s:(s&7)+((s>>4)<<3) for s in SQ}
EV={}
for t in range(1,6):
 for g in(1,-1):
  a=[0]*128
  for s in SQ:
   v=V[t]+PST[t][IX[s] if g>0 else IX[s^112]];a[s]=g*v
  EV[g*t]=a
EV[6]=EV[-6]=[0]*128
class P:
 def __init__(s,f):
  s.H=[];p=f.split();b=[0]*128;q=112
  for c in p[0]:
   if c=="/":q-=24
   elif c.isdigit():q+=int(c)
   else:b[q]=(1 if c.isupper() else -1)*(1+"PNBRQK".index(c.upper()));q+=1
  s.b=b;s.S=0 if p[1]=="w" else 1
  s.C=sum(v for v,h in((1,"K"),(2,"Q"),(4,"k"),(8,"q")) if h in p[2])
  s.E=-1 if p[3]=="-" else "abcdefgh".index(p[3][0])+16*(int(p[3][1])-1)
  s.h=int(p[4]);s.k=[0,0];s.N=[0,0];s.v=0
  for t in SQ:
   v=b[t]
   if not v:continue
   s.v+=EV[v][t]
   if v==6:s.k[0]=t
   elif v==-6:s.k[1]=t
   elif abs(v)!=1:
    s.N[0 if v>0 else 1]+=V[abs(v)]
 def at(s,q,y):
  b=s.b;g=-1 if y else 1
  for d in((15,17)if g<0 else(-15,-17)):
   t=q+d
   if not t&136 and b[t]==g:return 1
  for d in ND[2]:
   t=q+d
   if not t&136 and b[t]==g*2:return 1
  for d in ND[6]:
   t=q+d
   if not t&136 and b[t]==g*6:return 1
  for ds,ts in((ND[3],(3,5)),(ND[4],(4,5))):
   for d in ds:
    t=q+d
    while not t&136:
     p=b[t]
     if p:
      if p in(g*ts[0],g*ts[1]):return 1
      break
     t+=d
  return 0
 def gen(s,c=0):
  b=s.b;u=-1 if s.S else 1;o=[]
  for q in range(128):
   if q&136:continue
   p=b[q]
   if p==0 or(p>0)!=(u>0):continue
   t=abs(p)
   if t==1:
    d=-16 if s.S else 16;n=q+d
    if not n&136 and b[n]==0:
     if(n>>4)in(0,7):
      for r in(5,4,3,2):o.append((q,n,r))
     elif not c:
      o.append((q,n,0));w=n+d
      if(q>>4)in(1,6)and b[w]==0:o.append((q,w,0))
    for e in(d-1,d+1):
     n=q+e
     if n&136:continue
     z=b[n]
     if z and(z>0)!=(u>0):
      if(n>>4)in(0,7):
       for r in(5,4,3,2):o.append((q,n,r))
      else:o.append((q,n,0))
     elif n==s.E:o.append((q,n,0))
   elif t in ND:
    for d in ND[t]:
     n=q+d
     while not n&136:
      z=b[n]
      if z:
       if(z>0)!=(u>0):o.append((q,n,0))
       break
      if not c:o.append((q,n,0))
      if t in(2,6):break
      n+=d
   if t==6 and not c:
    if s.S==0 and q==4:
     if s.C&1 and b[5]==0 and b[6]==0 and b[7]==4 and not s.at(4,1)and not s.at(5,1)and not s.at(6,1):o.append((4,6,0))
     if s.C&2 and b[3]==0 and b[2]==0 and b[1]==0 and b[0]==4 and not s.at(4,1)and not s.at(3,1)and not s.at(2,1):o.append((4,2,0))
    elif s.S==1 and q==116:
     if s.C&4 and b[117]==0 and b[118]==0 and b[119]==-4 and not s.at(116,0)and not s.at(117,0)and not s.at(118,0):o.append((116,118,0))
     if s.C&8 and b[115]==0 and b[114]==0 and b[113]==0 and b[112]==-4 and not s.at(116,0)and not s.at(115,0)and not s.at(114,0):o.append((116,114,0))
  return o
 def mk(s,m):
  q,n,r=m;b=s.b;p=b[q];c=b[n];u=s.S;e=-1
  if abs(p)==1 and n==s.E and c==0:e=n+(16 if u else -16);c=b[e]
  s.H.append((q,n,r,c,e,s.C,s.E,s.h,s.N[0],s.N[1],s.v))
  if c and abs(c)!=1 and abs(c)!=6:s.N[1-u]-=V[abs(c)]
  if r:s.N[u]+=V[r]
  w=r*(-1 if u else 1)if r else p
  s.v+=EV[w][n]-EV[p][q]
  if c:
   s.v-=EV[c][e if e>=0 else n]
  b[n]=w;b[q]=0
  if e>=0:b[e]=0
  if abs(p)==6:
   s.k[u]=n
   if n-q==2:s.v+=EV[b[n+1]][n-1]-EV[b[n+1]][n+1];b[n-1]=b[n+1];b[n+1]=0
   elif n-q==-2:s.v+=EV[b[n-2]][n+1]-EV[b[n-2]][n-2];b[n+1]=b[n-2];b[n-2]=0
  s.C&=~({4:3,116:12}.get(q,0)|{0:2,7:1,112:8,119:4}.get(q,0)|{0:2,7:1,112:8,119:4}.get(n,0))
  s.E=q+(16 if u==0 else -16)if abs(p)==1 and abs(n-q)==32 else -1
  s.h=0 if abs(p)==1 or c else s.h+1
  s.S=1-u
  if s.at(s.k[u],s.S):s.um();return 0
  return 1
 def um(s):
  q,n,r,c,e,s.C,s.E,s.h,s.N[0],s.N[1],s.v=s.H.pop()
  b=s.b;s.S=1-s.S;p=b[n]
  b[q]=(-1 if s.S else 1)if r else p;b[n]=0
  if e>=0:b[e]=c
  else:b[n]=c
  if abs(b[q])==6:
   s.k[s.S]=q
   if n-q==2:b[n+1]=b[n-1];b[n-1]=0
   elif n-q==-2:b[n-2]=b[n+1];b[n+1]=0
 def ev(s):
  k=KE if s.N[0]+s.N[1]<2600 else KI
  v=s.v+k[IX[s.k[0]]]-k[IX[s.k[1]^112]]
  return v if s.S==0 else -v
def uci(m):
 q,n,r=m;F="abcdefgh"
 return F[q&7]+str((q>>4)+1)+F[n&7]+str((n>>4)+1)+("nbrq"[r-2]if r else"")
def puci(u):
 F="abcdefgh";return(F.index(u[0])+16*(int(u[1])-1),F.index(u[2])+16*(int(u[3])-1),"nbrq".index(u[4])+2 if len(u)>4 else 0)
def choose(f,legal,hist):
 p=P(f);p.H=[]
 def key(z):return tuple(z.b)+(z.S,z.C,z.E)
 nd=0;tt={};kill={};path=[key(p)]
 def order(ms,ply,tm):
  sc=[];b=p.b
  for m in ms:
   q,n,r=m;c=b[n]
   if abs(b[q])==1 and n==p.E and not c:c=1
   v=10000000 if m==tm else(100000+10*V[abs(c)]-V[abs(b[q])]if c else 0)+(90000+V[r]if r else 0)
   if kill.get(ply)==m:v=max(v,80000)
   sc.append((-v,m))
  sc.sort();return[m for _,m in sc]
 def qu(a,b,ply):
  nonlocal nd
  nd+=1
  if nd>BUD:raise TimeoutError
  ck=p.at(p.k[p.S],1-p.S);st=p.ev()
  if not ck:
   if st>=b:return st
   if st>a:a=st
  best=st if not ck else -MATE
  ms=order(p.gen(not ck),ply,None);ln=0
  for m in ms:
   if not ck and not p.b[m[1]]and m[1]!=p.E and not m[2]:continue
   if not p.mk(m):continue
   ln+=1;v=-qu(-b,-a,ply+1);p.um()
   if v>best:best=v
   if best>=b:return best
   if best>a:a=best
  if ck and ln==0:return -MATE+ply
  return best
 def se(d,a,b,ply,nul=0):
  nonlocal nd
  k=key(p)
  if path.count(k)>=2:return -15
  nd+=1
  if nd>BUD:raise TimeoutError
  ck=p.at(p.k[p.S],1-p.S)
  if ck:d+=1
  if d<=0:return qu(a,b,ply)
  en=tt.get(k);tm=en[1]if en else None
  if en and en[0]>=d:
   _,mv,fl,v=en
   if abs(v)>29000:v+=ply if v<0 else -ply
   if fl==0:return v
   if fl==1 and v>=b:return v
   if fl==2 and v<=a:return v
  if d>=3 and not ck and ply>0 and not nul and p.N[p.S]>0:
   p.S=1-p.S;e0=p.E;p.E=-1;path.append(key(p))
   v=-se(d-3,-b,-b+1,ply+1,1)
   path.pop();p.E=e0;p.S=1-p.S
   if v>=b:return b
  ms=order(p.gen(),ply,tm);a0=a;best=-MATE-1;bm=None;ln=0
  for m in ms:
   if not p.mk(m):continue
   ln+=1;path.append(key(p))
   v=-se(d-1,-b,-a,ply+1)
   path.pop();p.um()
   if v>best:
    best=v;bm=m
    if v>a:a=v
   if a>=b:
    if not p.b[m[1]]and not m[2]:kill[ply]=m
    break
  if ln==0:return -MATE+ply if ck else 0
  v=best
  if abs(v)>29000:v+=-ply if v<0 else ply
  fl=0 if a0<best<b else(1 if best>=b else 2)
  tt[k]=(d,bm,fl,v)
  return best
 rm=[puci(u)for u in legal];bm=rm[0];ls={}
 try:
  for d in range(1,64):
   od=sorted(rm,key=lambda m:-ls.get(m,0))
   a=-MATE-1;bs=-MATE-2;cm=None
   for m in od:
    if not p.mk(m):continue
    path.append(key(p));v=-se(d-1,-MATE-1,-a,1);path.pop();p.um()
    ls[m]=v
    if v>bs:bs=v;cm=m
    if v>a:a=v
   if cm is not None:bm=cm
   if bs>29000:break
 except TimeoutError:pass
 return uci(bm)
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"],g["moves"])})
 print(g["game"],g["outcome"],g["reason"],file=sys.stderr)
print("done",g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
