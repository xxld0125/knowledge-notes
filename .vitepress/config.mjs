import path from "node:path";
import { defineConfig } from "vitepress";
import {
  buildSidebar,
  collectKnowledgeSections,
  listKnowledgeCanvasFiles,
  listKnowledgeMarkdownFiles,
  mapCanvasToGeneratedMarkdown,
} from "../scripts/lib/docs-site.mjs";

const knowledgeBaseDir = path.resolve(process.cwd(), "knowledge-base");
const markdownFiles = await listKnowledgeMarkdownFiles(knowledgeBaseDir);
const canvasFiles = await listKnowledgeCanvasFiles(knowledgeBaseDir);
const sections = collectKnowledgeSections([
  ...markdownFiles,
  ...canvasFiles.map(mapCanvasToGeneratedMarkdown),
]);

export default defineConfig({
  title: "knowledge-notes",
  description: "个人知识库预览站",
  srcDir: ".vitepress/content",
  cleanUrls: true,
  ignoreDeadLinks: true,
  themeConfig: {
    nav: sections.map((section) => ({
      text: section.name,
      link: section.baseLink,
    })),
    sidebar: buildSidebar(sections),
    socialLinks: [],
    search: {
      provider: "local",
    },
  },
});
