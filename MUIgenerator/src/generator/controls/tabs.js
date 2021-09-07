const lorem = require('../loremIpsum');
const { random, randomBool, randomColor, randomChar } = require('../utils');

const scrollButtons = ['auto', 'desktop', 'off', 'on'];
const variant = ['fullWidth', 'scrollable', 'standard'];

const generator = () => {
    const tabs = Array.apply(null, Array(random(6) + 2));
    const structure = {
        variant: variant[random(3)],
        scrollButtons: scrollButtons[random(4)],
        icons: true,
        value: random(tabs.length),
        orientation: randomBool() ? 'horizontal' : 'vertical',
    }

    structure.tabs = tabs.map((item) => {
        return structure.icons ? random(7) : {label: lorem.generateWords(1)} 
    })

    return structure;
}

module.exports = generator;