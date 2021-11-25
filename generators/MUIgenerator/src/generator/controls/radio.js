const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const labelPlacement = ['bottom', 'end', 'start', 'top'];

const generator = () => {
    const groupLength = random(20) + 1;

    const structure = {
        group: [],
        formLabel: lorem.generateWords(1),
        labelPlacement: labelPlacement[random(4)],
        row: randomBool(),
    }

    for (let index = 0; index < groupLength; index++) {
        structure.group.push({
            disabled: randomBool(),
            label: lorem.generateWords(1),
        })
    }

    return structure;
}

module.exports = generator;