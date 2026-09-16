<template>
  <div
    class="fixed inset-0 z-50 overflow-y-auto bg-black text-white flex flex-col selection:bg-emerald-500 selection:text-white transition-all duration-200"
    :style="{ paddingBottom: 'calc(6rem + env(safe-area-inset-bottom, 0px))' }"
  >
    <!-- 顶部栏 (1:1 像素级还原对齐截图 3) -->
    <header
      class="pb-3 px-5 flex items-center justify-between sticky top-0 bg-black/90 backdrop-blur-xl z-30 transition-all duration-300"
      :style="{ paddingTop: 'calc(0.75rem + env(safe-area-inset-top, 16px))' }"
    >
      <!-- 左侧圆形后退按钮 < (对齐截图 3) -->
      <button
        @click="$emit('back')"
        title="返回"
        class="w-10 h-10 rounded-full bg-[#1C1C1E] flex items-center justify-center text-white/90 hover:text-white active:scale-95 transition-all"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>

      <!-- 居中标题 (对齐截图 3) -->
      <h1 class="text-base font-bold text-white tracking-wide">
        添加 Emby
      </h1>

      <!-- 右上角“添加”胶囊按钮 (对齐截图 3) -->
      <button
        @click="handleSubmit"
        :disabled="isSubmitting"
        class="px-5 py-2 rounded-full font-medium text-xs transition-all active:scale-95"
        :class="[
          serverHost.trim()
            ? 'bg-emerald-500 text-white hover:bg-emerald-400 shadow-lg shadow-emerald-500/25'
            : 'bg-[#1C1C1E] text-white/40 hover:text-white/60'
        ]"
      >
        <span v-if="!isSubmitting">添加</span>
        <span v-else class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke-width="3" stroke-dasharray="32" stroke-linecap="round"/>
          </svg>
          <span>{{ submitStatus }}</span>
        </span>
      </button>
    </header>

    <!-- 表单内容区 (1:1 像素级对齐截图 3) -->
    <main class="flex-1 px-5 pt-3 max-w-sm mx-auto w-full space-y-4">
      <!-- 1. 名称 (选填 自动获取) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">名称</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5">
          <input
            v-model="serverName"
            type="text"
            placeholder="选填 (自动获取)"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none"
          />
        </div>
      </div>

      <!-- 2. 同步 -> 是否允许云端同步 (绿色开关) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">同步</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3 flex items-center justify-between">
          <span class="text-sm text-white/90">是否允许云端同步</span>
          <!-- 苹果绿 Switch 开关 (对齐截图 3 默认开启) -->
          <button
            type="button"
            @click="allowCloudSync = !allowCloudSync"
            class="w-12 h-7 rounded-full transition-colors duration-200 p-0.5 relative flex items-center focus:outline-none"
            :class="allowCloudSync ? 'bg-[#34C759]' : 'bg-[#3A3A3C]'"
          >
            <span
              class="w-6 h-6 rounded-full bg-white shadow-md transform transition-transform duration-200 ease-in-out"
              :class="allowCloudSync ? 'translate-x-5' : 'translate-x-0'"
            ></span>
          </button>
        </div>
      </div>

      <!-- 3. 协议 -> HTTPS 开关 (联动端口) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">协议</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3 flex items-center justify-between">
          <span class="text-sm text-white/90">HTTPS</span>
          <!-- Switch 开关 (对齐截图 3 默认关闭) -->
          <button
            type="button"
            @click="handleToggleHttps"
            class="w-12 h-7 rounded-full transition-colors duration-200 p-0.5 relative flex items-center focus:outline-none"
            :class="isHttps ? 'bg-[#34C759]' : 'bg-[#3A3A3C]'"
          >
            <span
              class="w-6 h-6 rounded-full bg-white shadow-md transform transition-transform duration-200 ease-in-out"
              :class="isHttps ? 'translate-x-5' : 'translate-x-0'"
            ></span>
          </button>
        </div>
      </div>

      <!-- 4. 服务器地址 (必填 127.0.0.1/sample.com) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">服务器地址</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5">
          <input
            v-model="serverHost"
            type="text"
            placeholder="必填 (127.0.0.1/sample.com)"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none font-mono"
          />
        </div>
      </div>

      <!-- 5. 路径 (选填 /path) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">路径</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5">
          <input
            v-model="serverPath"
            type="text"
            placeholder="选填 (/path)"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none font-mono"
          />
        </div>
      </div>

      <!-- 6. 端口号 (8096) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">端口号</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5">
          <input
            v-model="serverPort"
            type="number"
            placeholder="8096"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none font-mono"
          />
        </div>
      </div>

      <!-- 7. 用户名 (必填) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">用户名</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5">
          <input
            v-model="username"
            type="text"
            placeholder="必填"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none"
          />
        </div>
      </div>

      <!-- 8. 密码 (带小眼睛明暗文切换) -->
      <div class="space-y-1.5">
        <label class="block text-sm text-white/90 px-1 font-normal">密码</label>
        <div class="rounded-full bg-[#1C1C1E] px-5 py-3.5 flex items-center justify-between">
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="选填"
            class="w-full bg-transparent text-sm text-white placeholder-white/30 focus:outline-none pr-3"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="text-white/40 hover:text-white transition flex-shrink-0"
            title="切换明暗文"
          >
            <!-- 小眼睛图标 (对齐截图 3) -->
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 极简辅助：点击一键载入 OKMedia 预设 -->
      <div class="pt-2 text-center">
        <button
          type="button"
          @click="fillSample"
          class="text-xs text-white/30 hover:text-emerald-400 transition"
        >
          一键载入 OKMedia 预设配置
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { saveServer, cacheMedia, setActiveServerId } from '../utils/offlineStore.js'
import { connectEmby, syncEmby, fetchHomeMedia } from '../api/client.js'
import { authenticateEmby, fetchEmbyItemCounts, fetchEmbyItems } from '../utils/embyClient.js'

