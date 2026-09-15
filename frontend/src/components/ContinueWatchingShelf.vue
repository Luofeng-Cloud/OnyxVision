<template>
  <section class="max-w-[1720px] mx-auto px-5 sm:px-8 lg:px-12 pt-6 pb-2 select-none">
    <!-- 标题: 继续观看 (1:1 像素级对齐截图 4) -->
    <h2 class="text-base sm:text-lg font-bold tracking-tight text-white mb-3">
      继续观看
    </h2>

    <!-- 16:9 宽屏横滑卡片流 (1:1 像素级对齐截图 4) -->
    <div class="flex items-start gap-3.5 overflow-x-auto no-scrollbar pb-2 -mx-5 px-5 sm:mx-0 sm:px-0">
      <div
        v-for="item in items"
        :key="item.id"
        @click="$emit('play', item)"
        class="flex-shrink-0 w-[205px] sm:w-[240px] group cursor-pointer"
      >
        <!-- 16:9 缩略图容器 (对齐截图 4) -->
        <div class="relative w-full aspect-[16/9] rounded-2xl overflow-hidden bg-white/5 border border-white/10 shadow-lg transition-all duration-300">
          <img
            :src="item.backdrop || item.poster"
            :alt="item.title"
            class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />

          <!-- 中心白色圆圈播放图标 (对齐截图 4) -->
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div class="w-10 h-10 rounded-full border border-white/80 bg-black/40 backdrop-blur-sm flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform">
              <svg class="w-4 h-4 fill-white translate-x-0.5" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </div>

          <!-- 底部贴底进度条 (对齐截图 4: 底部白色槽，内部红色条) -->
          <div class="absolute bottom-1 left-2 right-2 h-1 bg-white/30 rounded-full overflow-hidden">
            <div
              class="h-full bg-[#E50914] rounded-full transition-all duration-300"
              :style="{ width: getProgressWidth(item) }"
            ></div>
          </div>
        </div>

        <!-- 卡片下方标题 (对齐截图 4) -->
        <div class="mt-1.5 text-xs font-medium text-white/90 truncate group-hover:text-white transition-colors">
          {{ item.title }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

defineEmits(['play', 'open-detail'])

function getProgressWidth(item) {
  if (!item) return '0%'
  if (typeof item.progress === 'number' && item.progress > 0) {
    return `${Math.min(100, Math.max(1, Math.round(item.progress * 100)))}%`
  }
  if (item.playback?.playback_percentage !== undefined && item.playback.playback_percentage > 0) {
    return `${Math.min(100, Math.max(1, Math.round(item.playback.playback_percentage)))}%`
  }
  if (typeof item.playback_percentage === 'number' && item.playback_percentage > 0) {
    return `${Math.min(100, Math.max(1, Math.round(item.playback_percentage)))}%`
  }
  return '0%'
}
</script>
