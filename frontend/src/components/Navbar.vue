<template>
  <header class="fixed top-0 left-0 right-0 z-40 transition-all duration-300 pointer-events-none select-none">
    <div
      class="max-w-[1720px] mx-auto px-5 sm:px-6 lg:px-8 flex items-center justify-between gap-3 transition-all duration-300"
      :style="{ paddingTop: 'calc(0.75rem + env(safe-area-inset-top, 16px))' }"
    >
      <!-- 左侧：服务器切换浮动胶囊 (1:1 像素级对齐截图 4: 绿底菱形播放标 + OKMedia) -->
      <div class="relative pointer-events-auto">
        <button
          @click="showServerDropdown = !showServerDropdown"
          class="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#181920]/80 backdrop-blur-2xl border border-white/15 shadow-xl hover:bg-white/10 active:scale-95 transition-all text-xs font-semibold text-white group"
        >
          <!-- 翡翠绿菱形播放小图标 (对齐截图 4) -->
          <div class="w-5 h-5 rounded-[5px] bg-[#22C55E] flex items-center justify-center rotate-45 shadow-[0_0_8px_rgba(34,197,94,0.5)] flex-shrink-0">
            <svg class="w-2.5 h-2.5 fill-white -rotate-45 translate-x-0.2" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>

          <span class="tracking-wide">{{ activeServerName }}</span>
        </button>

        <!-- 服务器切换下拉菜单 -->
        <transition name="fade">
          <div
            v-if="showServerDropdown"
            class="absolute top-11 left-0 w-56 rounded-2xl bg-[#181920]/95 backdrop-blur-2xl border border-white/15 p-2 shadow-2xl space-y-1 z-50 text-xs"
          >
            <div class="px-3 py-1 text-[10px] text-white/40 font-medium tracking-wider">
              已保存的影视服务器 (本地持久化)
            </div>
            <button
              v-for="s in servers"
              :key="s.id"
              @click="handleSelect(s.id)"
              class="w-full text-left px-3 py-2 rounded-xl flex items-center justify-between text-white/80 hover:text-white hover:bg-white/10 transition"
              :class="{ 'bg-white/10 text-emerald-400 font-semibold': s.id === currentServerId }"
            >
              <div class="flex items-center gap-2 truncate">
                <span class="w-2 h-2 rounded-full" :class="s.status === 'online' ? 'bg-emerald-400' : 'bg-zinc-500'"></span>
                <span class="truncate">{{ s.name }}</span>
              </div>
              <span v-if="s.id === currentServerId" class="text-[10px] text-emerald-400">✓</span>
            </button>
            <div class="border-t border-white/10 pt-1">
              <button
                @click="$emit('switch-to-servers'); showServerDropdown = false"
                class="w-full text-left px-3 py-1.5 rounded-xl text-xs text-white/60 hover:text-white hover:bg-white/10 flex items-center gap-1.5"
              >
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                <span>管理与添加服务器...</span>
              </button>
            </div>
          </div>
        </transition>
      </div>

      <!-- 桌面端居中展示品牌 Logo (OnyxVision) -->
      <div class="hidden md:flex items-center gap-2 cursor-pointer select-none pointer-events-auto" @click="$emit('go-home')">
        <span class="text-sm font-bold tracking-wider bg-gradient-to-r from-white via-purple-200 to-cyan-200 bg-clip-text text-transparent">
          OnyxVision · 曜石视界
        </span>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
          Offline Sandboxed
        </span>
      </div>

      <!-- 右侧：圆形操作按钮 ... (1:1 像素级对齐截图 4) -->
      <div class="flex items-center gap-2 pointer-events-auto">
        <button
          @click="showMoreMenu = !showMoreMenu"
          title="更多选项"
          class="w-10 h-10 rounded-full bg-[#181920]/80 backdrop-blur-2xl border border-white/15 flex items-center justify-center text-white/90 hover:text-white hover:bg-white/10 active:scale-95 transition-all shadow-xl"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="5" cy="12" r="2"/>
            <circle cx="12" cy="12" r="2"/>
            <circle cx="19" cy="12" r="2"/>
          </svg>
        </button>

        <!-- 更多选项下拉浮层 -->
        <transition name="fade">
          <div
            v-if="showMoreMenu"
            class="absolute top-16 right-4 sm:right-8 w-48 rounded-2xl bg-[#181920]/95 backdrop-blur-2xl border border-white/15 p-2 shadow-2xl space-y-1 z-50 text-xs"
          >
            <button
              @click="$emit('open-qrcode'); showMoreMenu = false"
              class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
            >
              <svg class="w-4 h-4 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
              <span>移动端扫码即映</span>
            </button>
            <button
              @click="$emit('switch-to-servers'); showMoreMenu = false"
              class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
            >
              <svg class="w-4 h-4 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <rect x="3" y="4" width="18" height="7" rx="2" stroke-width="2"/>
                <rect x="3" y="13" width="18" height="7" rx="2" stroke-width="2"/>
              </svg>
              <span>影视服务器列表</span>
            </button>
            <button
              @click="$emit('open-settings'); showMoreMenu = false"
              class="w-full text-left px-3 py-2 rounded-xl text-white/80 hover:text-white hover:bg-white/10 flex items-center gap-2"
            >
              <svg class="w-4 h-4 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="3" stroke-width="2"/>
              </svg>
              <span>系统设置与关于</span>
            </button>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'

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

const emit = defineEmits(['go-home', 'select-server', 'switch-to-servers', 'open-qrcode', 'open-settings'])

const showServerDropdown = ref(false)
const showMoreMenu = ref(false)

const activeServerName = computed(() => {
  if (!props.servers || props.servers.length === 0) return '未连接服务器'
  const current = props.servers.find(s => s.id === props.currentServerId)
  return current ? current.name : (props.servers[0]?.name || '未连接服务器')
})

function handleSelect(id) {
  emit('select-server', id)
  showServerDropdown.value = false
}
</script>
