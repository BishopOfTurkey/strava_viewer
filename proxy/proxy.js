#!/usr/bin/env node

const { createProxyMiddleware } = require('http-proxy-middleware');
const polka = require('polka');

const { APP_URL, API_URL, PORT=8888 } = process.env;

polka()
  .use(
    createProxyMiddleware('/api', { target: API_URL, changeOrigin: true, pathRewrite: {'^/api': ''}}),
    createProxyMiddleware('/', { target: APP_URL, changeOrigin: true })
  )
  .listen(PORT, (err) => {
    if (err) throw err;
    console.log(`> Ready on localhost:${PORT}~!`);
  });