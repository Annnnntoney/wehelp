// Position
// 1. Assume that coordinate of 悟空 is (0, 0).
// 2. Assume that each cell is 1 distance unit.
// 3. Characters move only horizontally and vertically.
// 4. If a character moves to the other side, add additional 2 distance units.
// 5. If there are multiple characters at the same distance, print them all.

const positions = {
  "悟空": [0, 0],
  "丁滿": [-1, 4],
  "辛巴": [-3, 3],
  "貝吉塔": [-4, -1],
  "弗利沙": [4, -1],
  "特南克斯": [1, -2],
};

function func1(name) {
  // your code here
  const [ax, ay] = positions[name];
  const aSide = (ax + ay) > 1;

  const dists = {};
  for (const other in positions) {
    if (other === name) continue;
    const [bx, by] = positions[other];
    const bSide = (bx + by) > 1;
    let d = Math.abs(ax - bx) + Math.abs(ay - by);
    if (aSide !== bSide) {
      d += 2;
    }
    dists[other] = d;
  }

  const values = Object.values(dists);
  const far = Math.max(...values);
  const near = Math.min(...values);
  const farthest = Object.keys(dists).filter(n => dists[n] === far);
  const closest = Object.keys(dists).filter(n => dists[n] === near);
  console.log("最遠" + farthest.join("、") + "；最近" + closest.join("、"));
}

func1("辛巴");     // print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空");     // print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙");   // print 最遠辛巴；最近特南克斯
func1("特南克斯"); // print 最遠丁滿；最近悟空
