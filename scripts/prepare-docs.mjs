import fs from "node:fs/promises";
import path from "node:path";
import {
  buildCanvasPageMarkdown,
  buildHomeMarkdown,
  buildSectionMarkdown,
  collectKnowledgeSections,
  listKnowledgeCanvasFiles,
  listKnowledgeMarkdownFiles,
  mapCanvasToGeneratedMarkdown,
  rewriteMarkdownFiles,
  sanitizeMarkdownForVitePress,
} from "./lib/docs-site.mjs";

const rootDir = process.cwd();
const sourceDir = path.join(rootDir, "knowledge-base");
const outputDir = path.join(rootDir, ".vitepress", "content");
const copiedKnowledgeBaseDir = path.join(outputDir, "knowledge-base");

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function prepareDocs() {
  const sourceExists = await pathExists(sourceDir);
  if (!sourceExists) {
    throw new Error(`Missing source directory: ${sourceDir}`);
  }

  const markdownFiles = await listKnowledgeMarkdownFiles(sourceDir);
  const canvasFiles = await listKnowledgeCanvasFiles(sourceDir);
  const generatedCanvasMarkdownFiles = canvasFiles.map(mapCanvasToGeneratedMarkdown);
  const sections = collectKnowledgeSections([
    ...markdownFiles,
    ...generatedCanvasMarkdownFiles,
  ]);

  await fs.rm(outputDir, { recursive: true, force: true });
  await fs.mkdir(outputDir, { recursive: true });
  await fs.cp(sourceDir, copiedKnowledgeBaseDir, {
    recursive: true,
    filter: (entry) => !path.basename(entry).startsWith("."),
  });
  await rewriteMarkdownFiles(copiedKnowledgeBaseDir, (content, filePath) =>
    sanitizeMarkdownForVitePress(content, filePath),
  );
  await Promise.all(
    canvasFiles.map(async (canvasFile) => {
      const canvasRaw = await fs.readFile(path.join(rootDir, canvasFile), "utf8");
      const canvasBase64 = Buffer.from(canvasRaw, "utf8").toString("base64");

      const targetMarkdownPath = path.join(
        rootDir,
        ".vitepress",
        "content",
        mapCanvasToGeneratedMarkdown(canvasFile),
      );
      await fs.mkdir(path.dirname(targetMarkdownPath), { recursive: true });
      await fs.writeFile(
        targetMarkdownPath,
        buildCanvasPageMarkdown(canvasBase64),
        "utf8",
      );
    }),
  );

  await fs.writeFile(
    path.join(outputDir, "index.md"),
    buildHomeMarkdown(sections),
    "utf8",
  );

  for (const section of sections) {
    const targetDir = path.join(copiedKnowledgeBaseDir, section.name);
    const targetIndex = path.join(targetDir, "index.md");

    if (section.indexSource) {
      const sourceIndex = path.join(rootDir, section.indexSource);
      await fs.copyFile(sourceIndex, targetIndex);
      continue;
    }

    await fs.writeFile(targetIndex, buildSectionMarkdown(section), "utf8");
  }
}

prepareDocs().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
