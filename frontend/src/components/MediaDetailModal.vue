<template>
  <div class="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-2xl flex justify-center p-0 sm:p-4 lg:p-8 animate-fade-in">
    <!-- 模态框主体 -->
    <div class="relative w-full max-w-5xl bg-[#0A0B0E] border border-white/10 sm:rounded-3xl overflow-hidden shadow-2xl my-auto min-h-screen sm:min-h-0">
      <!-- 动态环境光漫射光晕 (Dynamic Ambient Light) -->
      <div
        class="absolute -top-32 -left-32 w-[600px] h-[600px] rounded-full blur-[140px] opacity-35 pointer-events-none transition-all duration-700"
        :style="{ backgroundColor: item.ambientColor || '#FF2A54' }"
      ></div>
      <div
        class="absolute top-10 right-0 w-[450px] h-[450px] rounded-full blur-[120px] opacity-20 pointer-events-none transition-all duration-700"
        :style="{ backgroundColor: item.ambientColor || '#8A2BE2' }"
      ></div>

      <!-- 关闭按钮 -->
      <button
        @click="$emit('close')"
        class="absolute z-40 p-2.5 rounded-full bg-black/60 hover:bg-white/20 text-white/80 hover:text-white backdrop-blur-xl border border-white/10 transition active:scale-95"
        :style="{
          top: 'calc(0.75rem + env(safe-area-inset-top, 16px))',
          right: 'calc(1rem + env(safe-area-inset-right, 0px))'
        }"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>

      <!-- 顶部沉浸横幅剧照 (带海报与占位图双重回退) -->
      <div class="relative w-full h-[320px] sm:h-[400px] overflow-hidden">
        <img
          :src="item.backdrop || item.poster || '/favicon.svg'"
          :alt="item.title"
          class="w-full h-full object-cover object-center"
        />
        <!-- 渐变融合层 -->
        <div class="absolute inset-0 bg-gradient-to-t from-[#0A0B0E] via-[#0A0B0E]/60 to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-r from-[#0A0B0E]/80 via-transparent to-transparent"></div>

        <!-- 悬浮在横幅上的海报与基础信息 -->
        <div class="absolute bottom-6 left-6 right-6 flex items-end gap-6 z-10">
          <!-- 2:3 黄金比例海报 -->
          <div class="hidden sm:block w-36 sm:w-44 aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl border border-white/20 flex-shrink-0">
            <img :src="item.poster || item.backdrop || '/favicon.svg'" :alt="item.title" class="w-full h-full object-cover" />
          </div>

          <!-- 标题与核心元数据 -->
          <div class="flex-1 space-y-2">
            <!-- 极客技术角标 -->
            <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
              <span
                v-for="b in item.badges"
                :key="b"
                class="px-2.5 py-0.5 text-[10px] font-bold uppercase rounded bg-white/15 backdrop-blur-md border border-white/20 text-white tracking-wider"
              >
                {{ b }}
              </span>
              <span class="text-xs font-bold text-yellow-400 bg-yellow-400/10 border border-yellow-400/20 px-2 py-0.5 rounded">
                ★ {{ item.rating }}
              </span>
            </div>

            <!-- 中文大标题 -->
            <h2 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight drop-shadow-md">
              {{ item.title }}
            </h2>

            <!-- 英文原名、年份、分级、时长 -->
            <div class="flex flex-wrap items-center gap-2 text-xs sm:text-sm text-white/70 font-medium">
              <span>{{ item.originalTitle }}</span>
              <span>·</span>
              <span>{{ item.year }}</span>
              <span>·</span>
              <span class="px-1.5 py-0.5 text-[10px] rounded border border-white/20 bg-white/5">
                {{ item.contentRating }}
              </span>
              <span>·</span>
              <span>{{ item.duration }}</span>
              <span>·</span>
              <span class="text-white/50">{{ Array.isArray(item.genres) ? item.genres.join(' / ') : (item.genres || '') }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 核心操作按钮条 -->
      <div class="px-6 py-4 border-b border-white/10 flex flex-wrap items-center justify-between gap-4 bg-white/[0.02]">
        <div class="flex items-center gap-3">
          <button
            @click="$emit('play', item)"
            class="flex items-center gap-2.5 px-7 py-3 rounded-full bg-white text-black font-semibold text-sm hover:bg-white/90 active:scale-95 shadow-xl shadow-white/10 transition"
          >
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <span>{{ (item.progress > 0 || (item.playback?.playback_percentage > 0) || (item.playback_percentage > 0)) ? '继续播放' : '立即播放' }}</span>
          </button>

          <button
            @click="toggleFavorite"
            class="flex items-center gap-2 px-4 py-3 rounded-full glass-pill text-white text-sm font-medium hover:bg-white/20 transition"
          >
            <svg
              class="w-4 h-4"
              :class="isFav ? 'text-red-500 fill-current' : 'text-white/80'"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
            <span>{{ isFav ? '已收藏' : '添加收藏' }}</span>
          </button>

          <button
            @click="showSpecsDrawer = !showSpecsDrawer"
            class="flex items-center gap-2 px-4 py-3 rounded-full glass-pill text-white text-sm font-medium hover:bg-white/20 transition"
          >
            <svg class="w-4 h-4 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <span>技术参数</span>
          </button>
        </div>

        <div class="flex items-center gap-2 text-xs text-white/60">
          <span>媒体源：</span>
          <span class="px-2 py-1 rounded bg-white/10 text-white font-medium">
            {{ item.source || 'Emby' }}
          </span>
        </div>
      </div>

      <!-- 内容主体：剧情、剧集选集、演职人员 -->
      <div class="p-6 space-y-8">
        <!-- 剧情梗概 -->
        <div>
          <h4 class="text-sm font-semibold uppercase tracking-wider text-white/50 mb-2">
            剧情简介
          </h4>
          <p class="text-base text-white/80 leading-relaxed font-normal">
            {{ item.overview }}
          </p>
        </div>

        <!-- 剧集选集栏（按季切换、单集 16:9 剧照与简介） -->
        <div v-if="item.type === 'series' && item.seasons" class="space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-semibold uppercase tracking-wider text-white/50">
              选集列表
            </h4>
            <!-- 季数切换 Tab -->
            <div class="flex items-center gap-2 bg-white/5 p-1 rounded-xl border border-white/10">
              <button
                v-for="s in item.seasons"
                :key="s.seasonNumber ?? s.season_number"
                @click="activeSeason = (s.seasonNumber ?? s.season_number)"
                class="px-3 py-1 rounded-lg text-xs font-semibold transition"
                :class="activeSeason === (s.seasonNumber ?? s.season_number) ? 'bg-white text-black' : 'text-white/60 hover:text-white'"
              >
                {{ s.seasonTitle || s.name || ('第 ' + (s.seasonNumber ?? s.season_number) + ' 季') }}
              </button>
            </div>
          </div>

          <!-- 单集 16:9 剧照列表 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div
              v-for="ep in currentSeasonEpisodes"
              :key="ep.episodeNumber"
              @click="$emit('play', { ...item, currentEpisode: ep })"
              class="group/ep relative bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl p-2.5 cursor-pointer transition-all duration-200 hover:scale-[1.02]"
            >
              <!-- 16:9 剧照 -->
              <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-black/40 mb-2">
                <img :src="ep.still" :alt="ep.title" class="w-full h-full object-cover group-hover/ep:scale-105 transition duration-300" />
                <div class="absolute inset-0 bg-black/30 group-hover/ep:bg-black/10 transition"></div>
                <!-- 播放悬浮小标 -->
                <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover/ep:opacity-100 transition">
                  <div class="w-8 h-8 rounded-full bg-white/90 text-black flex items-center justify-center shadow-lg">
                    <svg class="w-3.5 h-3.5 fill-current translate-x-0.5" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
                <!-- 时长角标 -->
                <span class="absolute bottom-1.5 right-1.5 px-1.5 py-0.5 text-[10px] rounded bg-black/70 text-white font-medium">
                  {{ ep.duration }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-white/90 truncate">
                  第 {{ ep.episodeNumber }} 集 · {{ ep.title }}
                </span>
              </div>
              <p class="text-[11px] text-white/50 line-clamp-2 mt-1 leading-snug">
                {{ ep.overview }}
              </p>
            </div>
          </div>
        </div>

        <!-- 演职人员横滑头像卡片 -->
        <div v-if="item.actors && item.actors.length > 0">
          <h4 class="text-sm font-semibold uppercase tracking-wider text-white/50 mb-3">
            演职人员
          </h4>
          <div class="flex gap-4 overflow-x-auto no-scrollbar pb-2">
            <div
              v-for="act in item.actors"
              :key="act.name"
              class="flex flex-col items-center text-center w-24 flex-shrink-0 group cursor-default"
            >
              <div class="w-16 h-16 rounded-full overflow-hidden border border-white/15 bg-white/5 shadow-md mb-2 group-hover:border-white/40 transition">
                <img :src="act.avatar" :alt="act.name" class="w-full h-full object-cover" />
              </div>
              <span class="text-xs font-medium text-white/90 truncate w-full">
                {{ act.name }}
              </span>
              <span class="text-[10px] text-white/50 truncate w-full">
                {{ act.role }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 视频技术参数抽屉面板 (Specs Inspector Drawer) -->
      <div
        v-if="showSpecsDrawer"
        class="border-t border-white/10 bg-white/[0.03] p-6 space-y-4 animate-fade-in"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <h4 class="text-base font-bold text-white">
              极客技术规格检视器 (OnyxVision Media Inspector)
            </h4>
          </div>
          <button @click="showSpecsDrawer = false" class="text-xs text-white/50 hover:text-white">
            收起面板
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">视频分辨率与画幅</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.resolution }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">视频编码标准</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.videoCodec }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">HDR 动态范围标准</span>
            <span class="text-yellow-400 font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.hdrFormat }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">色彩空间与色深</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.colorSpace }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">视频平均码率</span>
            <span class="text-red-400 font-mono font-bold text-sm mt-0.5 block">{{ safeSpecs.bitrate }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">母带音频与全景声</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.audioTrack }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">声道布局</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.audioChannels }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">容器封装与文件大小</span>
            <span class="text-white font-mono font-medium text-sm mt-0.5 block">{{ safeSpecs.container }} · {{ safeSpecs.fileSize }}</span>
          </div>

          <div class="bg-black/40 border border-white/10 p-3 rounded-xl">
            <span class="text-white/40 block text-[10px] uppercase font-semibold">外挂/内嵌字幕轨</span>
            <span class="text-white/90 font-mono text-xs mt-0.5 block">{{ safeSpecs.subtitles && safeSpecs.subtitles.length > 0 ? safeSpecs.subtitles.join(', ') : '无' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['close', 'play'])

const isFav = ref(false)
const showSpecsDrawer = ref(false)
const activeSeason = ref(1)

function toggleFavorite() {
  isFav.value = !isFav.value
}

const safeSpecs = computed(() => {
  const s = props.item.specs || props.item.technical_info || {}
  return {
    resolution: s.resolution || '-',
    videoCodec: s.videoCodec || s.video_codec || '-',
    hdrFormat: s.hdrFormat || s.hdr || (props.item.tags && props.item.tags.includes('Dolby Vision') ? 'Dolby Vision' : '-'),
    colorSpace: s.colorSpace || s.color_space || '-',
    bitrate: s.bitrate || '-',
    audioTrack: s.audioTrack || s.audio_codec || '-',
    audioChannels: s.audioChannels || s.audio_channels || '-',
    container: s.container || '-',
    fileSize: s.fileSize || s.file_size || '-',
    subtitles: Array.isArray(s.subtitles) ? s.subtitles : []
  }
})

const currentSeasonEpisodes = computed(() => {
  if (!props.item.seasons) return []
  const s = props.item.seasons.find(item => (item.seasonNumber ?? item.season_number) === activeSeason.value)
  return s ? s.episodes : []
})
</script>
