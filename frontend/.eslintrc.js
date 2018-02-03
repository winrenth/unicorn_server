module.exports = {
    root: true,
    parser: 'babel-eslint',
    parserOptions: {
        sourceType: 'module'
    },
    env: {
        browser: true,
        es6: true,
        node: true
    },
    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    extends: [
        'standard'
    ],
    // required to lint *.vue files
    plugins: [
        'html',
        'import'
    ],
    globals: {
        'cordova': true,
        'DEV': true,
        'PROD': true,
        '__THEME': true
    },
    // add your custom rules here
    'rules': {
        // allow paren-less arrow functions
        'arrow-parens': 0,
        'one-var': 0,
        'import/first': 0,
        'import/named': 2,
        'import/namespace': 2,
        'import/default': 2,
        'import/export': 2,
        // allow debugger during development
        'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
        'brace-style': [2, '1tbs', { 'allowSingleLine': true }],
        'no-alert': 0,
        'no-bitwise': 0,
        'camelcase': 0,
        'curly': 1,
        'eqeqeq': 0,
        'no-eq-null': 0,
        'guard-for-in': 1,
        'no-empty': 0,
        'max-len': [1, 120],
        'no-unused-vars': 0,
        'no-empty-function': 0,
        'space-before-function-paren': 0,
        'semi': 0,
        'indent': ["error", 4]
    }
};
