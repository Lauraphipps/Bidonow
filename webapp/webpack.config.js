const path = require('path');

module.exports = {
  entry: path.resolve(__dirname, 'static', 'js', 'main.js'),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static', 'dist')
  }
};
