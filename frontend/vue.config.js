// frontend/vue.config.js
const { defineConfig } = require('@vue/cli-service')


module.exports = {
  runtimeCompiler: true,
  lintOnSave: false,
  transpileDependencies: [],
  devServer: { devMiddleware: { writeToDisk: true } }
};

