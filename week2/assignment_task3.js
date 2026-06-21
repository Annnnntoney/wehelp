
function func3(index) {
  const diffs = [-2, -3, 1, 2];   
  let value = 25;                 
  for (let k = 0; k < index; k++) {   
    value += diffs[k % 4];     
  }
  console.log(value);
}

func3(1);   // print 23
func3(5);   // print 21
func3(10);  // print 16
func3(30);  // print 6
