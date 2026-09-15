<template>
  <div
    class="flex-1 flex flex-col px-4 sm:px-8 max-w-[1720px] mx-auto w-full select-none transition-all duration-200"
    :style="{
      paddingTop: 'calc(0.75rem + env(safe-area-inset-top, 16px))',
      paddingBottom: 'calc(8rem + env(safe-area-inset-bottom, 0px))'
    }"
  >
    <!-- 顶部三段式分段控制器 (Segmented Control) (1:1 像素级对齐) -->
    <div class="flex justify-center pt-2 pb-3">
      <div class="bg-[#232429]/80 backdrop-blur-md rounded-full p-1 inline-flex border border-white/10 shadow-lg">
        <button
          @click="activeSegment = 'general'"
          class="px-5 py-1.5 text-xs sm:text-sm rounded-full transition-all duration-200"
          :class="[
            activeSegment === 'general'
              ? 'bg-[#121316] text-white font-bold shadow-md'
              : 'text-white/60 hover:text-white font-medium'
          ]"
        >
          通用
        </button>
        <button
          @click="activeSegment = 'watch'"
          class="px-5 py-1.5 text-xs sm:text-sm rounded-full transition-all duration-200"
          :class="[
            activeSegment === 'watch'
              ? 'bg-[#121316] text-white font-bold shadow-md'
              : 'text-white/60 hover:text-white font-medium'
          ]"
        >
          观看
        </button>
        <button
          @click="activeSegment = 'favorites'"
          class="px-5 py-1.5 text-xs sm:text-sm rounded-full transition-all duration-200"
          :class="[
            activeSegment === 'favorites'
              ? 'bg-[#121316] text-white font-bold shadow-md'
              : 'text-white/60 hover:text-white font-medium'
          ]"
        >
          收藏
        </button>
      </div>
    </div>

    <!-- ==================== 1. 观看历史 (默认高亮选中) ==================== -->
    <section v-if="activeSegment === 'watch'" class="flex-1 flex flex-col mt-2">
      <!-- 大标题: 加粗高对比度白色大字 媒体观看 -->
      <h1 class="text-2xl md:text-3xl font-black text-white mt-4 mb-2 tracking-tight">
        媒体观看
      </h1>

      <!-- 服务器标识: 翡翠绿倾斜菱形播放标 (#28C76F) + OKMedia + > (chevron) + 翠绿色发光小圆点 (🟢) -->
      <div class="relative inline-block mb-4 self-start">
        <button
          @click="showServerDropdown = !showServerDropdown"
          class="inline-flex items-center gap-2 py-1.5 px-3 rounded-full bg-white/5 hover:bg-white/10 active:scale-95 border border-white/10 transition-all text-xs group"
          title="点击切换影视服务器历史"
        >
          <!-- 翡翠绿倾斜菱形播放标 (#28C76F) -->
          <div class="w-4 h-4 rounded-[3.5px] bg-[#28C76F] flex items-center justify-center rotate-45 shadow-[0_0_8px_rgba(40,199,111,0.6)] flex-shrink-0">
            <svg class="w-2 h-2 fill-white -rotate-45 translate-x-0.2" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>

          <!-- OKMedia -->
          <span class="font-bold text-white tracking-wide">{{ currentServerName }}</span>

          <!-- > (chevron) -->
          <svg class="w-3.5 h-3.5 text-white/50 group-hover:text-white transition-transform" :class="{ 'rotate-90': showServerDropdown }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M9 5l7 7-7 7"/>
          </svg>

          <!-- 翠绿色发光小圆点 (🟢) -->
          <span class="w-2 h-2 rounded-full bg-[#28C76F] shadow-[0_0_8px_#28C76F] animate-pulse"></span>
        </button>

        <!-- 服务器切换浮层下拉菜单 -->
        <transition name="fade">
          <div
            v-if="showServerDropdown"
            class="absolute top-10 left-0 w-56 rounded-2xl bg-[#181920]/95 backdrop-blur-2xl border border-white/15 p-2 shadow-2xl space-y-1 z-50 text-xs"
          >
            <div class="px-3 py-1 text-[10px] text-white/40 font-medium tracking-wider">
              切换历史所属服务器
            </div>
            <button
              v-for="s in servers"
              :key="s.id"
              @click="handleSelectServer(s.id)"
              class="w-full text-left px-3 py-2 rounded-xl flex items-center justify-between text-white/80 hover:text-white hover:bg-white/10 transition"
              :class="{ 'bg-white/10 text-emerald-400 font-semibold': s.id === currentServerId }"
            >
              <div class="flex items-center gap-2 truncate">
                <span class="w-2 h-2 rounded-full" :class="s.status === 'online' ? 'bg-emerald-400' : 'bg-zinc-500'"></span>
                <span class="truncate">{{ s.name }}</span>
              </div>
              <span v-if="s.id === currentServerId" class="text-[10px] text-emerald-400">✓</span>
            </button>
          </div>
        </transition>
      </div>

      <!-- 双列 16:9 历史卡片网格 (手机端标准双列流式排版) -->
      <div v-if="historyList.length > 0" class="grid grid-cols-2 gap-3.5 sm:gap-4 md:gap-5 max-w-4xl">
        <div
          v-for="item in historyList"
          :key="item.id"
          class="group cursor-pointer flex flex-col select-none"
          @click="playHistoryItem(item)"
        >
          <!-- 16:9 卡片圆角封面容器 -->
          <div class="relative w-full aspect-[16/9] rounded-xl sm:rounded-2xl overflow-hidden bg-[#181920] border border-white/10 shadow-lg transition-transform duration-300 group-hover:scale-[1.02]">
            <img
              :src="item.backdrop || item.poster"
              :alt="item.title"
              class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />

            <!-- 悬浮微型播放图标蒙层 -->
            <div class="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors flex items-center justify-center">
              <div class="w-10 h-10 rounded-full border border-white/80 bg-black/40 backdrop-blur-sm flex items-center justify-center shadow-xl opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all">
                <svg class="w-4 h-4 fill-white translate-x-0.5" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
            </div>

            <!-- 贴底进度指示条 (红/白色细条) -->
            <div class="absolute bottom-0 left-0 right-0 h-[3px] bg-white/25 overflow-hidden">
              <div
                class="h-full bg-[#E50914] rounded-full transition-all duration-300"
                :style="{ width: `${Math.min(Math.max((item.progress || 0.05) * 100, 3), 100)}%` }"
              ></div>
            </div>

            <!-- 右下角时间进度角标: 半透明黑底小药丸，内嵌白色微型播放小三角及时间比率 -->
            <div class="absolute bottom-2 right-2 px-2 py-0.5 rounded-full bg-black/75 backdrop-blur-md border border-white/15 text-[10px] text-white/95 flex items-center gap-1 font-mono tracking-tight pointer-events-none shadow-md">
              <svg class="w-2 h-2 fill-white flex-shrink-0" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <span>{{ item.progressTime }}</span>
            </div>
          </div>

          <!-- 卡片文字信息: 主标题 + 副标 -->
          <div class="mt-2 px-0.5">
            <h3 class="text-sm font-bold text-white truncate group-hover:text-emerald-400 transition-colors">
              {{ item.title }}
            </h3>
            <p class="text-xs text-white/50 truncate mt-0.5 font-medium">
              {{ item.subtitle }}
            </p>
          </div>
        </div>
      </div>

      <!-- 空记录状态 -->
      <div v-else class="text-center py-24 text-white/40 text-sm flex flex-col items-center gap-3">
        <svg class="w-12 h-12 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke-width="1.5"/>
          <polyline points="12 6 12 12 16 14" stroke-width="1.5"/>
        </svg>
        <span>暂无媒体观看记录，播放影片后将自动在此记录播放进度</span>
      </div>
    </section>

    <!-- ==================== 2. 收藏夹视图 ==================== -->
    <section v-else-if="activeSegment === 'favorites'" class="flex-1 flex flex-col mt-2">
      <h1 class="text-2xl md:text-3xl font-black text-white mt-4 mb-2 tracking-tight">
        媒体收藏
      </h1>
      <p class="text-xs text-white/40 mb-4">
        已离线持久化至本地沙盒的精选影视追剧收藏
      </p>

      <div v-if="favoritesList.length > 0" class="grid grid-cols-2 gap-3.5 sm:gap-4 md:gap-5 max-w-4xl">
        <div
          v-for="fav in favoritesList"
          :key="fav.id"
          class="group cursor-pointer flex flex-col select-none"
          @click="playFavoriteItem(fav)"
        >
          <div class="relative w-full aspect-[16/9] rounded-xl sm:rounded-2xl overflow-hidden bg-[#181920] border border-white/10 shadow-lg group-hover:scale-[1.02] transition-transform duration-300">
            <img
              :src="fav.backdrop || fav.poster"
              :alt="fav.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
            <div class="absolute top-2 right-2 px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-[10px] text-red-400 flex items-center gap-1 font-medium">
              <span>♥</span>
              <span>已收藏</span>
            </div>
            <div class="absolute bottom-2 left-2 px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md text-[10px] text-white/80 font-mono">
              ★ {{ fav.rating || '9.0' }}
            </div>
          </div>
          <div class="mt-2 px-0.5">
            <h3 class="text-sm font-bold text-white truncate group-hover:text-emerald-400 transition-colors">
              {{ fav.title }}
            </h3>
            <p class="text-xs text-white/50 truncate mt-0.5">
              {{ fav.subtitle }}
            </p>
          </div>
        </div>
      </div>
      <!-- 收藏夹空状态 -->
      <div v-else class="text-center py-24 text-white/40 text-sm flex flex-col items-center gap-3">
        <svg class="w-12 h-12 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke-width="1.5"/>
        </svg>
        <span>暂无收藏影视，在影视详情中可加入收藏</span>
      </div>
    </section>

    <!-- ==================== 3. 通用设置与管理视图 ==================== -->
    <section v-else-if="activeSegment === 'general'" class="flex-1 flex flex-col mt-2 max-w-2xl">
      <h1 class="text-2xl md:text-3xl font-black text-white mt-4 mb-2 tracking-tight">
        历史与通用管理
      </h1>
      <p class="text-xs text-white/40 mb-5">
        管理本地沙盒存储与媒体记录同步策略
      </p>

      <div class="space-y-3">
        <!-- 存储驱动卡片 -->
        <div class="p-4 rounded-2xl bg-[#181920]/80 border border-white/10 flex items-center justify-between">
          <div>
            <div class="text-sm font-semibold text-white">沙盒持久化存储引擎</div>
            <div class="text-xs text-white/40 mt-0.5">IndexedDB + LocalStorage 高保真双轨容灾</div>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#28C76F]"></span>
            <span class="text-xs font-mono text-emerald-400">已就绪 ({{ historyList.length }}条)</span>
          </div>
        </div>

        <!-- 自动记录进度开关 -->
        <div class="p-4 rounded-2xl bg-[#181920]/80 border border-white/10 flex items-center justify-between">
          <div>
            <div class="text-sm font-semibold text-white">实时保存播放进度</div>
            <div class="text-xs text-white/40 mt-0.5">播放器播放中每 3 秒实时回传写库</div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="autoSaveProgress" class="sr-only peer">
            <div class="w-11 h-6 bg-white/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
          </label>
        </div>

        <!-- 云端自动同步开关 -->
        <div class="p-4 rounded-2xl bg-[#181920]/80 border border-white/10 flex items-center justify-between">
          <div>
            <div class="text-sm font-semibold text-white">多端观影状态同步</div>
            <div class="text-xs text-white/40 mt-0.5">连通 Emby / Jellyfin 服务端回传心跳</div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="cloudSyncEnabled" class="sr-only peer">
            <div class="w-11 h-6 bg-white/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
          </label>
        </div>


        <!-- 清空所有历史 -->
        <div class="p-4 rounded-2xl bg-[#181920]/80 border border-red-500/20 flex items-center justify-between">
          <div>
            <div class="text-sm font-semibold text-red-400">清空所有观看记录</div>
            <div class="text-xs text-white/40 mt-0.5">擦除 IndexedDB 中的全量历史与断点记忆</div>
          </div>
          <button
            @click="handleClearHistory"
            class="px-3.5 py-1.5 rounded-xl bg-red-500/20 hover:bg-red-500/30 text-xs font-semibold text-red-300 transition active:scale-95"
          >
            清空记录
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  getInitialHistory,
  getPlaybackHistory,
  clearPlaybackHistory,
  getInitialFavorites,
  getFavorites
} from '../utils/offlineStore.js'

const props = defineProps({
  servers: {
    type: Array,
    default: () => []
  },
  currentServerId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['play', 'switch-server'])

// 分段控制器标签: 'watch' (默认) | 'general' | 'favorites'
const activeSegment = ref('watch')
const showServerDropdown = ref(false)

const autoSaveProgress = ref(true)
const cloudSyncEnabled = ref(true)

// 观看历史列表与收藏列表
const historyList = ref(getInitialHistory())
const favoritesList = ref(getInitialFavorites())

const currentServerName = computed(() => {
  const s = props.servers.find(item => item.id === props.currentServerId)
  return s ? s.name : (props.servers[0]?.name || '未选择服务器')
})

function handleSelectServer(serverId) {
  emit('switch-server', serverId)
  showServerDropdown.value = false
  refreshData(serverId)
}

async function refreshData(serverId = props.currentServerId) {
  historyList.value = await getPlaybackHistory(serverId)
  favoritesList.value = await getFavorites()
}

function playHistoryItem(item) {
  emit('play', {
    ...item,
    initialSeekTime: item.currentTime || 0
  })
}

function playFavoriteItem(fav) {
  emit('play', {
    ...fav,
    initialSeekTime: 0
  })
}

async function handleClearHistory() {
  if (confirm('确定要清空全部媒体观看历史吗？')) {
    await clearPlaybackHistory()
    historyList.value = []
  }
}

onMounted(async () => {
  await refreshData()
})

watch(() => props.currentServerId, (newId) => {
  refreshData(newId)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
