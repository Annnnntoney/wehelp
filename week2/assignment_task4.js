// Task 4: 找出最適合載 n 位乘客的車廂索引

function func4(sp, stat, n) {
  let bestIndex = -1;
  let bestDiff = Infinity;
  for (let i = 0; i < sp.length; i++) {
    if (stat[i] === "0") {              
      const diff = Math.abs(sp[i] - n); 
      if (diff < bestDiff) {
        bestDiff = diff;
        bestIndex = i;
      }
    }
  }
  console.log(bestIndex);
}

func4([3, 1, 5, 4, 3, 2], "101000", 2);   // print 5
func4([1, 0, 5, 1, 3], "10100", 4);       // print 4
func4([4, 6, 5, 8], "1000", 4);           // print 2
