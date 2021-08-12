const lorem = require('./src/generator/loremIpsum');
const { random, randomBool } = require('./src/generator/utils');
const fs = require('fs');

const structure = {
    data: Math.random(),
    autocomplete: random(4),
    badge: random(5),
};

fs.writeFile('src/generationStructure.txt', JSON.stringify(structure), (err) => {
  if (err) throw err;
  console.log('The file is rewritten!');
});

require('child_process').exec("npm run start", function (err, stdout, stderr) {
    err && console.log(err);
    stdout && console.log(stdout);
    stderr && console.log(stderr);
});

