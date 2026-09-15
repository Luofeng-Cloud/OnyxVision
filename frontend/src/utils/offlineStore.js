// OnyxVision (曜石视界) 手机端全量离线持久化引擎
// 核心机制：原生 IndexedDB + LocalStorage 双轨高速缓存 + 0毫秒冷启动渲染 + 服务器离线容灾

const DB_NAME = 'OnyxVisionOfflineDB'
const DB_VERSION = 1

export const DEFAULT_OFFLINE_SERVER = null
export const DEFAULT_OKMEDIA_ITEMS = []
export const DEFAULT_PLAYBACK_HISTORY = []
export const DEFAULT_FAVORITES = []

// ==================== 1. IndexedDB 核心驱动 ====================

let dbPromise = null

function openDatabase() {
  if (dbPromise) return dbPromise

  dbPromise = new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !window.indexedDB) {
      console.warn('[OnyxVision Offline] IndexedDB 不受当前环境支持，自动降级为 LocalStorage 模式')
      resolve(null)
      return
    }

    const request = window.indexedDB.open(DB_NAME, DB_VERSION)

    request.onupgradeneeded = (event) => {
      const db = event.target.result
      if (!db.objectStoreNames.contains('servers')) {
        db.createObjectStore('servers', { keyPath: 'id' })
      }
      if (!db.objectStoreNames.contains('mediaLibraries')) {
        db.createObjectStore('mediaLibraries', { keyPath: 'serverId' })
      }
      if (!db.objectStoreNames.contains('metadata')) {
        db.createObjectStore('metadata', { keyPath: 'key' })
      }
      if (!db.objectStoreNames.contains('playbackHistory')) {
        db.createObjectStore('playbackHistory', { keyPath: 'id' })
      }
    }

    request.onsuccess = (event) => {
      resolve(event.target.result)
    }

    request.onerror = (event) => {
      console.error('[OnyxVision Offline] IndexedDB 打开失败:', event.target.error)
      resolve(null) // 降级 LocalStorage
    }
  })

  return dbPromise
}

async function idbGet(storeName, key) {
  const db = await openDatabase()
  if (!db) return null
  return new Promise((resolve) => {
    try {
      const tx = db.transaction(storeName, 'readonly')
      const store = tx.objectStore(storeName)
      const req = store.get(key)
      req.onsuccess = () => resolve(req.result || null)
      req.onerror = () => resolve(null)
    } catch (e) {
      console.error(e)
      resolve(null)
    }
  })
}

async function idbGetAll(storeName) {
  const db = await openDatabase()
  if (!db) return []
  return new Promise((resolve) => {
    try {
      const tx = db.transaction(storeName, 'readonly')
      const store = tx.objectStore(storeName)
      const req = store.getAll()
      req.onsuccess = () => resolve(req.result || [])
      req.onerror = () => resolve([])
    } catch (e) {
      console.error(e)
      resolve([])
    }
  })
}

async function idbPut(storeName, item) {
  const db = await openDatabase()
  if (!db) return
  return new Promise((resolve, reject) => {
    try {
      const tx = db.transaction(storeName, 'readwrite')
      const store = tx.objectStore(storeName)
      const req = store.put(item)
      req.onsuccess = () => resolve(true)
      req.onerror = () => reject(req.error)
    } catch (e) {
      reject(e)
    }
  })
}

async function idbDelete(storeName, key) {
  const db = await openDatabase()
  if (!db) return
  return new Promise((resolve, reject) => {
    try {
      const tx = db.transaction(storeName, 'readwrite')
      const store = tx.objectStore(storeName)
      const req = store.delete(key)
      req.onsuccess = () => resolve(true)
      req.onerror = () => reject(req.error)
    } catch (e) {
      reject(e)
    }
  })
}

// ==================== 2. LocalStorage 兜底辅助方法 ====================

function lsGet(key, fallback = null) {
  try {
    const raw = localStorage.getItem(`onyx_${key}`)
    return raw ? JSON.parse(raw) : fallback
  } catch (e) {
    return fallback
  }
}

function lsSet(key, value) {
  try {
    localStorage.setItem(`onyx_${key}`, JSON.stringify(value))
  } catch (e) {
    console.warn('[OnyxVision LocalStorage] 写入受阻:', e)
  }
}

// ==================== 3. 0毫秒冷启动同步读取 (保证秒进无白屏) ====================

export function getInitialServers() {
  const cached = lsGet('servers')
  if (Array.isArray(cached) && cached.length > 0) {
    // 过滤清除遗留的 mock 演示源
    const real = cached.filter(s => s.id !== 'srv_okmedia' && s.id !== 'source_demo_local')
    return real
  }
  return []
}

export function getInitialActiveServerId() {
  const activeId = lsGet('activeServerId')
  if (activeId === 'srv_okmedia' || activeId === 'source_demo_local') return null
  return activeId || null
}

export function getInitialMedia(serverId) {
  if (!serverId || serverId === 'srv_okmedia' || serverId === 'source_demo_local') return []
  const allLibs = lsGet('mediaLibraries', {})
  if (allLibs && allLibs[serverId] && allLibs[serverId].length > 0) {
    return allLibs[serverId]
  }
  return []
}

