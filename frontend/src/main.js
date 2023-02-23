import { createApp } from "vue";
import App from "./App.vue";
import router from "./router.js";
import "./axios";
import TheHeader from "../src/components/layout/TheHeader.vue";
import TheFooter from "../src/components/layout/TheFooter.vue";

import { createPinia } from "pinia";
import VueGtag from "vue-gtag";

const app = createApp(App);

const pinia = createPinia();

app.component("the-header", TheHeader);
app.component("the-footer", TheFooter);

app.use(router);
app.use(VueGtag, { config: { id: "G-7S5VKGG2LQ" } }); // for google analytics
app.use(pinia);

app.mount("#app");
