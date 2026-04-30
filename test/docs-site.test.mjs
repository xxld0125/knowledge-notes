import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
  buildCanvasPageMarkdown,
  buildHomeMarkdown,
  buildSidebar,
  collectKnowledgeSections,
  mapCanvasToGeneratedMarkdown,
  sanitizeMarkdownForVitePress,
} from "../scripts/lib/docs-site.mjs";

test("collectKnowledgeSections sorts sections and files for VitePress routes", () => {
  const sections = collectKnowledgeSections([
    "knowledge-base/项目/vuex.md",
    "knowledge-base/AI/提示词.md",
    "knowledge-base/项目/上传组件开发.md",
    "knowledge-base/AI/Prompt.md",
    "knowledge-base/AI/Cursor/Cursor.md",
    "knowledge-base/AI/Cursor/进阶使用/前端项目应用/快速生成Docdd.md",
    "knowledge-base/面试训练/000_目录.md",
  ]);

  assert.deepEqual(
    sections.map((section) => section.name),
    ["AI", "面试训练", "项目"],
  );
  assert.deepEqual(
    sections[0].entries.map((entry) => ({
      type: entry.type,
      text: entry.text,
      link: entry.link,
    })),
    [
      {
        type: "directory",
        text: "Cursor",
        link: "/knowledge-base/AI/Cursor/",
      },
      {
        type: "page",
        text: "Prompt",
        link: "/knowledge-base/AI/Prompt",
      },
      {
        type: "page",
        text: "提示词",
        link: "/knowledge-base/AI/提示词",
      },
    ],
  );
  assert.deepEqual(
    sections[0].entries[0].entries.map((entry) => ({
      type: entry.type,
      text: entry.text,
      link: entry.link,
    })),
    [
      {
        type: "directory",
        text: "进阶使用",
        link: "/knowledge-base/AI/Cursor/进阶使用/",
      },
      {
        type: "page",
        text: "Cursor",
        link: "/knowledge-base/AI/Cursor/Cursor",
      },
    ],
  );
  assert.equal(sections[1].indexSource, "knowledge-base/面试训练/000_目录.md");
});

