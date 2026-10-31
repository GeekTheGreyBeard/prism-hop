(function(root){
  'use strict';
  const LEVELS=[
    {name:'Dawn Array',rows:8,enemies:1,unstable:[14,27],tempo:330},
    {name:'Mirror Steps',rows:9,enemies:2,unstable:[12,24,35],tempo:310},
    {name:'Signal Bloom',rows:9,enemies:2,unstable:[8,19,31,40],tempo:292},
    {name:'Night Relay',rows:10,enemies:3,unstable:[11,21,34,46,53],tempo:276},
    {name:'Prism Storm',rows:10,enemies:3,unstable:[7,17,29,42,54,59],tempo:260},
    {name:'Aurora Apex',rows:11,enemies:4,unstable:[9,18,30,43,55,63,65],tempo:244}
  ];
  const STEP_X=20,STEP_Y=14,TILE_W=20,TILE_H=11;
  function count(rows){return rows*(rows+1)/2}
  function tiles(rows){const out=[];let id=0;for(let r=0;r<rows;r++)for(let c=0;c<=r;c++)out.push({id:id++,r,c});return out}
  function at(rows,r,c){return r<0||r>=rows||c<0||c>r?-1:(r*(r+1))/2+c}
  function move(rows,id,dir){const t=tiles(rows)[id];if(!t)return-1;const next={ul:[t.r-1,t.c-1],ur:[t.r-1,t.c],dl:[t.r+1,t.c],dr:[t.r+1,t.c+1]}[dir];return next?at(rows,next[0],next[1]):-1}
  function worldPos(rows,id){const t=tiles(rows)[id];if(!t)return{x:0,y:0};return{x:(t.c-t.r/2)*STEP_X,y:t.r*STEP_Y}}
  function bounds(rows){const points=tiles(rows).map(t=>worldPos(rows,t.id));return {minX:Math.min(...points.map(p=>p.x))-TILE_W/2,maxX:Math.max(...points.map(p=>p.x))+TILE_W/2,minY:-TILE_H/2,maxY:Math.max(...points.map(p=>p.y))+TILE_H*1.8}}
  function clamp(n,a,b){return Math.max(a,Math.min(b,n))}
  function cameraFor(rows,id,viewW,viewH){const b=bounds(rows),p=worldPos(rows,id),pad=8;const minCx=b.minX-viewW/2+pad,maxCx=b.maxX+viewW/2-pad,minCy=b.minY-viewH/2+pad,maxCy=b.maxY+viewH/2-pad;return{x:clamp(p.x,minCx,maxCx),y:clamp(p.y,minCy,maxCy),bounds:b}}
  function project(world,camera,viewW,viewH){return{x:Math.round(viewW/2+(world.x-camera.x)),y:Math.round(viewH/2+(world.y-camera.y))}}
  function enemyPath(rows,index){const ts=tiles(rows),path=[];for(let r=rows-1;r>=0;r--){const row=ts.filter(t=>t.r===r);if((r+index)%2)row.reverse();path.push(...row.map(t=>t.id))}return index%2?path.slice().reverse():path}
  function routeSignature(level){return `${level.rows}/${count(level.rows)}/${level.enemies}/${level.unstable.length}/${level.tempo}`}
  const api={LEVELS,STEP_X,STEP_Y,TILE_W,TILE_H,count,tiles,at,move,worldPos,bounds,cameraFor,project,enemyPath,routeSignature};
  if(typeof module!=='undefined')module.exports=api;root.PrismCore=api;
})(typeof window!=='undefined'?window:globalThis);
