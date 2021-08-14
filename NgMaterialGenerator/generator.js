const lorem = require('./src/generator/loremIpsum');
const { random } = require('./src/generator/utils');
const fs = require('fs');

const structure = {
  autocomplete: random(4),
  badge: random(5),
  bottomSheet: random(4),
  button: random(6),
  buttonToggle: random(3),
  card: random(2),
  checkbox: random(3),
  chips: random(4),
  datepicker: random(4),
  dialog: random(2),
  divider: 0,
  expansionPanel: random(2),
  formField: random(7),
  gridList: random(2),
  input: random(9),
  list: random(3),
  menu: random(4),
  paginator: 0,
  progressBar: random(4),
  radio: random(2),
  select: random(4),
  sidenav: random(3),
  slideToggle: random(4),
  slider: random(6),
  snackbar: 0,
  sortHeader: 0,
  spinner: random(2),
  stepper: random(3),
  table: random(4),
  tabs: random(6),
  toolbar: random(5),
  tree: random(2),
};

fs.writeFile('src/generationStructure.json', JSON.stringify(structure), (err) => {
  if (err) throw err;
  console.log('The file is rewritten!');
});

require('child_process').exec("npm run build", function (err, stdout, stderr) {
  err && console.log(err);
  stdout && console.log(stdout);
  stderr && console.log(stderr);
});

