const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const generator = () => {
    const structure = {
        variant: randomBool() ? 'outlined' : 'elevation',
        header: lorem.generateWords(random(3)),
        content: lorem.generateSentences(random(4)),
        actionText: lorem.generateWords(random(3)),
        action: random(4),
    }
    
    return structure;
}

module.exports = generator;