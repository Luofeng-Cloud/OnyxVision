<template>
  <div
    class="min-h-screen bg-black text-white flex flex-col selection:bg-emerald-500 selection:text-white select-none transition-all duration-200"
    :style="{ paddingBottom: 'calc(8rem + env(safe-area-inset-bottom, 0px))' }"
  >
    <!-- 顶部导航栏 (1:1 像素级还原对齐截图 2) -->
    <header
      class="pb-3 px-5 flex items-center justify-between sticky top-0 bg-black/90 backdrop-blur-xl z-30 transition-all duration-300"
      :style="{ paddingTop: 'calc(0.75rem + env(safe-area-inset-top, 16px))' }"
    >
      <!-- 左侧圆形大加号 + (对齐截图 2) -->
      <button
        @click="$emit('open-add-drawer')"
        title="添加影视服务器"
        class="w-11 h-11 rounded-full bg-[#1C1C1E] flex items-center justify-center text-white/90 hover:text-white active:scale-95 transition-all text-2xl font-light"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>

      <!-- 居中标题 (改名为资源库) -->
      <h1 class="text-base font-bold text-white tracking-wide">
        资源库
      </h1>

      <!-- 右侧圆形 ... 菜单 (对齐截图 2) -->
      <button
        @click="showServerOptions = !showServerOptions"
        title="服务器选项"
        class="w-11 h-11 rounded-full bg-[#1C1C1E] flex items-center justify-center text-white/90 hover:text-white active:scale-95 transition-all"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="5" cy="12" r="2" />
          <circle cx="12" cy="12" r="2" />
          <circle cx="19" cy="12" r="2" />
        </svg>
      </button>
    </header>

    <!-- 服务器卡片区 (1:1 像素级还原对齐截图 2) -->
    <main class="flex-1 px-5 pt-4">
      <!-- 空状态引导 -->
      <div v-if="!servers || servers.length === 0" class="flex flex-col items-center justify-center py-20 text-center px-4">
        <div class="w-16 h-16 rounded-2xl bg-white/[0.06] border border-white/10 flex items-center justify-center mb-4 text-emerald-400 shadow-xl">
          <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-6l-2-2H5a2 2 0 0 0-2 2z"/>
          </svg>
        </div>
        <h3 class="text-base font-bold text-white mb-1.5">暂未添加影视服务器</h3>
        <p class="text-xs text-white/50 max-w-xs mb-6 leading-relaxed">
          点击上方「+」或下方按钮添加您的 Emby / Jellyfin 服务器，添加后将在此集中管理并自动同步影视资源。
        </p>
        <button
          @click="$emit('open-add-drawer')"
          class="px-5 py-2.5 rounded-full bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-white text-xs font-semibold shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>添加影视服务器</span>
        </button>
      </div>

      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="server in servers"
          :key="server.id"
          @click="handleSelectServer(server)"
          class="w-full rounded-[22px] bg-[#141518] border border-white/[0.08] p-4 cursor-pointer relative group active:scale-[0.98] transition-all"
        >
        <!-- 第一行：左侧翡翠绿圆角矩形播放标 + 主标题 + 翡翠绿在线状态小圆点 (对齐截图 2) -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <!-- 翡翠绿菱形/倾斜圆角徽标 + 白色实心播放三角 (对齐截图 2) -->
            <div class="w-7 h-7 rounded-lg bg-[#28C76F] flex items-center justify-center rotate-45 shadow-[0_0_10px_rgba(40,199,111,0.4)] flex-shrink-0">
              <svg class="w-3 h-3 fill-white -rotate-45 translate-x-0.2" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>

            <!-- 主标题 (OKMedia) -->
            <h2 class="text-base font-bold text-white">
              {{ server.name }}
            </h2>
          </div>

          <!-- 右侧：翡翠绿在线状态小圆点与删除按钮 -->
          <div class="flex items-center gap-2">
            <span
              class="w-2 h-2 rounded-full transition-all"
              :class="[
                isSimulatedOffline
                  ? 'bg-amber-400 shadow-[0_0_8px_#f59e0b]'
                  : server.status === 'online'
                    ? 'bg-[#28C76F] shadow-[0_0_8px_#28C76F]'
                    : 'bg-zinc-600'
              ]"
            ></span>
            <button
              @click.stop="$emit('delete-server', server.id)"
              class="w-6 h-6 rounded-full bg-white/5 hover:bg-red-500/20 text-white/30 hover:text-red-400 flex items-center justify-center transition"
              title="移除该服务器"
            >
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- 第二行：显示服务器 URL (https://link01.okemby.org:8443) (对齐截图 2) -->
        <div class="mt-2 text-[11px] text-white/50 font-mono truncate">
          {{ server.url }}
        </div>

        <!-- 第三行：显示统计：电影数量与剧集数量 -->
        <div class="mt-1 text-[11px] text-white/60">
          电影: {{ server.movieCount ?? '-' }} &nbsp; 剧集: {{ server.seriesCount ?? '-' }}
        </div>

        <!-- 第四行 (底端)：左下显示协议，右下显示最后同步时间 -->
        <div class="mt-2.5 pt-1.5 flex items-center justify-between text-[11px] text-white/40">
          <span>{{ server.protocol || 'Emby' }}</span>
          <span>{{ server.syncTime || '刚刚' }}</span>
        </div>
      </div>
    </div>
  </main>

    <!-- 顶部 ... 菜单下拉浮层 (包含离线容灾模拟、全量同步、添加服务器) -->
    <transition name="fade">
      <div
        v-if="showServerOptions"
        @click="showServerOptions = false"
        class="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm flex items-start justify-end p-5 pt-16"
      >
        <div
          @click.stop
          class="w-52 rounded-2xl bg-[#1C1C1E] border border-white/10 p-2 shadow-2xl space-y-1 text-xs"
        >
          <div class="px-3 py-1 text-[10px] text-white/40 font-medium border-b border-white/5 mb-1">
            容灾与中枢管理
          </div>
          <button
            @click="toggleSimulatedCrash"
            class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
          >
            <span class="w-2 h-2 rounded-full" :class="isSimulatedOffline ? 'bg-amber-400' : 'bg-emerald-400'"></span>
            <span>{{ isSimulatedOffline ? '恢复服务器在线' : '⚡ 模拟原服务器宕机' }}</span>
          </button>
          <button
            @click="syncActiveServer"
            class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
          >
            <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>重新全量同步缓存</span>
          </button>
          <button
            @click="$emit('open-add-drawer'); showServerOptions = false"
            class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
          >
            <svg class="w-3.5 h-3.5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>添加新服务器</span>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  servers: {
    type: Array,
    default: () => []
  },
  activeServerId: {
    type: String,
    default: ''
  },
  isSimulatedOffline: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['open-add-drawer', 'select-server', 'sync-server', 'toggle-simulated-offline', 'delete-server'])

const showServerOptions = ref(false)

function handleSelectServer(server) {
  emit('select-server', server.id)
}

function syncActiveServer() {
  showServerOptions.value = false
  emit('sync-server', props.activeServerId)
}

function toggleSimulatedCrash() {
  showServerOptions.value = false
  emit('toggle-simulated-offline')
}
</script>
