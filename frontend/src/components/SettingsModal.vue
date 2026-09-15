<template>
  <div class="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-2xl flex items-center justify-center p-4">
    <div class="relative w-full max-w-2xl bg-[#0A0B0E] border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
      <!-- 动态环境微光 -->
      <div class="absolute -top-24 -right-24 w-80 h-80 rounded-full blur-[100px] bg-purple-600/20 pointer-events-none"></div>
      <div class="absolute -bottom-24 -left-24 w-80 h-80 rounded-full blur-[100px] bg-cyan-600/20 pointer-events-none"></div>

      <!-- 弹窗头部 -->
      <div class="p-6 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-500/20 to-cyan-500/20 flex items-center justify-center border border-white/10">
            <svg class="w-4 h-4 text-cyan-300" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">
              OnyxVision v1.0.0 (曜石视界)
            </h3>
            <p class="text-xs text-white/50">
              极简私有云流媒体中枢 · 系统设置与开源关于
            </p>
          </div>
        </div>

        <button
          @click="$emit('close')"
          class="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white/80 hover:text-white transition"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- 内容区 -->
      <div class="p-6 space-y-6">
        <!-- 品牌标识卡片 -->
        <div class="flex items-center gap-4 p-4 rounded-2xl bg-white/[0.04] border border-white/10">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#a855f7] via-[#6366f1] to-[#06b6d4] p-[1px] shadow-lg shadow-purple-500/25 flex-shrink-0">
            <div class="w-full h-full bg-[#0A0B0E] rounded-[15px] flex items-center justify-center">
              <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none">
                <defs>
                  <linearGradient id="onyxModalGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#a855f7"/>
                    <stop offset="50%" stop-color="#6366f1"/>
                    <stop offset="100%" stop-color="#06b6d4"/>
                  </linearGradient>
                </defs>
                <polygon points="12,2 19,5.5 22,12 19,18.5 12,22 5,18.5 2,12 5,5.5" stroke="url(#onyxModalGlow)" stroke-width="1.8" stroke-linejoin="round" fill="none"/>
                <polygon points="12,6.5 16,8.5 17.5,12 16,15.5 12,17.5 8,15.5 6.5,12 8,8.5" stroke="url(#onyxModalGlow)" stroke-width="1.2" stroke-linejoin="round" fill="url(#onyxModalGlow)" fill-opacity="0.2"/>
                <line x1="12" y1="2" x2="12" y2="6.5" stroke="url(#onyxModalGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="22" y1="12" x2="17.5" y2="12" stroke="url(#onyxModalGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="12" y1="22" x2="12" y2="17.5" stroke="url(#onyxModalGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="2" y1="12" x2="6.5" y2="12" stroke="url(#onyxModalGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <circle cx="12" cy="12" r="1.5" fill="#06b6d4"/>
              </svg>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <h4 class="text-base font-bold text-white">OnyxVision v1.0.0 (曜石视界)</h4>
              <span class="px-2 py-0.5 text-[10px] font-bold rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">Stable</span>
            </div>
            <p class="text-xs text-white/50 mt-1">极简私有云流媒体中枢 · 跨屏直通流与原生视听体验</p>
          </div>
        </div>

        <!-- 开源版权与声明 -->
        <div class="space-y-3">
          <div class="text-xs font-semibold uppercase tracking-wider text-white/50">开源版权与项目信息</div>
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-3 text-xs">
            <p class="text-white/80 leading-relaxed">
              OnyxVision (曜石视界) 是一套由用户主导、遵循 Apple HIG 极简人机交互哲学的开源私有云流媒体中枢。项目支持跨设备自适应流媒体传输、HDR / 杜比视界高保真回放与私有家庭影院全生命周期管理。
            </p>
            <div class="pt-2 border-t border-white/5 flex flex-wrap items-center justify-between gap-2 text-white/60">
              <span>版权所有 © 2024-2026 OnyxVision Contributors. MIT 协议授权开源。</span>
              <a
                href="https://github.com/OnyxVision/onyxvision"
                target="_blank"
                rel="noreferrer"
                class="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium transition"
              >
                <span>GitHub 仓库</span>
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        <!-- 技术参数网格 -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
          <div class="p-3 rounded-xl bg-white/[0.03] border border-white/10">
            <div class="text-white/40 text-[10px]">系统版本</div>
            <div class="text-white font-mono font-medium mt-0.5">v1.0.0 (Onyx Core)</div>
          </div>
          <div class="p-3 rounded-xl bg-white/[0.03] border border-white/10">
            <div class="text-white/40 text-[10px]">内核引擎</div>
            <div class="text-white font-mono font-medium mt-0.5">Vite 5 + Vue 3.4</div>
          </div>
          <div class="p-3 rounded-xl bg-white/[0.03] border border-white/10 col-span-2 sm:col-span-1">
            <div class="text-white/40 text-[10px]">流媒体协议</div>
            <div class="text-white font-mono font-medium mt-0.5">HLS / MP4 / DirectStream</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close'])
</script>
