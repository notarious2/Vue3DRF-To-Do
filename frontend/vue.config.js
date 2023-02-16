// const { defineConfig } = require("@vue/cli-service");
// module.exports = defineConfig({
//   publicPath: "/",
//   transpileDependencies: true,
// });

// FOR GITHUB PAGES DEPLOYMENT:
// module.exports = {
//   publicPath: process.env.NODE_ENV === "production" ? "/VueToDoApp/" : "/",
// };

module.exports = {
  publicPath: "",
  productionSourceMap: false, // to hide source cod
  pluginOptions: {
    sitemap: {
      urls: [
        "https://django.stickydo.us/",
        "https://django.stickydo.us/login",
        "https://django.stickydo.us/register",
      ],
    },
  },
};
