module.exports = {
    publicPath: "/static/",
    devServer: {
        public: "localhost:8080",
        proxy: {
            '^/fs': {
                target: 'http://app:8081',
                ws: true,
                pathRewrite: { "^/fs/": "/fs/" },
                changeOrigin: true,
                secure: false,
            },
            '^/api': {
                target: 'http://app:8081',
                ws: true,
                pathRewrite: { "^/api/": "/api/" },
                changeOrigin: true,
                secure: false
            },
        }
    }
}