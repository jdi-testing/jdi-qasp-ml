const lorem = require('../loremIpsum');
const { random } = require('../utils');

const generator = () => {
    const structure = {
        basic: { type: random(8), label: lorem.generateWords(1) },
        label: random(2),
        group: random(2),
        groupItems: []
    };
    const groupLength = random(20);
    if (structure.group) {
        for (let i = 0; i < groupLength; i++) {
            structure.groupItems.push({ label: lorem.generateWords(random(3)) })
        }
    }
    return structure;
};

module.exports = generator;