const { random } = require('./src/generator/utils');
const fs = require('fs');
const process = require('process');

const structure = {
  autocomplete: random(4),  
  badge: random(5), 
  bottom-sheet: random(4), 
  button: random(6), 
  buttontoggle: random(3), 
  card: random(2), 
  checkbox: random(3),
  chips: random(4), 
  datepicker: random(4), 
  dialog: random(2), 
  expansion-panel: random(2), 
  form-field: random(7), 
  input-text-field: random(9), 
  input-text-area: random(9), 
  list: random(3), 
  menu: random(4), 
  paginator: 0, 
  progress-bar: random(4), 
  radio-buttons: random(2), 
  select-material-selector: random(4),
  select-native-selector: random(4),
  side-nav: random(3), 
  slide-toggle: random(4),
  slider: random(6), 
  snackbar: 0, 
  table: random(4), 
  tabs: random(6),  
  tree: random(2), 
};

/*const structure = 
    [
        () => ({ key: "autocomplete", value: { type: random(4) } }),
        () => ({ key: "badge", value: { type: random(5) } }),
        () => ({ key: "bottomSheet", value: { type: random(4) } }),
        () => ({ key: "button", value: { type: random(6) } }),
        () => ({ key: "buttonToggle", value: { type: random(3) } }),
        () => ({ key: "card", value: { type: random(2) } }),
        () => ({ key: "checkbox", value: { type: random(3) } }),
        () => ({ key: "chips", value: { type: random(4) } }),
        () => ({ key: "datepicker", value: { type: random(4) } }),
        () => ({ key: "dialog", value: { type: random(2) } }),
        () => ({ key: "expansionPanel", value: { type: random(2) } }),
        () => ({ key: "formField", value: { type: random(7) } }),
        () => ({ key: "input", value: { type: random(9), data-label: "TextField" } }),
        () => ({ key: "input", value: { type: random(9), data-label: "TextArea" } }),
        () => ({ key: "list", value: { type: random(3) } }),
        () => ({ key: "menu", value: { type: random(4) } }),
        () => ({ key: "paginator", value: {} }),
        () => ({ key: "progressBar", value: { type: random(4) } }),
        () => ({ key: "radio", value: { type: random(2) } }),
        () => ({ key: "select", value: { type: random(4) }, data-label: "NativeSelector" } }),
        () => ({ key: "sidenav", value: { type: random(3) } }),
        () => ({ key: "slideToggle", value: { type: random(4) } }),
        () => ({ key: "slider", value: { type: random(6) } }),
        () => ({ key: "snackbar", value: {} }),
        () => ({ key: "table", value: { type: random(4) } }),
        () => ({ key: "tabs", value: { type: random(6) } }),
        () => ({ key: "toolbar", value: { type: random(5) } }),
        () => ({ key: "tree", value: { type: random(2) } }),
    ];*/

fs.writeFile('src/generationStructure.json', JSON.stringify(structure), (err) => {
  if (err) throw err;
  console.log('generationStructure.json is updated');
});

const outputPath = process.argv[2]; /*outputPath - путь, куда записывается сгенерированный файл*/
console.log('Build to ' + outputPath);

require('child_process').exec("ng build --output-path=" + outputPath, function (err, stdout, stderr) {
  err && console.log(err);
  stdout && console.log(stdout);
  stderr && console.log(stderr);
});

