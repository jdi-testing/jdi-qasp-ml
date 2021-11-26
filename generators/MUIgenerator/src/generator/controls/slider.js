const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const generator = () => {
    const isRange = randomBool();
    const range = random(100);
    const marks = randomBool() ? Array.apply(null, Array(random(range))) : null;
    const structure = {
        orientation: randomBool() ? 'vertical' : 'horizontal',
        value: isRange ? [2, random(range / 2) + 5] : random(range),
        valueLabelDisplay: randomBool() ? "on" : "off",
        disabled: randomBool(),
    }

    if (marks) {
        structure.marks = marks.map((item) => {
            const n = random(range);
            return {
                value: n,
                label: n + randomChar(),
            }
        })
    }

    randomBool() && (structure.step = range / 10);
    if (isRange && randomBool()) {
        structure.min = (Math.min(marks) - random(5));
        structure.max = (Math.max(marks) + random(20));
    }

    return structure;
}

module.exports = generator;