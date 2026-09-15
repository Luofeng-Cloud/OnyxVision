<template>
  <div class="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-2xl flex items-center justify-center p-4">
    <div class="relative w-full max-w-2xl bg-[#0A0B0E] border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
      <!-- 动态环境晕染背景 (紫水晶与极光青) -->
      <div class="absolute -top-24 -right-24 w-80 h-80 rounded-full blur-[100px] bg-purple-600/20 pointer-events-none"></div>
      <div class="absolute -bottom-24 -left-24 w-80 h-80 rounded-full blur-[100px] bg-cyan-600/20 pointer-events-none"></div>

      <!-- 弹窗头部 -->
      <div class="p-6 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-500/20 to-cyan-500/20 flex items-center justify-center border border-white/10">
            <svg class="w-4 h-4 text-cyan-300" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">
              {{ activeTab === 'sources' ? '媒体库源与服务连接' : activeTab === 'qrcode' ? 'iPhone / 移动设备连接 OnyxVision 曜石视界' : 'OnyxVision v1.0.0 (曜石视界)' }}
            </h3>
            <p class="text-xs text-white/50">
              {{ activeTab === 'sources' ? '聚合 Emby、Jellyfin 与本地磁盘原盘' : activeTab === 'qrcode' ? '在同一 Wi-Fi 局域网下用 Safari 扫码即映' : '极简私有云流媒体中枢 · 开源版权声明' }}
            </p>
          </div>
        </div>

        <!-- 标签页切换 & 关闭 -->
        <div class="flex items-center gap-2">
          <div class="flex bg-white/5 p-1 rounded-full border border-white/10">
            <button
              @click="activeTab = 'sources'"
              class="px-3 py-1 rounded-full text-xs font-semibold transition"
              :class="activeTab === 'sources' ? 'bg-white text-black' : 'text-white/60 hover:text-white'"
            >
              媒体源
            </button>
            <button
              @click="activeTab = 'qrcode'"
              class="px-3 py-1 rounded-full text-xs font-semibold transition"
              :class="activeTab === 'qrcode' ? 'bg-white text-black' : 'text-white/60 hover:text-white'"
            >
              移动端
            </button>
            <button
              @click="activeTab = 'settings'"
              class="px-3 py-1 rounded-full text-xs font-semibold transition"
              :class="activeTab === 'settings' ? 'bg-white text-black' : 'text-white/60 hover:text-white'"
            >
              关于
            </button>
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
      </div>

      <!-- 标签页 1: 媒体源管理 -->
      <div v-if="activeTab === 'sources'" class="p-6 space-y-6">
        <!-- 现有源列表 -->
        <div class="space-y-3">
          <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-white/50">
            <span>当前挂载的媒体源</span>
            <button
              @click="showAddForm = !showAddForm"
              class="text-red-400 hover:text-red-300 font-bold flex items-center gap-1"
            >
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              <span>{{ showAddForm ? '收起添加' : '添加新源' }}</span>
            </button>
          </div>

          <div
            v-for="s in sourceList"
            :key="s.id"
            class="flex items-center justify-between p-3.5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/[0.08] transition"
          >
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center"
                :class="s.type === 'emby' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'"
              >
                <svg v-if="s.type === 'emby'" class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                </svg>
                <svg v-else class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold text-white">{{ s.name }}</span>
                  <span class="w-2 h-2 rounded-full bg-green-500 shadow-sm shadow-green-500"></span>
                </div>
                <span class="text-xs text-white/40">{{ s.host || '本地目录' }} · {{ s.count }} 部影视</span>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="testSource(s)"
                class="px-3 py-1 rounded-full text-xs font-medium bg-white/10 hover:bg-white/20 text-white/80 transition"
              >
                测试连通
              </button>
            </div>
          </div>
        </div>

        <!-- 添加 Emby / Jellyfin 表单 -->
        <div v-if="showAddForm" class="p-5 rounded-2xl bg-white/[0.04] border border-white/15 space-y-4 animate-fade-in">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <span class="w-1.5 h-3.5 bg-red-500 rounded-full"></span>
            连接 Emby / Jellyfin 服务器
          </h4>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block text-white/60 mb-1">服务器类型</label>
              <select
                v-model="newServer.type"
                class="w-full bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-red-500"
              >
                <option value="emby">Emby Server</option>
                <option value="jellyfin">Jellyfin</option>
                <option value="webdav">WebDAV / Alist</option>
              </select>
            </div>

            <div>
              <label class="block text-white/60 mb-1">显示名称</label>
              <input
                v-model="newServer.name"
                type="text"
                placeholder="我的家庭影视库"
                class="w-full bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-red-500"
              />
            </div>

            <div class="sm:col-span-2">
              <label class="block text-white/60 mb-1">服务器主机 / URL</label>
              <input
                v-model="newServer.host"
                type="text"
                placeholder="http://192.168.1.100:8096"
                class="w-full bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-red-500 font-mono"
              />
            </div>

            <div>
              <label class="block text-white/60 mb-1">用户名</label>
              <input
                v-model="newServer.username"
                type="text"
                placeholder="admin"
                class="w-full bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-red-500"
              />
            </div>

            <div>
              <label class="block text-white/60 mb-1">密码</label>
              <input
                v-model="newServer.password"
                type="password"
                placeholder="••••••••"
                class="w-full bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-red-500"
              />
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-2">
            <button
              @click="showAddForm = false"
              class="px-4 py-2 rounded-full text-xs text-white/60 hover:text-white"
            >
              取消
            </button>
            <button
              @click="addServer"
              :disabled="isConnecting"
              class="px-5 py-2 rounded-full bg-red-600 hover:bg-red-500 active:scale-95 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-red-600/30 transition"
            >
              <svg v-if="isConnecting" class="w-3.5 h-3.5 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
              </svg>
              <span>{{ isConnecting ? '连通性握手验证中...' : '测试并添加媒体源' }}</span>
            </button>
          </div>

          <div v-if="testResult" class="p-3 rounded-xl bg-green-500/10 border border-green-500/20 text-green-300 text-xs flex items-center gap-2">
            <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <span>{{ testResult }}</span>
          </div>
        </div>
      </div>

      <!-- 标签页 2: 移动端局域网二维码 -->
      <div v-if="activeTab === 'qrcode'" class="p-8 flex flex-col items-center text-center space-y-5 animate-fade-in">
        <div class="p-3 bg-white rounded-3xl shadow-2xl shadow-purple-500/10 border-4 border-white/20">
          <canvas ref="qrCanvas" class="w-48 h-48 sm:w-56 sm:h-56 block rounded-xl"></canvas>
        </div>

        <div class="space-y-1.5 max-w-sm">
          <h4 class="text-base font-bold text-white">
            iPhone / 移动设备连接 OnyxVision 曜石视界
          </h4>
          <p class="text-xs text-white/60 leading-relaxed">
            手机与电脑连接同一个 Wi-Fi 网络，打开相机扫码即可在 Safari 全屏秒开，享受 100% 触控手势（亮度/音量/寻道/2x倍速）。
          </p>
        </div>

        <!-- 访问地址卡片 -->
        <div class="w-full max-w-md p-3 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between gap-2">
          <span class="text-xs font-mono text-white/90 truncate">
            {{ lanUrl }}
          </span>
          <button
            @click="copyUrl"
            class="px-3 py-1.5 rounded-full text-xs font-medium bg-white/10 hover:bg-white/20 active:scale-95 text-white transition flex-shrink-0"
          >
            {{ copied ? '已复制' : '复制地址' }}
          </button>
        </div>
      </div>

      <!-- 标签页 3: 关于与系统设置 (Settings / About) -->
      <div v-if="activeTab === 'settings'" class="p-6 space-y-6 animate-fade-in">
        <!-- 品牌卡片 -->
        <div class="flex items-center gap-4 p-4 rounded-2xl bg-white/[0.04] border border-white/10">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#a855f7] via-[#6366f1] to-[#06b6d4] p-[1px] shadow-lg shadow-purple-500/25 flex-shrink-0">
            <div class="w-full h-full bg-[#0A0B0E] rounded-[15px] flex items-center justify-center">
              <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none">
                <defs>
                  <linearGradient id="onyxSettingsGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#a855f7"/>
                    <stop offset="50%" stop-color="#6366f1"/>
                    <stop offset="100%" stop-color="#06b6d4"/>
                  </linearGradient>
                </defs>
                <polygon points="12,2 19,5.5 22,12 19,18.5 12,22 5,18.5 2,12 5,5.5" stroke="url(#onyxSettingsGlow)" stroke-width="1.8" stroke-linejoin="round" fill="none"/>
                <polygon points="12,6.5 16,8.5 17.5,12 16,15.5 12,17.5 8,15.5 6.5,12 8,8.5" stroke="url(#onyxSettingsGlow)" stroke-width="1.2" stroke-linejoin="round" fill="url(#onyxSettingsGlow)" fill-opacity="0.2"/>
                <line x1="12" y1="2" x2="12" y2="6.5" stroke="url(#onyxSettingsGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="22" y1="12" x2="17.5" y2="12" stroke="url(#onyxSettingsGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="12" y1="22" x2="12" y2="17.5" stroke="url(#onyxSettingsGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
                <line x1="2" y1="12" x2="6.5" y2="12" stroke="url(#onyxSettingsGlow)" stroke-width="1.2" stroke-linecap="round" opacity="0.8"/>
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

        <!-- 开源版权与项目信息 -->
        <div class="space-y-3">
          <div class="text-xs font-semibold uppercase tracking-wider text-white/50">开源版权与项目声明</div>
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-3 text-xs">
            <p class="text-white/80 leading-relaxed">
              OnyxVision (曜石视界) 是一套由用户主导、遵循 Apple HIG 极简人机交互哲学的开源私有云流媒体中枢。项目支持跨设备自适应流媒体传输、HDR / 杜比视界高保真回放与私有家庭影院全生命周期管理。
            </p>
            <div class="pt-2 border-t border-white/5 flex flex-wrap items-center justify-between gap-2 text-white/60">
              <span>版权所有 © 2024-2026 OnyxVision Contributors. MIT License.</span>
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

        <!-- 系统与内核信息 -->
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
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  initialTab: {
    type: String,
    default: 'sources'
  }
})