test("buildSidebar preserves nested directory groups", () => {
  const sidebar = buildSidebar([
    {
      name: "AI",
      baseLink: "/knowledge-base/AI/",
      entries: [
        {
          type: "directory",
          text: "Cursor",
          link: "/knowledge-base/AI/Cursor/",
          entries: [
            { type: "page", text: "Cursor", link: "/knowledge-base/AI/Cursor/Cursor" },
            {
              type: "directory",
              text: "进阶使用",
              link: "/knowledge-base/AI/Cursor/进阶使用/",
              entries: [
                {
                  type: "directory",
                  text: "前端项目应用",
                  link: "/knowledge-base/AI/Cursor/进阶使用/前端项目应用/",
                  entries: [
                    {
                      type: "page",
                      text: "快速生成Docdd",
                      link: "/knowledge-base/AI/Cursor/进阶使用/前端项目应用/快速生成Docdd",
                    },
                  ],
                },
              ],
            },
          ],
        },
        { type: "page", text: "Prompt", link: "/knowledge-base/AI/Prompt" },
        { type: "page", text: "提示词", link: "/knowledge-base/AI/提示词" },
      ],
    },
  ]);

  assert.deepEqual(sidebar, {
    "/knowledge-base/AI/": [
      {
        text: "AI",
        items: [
          { text: "概览", link: "/knowledge-base/AI/" },
          {
            text: "Cursor",
            items: [
              { text: "Cursor", link: "/knowledge-base/AI/Cursor/Cursor" },
              {
                text: "进阶使用",
                items: [
                  {
                    text: "前端项目应用",
                    items: [
                      {
                        text: "快速生成Docdd",
                        link: "/knowledge-base/AI/Cursor/进阶使用/前端项目应用/快速生成Docdd",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          { text: "Prompt", link: "/knowledge-base/AI/Prompt" },
          { text: "提示词", link: "/knowledge-base/AI/提示词" },
        ],
      },
    ],
  });
});

test("buildHomeMarkdown renders a category list for the generated landing page", () => {
  const markdown = buildHomeMarkdown([
    {
      name: "AI",
      baseLink: "/knowledge-base/AI/",
      entries: [
        { type: "page", text: "Prompt", link: "/knowledge-base/AI/Prompt" },
      ],
    },
    {
      name: "项目",
      baseLink: "/knowledge-base/项目/",
      entries: [],
    },
  ]);

  assert.match(markdown, /# knowledge-notes/);
  assert.match(markdown, /\[AI\]\(\/knowledge-base\/AI\/\)/);
  assert.match(markdown, /1 篇/);
  assert.match(markdown, /\[项目\]\(\/knowledge-base\/项目\/\)/);
});

test("sanitizeMarkdownForVitePress escapes raw html outside fenced code blocks", () => {
  const markdown = [
    "正文里有 <font style=\"color:red;\">标签</font>",
    "兼容写法 <span style=\"color:#333;\">文本</span>",
    "危险标签 <script>alert('xss')</script>",
    "跨行开标签 <font style=\"color:blue;\">",
    "</font>",
    "插值示例 {{ demo.value }}",
    "对象说明 { foo: bar }",
    "![](C:\\Users\\demo\\image.png)",
    "![](missing/asset.webp)",
    "",
    "```vue",
    "<template><div>keep</div></template>",
    "{{ keepInterpolation }}",
    "```",
    "",
    "<bad-tag",
  ].join("\n");

  const sanitized = sanitizeMarkdownForVitePress(
    markdown,
    path.join(process.cwd(), "test", "fixtures", "demo.md"),
  );

  assert.match(
    sanitized,
    /正文里有 <font style="color:red;">标签<\/font>/,
  );
  assert.match(sanitized, /兼容写法 <span style="color:#333;">文本<\/span>/);
  assert.match(sanitized, /危险标签 &lt;script&gt;alert\('xss'\)&lt;\/script&gt;/);
  assert.match(sanitized, /跨行开标签 &lt;font style="color:blue;"&gt;/);
  assert.match(sanitized, /&lt;\/font&gt;/);
  assert.match(sanitized, /插值示例 &#123;&#123; demo.value &#125;&#125;/);
  assert.match(sanitized, /对象说明 &#123; foo: bar &#125;/);
  assert.match(sanitized, /本地图片路径：`C:\\Users\\demo\\image\.png`/);
  assert.match(sanitized, /缺失图片资源：`missing\/asset\.webp`/);
  assert.match(sanitized, /<template><div>keep<\/div><\/template>/);
  assert.match(sanitized, /\{\{ keepInterpolation \}\}/);
  assert.match(sanitized, /&lt;bad-tag/);
});

test("canvas helpers generate markdown route and page content", () => {
  const source = "knowledge-base/项目/前端扩展点/无标题画板.canvas";
  assert.equal(
    mapCanvasToGeneratedMarkdown(source),
    "knowledge-base/项目/前端扩展点/无标题画板.canvas.md",
  );
  assert.equal(
    buildCanvasPageMarkdown("eyJub2RlcyI6W119"),
    [
      "<!-- Auto-generated by scripts/prepare-docs.mjs -->",
      "",
      "<CanvasPage canvas-base64=\"eyJub2RlcyI6W119\" />",
      "",
    ].join("\n"),
  );
});

test("collectKnowledgeSections includes generated canvas pages in navigation", () => {
  const sections = collectKnowledgeSections([
    "knowledge-base/读书笔记/JavaScript/JavaScript重难点实例精讲/2-引用数据类型.canvas.md",
    "knowledge-base/读书笔记/JavaScript/JavaScript重难点实例精讲/2-引用数据类型.md",
  ]);
  const jsBookSection = sections.find((section) => section.name === "读书笔记");
  assert.ok(jsBookSection);
  const serialized = JSON.stringify(jsBookSection);
  assert.match(serialized, /2-引用数据类型\.canvas/);
  assert.match(serialized, /\/knowledge-base\/读书笔记\/JavaScript\/JavaScript重难点实例精讲\/2-引用数据类型\.canvas/);
});
