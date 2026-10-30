(function(root){
  const LEVELS=[
    {name:'Dawn Array',rows:4,enemies:1,unstable:[],tempo:620},
    {name:'Mirror Steps',rows:5,enemies:1,unstable:[9],tempo:570},
    {name:'Signal Bloom',rows:5,enemies:2,unstable:[5,12],tempo:530},
    {name:'Night Relay',rows:6,enemies:2,unstable:[8,16,19],tempo:490},
    {name:'Prism Storm',rows:6,enemies:3,unstable:[6,13,20,25],tempo:455},
    {name:'Aurora Apex',rows:7,enemies:3,unstable:[9,17,24,29,33],tempo:420}
  ];
  function tiles(rows){const a=[];let id=0;for(let r=0;r<rows;r++)for(let c=0;c<=r;c++)a.push({id:id++,r,c});return a}
  function at(rows,r,c){return r<0||r>=rows||c<0||c>r?-1:(r*(r+1))/2+c}
  function move(rows,id,dir){const t=tiles(rows)[id];if(!t)return-1;const map={ul:[t.r-1,t.c-1],ur:[t.r-1,t.c],dl:[t.r+1,t.c],dr:[t.r+1,t.c+1]};const p=map[dir];return p?at(rows,p[0],p[1]):-1}
  function pos(rows,id,width){const t=tiles(rows)[id], cx=width/2, dx=17, dy=18;return{x:cx+(t.c-t.r/2)*dx*2,y:8+t.r*dy}}
  function enemyPath(rows,index){const count=(rows*(rows+1))/2;const path=[];for(let i=0;i<count;i++)path.push(i); if(index%2)path.reverse(); return path}
  const api={LEVELS,tiles,at,move,pos,enemyPath};
  if(typeof module!=='undefined')module.exports=api;root.PrismCore=api;
})(typeof window!=='undefined'?window:globalThis);
