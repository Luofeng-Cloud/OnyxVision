<template>
  <div class="min-h-screen bg-[#0A0B0E] text-white flex flex-col selection:bg-emerald-500 selection:text-white pb-32">
    <!-- 顶部标题栏 -->
    <header class="pt-10 pb-4 px-5 flex items-center justify-between sticky top-0 bg-[#0A0B0E]/90 backdrop-blur-xl z-30 border-b border-white/5">
      <div class="w-11"></div>
      <h1 class="text-base sm:text-lg font-bold text-white tracking-wide">
        文件源
      </h1>
      <button
        @click="showAddSource = true"
        class="w-11 h-11 rounded-full bg-[#1C1D21]/90 border border-white/10 flex items-center justify-center text-white hover:bg-white/10 active:scale-95 transition-all shadow-lg text-xl"
        title="挂载新存储源"
      >
        +
      </button>
    </header>

    <!-- 主列表区 -->
    <main class="flex-1 px-5 pt-4 max-w-md mx-auto w-full space-y-4">
      <div class="text-xs text-white/50 px-1">已挂载的存储协议</div>

      <div
        v-for="source in fileSources"
        :key="source.id"
        class="w-full rounded-[22px] bg-[#141519] border border-white/[0.08] p-4 flex items-center justify-between hover:border-white/20 transition-all cursor-pointer group"
      >
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-white/80 group-hover:text-emerald-400 group-hover:border-emerald-500/30 transition-colors">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-6l-2-2H5a2 2 0 0 0-2 2z"/>
            </svg>
          </div>
          <div>
            <div class="text-sm font-semibold text-white group-hover:text-emerald-400 transition-colors">
              {{ source.name }}
            </div>
            <div class="text-[11px] text-white/45 font-mono">
              {{ source.protocol }} · {{ source.endpoint }}
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#22c55e]"></span>
          <svg class="w-4 h-4 text-white/30" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </div>
      </div>

      <!-- 说明卡片 -->
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/8 text-xs text-white/50 space-y-1 leading-relaxed">
        <div class="text-white/80 font-medium">支持多种存储挂载</div>
        <p>支持挂载 Alist 网盘聚合、WebDAV 云盘、局域网 SMB 共享与 NAS 本地目录，与 Emby 影视库无缝聚合。</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showAddSource = ref(false)

const fileSources = ref([
  { id: 'fs_webdav', name: '阿里云盘 WebDAV', protocol: 'WebDAV', endpoint: 'http://192.168.1.100:8080/aliyun', status: 'online' },
  { id: 'fs_smb', name: '家庭 NAS 原盘共享', protocol: 'SMB (Samba)', endpoint: 'smb://192.168.1.200/Media', status: 'online' },
  { id: 'fs_alist', name: 'Alist 聚合存储池', protocol: 'Alist API', endpoint: 'https://pan.sample.com:5244', status: 'online' },
  { id: 'fs_local', name: '本地 4K 原盘 (D:/Movies)', protocol: 'Direct Path', endpoint: 'D:\\Movies\\4K_Remux', status: 'online' }
])
</script>
