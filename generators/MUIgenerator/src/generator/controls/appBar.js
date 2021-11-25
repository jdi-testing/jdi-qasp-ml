const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const generator = () => {
    const structure = {
        type: random(4),
        header: lorem.generateWords(random(3)),
    }

    return structure;
}

module.exports = generator;