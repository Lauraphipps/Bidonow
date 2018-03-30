const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');
const webpack = require('webpack');


module.exports = merge(common, {
    entry: {
        "main": path.resolve(__dirname, 'static', 'js', 'main.js'),
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.$': 'jquery',
            'window.jQuery': 'jquery',
        }),
    ],
    resolve: {
        alias: {
            'jquery': path.resolve('node_modules/jquery/dist/jquery')
        }
    }
})
