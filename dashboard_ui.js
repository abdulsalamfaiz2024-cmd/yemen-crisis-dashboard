// Independent navigation: works even if a dashboard chart or map fails.
(function(){
 function setup(){
  const d=document.getElementById('drawer'),o=document.getElementById('drawer-overlay');
  if(!d||!o)return;
  const triggers=[...document.querySelectorAll('[data-drawer-toggle]')],closeBtn=document.getElementById('drawer-close');
  const set=open=>{
   d.classList.toggle('active',open);o.classList.toggle('active',open);
   d.setAttribute('aria-hidden',String(!open));triggers.forEach(x=>x.setAttribute('aria-expanded',String(open)));
  };
  triggers.forEach(x=>x.addEventListener('click',e=>{e.preventDefault();set(!d.classList.contains('active'))}));
  o.addEventListener('click',()=>set(false));
  if(closeBtn)closeBtn.addEventListener('click',e=>{e.preventDefault();set(false)});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')set(false)});
  set(false);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup,{once:true});
 else setup();
})();

// Local canvas fallback: the original Chart.js remains first choice.
// A blocked third-party CDN must not leave the user's dashboard empty.
(function(){
 if(window.Chart)return;
 function color(c,i){
  if(Array.isArray(c))return c[i%c.length];
  if(typeof c==='string'&&c.trim()&&!c.startsWith('var('))return c;
  return ['#38bdf8','#14b8a6','#f59e0b','#8b5cf6','#ef4444'][i%5];
 }
 const num=v=>typeof v==='number'?v:(v&&typeof v.y==='number'?v.y:null);
 const values=d=>(d||[]).map(num);
 const rect=(ctx,x,y,w,h,c)=>{
  ctx.fillStyle=c;ctx.beginPath();
  if(ctx.roundRect)ctx.roundRect(x,y,Math.max(0,w),Math.max(0,h),Math.min(5,h/2));
  else ctx.rect(x,y,Math.max(0,w),Math.max(0,h));
  ctx.fill();
 };
 function makeCanvas(el){
  const box=el.getBoundingClientRect(),w=Math.max(270,box.width||400),h=Math.max(180,box.height||230);
  const ratio=Math.min(2,window.devicePixelRatio||1);
  el.width=Math.round(w*ratio);el.height=Math.round(h*ratio);
  const ctx=el.getContext('2d');ctx.setTransform(ratio,0,0,ratio,0,0);
  ctx.clearRect(0,0,w,h);
  return{ctx,w,h};
 }
 class CanvasChart {
  static defaults={color:'#64748b',borderColor:'#e2e8f0',font:{family:'Arial'}};
  constructor(el,config){
   this.canvas=typeof el==='string'?document.getElementById(el):(el&&el.canvas?el.canvas:el);
   if(!this.canvas)throw Error('Missing chart canvas');
   this.config=config;this.options=config.options||{};this.data=config.data||{};
   this._resize=()=>this.update();
   window.addEventListener('resize',this._resize);this.update();
  }
  destroy(){window.removeEventListener('resize',this._resize);this.canvas?.getContext('2d')?.clearRect(0,0,this.canvas.width,this.canvas.height)}
  update(){
   const{ctx,w,h}=makeCanvas(this.canvas),data=this.data,datasets=data.datasets||[],kind=this.config.type||'bar';
   const names=data.labels||[], textColor=CanvasChart.defaults.color||'#64748b';
   ctx.font='11px Arial';ctx.textBaseline='middle';
   const sectors=kind==='doughnut'||kind==='pie'||kind==='polarArea';
   if(sectors){
    const ds=datasets[0]||{},v=values(ds.data).map(a=>Math.max(0,a||0)),sum=v.reduce((a,b)=>a+b,0)||1;
    const cx=w/2,cy=h/2,r=Math.max(25,Math.min(w*.32,h*.38));let start=-Math.PI/2;
    v.forEach((x,i)=>{const end=start+Math.PI*2*x/sum;ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,start,end);ctx.closePath();ctx.fillStyle=color(ds.backgroundColor,i);ctx.fill();start=end});
    if(kind==='doughnut'){ctx.beginPath();ctx.arc(cx,cy,r*.56,0,Math.PI*2);ctx.fillStyle=getComputedStyle(this.canvas).backgroundColor||'#fff';ctx.fill();}
    return;
   }
   if(kind==='radar'){
    const vs=values(datasets[0]?.data),n=vs.length;if(!n)return;
    const cx=w/2,cy=h/2,r=Math.min(w,h)*.37,max=Math.max(100,...vs.map(v=>v||0));
    ctx.strokeStyle='#94a3b84d';ctx.lineWidth=1;
    [0.25,.5,.75,1].forEach(t=>{ctx.beginPath();for(let i=0;i<n;i++){const a=-Math.PI/2+2*Math.PI*i/n;const xx=cx+r*t*Math.cos(a),yy=cy+r*t*Math.sin(a);i?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy)}ctx.closePath();ctx.stroke()});
    ctx.beginPath();vs.forEach((v,i)=>{const a=-Math.PI/2+2*Math.PI*i/n;const x=cx+r*(v||0)/max*Math.cos(a),y=cy+r*(v||0)/max*Math.sin(a);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});
    ctx.closePath();ctx.fillStyle='#38bdf840';ctx.fill();ctx.strokeStyle='#38bdf8';ctx.lineWidth=2;ctx.stroke();
    return;
   }
   const horizontal=kind==='bar'&&this.options.indexAxis==='y';
   const n=Math.max(names.length,...datasets.map(d=>(d.data||[]).length),1);
   const all=datasets.flatMap(d=>values(d.data).filter(v=>v!==null&&!Number.isNaN(v))),min=Math.min(0,...all),max=Math.max(1,...all);
   const left=horizontal?Math.min(122,w*.33):42,right=14,top=24,bottom=horizontal?24:43,pw=w-left-right,ph=h-top-bottom;
   ctx.strokeStyle='#94a3b835';ctx.fillStyle=textColor;ctx.textAlign='left';ctx.lineWidth=1;
   for(let k=0;k<=4;k++){const y=top+ph*k/4;ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(w-right,y);ctx.stroke();}
   const v2x=v=>left+(v-min)/(max-min||1)*pw;
   const v2y=v=>top+ph-(v-min)/(max-min||1)*ph;
   if(kind==='line'){
    datasets.forEach((ds,i)=>{
     const arr=values(ds.data);ctx.strokeStyle=color(ds.borderColor,i);ctx.lineWidth=2.5;ctx.beginPath();let started=false;
     arr.forEach((v,j)=>{if(v===null||!Number.isFinite(v)){started=false;return;}const x=left+(j+.5)*pw/n,y=v2y(v);if(!started){ctx.moveTo(x,y);started=true}else ctx.lineTo(x,y)});
     ctx.stroke();arr.forEach((v,j)=>{if(v===null||!Number.isFinite(v))return;ctx.beginPath();ctx.arc(left+(j+.5)*pw/n,v2y(v),2.7,0,Math.PI*2);ctx.fillStyle=color(ds.borderColor,i);ctx.fill();});
    });
   }else{
    const stacks=datasets.length,group=horizontal?ph/n:pw/n,barW=Math.min(25,group*.74/Math.max(1,stacks));
    datasets.forEach((ds,i)=>values(ds.data).forEach((v,j)=>{if(v===null||!Number.isFinite(v))return;
     const fill=color(ds.backgroundColor,i);
     if(horizontal){const y=top+j*group+(group-barW*stacks)/2+i*barW,zero=v2x(0),vx=v2x(v);rect(ctx,Math.min(zero,vx),y,Math.abs(vx-zero),barW-2,fill);}
     else{const x=left+j*group+(group-barW*stacks)/2+i*barW,zero=v2y(0),vy=v2y(v);rect(ctx,x,Math.min(zero,vy),barW-2,Math.abs(vy-zero),fill);}
    }));
   }
   ctx.fillStyle=textColor;ctx.font='10px Arial';
   const stride=Math.max(1,Math.ceil(n/7));
   for(let j=0;j<n;j+=stride){const lab=String(names[j]??j+1).slice(0,horizontal?17:8);
    if(horizontal){ctx.textAlign='right';ctx.fillText(lab,left-7,top+(j+.5)*ph/n)}
    else{ctx.textAlign='center';ctx.fillText(lab,left+(j+.5)*pw/n,h-bottom+15)}
   }
   if(kind==='line'||kind==='bar'){ctx.textAlign='right';for(let i=0;i<=4;i++){const val=min+(max-min)*(4-i)/4;ctx.fillText(Math.abs(val)>=1000?Math.round(val).toLocaleString():val.toFixed(1),left-5,top+ph*i/4)}}
  }
 }
 window.Chart=CanvasChart;
 window.Chart.__fallback=true;
})();


