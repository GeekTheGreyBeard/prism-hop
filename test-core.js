const assert=require('assert');
const c=require('./game-core.js');
assert.equal(c.LEVELS.length,6,'six escalating routes');
assert.deepEqual(c.LEVELS.map(x=>x.name),['Dawn Array','Mirror Steps','Signal Bloom','Night Relay','Prism Storm','Aurora Apex']);
for(const l of c.LEVELS){const ts=c.tiles(l.rows);assert.equal(ts.length,l.rows*(l.rows+1)/2);assert.equal(c.move(l.rows,0,'ul'),-1);assert.equal(c.move(l.rows,0,'ur'),-1);assert.equal(c.move(l.rows,0,'dl'),1);assert.equal(c.move(l.rows,0,'dr'),2);for(const t of ts){const p=c.pos(l.rows,t.id,220);assert(p.x>0&&p.x<220&&p.y>=0,'tile stays on board')}}
for(let i=1;i<c.LEVELS.length;i++){assert(c.LEVELS[i].rows>=c.LEVELS[i-1].rows);assert(c.LEVELS[i].enemies>=c.LEVELS[i-1].enemies);assert(c.LEVELS[i].tempo<c.LEVELS[i-1].tempo)}
console.log('core checks passed: board topology, bounds, and route escalation');
