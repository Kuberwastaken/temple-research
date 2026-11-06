import json,csv,os,sys,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'svg.fonttype':'none','font.family':'sans-serif','font.size':12,'axes.edgecolor':'#888','axes.labelcolor':'#888','xtick.color':'#888','ytick.color':'#888','text.color':'#888','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'none','axes.facecolor':'none','savefig.transparent':True,'axes.grid':True,'grid.color':'#888','grid.alpha':.2})
R=json.load(open('results.json'))['devices']
root=sys.argv[1]
def raw(p):
 d={}
 if not os.path.exists(p):return d
 for row in csv.DictReader(open(p)):
  try:t=int(float(row['t_s']));v=float(row['hr_bpm'])
  except ValueError:continue
  if 36<=v<=240:d.setdefault(t,[]).append(v)
 return {t:float(np.mean(v)) for t,v in d.items()}
PP={}
for part in sorted(os.listdir(root+'/raw')):
 r=raw(root+'/raw/'+part+'/polar_h10_taped.csv')
 for f in os.listdir(root+'/raw/'+part):
  dv=f[:-4]
  if dv=='polar_h10_taped':continue
  a=raw(root+'/raw/'+part+'/'+f);e=[abs(a[t]-r[t])for t in a if t in r]
  if e:PP.setdefault(dv,{})[part]=(float(np.mean(e)),float(np.median(e)))
D=['temple','apple_watch_s12','fitbit_air','whoop_mg','garmin_forerunner_970','oura_ring_5','polar_h10_untaped'];N=['Temple','Apple S12','Fitbit Air','WHOOP MG','Garmin 970','Oura Ring 5','Polar untaped'];names=dict(zip(D,N));colors=['#4169ff','#858585','#b77932','#8172c8','#42a5a1','#cb658c','#df7b36'];color=dict(zip(D,colors));B=colors[0];O=colors[-1]
def save(fig,n):fig.tight_layout();fig.savefig('img/'+n+'.svg');plt.close(fig)

# NIRS: three horizontal panels as separate figures
vals=[[.912,.494,.826,.832,.649],[.843,.700,.701,.850,.570],[.839,.767,.796,.654,.438]]
titles=['Head-down tilt','Stand to squat','Stand to supine'];ps=['p < 0.001','p < 0.001','p = 0.082'];outs=['nirs-tilt','nirs-squat','nirs-supine']
for v,title,p,out in zip(vals,titles,ps,outs):
 fig,ax=plt.subplots(figsize=(4.8,3.1))
 ax.barh(range(5),v,color=[B,'#888','#a0b4ff','#7589d0',O]);ax.set_yticks(range(5),['Brain, lagged','Scalp, lagged','Brain, zero lag','Brain, HR adj.','Brain, scalp adj.'],fontsize=10);ax.invert_yaxis();ax.set_xlim(0,1.05)
 for i,z in enumerate(v):ax.text(z+.015,i,f'{z:.3f}',va='center',fontsize=10)
 ax.set_title(title+' | '+p,fontsize=11);ax.set_xticks([0,.5,1]);ax.grid(axis='y',alpha=0);ax.set_xlabel('Median correlation')
 save(fig,out)

# age-features: two panels as separate figures
fig,ax=plt.subplots(figsize=(4.8,2.9));ax.bar([0,1],[14,3],color=[B,'#888']);ax.set_xticks([0,1],['Temple','Wrist']);ax.set_ylim(0,17);ax.set_ylabel('Age-linked features /89')
for i,z in enumerate([14,3]):ax.text(i,z+.3,str(z),ha='center')
save(fig,'age-counts')
fig,ax=plt.subplots(figsize=(4.8,3.4));ax.barh([0,1,2],[70,39.5,10.1],color=[B,B,'#888']);ax.set_yticks([0,1,2],['Temple\n(Ad-Ab)/Aa','Temple\nAGImod','Wrist\nAd/Aa'],fontsize=10);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Selected after FDR correction\n(% of 1,000 resamples)')
for i,z in enumerate([70,39.5,10.1]):ax.text(z+2,i,f'{z}%',va='center',fontsize=11)
save(fig,'age-selection')

# hr-paired: two panels as separate figures
for d,out in zip(['apple_watch_s12','polar_h10_untaped'],['hr-paired-apple','hr-paired-polar']):
 fig,ax=plt.subplots(figsize=(4.8,3.3))
 v=sorted(PP[d][p][0]-PP['temple'][p][0] for p in PP[d]);ax.bar(range(len(v)),v,color=[B if z>0 else O for z in v]);ax.axhline(0,color='#888');ax.set_title(names[d]+': Temple wins '+str(sum(z>0 for z in v))+'/43',fontsize=12);ax.set_xticks([]);ax.set_ylabel('Other MAE - Temple MAE');ax.set_xlabel('People, sorted by difference')
 save(fig,out)
print('done')
