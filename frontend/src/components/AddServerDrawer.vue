<template>
  <!-- 背景遮罩：透明可点击，保持背后原界面（包含右上角 ... 与底栏）隐约可见 (1:1 像素级对齐截图 1) -->
  <div class="fixed inset-0 z-50 bg-black/40 backdrop-blur-[2px] select-none" @click="$emit('close')">
    <!-- 浮动在左上方的黑曜石毛玻璃卡片 (对齐截图 1) -->
    <div
      @click.stop
      class="absolute w-[240px] rounded-[24px] bg-[#222226]/95 backdrop-blur-[40px] border border-white/10 p-4 shadow-[0_20px_60px_rgba(0,0,0,0.85)] animate-in fade-in zoom-in-95 duration-200"
      :style="{
        top: 'calc(3.5rem + env(safe-area-inset-top, 16px))',
        left: 'calc(1rem + env(safe-area-inset-left, 0px))'
      }"
    >
      <!-- 标题：添加影视服务器 (对齐截图 1 浅灰柔和标题) -->
      <div class="text-[13px] font-normal text-white/40 mb-3 px-2">
        添加影视服务器
      </div>

      <!-- 协议列表 (对齐截图 1) -->
      <div class="space-y-0.5">
        <div
          v-for="protocol in protocols"
          :key="protocol.id"
          @click="handleSelect(protocol)"
          class="px-2.5 py-2 rounded-xl text-white/95 hover:text-white hover:bg-white/10 active:bg-white/15 cursor-pointer transition-colors text-sm font-normal"
        >
          {{ protocol.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close', 'select-protocol'])

const protocols = [
  { id: 'emby', name: 'Emby' },
  { id: 'jellyfin', name: 'Jellyfin' },
  { id: 'plex', name: 'Plex' },
  { id: 'fnos', name: '飞牛私有云' },
  { id: 'zspace', name: '极空间影视' },
  { id: 'ugreen', name: '绿联云影视' },
  { id: 'kinoflow', name: 'KinoFlow' }
]

function handleSelect(protocol) {
  emit('select-protocol', protocol.name)
}
</script>
