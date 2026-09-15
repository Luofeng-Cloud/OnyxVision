<template>
  <div
    class="fixed left-0 right-0 z-50 flex items-center justify-center pointer-events-none select-none px-4 transition-all duration-200"
    :style="{ bottom: 'calc(1.25rem + env(safe-area-inset-bottom, 0px))' }"
  >
    <div class="flex items-center gap-3 pointer-events-auto">
      <!-- 主 Dock 四分仓黑曜石毛玻璃胶囊 (1:1 像素级对标截图 1、2、4) -->
      <nav class="flex items-center bg-[#1B1C20]/80 backdrop-blur-[30px] border border-white/[0.12] rounded-full p-1.5 shadow-[0_16px_40px_rgba(0,0,0,0.8)]">
        <!-- 1. 首页 (对标截图: [首页]) -->
        <button
          @click="$emit('update:activeTab', 'library')"
          class="flex flex-col items-center justify-center transition-all duration-200"
          :class="[
            activeTab === 'library'
              ? 'bg-black/70 text-white font-medium rounded-full px-4 py-1.5 shadow-inner'
              : 'text-white/60 hover:text-white px-3.5 py-1.5'
          ]"
        >
          <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="4" width="18" height="13" rx="3" stroke="currentColor" stroke-width="1.8" />
            <polygon points="10,8.5 15,10.5 10,12.5" fill="currentColor" />
          </svg>
          <span class="text-[10px] tracking-tight mt-0.5">首页</span>
        </button>

        <!-- 2. 资源库 (改版：点击直达影视服务器列表与添加) -->
        <button
          @click="$emit('update:activeTab', 'servers')"
          class="flex flex-col items-center justify-center transition-all duration-200"
          :class="[
            activeTab === 'servers'
              ? 'bg-black/70 text-white font-medium rounded-full px-4 py-1.5 shadow-inner'
              : 'text-white/60 hover:text-white px-3.5 py-1.5'
          ]"
        >
          <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-6l-2-2H5a2 2 0 0 0-2 2z"/>
          </svg>
          <span class="text-[10px] tracking-tight mt-0.5">资源库</span>
        </button>

        <!-- 3. 记录 (对标截图: [记录], 用户/书签卡片图标) -->
        <button
          @click="$emit('update:activeTab', 'history')"
          class="flex flex-col items-center justify-center transition-all duration-200"
          :class="[
            activeTab === 'history'
              ? 'bg-black/70 text-white font-medium rounded-full px-4 py-1.5 shadow-inner'
              : 'text-white/60 hover:text-white px-3.5 py-1.5'
          ]"
        >
          <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="3.5" y="3.5" width="17" height="17" rx="3" />
            <path d="M7.5 3.5v7l2.5-1.5 2.5 1.5v-7" />
            <line x1="16.5" y1="13" x2="8.5" y2="13" stroke-linecap="round"/>
            <line x1="16.5" y1="16" x2="11.5" y2="16" stroke-linecap="round"/>
          </svg>
          <span class="text-[10px] tracking-tight mt-0.5">记录</span>
        </button>

        <!-- 4. 设置 -->
        <button
          @click="$emit('update:activeTab', 'settings')"
          class="flex flex-col items-center justify-center transition-all duration-200"
          :class="[
            activeTab === 'settings'
              ? 'bg-black/70 text-white font-medium rounded-full px-4 py-1.5 shadow-inner'
              : 'text-white/60 hover:text-white px-3.5 py-1.5'
          ]"
        >
          <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
          <span class="text-[10px] tracking-tight mt-0.5">设置</span>
        </button>
      </nav>

      <!-- 5. 右侧独立悬浮 [🔍 搜索] 圆形按钮 (1:1 像素级对齐截图 1、2、4) -->
      <button
        @click="$emit('toggle-search')"
        :title="isSearchOpen ? '关闭搜索' : '全库搜索'"
        class="w-13 h-13 sm:w-14 sm:h-14 w-[52px] h-[52px] rounded-full bg-[#1B1C20]/80 backdrop-blur-[30px] border border-white/[0.12] flex items-center justify-center transition-all duration-200 shadow-[0_16px_40px_rgba(0,0,0,0.8)] active:scale-95"
        :class="isSearchOpen ? 'bg-white text-black font-bold' : 'text-white/80 hover:text-white'"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="6.5"/>
          <line x1="16" y1="16" x2="21" y2="21" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    default: 'library'
  },
  isSearchOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:activeTab', 'toggle-search'])
</script>
