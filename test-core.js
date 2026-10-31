const assert=require('assert');
const c=require('./game-core.js');
assert.equal(c.LEVELS.length,6,'six escalating routes');
assert.deepEqual(c.LEVELS.map(x=>x.name),['Dawn Array','Mirror Steps','Signal Bloom','Night Relay','Prism Storm','Aurora Apex']);
assert(c.LEVELS[0].rows>=8,'opening route is meaningfully larger than the former 4-row board');
assert(c.count(c.LEVELS[0].rows)>=36,'opening board has at least 36 playable prisms');
for(const l of c.LEVELS){
  const ts=c.tiles(l.rows),b=c.bounds(l.rows);
  assert.equal(ts.length,c.count(l.rows));
  assert.equal(c.move(l.rows,0,'ul'),-1);assert.equal(c.move(l.rows,0,'ur'),-1);assert.equal(c.move(l.rows,0,'dl'),1);assert.equal(c.move(l.rows,0,'dr'),2);
  assert(b.maxY-b.minY>100,'board is taller than the 149px camera view');
  const top=c.cameraFor(l.rows,0,230,149),bottom=c.cameraFor(l.rows,ts.length-1,230,149);
  assert(bottom.y>top.y,'camera scrolls as player travels down the enlarged board');
  for(const t of ts){const projected=c.project(c.worldPos(l.rows,t.id),bottom,230,149);assert(Number.isFinite(projected.x)&&Number.isFinite(projected.y));}
  const path=c.enemyPath(l.rows,0);assert.equal(path.length,ts.length);assert.equal(new Set(path).size,ts.length);
}
for(let i=1;i<c.LEVELS.length;i++){
  assert(c.LEVELS[i].rows>=c.LEVELS[i-1].rows);assert(c.LEVELS[i].enemies>=c.LEVELS[i-1].enemies);assert(c.LEVELS[i].tempo<c.LEVELS[i-1].tempo);
}
assert.equal(c.count(11),66,'final board more than doubles former 28-prism finale');
console.log('core checks passed: enlarged boards, camera bounds, topology, paths, and escalation');
