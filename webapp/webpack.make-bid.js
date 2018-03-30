const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const path = require('path');


module.exports = merge(common, {
    entry: {
        "make-bid": path.resolve(__dirname, 'static', 'js', 'make-bid.js'),
    }
})
