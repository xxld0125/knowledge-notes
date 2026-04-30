<script setup>
import { JSONCanvasViewerComponent } from "@json-canvas-viewer/vue";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const props = defineProps({
  canvasBase64: {
    type: String,
    required: true,
  },
});

let canvas = null;
let errorMessage = "";
const containerRef = ref(null);
const isFullscreen = ref(false);
const isToggleHovered = ref(false);
const fullscreenButtonLabel = computed(() =>
  isFullscreen.value ? "退出全屏" : "全屏展示",
);
const fullscreenTipText = computed(() =>
  isFullscreen.value ? "按 Esc 退出全屏" : "全屏展示",
);
const showFullscreenTip = computed(
  () => isFullscreen.value || isToggleHovered.value,
);

try {
  const rawBytes = Uint8Array.from(atob(props.canvasBase64), (char) =>
    char.charCodeAt(0),
  );
  const rawText = new TextDecoder().decode(rawBytes);
  canvas = JSON.parse(rawText);
} catch (error) {
  errorMessage = error instanceof Error ? error.message : String(error);
}

function handleFullscreenChange() {
  if (typeof document === "undefined") {
    return;
  }
  isFullscreen.value = document.fullscreenElement === containerRef.value;
}

async function toggleFullscreen() {
  if (typeof document === "undefined") {
    return;
  }

  if (document.fullscreenElement === containerRef.value) {
    await document.exitFullscreen();
    return;
  }

  await containerRef.value?.requestFullscreen?.();
}

onMounted(() => {
  document.addEventListener("fullscreenchange", handleFullscreenChange);
  handleFullscreenChange();
});

onBeforeUnmount(() => {
  document.removeEventListener("fullscreenchange", handleFullscreenChange);
});
</script>

<template>
  <ClientOnly>
    <section ref="containerRef" class="canvas-page">
      <button
        class="fullscreen-toggle"
        type="button"
        :aria-label="fullscreenButtonLabel"
        :title="fullscreenButtonLabel"
        @click="toggleFullscreen"
        @mouseenter="isToggleHovered = true"
        @mouseleave="isToggleHovered = false"
        @focus="isToggleHovered = true"
        @blur="isToggleHovered = false"
      >
        <svg
          v-if="!isFullscreen"
          viewBox="0 0 24 24"
          aria-hidden="true"
          class="fullscreen-icon"
        >
          <path
            d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          />
        </svg>
        <svg
          v-else
          viewBox="0 0 24 24"
          aria-hidden="true"
          class="fullscreen-icon"
        >
          <path
            d="M9 4H4v5M15 4h5v5M9 20H4v-5M20 20h-5v-5"
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          />
        </svg>
      </button>
      <Transition name="fullscreen-tip-fade">
        <p v-if="showFullscreenTip" class="fullscreen-tip">
          {{ fullscreenTipText }}
        </p>
      </Transition>
      <p v-if="errorMessage" class="canvas-error">
        Canvas 加载失败：{{ errorMessage }}
      </p>
      <Suspense v-else>
        <div class="canvas-viewer-host">
          <JSONCanvasViewerComponent :canvas="canvas" />
        </div>
        <template #fallback>
          <p class="canvas-loading">正在加载 Canvas...</p>
        </template>
      </Suspense>
    </section>
  </ClientOnly>
</template>

<style scoped>
.canvas-page {
  position: relative;
  height: 70vh;
  min-height: 70vh;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
  background: var(--vp-c-bg);
}

.canvas-page:fullscreen {
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  border: none;
  border-radius: 0;
}

.canvas-viewer-host {
  width: 100%;
  height: 100%;
}

.canvas-viewer-host :deep(section) {
  width: 100%;
  height: 100%;
  max-width: none !important;
  max-height: none !important;
}

.canvas-viewer-host :deep(.JSON-Canvas-Viewer) {
  width: 100%;
  height: 100%;
}

.fullscreen-toggle {
  position: absolute;
  z-index: 10;
  top: 12px;
  right: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 85%, transparent);
  border-radius: 999px;
  background: color-mix(in srgb, var(--vp-c-bg) 72%, transparent);
  backdrop-filter: blur(8px);
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.fullscreen-toggle:hover {
  border-color: color-mix(
    in srgb,
    var(--vp-c-brand-1) 50%,
    var(--vp-c-divider)
  );
  background: color-mix(in srgb, var(--vp-c-bg) 86%, var(--vp-c-brand-soft));
  color: var(--vp-c-text-1);
}

.fullscreen-tip {
  position: absolute;
  z-index: 10;
  top: 56px;
  right: 12px;
  margin: 0;
  padding: 4px 10px;
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 85%, transparent);
  border-radius: 999px;
  background: color-mix(in srgb, var(--vp-c-bg) 72%, transparent);
  backdrop-filter: blur(8px);
  color: var(--vp-c-text-2);
  font-size: 12px;
  line-height: 1.4;
  pointer-events: none;
}

.fullscreen-tip-fade-enter-active,
.fullscreen-tip-fade-leave-active {
  transition:
    opacity 0.18s ease,
    transform 0.18s ease;
}

.fullscreen-tip-fade-enter-from,
.fullscreen-tip-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.fullscreen-icon {
  width: 18px;
  height: 18px;
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
