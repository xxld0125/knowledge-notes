import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";

const INDEX_CANDIDATES = new Set([
  "index.md",
  "README.md",
  "000_目录.md",
  "doc000_目录.md",
]);
const SAFE_INLINE_TAG_PAIR_PATTERN =
  /<(font|span)\b[^>\n]*>[^<]*<\/\1>/gi;

function compareNames(left, right) {
  const leftAscii = /^[\x00-\x7F]/.test(left);
  const rightAscii = /^[\x00-\x7F]/.test(right);

  if (leftAscii !== rightAscii) {
    return leftAscii ? -1 : 1;
  }

  return left.localeCompare(right, "zh-Hans-CN", {
    numeric: true,
    sensitivity: "base",
  });
}

function normalizePath(filePath) {
  return filePath.split(path.sep).join("/");
}

function stripMarkdownExtension(fileName) {
  return fileName.replace(/\.md$/i, "");
}

function stripCanvasExtension(fileName) {
  return fileName.replace(/\.canvas$/i, "");
}

function buildDocLink(source) {
  const normalized = normalizePath(source);
  return `/${stripMarkdownExtension(normalized)}`;
}

function buildDirectoryLink(sectionName, segments) {
  const suffix = segments.length > 0 ? `${segments.join("/")}/` : "";
  return `/knowledge-base/${sectionName}/${suffix}`;
}

function createDirectoryEntry(sectionName, name, segments) {
  return {
    type: "directory",
    text: name,
    link: buildDirectoryLink(sectionName, segments),
    entries: [],
  };
}

function createPageEntry(source, fileName) {
  return {
    type: "page",
    text: stripMarkdownExtension(fileName),
    link: buildDocLink(source),
    source,
  };
}

function sortEntries(entries) {
  return entries
    .sort((left, right) => {
      if (left.type !== right.type) {
        return left.type === "directory" ? -1 : 1;
      }
      return compareNames(left.text, right.text);
    })
    .map((entry) =>
      entry.type === "directory"
        ? { ...entry, entries: sortEntries(entry.entries) }
        : entry,
    );
}

function countPages(entries) {
  return entries.reduce(
    (total, entry) =>
      total + (entry.type === "page" ? 1 : countPages(entry.entries)),
    0,
  );
}

function buildSectionListLines(entries, depth = 0) {
  const lines = [];
  const indent = "  ".repeat(depth);

  for (const entry of entries) {
    if (entry.type === "page") {
      lines.push(`${indent}- [${entry.text}](${entry.link})`);
      continue;
    }

    lines.push(`${indent}- **${entry.text}**`);
    lines.push(...buildSectionListLines(entry.entries, depth + 1));
  }

  return lines;
}

function buildSidebarItems(entries) {
  return entries.map((entry) =>
    entry.type === "page"
      ? { text: entry.text, link: entry.link }
      : { text: entry.text, items: buildSidebarItems(entry.entries) },
  );
}

export function collectKnowledgeSections(filePaths) {
  const sectionsByName = new Map();

  for (const filePath of filePaths) {
    const normalized = normalizePath(filePath);
    if (!normalized.startsWith("knowledge-base/") || !normalized.endsWith(".md")) {
      continue;
    }

    const segments = normalized.split("/");
    if (segments.length < 3) {
      continue;
    }

    const sectionName = segments[1];
    const fileName = segments.at(-1);

    if (!sectionsByName.has(sectionName)) {
      sectionsByName.set(sectionName, {
        name: sectionName,
        baseLink: `/knowledge-base/${sectionName}/`,
        sourceDir: `knowledge-base/${sectionName}`,
        indexSource: null,
        entries: [],
      });
    }

    const section = sectionsByName.get(sectionName);
    if (INDEX_CANDIDATES.has(fileName)) {
      section.indexSource ??= normalized;
      continue;
    }

    const nestedSegments = segments.slice(2, -1);
    let currentEntries = section.entries;

    for (let index = 0; index < nestedSegments.length; index += 1) {
      const segment = nestedSegments[index];
      let directory = currentEntries.find(
        (entry) => entry.type === "directory" && entry.text === segment,
      );

      if (!directory) {
        directory = createDirectoryEntry(
          sectionName,
          segment,
          nestedSegments.slice(0, index + 1),
        );
        currentEntries.push(directory);
      }

      currentEntries = directory.entries;
    }

    currentEntries.push(createPageEntry(normalized, fileName));
  }

  return [...sectionsByName.values()]
    .sort((left, right) => compareNames(left.name, right.name))
    .map((section) => ({
      ...section,
      entries: sortEntries(section.entries),
    }));
}

export function buildSidebar(sections) {
  return Object.fromEntries(
    sections.map((section) => [
      section.baseLink,
      [
        {
          text: section.name,
          items: [{ text: "概览", link: section.baseLink }, ...buildSidebarItems(section.entries)],
        },
      ],
    ]),
  );
}

