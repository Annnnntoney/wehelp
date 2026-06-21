const bookings = {};

function isFree(name, start, end) {
  const slots = bookings[name] || [];
  for (const [s, e] of slots) {
    if (start < e && s < end) return false;  
  }
  return true;
}

function func2(ss, start, end, criteria) {

  let op, field, value;
  if (criteria.includes(">=")) {
    op = ">=";
    [field, value] = criteria.split(">=");
  } else if (criteria.includes("<=")) {
    op = "<=";
    [field, value] = criteria.split("<=");
  } else {
    op = "=";
    [field, value] = criteria.split("=");
  }

  const candi = [];
  for (const s of ss) {
    if (!isFree(s.name, start, end)) continue;   
    if (op === "=") {
      if (s.name === value) candi.push(s);
    } else {
      const num = parseFloat(value);
      if (op === ">=" && s[field] >= num) candi.push(s);
      else if (op === "<=" && s[field] <= num) candi.push(s);
    }
  }

  if (candi.length === 0) {
    console.log("Sorry");
    return;
  }


  let best;
  if (op === ">=") {
    best = candi.reduce((a, b) => (a[field] <= b[field] ? a : b)); // 值最小
  } else if (op === "<=") {
    best = candi.reduce((a, b) => (a[field] >= b[field] ? a : b)); // 值最大
  } else {
    best = candi[0];
  }


  if (!bookings[best.name]) bookings[best.name] = [];
  bookings[best.name].push([start, end]);
  console.log(best.name);
}

const services = [
  {"name": "S1", "r": 4.5, "c": 1000},
  {"name": "S2", "r": 3,   "c": 1200},
  {"name": "S3", "r": 3.8, "c": 800}
];

func2(services, 15, 17, "c>=800");   // S3
func2(services, 11, 13, "r<=4");     // S3
func2(services, 10, 12, "name=S3");  // Sorry
func2(services, 15, 18, "r>=4.5");   // S1
func2(services, 16, 18, "r>=4");     // Sorry
func2(services, 13, 17, "name=S1");  // Sorry
func2(services, 8, 9, "c<=1500");    // S2