// ==================== 4. 异步全量持久化 API (IndexedDB + LocalStorage) ====================

/**
 * 初始化离线数据库并在启动时自动清理旧版 mock 假数据，保持纯净框架
 */
export async function initOfflineStore() {
  try {
    // 自动清理过去写入的 mock 假数据，确保用户在未添加 Emby 前呈现纯净空态
    const existingServers = await idbGetAll('servers')
    if (existingServers && existingServers.length > 0) {
      for (const s of existingServers) {
        if (s.id === 'srv_okmedia' || s.id === 'source_demo_local') {
          await idbDelete('servers', s.id)
          await idbDelete('mediaLibraries', s.id)
        }
      }
    }

    const lsServers = lsGet('servers', [])
    if (Array.isArray(lsServers)) {
      const cleanServers = lsServers.filter(s => s.id !== 'srv_okmedia' && s.id !== 'source_demo_local')
      lsSet('servers', cleanServers)
      if (lsGet('activeServerId') === 'srv_okmedia' || lsGet('activeServerId') === 'source_demo_local') {
        lsSet('activeServerId', cleanServers[0]?.id || null)
      }
    }

    const allLibs = lsGet('mediaLibraries', {})
    if (allLibs['srv_okmedia'] || allLibs['source_demo_local']) {
      delete allLibs['srv_okmedia']
      delete allLibs['source_demo_local']
      lsSet('mediaLibraries', allLibs)
    }

    // 清理假历史记录
    const existingHistory = await idbGetAll('playbackHistory')
    if (existingHistory && existingHistory.length > 0) {
      for (const h of existingHistory) {
        if (h.serverId === 'srv_okmedia' || String(h.id).startsWith('history_')) {
          await idbDelete('playbackHistory', h.id)
        }
      }
    }
  } catch (err) {
    console.error('[OnyxVision Offline] 初始化离线库异常:', err)
  }
}

/**
 * 获取所有持久化保存的服务器
 */
export async function getServers() {
  try {
    const fromIdb = await idbGetAll('servers')
    if (fromIdb && fromIdb.length > 0) {
      lsSet('servers', fromIdb)
      return fromIdb
    }
  } catch (e) {
    console.warn('[OnyxVision Offline] 从 IndexedDB 读取服务器失败，回退 LocalStorage')
  }
  return getInitialServers()
}

/**
 * 保存或更新一个服务器
 */
export async function saveServer(server) {
  if (!server.id) {
    server.id = 'srv_' + Date.now().toString(36)
  }
  if (!server.status) server.status = 'online'
  if (!server.syncTime) server.syncTime = '刚刚'
  if (!server.lastSyncTimestamp) server.lastSyncTimestamp = Date.now()
  server.isCached = true

  // 1. 写入 IndexedDB
  try {
    await idbPut('servers', server)
  } catch (e) {
    console.warn('[OnyxVision Offline] idbPut servers 失败:', e)
  }

  // 2. 同步写入 LocalStorage (按 id 或相同 url 查重合并)
  const list = getInitialServers()
  const idx = list.findIndex(s => s.id === server.id || (server.url && s.url === server.url))
  if (idx >= 0) {
    server.id = list[idx].id
    list[idx] = { ...list[idx], ...server }
  } else {
    list.push(server)
  }
  lsSet('servers', list)

  return server
}

/**
 * 删除服务器
 */
export async function removeServer(serverId) {
  try {
    await idbDelete('servers', serverId)
    await idbDelete('mediaLibraries', serverId)
  } catch (e) {
    console.warn('[OnyxVision Offline] idbDelete 失败:', e)
  }

  const list = getInitialServers().filter(s => s.id !== serverId)
  lsSet('servers', list)

  const allLibs = lsGet('mediaLibraries', {})
  delete allLibs[serverId]
  lsSet('mediaLibraries', allLibs)

  // 若删除的是当前活跃服务器，自动重置活跃服务器 ID，防止状态漂移
  if (lsGet('activeServerId') === serverId) {
    const nextActiveId = list[0]?.id || null
    lsSet('activeServerId', nextActiveId)
    try {
      await idbPut('metadata', { key: 'activeServerId', value: nextActiveId })
    } catch (e) {}
  }

  return list
}

/**
 * 获取当前活跃服务器 ID
 */
export async function getActiveServerId() {
  try {
    const meta = await idbGet('metadata', 'activeServerId')
    if (meta && meta.value) return meta.value
  } catch (e) {}
  return getInitialActiveServerId()
}

/**
 * 设置当前活跃服务器 ID
 */
export async function setActiveServerId(serverId) {
  lsSet('activeServerId', serverId)
  try {
    await idbPut('metadata', { key: 'activeServerId', value: serverId })
  } catch (e) {}
}

/**
 * 获取指定服务器本地缓存的全量媒体库 (0ms容灾)
 */
