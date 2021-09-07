This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm run generate`

and find the builded app in `\build` folder.

### `set BUILD_PATH=$directory && npm run generate`

to srecify build path.
Example: 

`set BUILD_PATH=build/dist1 && npm run generate`

## Windows users

- install node.js
- install needed packages:

### `npm install lorem-ipsum`

- generate N sites:

```
set BUILD_PATH=build/site1
npm run generate
...
set BUILD_PATH=build/siteN 
npm run generate
```