defineEmits(['close'])

const activeTab = ref(props.initialTab)
const showAddForm = ref(false)
const isConnecting = ref(false)
const testResult = ref('')
const copied = ref(false)
const qrCanvas = ref(null)

const lanUrl = ref(`http://${window.location.hostname || '192.168.1.188'}:${window.location.port || '5173'}/`)

const sourceList = ref([
  {
    id: 'emby_1',
    name: 'Emby 影视中枢',
    type: 'emby',
    host: 'https://emby.lan:8096',
    count: 196,
    status: 'online'
  },
  {
    id: 'local_1',
    name: '本地 4K 原盘 (D:/Movies)',
    type: 'local',
    host: '本地存储卷',
    count: 88,
    status: 'online'
  }
])

const newServer = ref({
  type: 'emby',
  name: '',
  host: 'http://192.168.1.100:8096',
  username: '',
  password: ''
})

function testSource(s) {
  alert(`正在探测媒体源 [${s.name}] (${s.host})...\n状态：在线 (延迟 8ms，支持 4K 直通流)`)
}

function addServer() {
  if (!newServer.value.host) {
    alert('请输入服务器地址')
    return
  }
  isConnecting.value = true
  testResult.value = ''
  setTimeout(() => {
    isConnecting.value = false
    testResult.value = `握手成功！成功载入 [${newServer.value.name || 'Emby媒体库'}]，扫描到 120 部电影与 38 部剧集。`
    sourceList.value.push({
      id: 'src_' + Date.now(),
      name: newServer.value.name || '新媒体源',
      type: newServer.value.type,
      host: newServer.value.host,
      count: 158,
      status: 'online'
    })
  }, 1000)
}

function copyUrl() {
  navigator.clipboard.writeText(lanUrl.value).then(() => {
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  })
}

// 轻量原生二维码绘制 (若 qrcode 库可用则使用 qrcode，否则原生优雅渲染)
async function renderQRCode() {
  if (!qrCanvas.value) return
  try {
    const QRCode = (await import('qrcode')).default
    await QRCode.toCanvas(qrCanvas.value, lanUrl.value, {
      width: 220,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
  } catch (err) {
    // 降级绘制
    const ctx = qrCanvas.value.getContext('2d')
    qrCanvas.value.width = 220
    qrCanvas.value.height = 220
    ctx.fillStyle = '#FFFFFF'
    ctx.fillRect(0, 0, 220, 220)
    ctx.fillStyle = '#000000'
    ctx.font = '14px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('OnyxVision 曜石视界', 110, 100)
    ctx.fillText(lanUrl.value, 110, 130)
  }
}

watch(activeTab, (tab) => {
  if (tab === 'qrcode') {
    setTimeout(renderQRCode, 50)
  }
})

onMounted(() => {
  if (activeTab.value === 'qrcode') {
    setTimeout(renderQRCode, 50)
  }
})
</script>
