const lorem = require('../loremIpsum');
const { random, randomBool } = require('../utils');

const colors = [
    'default',
    'primary',
    'secondary'
];

const generator = () => {
    const groupLenghth = random(20) + 1;
    const group = [];
    for (let i = 0; i < groupLenghth; i++) {
        group.push({
            label: lorem.generateWords(2),
            typenumber: random(11),
            variant: randomBool() ? 'outlined' : 'default',
            size: randomBool() ? 'small' : 'medium',
            color: colors[random(3)]
        });
    }
    return { group };
}

module.exports = generator;