export async function getCachedMedia(serverId) {
  try {
    const record = await idbGet('mediaLibraries', serverId)
    if (record && record.items && record.items.length > 0) {
      // 保持 LocalStorage 镜像
      const allLibs = lsGet('mediaLibraries', {})
      allLibs[serverId] = record.items
      lsSet('mediaLibraries', allLibs)
      return record.items
    }
  } catch (e) {}
  return getInitialMedia(serverId)
}

/**
 * 缓存或更新指定服务器的影视数据 (完整持久化)
 */
export async function cacheMedia(serverId, mediaList) {
  if (!Array.isArray(mediaList)) return
  try {
    await idbPut('mediaLibraries', {
      serverId,
      items: mediaList,
      updatedAt: Date.now()
    })
  } catch (e) {
    console.warn('[OnyxVision Offline] 媒体写入 IndexedDB 失败:', e)
  }

  const allLibs = lsGet('mediaLibraries', {})
  allLibs[serverId] = mediaList
  lsSet('mediaLibraries', allLibs)
}

/**
 * 播放历史与收藏记录管理 (原生 IndexedDB + LocalStorage 双轨高速持久化)
 */
export function getInitialHistory() {
  const cached = lsGet('playbackHistory')
  if (Array.isArray(cached) && cached.length > 0) {
    return cached.filter(h => h.serverId !== 'srv_okmedia' && !String(h.id).startsWith('history_'))
  }
  return []
}

export async function getPlaybackHistory(serverId) {
  try {
    const history = await idbGetAll('playbackHistory')
    if (history && history.length > 0) {
      const real = history.filter(h => h.serverId !== 'srv_okmedia' && !String(h.id).startsWith('history_'))
      real.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0))
      lsSet('playbackHistory', real)
      if (serverId) {
        return real.filter(h => !h.serverId || h.serverId === serverId)
      }
      return real
    }
  } catch (e) {
    console.warn('[OnyxVision Offline] 读取历史失败:', e)
  }
  const fallback = getInitialHistory()
  if (serverId) {
    return fallback.filter(h => !h.serverId || h.serverId === serverId)
  }
  return fallback
}

export async function savePlaybackHistory(mediaItem, progress, progressTime, currentTime, duration) {
  if (!mediaItem || !mediaItem.title) return
  const id = mediaItem.historyId || mediaItem.id || `hist_${Date.now()}`
  const record = {
    id,
    mediaId: mediaItem.mediaId || mediaItem.id,
    title: mediaItem.title,
    subtitle: mediaItem.subtitle || (mediaItem.currentEpisode ? `第 ${mediaItem.currentEpisode.episodeNumber} 集 · ${mediaItem.currentEpisode.title}` : (mediaItem.year ? String(mediaItem.year) : '已观看')),
    originalTitle: mediaItem.originalTitle || '',
    poster: mediaItem.poster || mediaItem.backdrop || '',
    backdrop: mediaItem.backdrop || mediaItem.poster || '',
    progress: typeof progress === 'number' ? progress : 0.05,
    progressTime: progressTime || '00:00 / 00:00',
    currentTime: typeof currentTime === 'number' ? currentTime : 0,
    duration: typeof duration === 'number' ? duration : 0,
    initialSeekTime: typeof currentTime === 'number' ? currentTime : 0,
    serverId: mediaItem.serverId || '',
    videoUrl: mediaItem.videoUrl || '',
    badges: mediaItem.badges || ['4K UHD'],
    updatedAt: Date.now()
  }

  try {
    await idbPut('playbackHistory', record)
  } catch (e) {
    console.warn('[OnyxVision Offline] 历史写入 IndexedDB 失败:', e)
  }

  const history = getInitialHistory()
  const idx = history.findIndex(h => h.id === record.id || (h.mediaId && h.mediaId === record.mediaId) || (h.title === record.title))
  if (idx >= 0) {
    history[idx] = { ...history[idx], ...record }
  } else {
    history.unshift(record)
  }
  history.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0))
  lsSet('playbackHistory', history.slice(0, 50))
  return record
}

export async function deletePlaybackHistory(id) {
  try {
    await idbDelete('playbackHistory', id)
  } catch (e) {}
  const list = getInitialHistory().filter(h => h.id !== id)
  lsSet('playbackHistory', list)
  return list
}

export async function clearPlaybackHistory() {
  try {
    const all = await idbGetAll('playbackHistory')
    for (const item of all) {
      await idbDelete('playbackHistory', item.id)
    }
  } catch (e) {}
  lsSet('playbackHistory', [])
  return []
}

export function getInitialFavorites() {
  const cached = lsGet('favorites')
  if (Array.isArray(cached) && cached.length > 0) {
    return cached.filter(f => f.serverId !== 'srv_okmedia' && !String(f.id).startsWith('fav_'))
  }
  return []
}

export async function getFavorites() {
  return getInitialFavorites()
}

/**
 * 模拟服务器宕机/离线模式开关 (用于演示即使服务器挂了，手机端依旧秒进且海报墙立即可用)
 */
export function getSimulatedOffline() {
  return lsGet('simulatedOffline', false)
}

export function setSimulatedOffline(val) {
  lsSet('simulatedOffline', !!val)
}
