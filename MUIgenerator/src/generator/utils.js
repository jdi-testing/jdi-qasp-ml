const random = (number) => Math.floor(Math.random() * number);
const randomBool = () => !!random(2);
const randomColor = () => {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
};

const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const randomChar = () => characters.charAt(Math.floor(Math.random() *
    characters.length));

module.exports = { random, randomBool, randomColor, randomChar };