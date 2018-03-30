const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');


module.exports = merge(common, {
    entry: {
        "control-panel": path.resolve(__dirname, 'static', 'js', 'control-panel.js')
    }
})
