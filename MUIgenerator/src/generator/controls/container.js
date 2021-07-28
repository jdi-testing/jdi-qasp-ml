const lorem = require('../loremIpsum');
const { random, randomBool, randomColor } = require('../utils');

const maxWigth = [
    'lg', 'md', 'sm', 'xl', 'xs', false
];

const generator = () => {
    const structure = {
        maxWigth: random(6),
        fixed: randomBool(2),
        style: {
            backgroundColor: randomColor(),
            height: (random(100) + 'vh'),
        },
        text: lorem.generateSentences(3),
    };

    return structure;
};

module.exports = generator;