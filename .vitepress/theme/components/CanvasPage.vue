<script setup>
import { JSONCanvasViewerComponent } from "@json-canvas-viewer/vue";

const props = defineProps({
  canvasBase64: {
    type: String,
    required: true,
  },
});

let canvas = null;
let errorMessage = "";

try {
  const rawBytes = Uint8Array.from(atob(props.canvasBase64), (char) =>
    char.charCodeAt(0),
  );
  const rawText = new TextDecoder().decode(rawBytes);
  canvas = JSON.parse(rawText);
} catch (error) {
  errorMessage = error instanceof Error ? error.message : String(error);
}
</script>

<template>
  <ClientOnly>
    <section class="canvas-page">
      <p v-if="errorMessage" class="canvas-error">
        Canvas 加载失败：{{ errorMessage }}
      </p>
      <Suspense v-else>
        <JSONCanvasViewerComponent :canvas="canvas" />
        <template #fallback>
          <p class="canvas-loading">正在加载 Canvas...</p>
        </template>
      </Suspense>
    </section>
  </ClientOnly>
</template>

<style scoped>
.canvas-page {
  min-height: 70vh;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
}

.canvas-loading,
.canvas-error {
  margin: 0;
  padding: 16px;
  color: var(--vp-c-text-2);
}

.canvas-error {
  color: var(--vp-c-danger-1);
}
</style>
