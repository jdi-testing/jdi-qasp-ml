const { exec } = require('child_process');
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

const structure = JSON.stringify(
    {
        Accordion: { type: random(3) },
        Alert: { type: random(4), text: lorem.generateSentences(1) },
        AppBar: appBar(),
        Avatar: avatar(),
        Backdrop: { width: random(1000), height: random(1000), top: random(500), left: random(500), open: randomBool() },
        Badge: { type: random(5) },
        ButtonGroup: { type: random(6) },
        Breadcrumbs: { type: random(3) },
        BottomNavigation: { type: random(2) },
        Box: {},
        Card: card(),
        Checkbox: checkboxGenerator(),
        Chip: chip(),
        Circular: { type: random(6) },
        Container: container(),
        DateTimePicker: { type: random(3) },
        Dialog: { type: random(5) },
        Divider: { type: random(5) },
        Drawer: { type: random(3) },
        Grid: { type: random(2) },
        Link: { type: random(3) },
        List: { type: random(3) },
        Menu: {},
        Popover: { type: random(2) },
        Popper: { type: random(2) },
        Portal: {},
        Radio: radio(),
        Select: { type: [random(3), random(5)] },
        Slider: slider(),
        Snackbar: ({ text: lorem.generateSentences(1) }),
        Stepper: stepper(),
        Switch: { type: random(5) },
        Tabs: tabs(),
        Table: { type: random(6) },
        TextArea: { type: random(3) },
        TextField: { type: random(8) },
    });
process.env.REACT_APP_NOT_SECRET_CODE = structure;
process.env.PUBLIC_URL = ".";

require('child_process').exec("npm run build", function(err, stdout, stderr) { 
    err && console.log(err); 
    stdout && console.log(stdout); 
    stderr && console.log(stderr); 
});

