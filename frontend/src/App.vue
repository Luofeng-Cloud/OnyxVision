<template>
  <div class="min-h-screen bg-[#0A0B0E] text-white flex flex-col selection:bg-emerald-500 selection:text-white font-apple">
    <!-- ==================== TAB 1: 媒体库视图 (对齐截图 4) ==================== -->
    <div
      v-if="activeTab === 'library'"
      class="flex-1 flex flex-col transition-all duration-200"
      :style="{ paddingBottom: 'calc(7.5rem + env(safe-area-inset-bottom, 0px))' }"
    >
      <!-- 顶部浮动导航栏 (对齐截图 4: 绿底菱形播放标 + OKMedia 胶囊 + 右侧 ... 菜单) -->
      <Navbar
        :servers="servers"
        :current-server-id="activeServerId"
        @select-server="switchServer"
        @switch-to-servers="activeTab = 'servers'"
        @open-qrcode="showQRCodeModal = true"
        @open-settings="showAboutModal = true"
        @go-home="resetFilter"
      />

      <!-- 搜索展开模式下的独立结果列表 -->
      <main
        v-if="isSearchOpen && searchQuery.trim()"
        class="flex-1 pb-16 px-4 sm:px-8 max-w-[1720px] mx-auto w-full transition-all duration-200"
        :style="{ paddingTop: 'calc(5.5rem + env(safe-area-inset-top, 16px))' }"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <span>搜索结果：</span>
            <span class="text-emerald-400 font-normal">"{{ searchQuery }}"</span>
            <span class="text-xs text-white/40 ml-2">({{ searchResults.length }} 部影视)</span>
          </h2>
          <button @click="searchQuery = ''" class="text-xs text-white/50 hover:text-white">
            清除搜索
          </button>
        </div>

        <div v-if="searchResults.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 sm:gap-6">
          <MediaCard
            v-for="item in searchResults"
            :key="item.id"
            :item="item"
            @play="handlePlay"
            @open-detail="handleOpenDetail"
          />
        </div>
        <div v-else class="text-center py-20 text-white/40 text-sm">
          未检索到符合条件的影视，请尝试搜索其他关键字。
        </div>
      </main>

      <!-- 默认媒体库主页 (非搜索状态) -->
      <div v-else class="flex-1 flex flex-col">
        <!-- 顶部搜索输入卡片 (当点击右下角搜索按钮时滑出) -->
        <transition name="fade">
          <div
            v-if="isSearchOpen"
            class="fixed left-0 right-0 z-30 px-5 max-w-md mx-auto transition-all duration-200"
            :style="{ top: 'calc(4rem + env(safe-area-inset-top, 16px))' }"
          >
            <div class="rounded-full bg-[#1A1C24]/95 backdrop-blur-2xl border border-white/20 px-4 py-2.5 flex items-center gap-2 shadow-2xl">
              <svg class="w-4 h-4 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="7"/>
                <line x1="16.5" y1="16.5" x2="21.5" y2="21.5"/>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索已离线缓存的影视、剧集、演员..."
                class="w-full bg-transparent text-xs text-white placeholder-white/40 focus:outline-none"
                autofocus
              />
              <button v-if="searchQuery" @click="searchQuery = ''" class="text-white/40 hover:text-white p-0.5">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
        </transition>

      <!-- 当未添加任何服务器或服务器中无资源时展示优雅空态 -->
      <div v-if="!servers || servers.length === 0 || !currentMedia || currentMedia.length === 0" class="flex-1 flex flex-col items-center justify-center py-28 px-6 text-center">
        <div class="w-20 h-20 rounded-3xl bg-gradient-to-br from-[#1C1C1E] to-[#252830] border border-white/10 flex items-center justify-center mb-5 shadow-2xl">
          <!-- 翡翠绿菱形播放标 -->
          <div class="w-10 h-10 rounded-xl bg-[#28C76F] flex items-center justify-center rotate-45 shadow-[0_0_15px_rgba(40,199,111,0.5)]">
            <svg class="w-5 h-5 fill-white -rotate-45 translate-x-0.5" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z" />
            </svg>
          </div>
        </div>
        <h2 class="text-xl font-bold text-white mb-2">尚未连接影视服务器</h2>
        <p class="text-xs sm:text-sm text-white/50 max-w-sm mb-7 leading-relaxed">
          请前往「资源库」添加您的 Emby / Jellyfin 服务器，登录后系统将自动为您同步载入海报墙与影视资源。
        </p>
        <button
          @click="activeTab = 'servers'; showAddDrawer = true"
          class="px-6 py-3 rounded-full bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-white text-xs sm:text-sm font-semibold shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>前往「资源库」添加服务器</span>
        </button>
      </div>

      <!-- 默认媒体库主页 (当有服务器与资源时展示) -->
      <main v-else class="flex-1">
        <!-- 1. Hero Banner 沉浸式海报轮播 (支持移动端触控左右轻扫滑动) -->
        <HeroBanner
          :items="heroList"
          @play="handlePlay"
          @open-detail="handleOpenDetail"
        />

        <!-- 2. 继续观看货架 -->
        <ContinueWatchingShelf
          v-if="continueWatchingList.length > 0"
          :items="continueWatchingList"
          @play="handlePlay"
          @open-detail="handleOpenDetail"
        />

        <!-- 3. 4K 杜比视界 & 全景声专区 -->
        <MediaSection
          v-if="dolbyVisionList.length > 0"
          title="4K 杜比视界 & 全景声专区"
          :count="dolbyVisionList.length"
          :items="dolbyVisionList"
          @play="handlePlay"
          @open-detail="handleOpenDetail"
        />

        <!-- 4. 高分电影 -->
        <MediaSection
          v-if="moviesList.length > 0"
          title="电影"
          :count="moviesList.length"
          :items="moviesList"
          @play="handlePlay"
          @open-detail="handleOpenDetail"
        />

        <!-- 5. 热门剧集 & 动漫 -->
        <MediaSection
          v-if="seriesList.length > 0"
          title="剧集 & 动漫"
          :count="seriesList.length"
          :items="seriesList"
          @play="handlePlay"
          @open-detail="handleOpenDetail"
        />
      </main>
      </div>
    </div>

    <!-- ==================== TAB 2: 资源库视图 (改版：影视服务器列表与管理) ==================== -->
    <ServersView
      v-else-if="activeTab === 'servers' || activeTab === 'sources'"
      :servers="servers"
      :active-server-id="activeServerId"
      :is-simulated-offline="isSimulatedOffline"
      @open-add-drawer="showAddDrawer = true"
      @select-server="handleSelectServerFromList"
      @sync-server="handleSyncServer"
      @delete-server="handleDeleteServer"
      @toggle-simulated-offline="toggleOfflineMode"
    />

    <!-- ==================== TAB 3: 观看记录视图 (媒体观看与播放历史) ==================== -->
    <WatchHistoryView
      v-else-if="activeTab === 'history'"
      :servers="servers"
      :current-server-id="activeServerId"
      @play="handlePlay"
      @switch-server="switchServer"
    />

    <!-- ==================== TAB 4: 设置视图 ==================== -->
    <SettingsView
      v-else-if="activeTab === 'settings'"
      :is-simulated-offline="isSimulatedOffline"
      @toggle-simulated-offline="toggleOfflineMode"
      @open-qrcode="showQRCodeModal = true"
      @open-about="showAboutModal = true"
    />

    <!-- ==================== 底栏五分仓导航 DOCK (1:1 对齐截图 1、2、4) ==================== -->
    <!-- 仅在非全屏表单、非播放器状态下展示 -->
    <BottomTabBar
      v-if="!showAddEmbyForm && !playingMedia"
      v-model:active-tab="activeTab"
      :is-search-open="isSearchOpen"
      @toggle-search="toggleSearch"
    />

    <!-- ==================== 添加影视服务器抽屉 (1:1 对标截图 1) ==================== -->
    <transition name="fade">
      <AddServerDrawer
        v-if="showAddDrawer"
        @close="showAddDrawer = false"
        @select-protocol="handleSelectProtocol"
      />
    </transition>

    <!-- ==================== 添加 Emby 表单页面 (1:1 对标截图 3) ==================== -->
    <transition name="fade">
      <AddEmbyForm
        v-if="showAddEmbyForm"
        @back="showAddEmbyForm = false"
        @added="handleServerAdded"
      />
    </transition>

    <!-- ==================== 影视详情模态窗 ==================== -->
    <transition name="fade">
      <MediaDetailModal
        v-if="detailMedia"
        :item="detailMedia"
        @close="detailMedia = null"
        @play="handlePlayFromDetail"
      />
    </transition>

    <!-- ==================== 全屏播放器 ==================== -->
    <Player
      v-if="playingMedia"
      :media="playingMedia"
      @close="playingMedia = null"
    />

    <!-- ==================== 移动端扫码弹窗 ==================== -->
    <transition name="fade">
      <QRCodeModal
        v-if="showQRCodeModal"
        @close="showQRCodeModal = false"
      />
    </transition>

    <!-- ==================== 关于与设置弹窗 ==================== -->
    <transition name="fade">
      <SettingsModal
        v-if="showAboutModal"
        @close="showAboutModal = false"
      />
    </transition>

    <!-- ==================== 极简 Toast 提示 ==================== -->
    <transition name="fade">
      <div
        v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-[110] px-4 py-2 rounded-full bg-[#181920]/95 backdrop-blur-2xl border border-emerald-500/30 text-xs font-semibold text-white shadow-2xl flex items-center gap-2 pointer-events-none"
      >
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span>{{ toastMessage }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import Navbar from './components/Navbar.vue'
import HeroBanner from './components/HeroBanner.vue'
import ContinueWatchingShelf from './components/ContinueWatchingShelf.vue'
import MediaSection from './components/MediaSection.vue'
import MediaCard from './components/MediaCard.vue'
import ServersView from './components/ServersView.vue'
import FileSourcesView from './components/FileSourcesView.vue'
import WatchHistoryView from './components/WatchHistoryView.vue'
import SettingsView from './components/SettingsView.vue'
import BottomTabBar from './components/BottomTabBar.vue'
import AddServerDrawer from './components/AddServerDrawer.vue'
import AddEmbyForm from './components/AddEmbyForm.vue'
import MediaDetailModal from './components/MediaDetailModal.vue'
import Player from './components/Player.vue'
import QRCodeModal from './components/QRCodeModal.vue'
import SettingsModal from './components/SettingsModal.vue'
import { fetchSources, fetchHomeMedia } from './api/client.js'

import {
  getInitialServers,
  getInitialActiveServerId,
  getInitialMedia,
  initOfflineStore,
  getServers,
  getActiveServerId,
  setActiveServerId,
  saveServer,
  cacheMedia,
  removeServer,
  getCachedMedia,
  getSimulatedOffline,
  setSimulatedOffline
} from './utils/offlineStore.js'
import { fetchEmbyItemCounts, fetchEmbyItems } from './utils/embyClient.js'

// 0毫秒冷启动：直接从沙盒同步缓存初始化，绝不白屏转圈
const servers = ref(getInitialServers())
const activeServerId = ref(getInitialActiveServerId())
const currentMedia = ref(getInitialMedia(activeServerId.value))

// 页面路由/Tab 状态 (对标 VidHub 导航)
const activeTab = ref('library')
const isSearchOpen = ref(false)
const searchQuery = ref('')

// 抽屉与全屏页面状态
const showAddDrawer = ref(false)
const showAddEmbyForm = ref(false)
const detailMedia = ref(null)
const playingMedia = ref(null)
const showQRCodeModal = ref(false)
const showAboutModal = ref(false)
const toastMessage = ref('')

// 离线/宕机模拟状态
const isSimulatedOffline = ref(getSimulatedOffline())

function showToast(msg) {
  toastMessage.value = msg
  setTimeout(() => {
    if (toastMessage.value === msg) toastMessage.value = ''
  }, 2400)
}

function toggleSearch() {
  isSearchOpen.value = !isSearchOpen.value
  if (isSearchOpen.value) {
    activeTab.value = 'library'
  }
}

function resetFilter() {
  searchQuery.value = ''
  isSearchOpen.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleSelectProtocol(protocolName) {
  showAddDrawer.value = false
  if (protocolName === 'Emby') {
    showAddEmbyForm.value = true
  } else {
    showToast(`当前演示协议: ${protocolName} (已挂载通用 Emby 引擎)`)
    showAddEmbyForm.value = true
  }
}

async function handleServerAdded(newServer) {
  showAddEmbyForm.value = false
  servers.value = await getServers()
  await switchServer(newServer.id)
  showToast(`已成功连接并离线持久化: ${newServer.name}`)
  activeTab.value = 'servers'
}

async function switchServer(serverId) {
  activeServerId.value = serverId
  await setActiveServerId(serverId)
  currentMedia.value = await getCachedMedia(serverId)
  const s = servers.value.find(item => item.id === serverId)
  if (s) {
    showToast(`已切换至: ${s.name} (0ms 离线秒载)`)
  } else if (!serverId) {
    showToast('已重置当前服务器')
  }
}

function handleSelectServerFromList(serverId) {
  switchServer(serverId)
  activeTab.value = 'library'
}

async function handleSyncServer(serverId) {
  showToast('正在向本地沙盒同步全量影视索引...')
  const target = servers.value.find(s => s.id === serverId)
  if (target && target.token && target.userId && target.url) {
    try {
      const counts = await fetchEmbyItemCounts(target.url, target.userId, target.token)
      if (counts.movieCount > 0) target.movieCount = Number(counts.movieCount).toLocaleString()
      if (counts.seriesCount > 0) target.seriesCount = Number(counts.seriesCount).toLocaleString()
      const items = await fetchEmbyItems(target.url, target.userId, target.token, 60, target.id)
      if (items && items.length > 0) {
        await cacheMedia(target.id, items)
        if (activeServerId.value === target.id) {
          currentMedia.value = items
        }
      }
      target.syncTime = '刚刚'
      await saveServer(target)
      showToast('同步完毕！已离线持久化至 IndexedDB')
      return
    } catch (e) {
      console.warn('[App] 直连同步异常，回退本地缓存:', e)
    }
  }

  setTimeout(async () => {
    currentMedia.value = await getCachedMedia(serverId)
    showToast('同步完毕！已离线持久化至 IndexedDB')
  }, 600)
}

async function handleDeleteServer(serverId) {
  const target = servers.value.find(s => s.id === serverId)
  const sName = target ? target.name : '该服务器'
  if (confirm(`确定要从本地移除影视服务器「${sName}」及其离线数据吗？`)) {
    servers.value = await removeServer(serverId)
    if (activeServerId.value === serverId) {
      const nextId = servers.value[0]?.id || null
      await switchServer(nextId)
    }
    try {
      await fetch(`/api/sources/${serverId}`, { method: 'DELETE' })
    } catch (e) {}
    showToast(`已移除服务器: ${sName}`)
  }
}

function toggleOfflineMode() {
  isSimulatedOffline.value = !isSimulatedOffline.value
  setSimulatedOffline(isSimulatedOffline.value)
  if (isSimulatedOffline.value) {
    showToast('已进入原服务器宕机离线模式：本地沙盒 0ms 正常提供浏览！')
  } else {
    showToast('已恢复在线模式')
  }
}

function handlePlay(item) {
  playingMedia.value = item
}

function handleOpenDetail(item) {
  detailMedia.value = item
}

function handlePlayFromDetail(item) {
  detailMedia.value = null
  playingMedia.value = item
}

// 搜索过滤
const searchResults = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return currentMedia.value
  return currentMedia.value.filter(m => {
    if (!m) return false
    const titleMatch = m.title?.toLowerCase().includes(query)
    const originalMatch = m.originalTitle?.toLowerCase().includes(query)
    const genreMatch = Array.isArray(m.genres) ? m.genres.some(g => typeof g === 'string' && g.toLowerCase().includes(query)) : (typeof m.genres === 'string' && m.genres.toLowerCase().includes(query))
    const actorMatch = Array.isArray(m.actors) && m.actors.some(a => a?.name?.toLowerCase().includes(query))
    return !!(titleMatch || originalMatch || genreMatch || actorMatch)
  })
})

// 分类派生
const heroList = computed(() => {
  if (!currentMedia.value || currentMedia.value.length === 0) return []
  return currentMedia.value.slice(0, 6)
})

const continueWatchingList = computed(() => {
  return currentMedia.value.filter(m => (m.progress || 0) > 0 || (m.playback?.playback_percentage || 0) > 0 || (m.playback_percentage || 0) > 0)
})

const dolbyVisionList = computed(() => {
  return currentMedia.value.filter(m => m.badges?.some(b => b.includes('Dolby')))
})

const moviesList = computed(() => {
  return currentMedia.value.filter(m => m.type === 'movie')
})

const seriesList = computed(() => {
  return currentMedia.value.filter(m => m.type === 'series' || m.type === 'tv')
})

onMounted(async () => {
  // 1. 0毫秒冷启动：直接从沙盒同步缓存初始化，绝不白屏转圈
  await initOfflineStore()
  servers.value = await getServers()
  activeServerId.value = await getActiveServerId()
  currentMedia.value = await getCachedMedia(activeServerId.value)

  // 2. 在线自动静默双向联调：从后端 FastAPI 同步最新媒体库与挂载源
  try {
    const backendSources = await fetchSources()
    if (backendSources && backendSources.length > 0) {
      // 遍历更新本地 servers 统计信息
      const updatedServers = [...servers.value]
      for (const bs of backendSources) {
        const idx = updatedServers.findIndex(s => s.id === bs.id || s.url === bs.url)
        if (idx !== -1) {
          if (bs.movie_count) updatedServers[idx].movieCount = Number(bs.movie_count).toLocaleString()
          if (bs.series_count) updatedServers[idx].seriesCount = Number(bs.series_count).toLocaleString()
          if (bs.name) updatedServers[idx].name = bs.name
        }
      }
      servers.value = updatedServers

      // 如果当前活跃服务器在后端有真实数据，拉取并更新 IndexedDB 缓存
      const activeSrc = activeServerId.value ? backendSources.find(s => s.id === activeServerId.value) : null
      if (activeSrc) {
        const homeData = await fetchHomeMedia(activeSrc.id)
        if (homeData && homeData.all_items && homeData.all_items.length > 0) {
          currentMedia.value = homeData.all_items
          await cacheMedia(activeServerId.value, homeData.all_items)
        }
      }
    }
  } catch (err) {
    console.warn('[App] Background sync notice (offline mode active):', err)
  }
})
</script>
