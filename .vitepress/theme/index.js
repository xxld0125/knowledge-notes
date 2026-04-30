import DefaultTheme from "vitepress/theme";
import CanvasPage from "./components/CanvasPage.vue";

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    DefaultTheme.enhanceApp?.({ app });
    app.component("CanvasPage", CanvasPage);
  },
};
