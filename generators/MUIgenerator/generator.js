const process = require('process');

const appBar = require('./src/generator/controls/appBar');
const avatar = require('./src/generator/controls/avatar');
const card = require('./src/generator/controls/card');
const checkboxGenerator = require('./src/generator/controls/checkbox');
const chip = require('./src/generator/controls/chip');
const container = require('./src/generator/controls/container');
const radio = require('./src/generator/controls/radio');
const slider = require('./src/generator/controls/slider');
const stepper = require('./src/generator/controls/stepper');
const tabs = require('./src/generator/controls/tabs');
const lorem = require('./src/generator/loremIpsum');
const { random, randomBool } = require('./src/generator/utils');

const controls =
    [
        () => ({ key: "Accordion", value: { type: random(3) } }),
        () => ({ key: "Alert", value: { type: random(4), text: lorem.generateSentences(1) } }),
        () => ({ key: "AppBar", value: appBar() }),
        () => ({ key: "Avatar", value: avatar() }),
        () => ({ key: "Backdrop", value: { width: random(1000), height: random(1000), top: random(500), left: random(500), open: randomBool() } }),
        () => ({ key: "Badge", value: { type: random(5) } }),
        () => ({ key: "Button", value: { type: random(6) } }),
        () => ({ key: "ButtonGroup", value: { type: random(6) } }),
        () => ({ key: "Breadcrumbs", value: { type: random(3) } }),
        () => ({ key: "BottomNavigation", value: { type: random(2) } }),
        () => ({ key: "Box", value: {} }),
        () => ({ key: "Card", value: card() }),
        () => ({ key: "Checkbox", value: checkboxGenerator() }),
        () => ({ key: "Chip", value: chip() }),
        () => ({ key: "Circular", value: { type: random(6) } }),
        () => ({ key: "Container", value: container() }),
        () => ({ key: "DateTimePicker", value: { type: random(3) } }),
        () => ({ key: "Dialog", value: { type: random(5) } }),
        () => ({ key: "Divider", value: { type: random(5) } }),
        () => ({ key: "Drawer", value: { type: random(3) } }),
        () => ({ key: "Grid", value: { type: random(2) } }),
        () => ({ key: "InputBase", value: { type: random(5) } }),
        () => ({ key: "Link", value: { type: random(3) } }),
        () => ({ key: "List", value: { type: random(3) } }),
        () => ({ key: "Menu", value: {} }),
        // () => ({ key: "Modal", value: { text: lorem.generateSentences(1) } }),
        () => ({ key: "Popover", value: { type: random(2) } }),
        () => ({ key: "Popper", value: { type: random(2) } }),
        () => ({ key: "Portal", value: {} }),
        () => ({ key: "Radio", value: radio() }),
        () => ({ key: "Select", value: { type: [random(4), random(5)] } }),
        () => ({ key: "Slider", value: slider() }),
        () => ({ key: "Snackbar", value: ({ text: lorem.generateSentences(1) }) }),
        () => ({ key: "Stepper", value: stepper() }),
        () => ({ key: "Switch", value: { type: random(5) } }),
        () => ({ key: "Tabs", value: tabs() }),
        () => ({ key: "Table", value: { type: random(6) } }),
        () => ({ key: "TextArea", value: { type: random(3) } }),
        () => ({ key: "TextField", value: { type: random(8) } }),
    ];

const getRandomStructure = () => {
    const randomControls = [];
    for (let index = 0; index < 50; index++) {
        randomControls.push((controls[random(controls.length)])());
    }
    return JSON.stringify(randomControls);
}

process.env.REACT_APP_GENERATED_STRUCTURE = getRandomStructure();
process.env.PUBLIC_URL = ".";

require('child_process').exec("npm run build", function (err, stdout, stderr) {
    err && console.log(err);
    stdout && console.log(stdout);
    stderr && console.log(stderr);
});

