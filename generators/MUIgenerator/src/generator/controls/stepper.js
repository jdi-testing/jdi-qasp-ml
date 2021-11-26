const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const orientation = ['horizontal', 'vertical'];

const generator = () => {
    const stepsNumber = random(3) + 2;
    const type = random(4);
    const orientation = type !== 3 && randomBool() ? 'vertical' : 'horizontal';    
    const structure = {
        type, 
        orientation,
        activeStep: random(stepsNumber),
        alternativeLabel: orientation === 'horizontal' ? randomBool() : false,
        steps: [],
    }

    for (let index = 0; index < stepsNumber; index++) {
        structure.steps.push(lorem.generateWords(random(5)));
    }

    return structure;
}

module.exports = generator;