export function buildHomeMarkdown(sections) {
  const lines = [
    "# knowledge-notes",
    "",
    "个人知识库预览站，内容来自 `knowledge-base/`。",
    "",
    "## 栏目",
    "",
  ];

  for (const section of sections) {
    const countLabel = `${countPages(section.entries)} 篇`;
    lines.push(`- [${section.name}](${section.baseLink}) · ${countLabel}`);
  }

  if (sections.length === 0) {
    lines.push("- 暂无可发布内容");
  }

  return `${lines.join("\n")}\n`;
}

export function buildSectionMarkdown(section) {
  const lines = [
    `# ${section.name}`,
    "",
    `当前栏目共 ${countPages(section.entries)} 篇文档。`,
    "",
    "## 文档列表",
    "",
  ];

  if (section.entries.length === 0) {
    lines.push("- 暂无内容");
  } else {
    lines.push(...buildSectionListLines(section.entries));
  }

  return `${lines.join("\n")}\n`;
}

export function sanitizeMarkdownForVitePress(markdown, filePath = "") {
  const lines = markdown.split("\n");
  let inFence = false;

  return lines
    .map((line) => {
      if (/^```/.test(line.trim())) {
        inFence = !inFence;
        return line;
      }

      if (inFence) {
        return line;
      }

      const normalizedLine = line.replace(
        /!\[([^\]]*)\]\(((?:[A-Za-z]:\\|file:\/\/)[^)]+)\)/g,
        (_, _alt, target) => `本地图片路径：\`${target}\``,
      );
      const safeImageLine = normalizedLine.replace(
        /!\[([^\]]*)\]\(((?!https?:\/\/|\/)[^)]+)\)/g,
        (match, _alt, target) => {
          if (!filePath) {
            return match;
          }

          const resolvedTarget = path.resolve(path.dirname(filePath), target);
          return fs.existsSync(resolvedTarget)
            ? match
            : `缺失图片资源：\`${target}\``;
        },
      );
      const placeholders = [];
      const protectedLine = safeImageLine.replace(
        SAFE_INLINE_TAG_PAIR_PATTERN,
        (match) => {
          const marker = `__SAFE_HTML_TAG_${placeholders.length}__`;
          placeholders.push(match);
          return marker;
        },
      );
      const escapedLine = protectedLine
        .replace(/<[^>\n]*>?/g, (match) =>
          match.replace(/</g, "&lt;").replace(/>/g, "&gt;"),
        )
        .replace(/\{/g, "&#123;")
        .replace(/\}/g, "&#125;");

      return escapedLine.replace(/__SAFE_HTML_TAG_(\d+)__/g, (_, index) => placeholders[Number(index)]);
    })
    .join("\n");
}

export function buildCanvasPageMarkdown(canvasBase64) {
  return [
    "<!-- Auto-generated by scripts/prepare-docs.mjs -->",
    "",
    `<CanvasPage canvas-base64="${canvasBase64}" />`,
    "",
  ].join("\n");
}

export async function listKnowledgeMarkdownFiles(contentDir) {
  const files = [];

  async function walk(currentDir) {
    const entries = await fsp.readdir(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith(".")) {
        continue;
      }

      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }

      if (entry.isFile() && entry.name.endsWith(".md")) {
        files.push(normalizePath(path.relative(process.cwd(), fullPath)));
      }
    }
  }

  await walk(contentDir);
  return files.sort(compareNames);
}

export async function listKnowledgeCanvasFiles(contentDir) {
  const files = [];

  async function walk(currentDir) {
    const entries = await fsp.readdir(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith(".")) {
        continue;
      }

      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }

      if (entry.isFile() && entry.name.endsWith(".canvas")) {
        files.push(normalizePath(path.relative(process.cwd(), fullPath)));
      }
    }
  }

  await walk(contentDir);
  return files.sort(compareNames);
}

export function mapCanvasToGeneratedMarkdown(filePath) {
  return normalizePath(filePath).replace(/\.canvas$/i, ".canvas.md");
}

export function mapCanvasToSitePath(filePath) {
  const normalized = normalizePath(filePath);
  return normalized.startsWith("/") ? normalized : `/${normalized}`;
}

export function toCanvasPageTitle(filePath) {
  return stripCanvasExtension(path.basename(filePath));
}

export async function rewriteMarkdownFiles(rootDir, transform) {
  async function walk(currentDir) {
    const entries = await fsp.readdir(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }

      if (!entry.isFile() || !entry.name.endsWith(".md")) {
        continue;
      }

      const original = await fsp.readFile(fullPath, "utf8");
      const updated = transform(original, fullPath);
      if (updated !== original) {
        await fsp.writeFile(fullPath, updated, "utf8");
      }
    }
  }

  await walk(rootDir);
}
