var needs_better_name = ["open", "closed"];
var data = [
  { date: "1000000000", open: [nan, nan], closed: 0 },
  { date: "1000000001", open: [1.0, 1.0], closed: 0 },
  { date: "1000000002", open: [2.0, 1.0], closed: 0 },
  { date: "1000000003", open: [3.0, 1.0], closed: 0 },
  { date: "1000000004", open: [4.0, 4.0], closed: 0 },
  { date: "1000000005", open: [4.0, 4.0], closed: 0 },
  { date: "1000000006", open: [5.0, 6.0], closed: 0 },
  { date: "1000000007", open: [6.0, 9.0], closed: 0 },
  { date: "1000000008", open: [6.0, 9.0], closed: 0 },
  { date: "1000000009", open: [6.0, 9.0], closed: 0 },
  { date: "1000000010", open: [6.0, 9.0], closed: 0 },
  { date: "1000000011", open: [nan, nan], closed: 0 },
  { date: "1000000012", open: [nan, nan], closed: 0 },
];

(function() {
  var format = pv.Format.date("%s");
  data.forEach(function(d) { d.date = format.parse(d.date); });
})();