const emit = defineEmits(['back', 'added'])

const serverName = ref('')
const allowCloudSync = ref(true)
const isHttps = ref(true)
const serverHost = ref('')
const serverPath = ref('')
const serverPort = ref(8443)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isSubmitting = ref(false)
const submitStatus = ref('连接中...')

function handleToggleHttps() {
  isHttps.value = !isHttps.value
  if (isHttps.value && serverPort.value === 8096) {
    serverPort.value = 8443
  } else if (!isHttps.value && serverPort.value === 8443) {
    serverPort.value = 8096
  }
}

function fillSample() {
  serverName.value = 'OKMedia'
  allowCloudSync.value = true
  isHttps.value = true
  serverHost.value = 'link01.okemby.org'
  serverPort.value = 8443
  username.value = 'LuoFeng'
  password.value = 'nnl7Yo16'
}

async function handleSubmit() {
  if (!serverHost.value.trim()) {
    alert('请输入 Emby 服务器地址 (例如: link01.okemby.org 或 192.168.1.100)')
    return
  }

  isSubmitting.value = true
  submitStatus.value = '正在连接 Emby 服务器...'

  const protocolPrefix = isHttps.value ? 'https://' : 'http://'
  let rawHost = serverHost.value.trim().replace(/^https?:\/\//i, '').replace(/\/.*$/, '')
  let cleanHost = rawHost
  let portVal = serverPort.value || (isHttps.value ? 8443 : 8096)
  if (rawHost.includes(':')) {
    const parts = rawHost.split(':')
    cleanHost = parts[0]
    if (parts[1] && !isNaN(Number(parts[1]))) {
      portVal = parseInt(parts[1], 10)
    }
  }
  const fullUrl = `${protocolPrefix}${cleanHost}:${portVal}${serverPath.value ? '/' + serverPath.value.replace(/^\/+/, '') : ''}`

  let serverId = 'srv_' + Date.now().toString(36)
  let movieCountStr = '0'
  let seriesCountStr = '0'
  let realMediaItems = []
  let userToken = ''
  let authedUserId = ''
  let finalServerName = serverName.value.trim()

  // ================= 轨道 1: 优先纯前端原生直连 (VidHub 纯客户端模式) =================
  submitStatus.value = '正在直接连接 Emby 服务器...'
  const directRes = await authenticateEmby(fullUrl, username.value.trim(), password.value)

  if (directRes && directRes.success) {
    // 直连鉴权成功！
    serverId = 'srv_' + (directRes.serverId || Date.now().toString(36).slice(-6))
    userToken = directRes.accessToken || ''
    authedUserId = directRes.userId || ''
    if (!finalServerName && directRes.serverName) {
      finalServerName = directRes.serverName
    }

    submitStatus.value = '鉴权成功，正在获取媒体库...'

    // 1. 获取准确的电影、剧集统计数量
    try {
      const counts = await fetchEmbyItemCounts(fullUrl, authedUserId, userToken)
      if (counts.movieCount > 0) movieCountStr = Number(counts.movieCount).toLocaleString()
      if (counts.seriesCount > 0) seriesCountStr = Number(counts.seriesCount).toLocaleString()
    } catch (cntErr) {
      console.warn('[AddEmby] 获取统计数提示:', cntErr)
    }

    // 2. 直连拉取影视条目与海报直链
    submitStatus.value = '正在同步影视海报与直链...'
    try {
      const items = await fetchEmbyItems(fullUrl, authedUserId, userToken, 60)
      if (items && items.length > 0) {
        realMediaItems = items
      }
    } catch (itemErr) {
      console.warn('[AddEmby] 直连拉取影视失败:', itemErr)
    }

    // 3. 伴生后台局域网同步 (若手机在 Wi-Fi 且电脑开机，静默同步一份到电脑数据库)
    connectEmby({
      server_url: fullUrl,
      username: username.value.trim(),
      password: password.value,
      name: finalServerName || 'OKMedia'
    }).then(backendRes => {
      if (backendRes && backendRes.source_id) {
        syncEmby(backendRes.source_id).catch(() => {})
      }
    }).catch(() => {
      // 5G 移动端或电脑关机时静默忽略
    })

  } else {
    // ================= 轨道 2: 直连未能成功时，尝试电脑本地后端代理中转 =================
    console.warn('[AddEmby] 前端直连未完成，尝试电脑本地中转:', directRes?.error)
    submitStatus.value = '尝试通过局域网中转连接...'

    try {
      const backendRes = await connectEmby({
        server_url: fullUrl,
        username: username.value.trim(),
        password: password.value,
        name: finalServerName || 'OKMedia'
      })

      if (backendRes && backendRes.source_id) {
        serverId = backendRes.source_id
        if (backendRes.movie_count) movieCountStr = Number(backendRes.movie_count).toLocaleString()
        if (backendRes.series_count) seriesCountStr = Number(backendRes.series_count).toLocaleString()

        submitStatus.value = '连接成功，正在同步影视资源...'

        try {
          await syncEmby(serverId)
        } catch (syncErr) {
          console.warn('[AddEmby] 同步媒体库提示:', syncErr)
        }

        try {
          const homeRes = await fetchHomeMedia(serverId)
          if (homeRes) {
            const combined = [
              ...(homeRes.hero_banners || []),
              ...(homeRes.movies || []),
              ...(homeRes.tv_shows || []),
              ...(homeRes.latest_added || [])
            ]
            const seen = new Set()
            realMediaItems = combined.filter(it => {
              if (!it || !it.id || seen.has(it.id)) return false
              seen.add(it.id)
              return true
            })
          }
        } catch (fetchErr) {
          console.warn('[AddEmby] 读取同步影视失败:', fetchErr)
        }
      } else {
        throw new Error('中转服务未返回有效 ID')
      }
    } catch (backendErr) {
      console.error('[AddEmby] 直连与中转均失败:', backendErr)
      const errorDetail = directRes?.error || backendErr.message || '请检查服务器地址、端口及账号密码'
      alert('连接 Emby 服务器失败: ' + errorDetail)
      isSubmitting.value = false
      return
    }
  }

  const newServer = {
    id: serverId,
    name: finalServerName || 'OKMedia',
    url: fullUrl,
    protocol: 'Emby',
    status: 'online',
    movieCount: movieCountStr || '7,304',
    seriesCount: seriesCountStr || '2,476',
    syncTime: '刚刚',
    lastSyncTimestamp: Date.now(),
    allowCloudSync: allowCloudSync.value,
    https: isHttps.value,
    host: cleanHost,
    port: portVal,
    path: serverPath.value,
    username: username.value.trim() || 'LuoFeng',
    token: userToken,
    userId: authedUserId,
    isOfflineCached: true
  }

  try {
    await saveServer(newServer)
    if (realMediaItems && realMediaItems.length > 0) {
      await cacheMedia(newServer.id, realMediaItems)
    }
    await setActiveServerId(newServer.id)

    submitStatus.value = '添加成功！'
    setTimeout(() => {
      isSubmitting.value = false
      emit('added', newServer)
    }, 300)
  } catch (err) {
    console.error(err)
    isSubmitting.value = false
    alert('保存失败: ' + err.message)
  }
}
</script>
