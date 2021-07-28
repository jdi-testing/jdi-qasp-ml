const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const variant = ['circular', 'rounded', 'square'];

const generator = () => {
    const structure = {
        groupLength: randomBool() ? random(10) + 1 : 1,
        variant: variant[random(4)],
        group: []
    };
    for (let i = 0; i < structure.groupLength; i++) {
        structure.group.push({
            type: random(6),
        })
    }

    return structure;
};

module.exports = generator;