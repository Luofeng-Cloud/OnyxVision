<template>
  <div
    class="group relative flex flex-col cursor-pointer select-none transition-all duration-300"
    @click="$emit('open-detail', item)"
  >
    <!-- 2:3 黄金比例海报容器 -->
    <div class="relative w-full aspect-[2/3] rounded-2xl overflow-hidden bg-white/5 border border-white/10 shadow-lg group-hover:shadow-2xl group-hover:shadow-red-500/10 group-hover:scale-[1.035] group-hover:border-white/25 transition-all duration-300 ease-out">
      <!-- 海报图片 (带背景图与占位图双重回退) -->
      <img
        :src="item.poster || item.backdrop || '/favicon.svg'"
        :alt="item.title"
        class="w-full h-full object-cover object-center group-hover:brightness-105 transition-all duration-500"
        loading="lazy"
      />

      <!-- 顶部技术小标与来源 (有来源时才渲染，杜绝空蓝框) -->
      <div class="absolute top-2 left-2 right-2 flex items-center justify-between pointer-events-none">
        <span class="px-1.5 py-0.5 text-[9px] font-bold tracking-wider rounded bg-black/60 backdrop-blur-md text-white/90 border border-white/10">
          {{ item.badges?.[0] || item.tags?.[0] || '4K' }}
        </span>
        <span
          v-if="item.source || item.source_id"
          class="px-1.5 py-0.5 text-[9px] font-medium rounded backdrop-blur-md border border-white/10"
          :class="(item.source || 'Emby') === 'Emby' ? 'bg-green-500/20 text-green-300' : 'bg-blue-500/20 text-blue-300'"
        >
          {{ item.source || 'Emby' }}
        </span>
      </div>

      <!-- 悬浮时居中显示的快捷播放按钮 -->
      <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
        <button
          @click.stop="$emit('play', item)"
          class="w-12 h-12 rounded-full bg-white text-black flex items-center justify-center shadow-xl hover:scale-110 active:scale-95 transition-all"
        >
          <svg class="w-5 h-5 fill-current translate-x-0.5" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </button>
      </div>

      <!-- 底部微型已播进度红线 -->
      <div v-if="(item.progress || 0) > 0 || (item.playback?.playback_percentage || 0) > 0" class="absolute bottom-0 left-0 right-0 h-1 bg-black/60 overflow-hidden">
        <div
          class="h-full bg-gradient-to-r from-red-600 to-red-400"
          :style="{ width: `${((item.progress !== undefined ? item.progress : (item.playback?.playback_percentage || 0) / 100)) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- 底部文字信息区 -->
    <div class="mt-2.5 px-0.5 flex flex-col space-y-0.5">
      <div class="flex items-center justify-between gap-1">
        <h3 class="text-sm font-semibold text-white/90 truncate group-hover:text-white transition-colors">
          {{ item.title }}
        </h3>
        <span v-if="item.rating" class="text-xs font-bold text-yellow-400 flex items-center flex-shrink-0">
          ★{{ item.rating }}
        </span>
      </div>
      <div class="flex items-center gap-1.5 text-xs text-white/50">
        <span>{{ item.year }}</span>
        <span>·</span>
        <span class="truncate">{{ (Array.isArray(item.genres) ? item.genres[0] : item.genres) || '影视' }}</span>
        <span v-if="item.type === 'series' || item.type === 'tv'" class="text-[10px] px-1 py-0.2 rounded bg-purple-500/20 text-purple-300 ml-auto flex-shrink-0">
          剧集
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['play', 'open-detail'])
</script>
