module.exports = {
    env: {
      browser: true,
      es2021: true,
      jest: true,
    },
    extends: [
            'eslint:recommended',
            'plugin:react/recommended',
        ],
        parserOptions: {
            ecmaFeatures: {
                jsx: true,
            },
            ecmaVersion: 12,
            sourceType: 'module',
            project: './tsconfig.json',
        },
        plugins: ['react', 'functional'],
        settings: {
            react: {
                version: 'detect',
        },
    },
    rules: {
        // General
        'no-console': 'error',

        // React
        'react/jsx-boolean-value': 'warn',
        'react/jsx-curly-brace-presence': 'warn',
        'react/jsx-fragments': 'warn',
        'react/jsx-no-useless-fragment': 'warn',
        'react/jsx-uses-react': 'off',
        'react/prefer-stateless-function': 'warn',
        'react/prop-types': 'off',
        'react/react-in-jsx-scope': 'off',
  
        // Functional
        'functional/prefer-readonly-type': [
            'warn',
            {
            allowLocalMutation: true,
            allowMutableReturnType: true,
            ignoreClass: true,
            },
        ],
    },
<<<<<<< HEAD
};
=======
};
>>>>>>> 81a9594c2943be6be1e0ab75f1b3b2642a5221a1
