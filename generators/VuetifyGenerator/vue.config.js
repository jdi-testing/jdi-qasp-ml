const { defineConfig } = require('@vue/cli-service');
const { getRandomSite, getRandomComponentsOrder } = require('./generator');

const generatedSite = JSON.stringify(getRandomSite());
const generatedComponentsOrder = JSON.stringify(getRandomComponentsOrder());
console.log(generatedSite);
console.log(generatedComponentsOrder);

module.exports = defineConfig({
  publicPath: './',
  transpileDependencies: [
    'vuetify'
  ],
  chainWebpack: (config) => {
    config.plugin('define').tap((definitions) => {
      definitions[0]['process.env']['GENERATED_STRUCTURE'] = generatedSite;
      definitions[0]['process.env']['GENERATED_COMPONENTS_ORDER'] = generatedComponentsOrder;
      return definitions;
    });
  }
})
