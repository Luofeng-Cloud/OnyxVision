<template>
  <div class="min-h-screen bg-[#0A0B0E] text-white flex flex-col selection:bg-emerald-500 selection:text-white pb-32">
    <!-- 顶部标题栏 -->
    <header class="pt-10 pb-4 px-5 flex items-center justify-between sticky top-0 bg-[#0A0B0E]/90 backdrop-blur-xl z-30 border-b border-white/5">
      <div class="w-11"></div>
      <h1 class="text-base sm:text-lg font-bold text-white tracking-wide">
        系统设置
      </h1>
      <div class="w-11"></div>
    </header>

    <main class="flex-1 px-5 pt-4 max-w-md mx-auto w-full space-y-5">
      <!-- 品牌卡片 -->
      <div class="p-5 rounded-[24px] bg-gradient-to-br from-[#181920] to-[#121318] border border-white/10 flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#a855f7] via-[#6366f1] to-[#06b6d4] p-[1px] shadow-lg flex-shrink-0">
          <div class="w-full h-full bg-[#0A0B0E] rounded-[15px] flex items-center justify-center">
            <svg class="w-6 h-6 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polygon points="12,2 19,5.5 22,12 19,18.5 12,22 5,18.5 2,12 5,5.5" stroke-width="2"/>
            </svg>
          </div>
        </div>
        <div>
          <div class="text-base font-bold text-white">OnyxVision (曜石视界)</div>
          <div class="text-xs text-white/50">v1.0.0 · 极简私有云流媒体中枢</div>
        </div>
      </div>

      <!-- 离线持久化中枢状态卡片 -->
      <div class="space-y-2">
        <div class="text-xs text-white/50 px-1 font-medium">离线持久化与沙盒容灾</div>
        <div class="rounded-[22px] bg-[#141519] border border-white/[0.08] p-4 space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#22c55e]"></span>
              <span class="text-sm font-semibold text-white">IndexedDB 离线沙盒</span>
            </div>
            <span class="text-xs text-emerald-400 font-mono">100% 缓存已就绪</span>
          </div>

          <p class="text-xs text-white/55 leading-relaxed">
            配置好的服务器及其全部海报、选集、剧情简介均已写入手机本地沙盒。原 Emby 服务器断开后依然可以 0ms 秒进浏览与选集。
          </p>

          <div class="pt-2 border-t border-white/5 flex items-center justify-between text-xs">
            <span class="text-white/70">模拟原服务器宕机/离线模式</span>
            <button
              @click="$emit('toggle-simulated-offline')"
              class="px-3 py-1 rounded-full text-xs font-medium transition"
              :class="isSimulatedOffline ? 'bg-amber-500 text-black font-bold' : 'bg-white/10 text-white/70 hover:text-white'"
            >
              {{ isSimulatedOffline ? '离线模式开启中' : '正常在线模式' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 播放与解码选项 -->
      <div class="space-y-2">
        <div class="text-xs text-white/50 px-1 font-medium">视听回放引擎</div>
        <div class="rounded-[22px] bg-[#141519] border border-white/[0.08] divide-y divide-white/5 text-xs">
          <div class="p-4 flex items-center justify-between">
            <span class="text-white/90">HDR / 杜比视界色彩映射</span>
            <span class="text-emerald-400 font-mono">DCI-P3 自动映射</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <span class="text-white/90">空间音频 / 杜比全景声透传</span>
            <span class="text-emerald-400 font-mono">原生已启用</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <span class="text-white/90">手势调节亮度与音量</span>
            <span class="text-emerald-400 font-mono">左右双轨手势</span>
          </div>
        </div>
      </div>

      <!-- 快捷操作按钮 -->
      <div class="space-y-2 pt-2">
        <button
          @click="$emit('open-qrcode')"
          class="w-full py-3.5 rounded-full bg-white/10 hover:bg-white/15 text-white font-medium text-xs flex items-center justify-center gap-2 transition active:scale-95"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <span>在 iPhone / 移动端扫码即映</span>
        </button>

        <button
          @click="$emit('open-about')"
          class="w-full py-3 rounded-full text-white/50 hover:text-white text-xs transition"
        >
          关于 OnyxVision (曜石视界) 开源许可
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
defineProps({
  isSimulatedOffline: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-simulated-offline', 'open-qrcode', 'open-about'])
</script>
