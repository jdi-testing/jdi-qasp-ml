const { random, randomBool, lorem, randomColor, shuffleArray } = require('./generatorUtils');

const components = {
    alert: {
        type: () => random(5),
        shaped: () => randomBool(),
        dense: () => randomBool(),
        prominent: () => randomBool(),
        outlined: () => randomBool(),
        dissmissible: () => randomBool(),
        "colored-border": () => randomBool(),
        border: () => random(5),
        text: () => lorem.generateSentences(1),
    },
    badge: {
        bordered: () => randomBool(),
        bottom: () => randomBool(),
        dot: () => randomBool(),
        inline: () => randomBool(),
        left: () => randomBool(),
        overlap: () => randomBool(),
        tile: () => randomBool(),
        icon: () => random(5),
    },
    appBar: {
        type: () => random(7),
    },
    toolBar: {
        type: () => random(8),
    },
    systemBar: {
        type: () => random(4),
    },
    bottomNavigation: {
        type: () => random(5),
    },
    bottomSheet: {
        type: () => random(5),
    },
    button: {
        color: () => randomColor(),
        text: () => randomBool(),
        block: () => randomBool(),
        disabled: () => randomBool(),
        depressed: () => randomBool(),
        large: () => randomBool(),
        outlined: () => randomBool(),
        plain: () => randomBool(),
        rounded: () => randomBool(),
        tile: () => randomBool(),
        loading: () => randomBool(),
        small: () => randomBool(),
        fab: () => randomBool(),
        'x-large': () => randomBool(),
        'x-small': () => randomBool(),
        label: () => lorem.generateWords(2),
    },
    breadcrumbs: {
        type: () => random(4),
    },
    calendar: {
        type: () => random(8),
    },
    card: {
        type: () => random(11),
    },
    carousel: {
        type: () => random(6),
    },
    chip: {
        filter: () => randomBool(),
        color: () => randomColor(),
        label: () => randomBool(),
        link: () => randomBool(),
        outlined: () => randomBool(),
        pill: () => randomBool(),
        close: () => randomBool(),
        draggable: () => randomBool(),
    },
    dialog: {
        type: () => random(7),
    },
    expansionPanel: {
        type: () => random(6),
    },
    autocomplete: {
        'auto-select-first': () => randomBool(),
        chips: () => randomBool(),
        clearable: () => randomBool(),
        'deletable-chips': () => randomBool(),
        dense: () => randomBool(),
        filled: () => randomBool(),
        multiple: () => randomBool(),
        rounded: () => randomBool(),
        'small-chips': () => randomBool(),
        solo: () => randomBool(),
        'solo-inverted': () => randomBool(),
    },
    checkbox: {
        color: () => randomColor(),
        label: () => lorem.generateWords(1),
        indeterminate: () => randomBool,
    },
    combobox: {
        clearable: () => randomBool(),
        dense: () => randomBool(),
        filled: () => randomBool(),
        "hide-selected": () => randomBool(),
        multiple: () => randomBool(),
        outlined: () => randomBool(),
        "persistent-hint": () => randomBool(),
        "small-chips": () => randomBool(),
        solo: () => randomBool(),
        label: () => lorem.generateSentences(1),
    },
    fileInput: {
        type: () => random(8),
    },
    input: {
        type: () => random(5),
    },
    otpInput: {
        dark: () => randomBool(),
        disabled: () => randomBool(),
        plain: () => randomBool(),
        length: () => random(6),
        type: () => random(3),
    },
    overflowBtn: {
        dense: () => randomBool(),
        disabled: () => randomBool(),
        editable: () => randomBool(),
        filled: () => randomBool(),
        loading: () => randomBool(),
        overflow: () => randomBool(),
        "persistent-hint": () => randomBool(),
        readonly: () => randomBool(),
        reverse: () => randomBool(),
        segmented: () => randomBool(),
        label: () => lorem.generateWords(2),
    },
    radioButton: {
        type: () => random(2),
    },
    rangeSlider: {
        dense: () => randomBool(),
        disabled: () => randomBool(),
        "hide-details": () => randomBool(),
        hint: () => lorem.generateWords(2),
        "inverse-label": () => randomBool(),
        max: () => random(100),
        min: () => 0,
        "persistent-hint": () => randomBool(),
        readonly: () => randomBool(),
        vertical: () => randomBool(),
    },
    select: {
        type: () => random(6),
    },
    slider: {
        dense: () => randomBool(),
        disabled: () => randomBool(),
        "hide-details": () => randomBool(),
        hint: () => lorem.generateWords(2),
        "inverse-label": () => randomBool(),
        max: () => random(100),
        min: () => 0,
        "persistent-hint": () => randomBool(),
        readonly: () => randomBool(),
        vertical: () => randomBool(),
    },
    switch: {
        color: () => randomColor(),
        flat: () => randomBool(),
        inset: () => randomBool(),
        loading: () => randomBool(),
    },
    textField: {
        type: () => random(16),
    },
    textArea: {
        type: () => random(6),
    },
    buttonGroup: {
        type: () => random(4),
    },
    chipGroup: {
        type: () => random(3),
    },
    slideGroup: {
        'center-active': () => randomBool(),
        'show-arrows': () => randomBool(),
        mandatory: () => randomBool(),
        multiple: () => randomBool(),
    },
    window: {
        type: () => random(5),
    },
    hover: {
        type: () => random(4),
    },
    list: {
        type: () => random(12),
    },
    menu: {
        type: () => random(4),
    },
    navigationDrawer: {
        type: () => random(6),
    },
    pagination: {
        type: () => random(4),
    },
    colorPicker: {
        disabled: () => randomBool(),
        "dot-size": () => random(100),
        "hide-canvas": () => randomBool(),
        "hide-inputs": () => randomBool(),
        "hide-mode-switch": () => randomBool(),
        "hide-sliders": () => randomBool(),
        mode: () => random(3),
        "show-swatches": () => randomBool(),
        "swatches-max-height": () => random(200),
    },
    datePicker: {
        type: () => random(10),
    },
    datePickerMonth: {
        type: () => random(5),
    },
    timePicker: {
        "ampm-in-title": () => randomBool(),
        disabled: () => randomBool(),
        format: () => random(2),
        "full-width": () => randomBool(),
        landscape: () => randomBool(),
        "no-title": () => randomBool(),
        readonly: () => randomBool(),
        scrollable: () => randomBool(),
        "use-seconds": () => randomBool(),
    },
    rating: {
        dense: () => randomBool(),
        "empty-icon": () => random(2),
        "full-icon": () => random(2),
        "half-icon": () => random(2),
        "half-increments": () => randomBool(),
        hover: () => randomBool(),
        length: () => random(10),
        readonly: () => randomBool(),
        size: () => random(100),
        value: () => random(10),
    },
    stepper: {
        type: () => random(4),
    },
    simpleTable: {
        type: () => random(4),
    },
    dataTable: {
        type: () => random(11),
    },
    tabs: {
        type: () => random(10),
    },
    timeline: {
        type: () => random(7),
    },
    treeview: {
        type: () => random(9),
    },
    virtualScroller: {
        type: () => random(2),
    }
}

const getRandomSite = () => {
    return Object.keys(components).reduce((acc, componentName) => {
        const valueFns = components[componentName];
        Object.entries(valueFns).forEach(([valueName, valueFn]) => {
            acc[componentName] = acc[componentName] || {};
            acc[componentName][valueName] = valueFn();
        })
        return acc;
    }, {});
}

const getRandomComponentsOrder = () => {
    const componentNames = Object.keys(components);
    shuffleArray(componentNames);
    return componentNames;
}

module.exports = {
    getRandomSite,
    getRandomComponentsOrder,
}