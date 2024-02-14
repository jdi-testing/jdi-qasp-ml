const { random } = require('./src/generator/utils');
const fs = require('fs');
const process = require('process');

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
  inputTextField: random(7),
  inputTextArea: 7 + random(2),
  list: random(3),
  menu: random(4),
  paginator: 0,
  progressBar: random(4),
  radio: random(2),
  selectMaterial: random(2),
  selectNative: 2 + random(2),
  sidenav: random(3),
  slideToggle: random(4),
  slider: random(6),
  snackbar: 0,
  sortHeader: 0,
  stepper: random(3),
  table: random(4),
  tabs: random(6),
  toolbar: random(5),
  tree: random(2),
};

fs.writeFile('src/generationStructure.json', JSON.stringify(structure), (err) => {
  if (err) throw err;
  console.log('generationStructure.json is updated');
});

const outputPath = process.argv[2];
console.log('Build to ' + outputPath);

require('child_process').exec("ng build --output-path=" + outputPath, function (err, stdout, stderr) {
// require('child_process').exec("ng build", function (err, stdout, stderr) {
  err && console.log(err);
  stdout && console.log(stdout);
  stderr && console.log(stderr);
});

