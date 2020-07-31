const path = require('path');

module.exports = {
    mode: 'production',
    entry: './src/index.tsx',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'dist'),
        libraryTarget: 'umd',
        library: 'Blitz',
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js'],
    },
    module: {
        rules: [{test: /\.tsx?$/, loader: 'ts-loader'}],
    },
    externals: {
        react: {root: 'React', commonjs: 'react', commonjs2: 'react', amd: 'react'},
        'react-dom': {root: 'ReactDOM', commonjs: 'react-dom', commonjs2: 'react-dom', amd: 'react-dom'},
    },
};