// A self-contained map overview if the user's network blocks third-party tile servers.
window.dashboardMapFallback=function(id,cityData){
 const host=document.getElementById(id);if(!host)return;
 const old=host.querySelector('.local-map-backup');
 if(old)old.remove();
 host.style.position='relative';
 const box=document.createElement('div');
 box.className='local-map-backup';
 box.style.cssText='position:absolute;inset:0;z-index:1300;background:linear-gradient(145deg,#0e2536,#123545 48%,#102335);pointer-events:none;overflow:hidden';
 const xmlns='http://www.w3.org/2000/svg',svg=document.createElementNS(xmlns,'svg');
 svg.setAttribute('viewBox','0 0 900 500');
 svg.setAttribute('preserveAspectRatio','xMidYMid meet');
 svg.style.cssText='width:100%;height:100%';
 const grid=document.createElementNS(xmlns,'path');
 let lines='';
 for(let x=0;x<=900;x+=75)lines+='M'+x+',0V500 ';
 for(let y=0;y<=500;y+=60)lines+='M0,'+y+'H900 ';
 grid.setAttribute('d',lines);
 grid.setAttribute('stroke','#8fd7ed');grid.setAttribute('stroke-opacity','0.09');grid.setAttribute('fill','none');svg.appendChild(grid);
 const rough=document.createElementNS(xmlns,'path');
 rough.setAttribute('d','M112,324 L142,275 L154,205 L179,166 L263,145 L372,122 L480,143 L562,164 L695,197 L762,243 L688,309 L608,340 L533,378 L444,403 L345,411 L245,392 L172,366 Z');
 rough.setAttribute('fill','#174c5a');rough.setAttribute('stroke','#66bed2');rough.setAttribute('stroke-width','2.8');rough.setAttribute('stroke-linejoin','round');svg.appendChild(rough);
 const pts=Array.isArray(cityData)&&cityData.length?cityData:[
  {city_name:"Sana'a",latitude:15.3694,longitude:44.191},
  {city_name:"Aden",latitude:12.7794,longitude:45.0367},
  {city_name:"Taiz",latitude:13.5795,longitude:44.0209},
  {city_name:"Al Hudaydah",latitude:14.7978,longitude:42.9545},
  {city_name:"Ibb",latitude:13.9667,longitude:44.1833},
  {city_name:"Mukalla",latitude:14.5425,longitude:49.1242}
 ];
 pts.slice(0,12).forEach(c=>{
  const lon=Number(c.longitude??c.lon),lat=Number(c.latitude??c.lat);
  if(!Number.isFinite(lon)||!Number.isFinite(lat))return;
  const x=130+(lon-42.5)*80,y=400-(lat-12.5)*47;
  const circle=document.createElementNS(xmlns,'circle');
  circle.setAttribute('cx',x);circle.setAttribute('cy',y);circle.setAttribute('r','4.5');
  circle.setAttribute('fill','#31e8f1');circle.setAttribute('stroke','#ddfbff');circle.setAttribute('stroke-width','1.1');svg.appendChild(circle);
  const t=document.createElementNS(xmlns,'text');t.setAttribute('x',x+8);t.setAttribute('y',y-8);
  t.setAttribute('font-size','12');t.setAttribute('font-family','Arial');t.setAttribute('fill','#c9ebf1');
  t.textContent=c.city_name||c.name||'Location';svg.appendChild(t);
 });
 box.appendChild(svg);
 const subtitle=document.createElement('div');
 subtitle.textContent='YEMEN · REGIONAL OVERVIEW';
 subtitle.style.cssText='position:absolute;top:15px;left:16px;font:700 11px Arial,sans-serif;color:#8fd7ed;letter-spacing:1px';
 box.appendChild(subtitle);
 host.appendChild(box);
};
