/*jshint esversion: 6 */

// import {getCssSelector} from "index.js";
// import {finder} from "finder.js";

const generateSelectorByElement = (element) => {
  "use strict";
  let selectorByGenerator;
  let selectorByFinder;

  // Due to finder lib issue, we have to catch errors.
  // If css selector generated by finder contains ".", for example #Country_16856319000360.6264611129794591
  // We get "Uncaught DOMException: Failed to execute 'querySelectorAll' on 'Document':
  // '#Country_16856319000360.6264611129794591' is not a valid selector."
  // And because of lib logic we can't prevent generation these selectors.
  // Reproduced on https://www.docker.com
  try {
    const finderForbiddenAttributes = ['jdn-hash', 'href', 'class', 'xmlns', 'xmlns:xlink', 'xlink:href'];
    selectorByFinder = finder(element, {
      attr: (name, value) => value && !finderForbiddenAttributes.includes(name),
    });
  } catch (err) {
    selectorByFinder = err;
  }

  // If "id" attribute starts with number, for example id="6264611129794591"
  // We get "Uncaught DOMException: Failed to execute 'querySelectorAll' on 'Document':
  // '#6264611129794591' is not a valid selector."
  // And because of lib logic we can't prevent generation these selectors.
  // Reproduced on https://www.otto.de
  const generatorOptions = {
    blacklist: [/jdn-hash/, /href/],
    maxCombinations: 30,
    maxCandidates: 30,
  };

  try {
    selectorByGenerator = CssSelectorGenerator.getCssSelector(element, generatorOptions);
  } catch (err) {
    selectorByGenerator = err;
  }

  const isSelectorByGeneratorString = typeof selectorByGenerator === 'string';
  const isSelectorByFinderString = typeof selectorByFinder === 'string';

  let selectorGenerationResult;

  if (isSelectorByGeneratorString && isSelectorByFinderString) {
    selectorGenerationResult = selectorByGenerator.length < selectorByFinder.length ? selectorByGenerator : selectorByFinder;
  } else if (!isSelectorByFinderString && isSelectorByGeneratorString) {
    selectorGenerationResult = selectorByGenerator;
  } else if (!isSelectorByGeneratorString && isSelectorByFinderString) {
    selectorGenerationResult = selectorByFinder;
  } else {
    selectorGenerationResult = 'CSS selector generation was failed';
  }
  return selectorGenerationResult;
};