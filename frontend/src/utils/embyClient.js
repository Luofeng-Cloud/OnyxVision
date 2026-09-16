// OnyxVision Frontend Direct Emby Client
// 纯前端直连 Emby / Jellyfin 官方 REST API 驱动
// 实现客户端原生直连、鉴权、媒体库拉取与原画直链构造 (VidHub 同款客户端机制)

const CLIENT_NAME = 'OnyxVision'
const DEVICE_NAME = 'OnyxVision-Mobile'
const DEVICE_ID = 'onyxvision-mobile-client'
const VERSION = '1.0.0'

/**
 * 构造 Emby 标准鉴权 Headers
 */
export function getEmbyAuthHeaders(token = '') {
  const parts = [
    `Client="${CLIENT_NAME}"`,
    `Device="${DEVICE_NAME}"`,
    `DeviceId="${DEVICE_ID}"`,
    `Version="${VERSION}"`
  ]
  if (token) {
    parts.push(`Token="${token}"`)
  }

  const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Emby-Authorization': `MediaBrowser ${parts.join(', ')}`
  }

  if (token) {
    headers['X-Emby-Token'] = token
  }

  return headers
}

/**
 * 探测 Emby / Jellyfin 公共系统信息
 */
export async function testEmbyConnection(serverUrl, timeoutMs = 8000) {
  const cleanUrl = serverUrl.replace(/\/+$/, '')
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const res = await fetch(`${cleanUrl}/System/Info/Public`, {
      method: 'GET',
      headers: getEmbyAuthHeaders(),
      signal: controller.signal
    })
    clearTimeout(timer)

    if (res.ok) {
      const data = await res.json()
      return {
        success: true,
        serverName: data.ServerName || 'Emby Server',
        version: data.Version || '',
        id: data.Id || '',
        raw: data
      }
    }
    return { success: false, error: `HTTP ${res.status}` }
  } catch (err) {
    clearTimeout(timer)
    return { success: false, error: err.name === 'AbortError' ? '连接超时' : (err.message || '网络连接失败') }
  }
}

/**
 * 用户名密码直接向 Emby 服务器鉴权
 */
export async function authenticateEmby(serverUrl, username, password, timeoutMs = 12000) {
  const cleanUrl = serverUrl.replace(/\/+$/, '')
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  const payload = {
    Username: username,
    Pw: password || ''
  }

  try {
    const res = await fetch(`${cleanUrl}/Users/AuthenticateByName`, {
      method: 'POST',
      headers: getEmbyAuthHeaders(),
      body: JSON.stringify(payload),
      signal: controller.signal
    })
    clearTimeout(timer)

    if (!res.ok) {
      let errorDetail = `HTTP ${res.status}`
      try {
        const errJson = await res.json()
        errorDetail = errJson.message || errJson.detail || errorDetail
      } catch {
        const text = await res.text().catch(() => '')
        if (text) errorDetail = text.substring(0, 100)
      }

      if (res.status === 401 || res.status === 400) {
        return { success: false, error: '用户名或密码错误，请核对后重试' }
      }
      return { success: false, error: `服务器鉴权失败 (${errorDetail})` }
    }

    const data = await res.json()
    const accessToken = data.AccessToken || ''
    const user = data.User || {}
    const userId = user.Id || ''
    const serverId = data.ServerId || ''

    return {
      success: true,
      accessToken,
      userId,
      userName: user.Name || username,
      serverId,
      serverName: data.ServerName || ''
    }
  } catch (err) {
    clearTimeout(timer)
    if (err.name === 'AbortError') {
      return { success: false, error: '连接 Emby 服务器超时，请检查网络或服务器地址' }
    }
    return { success: false, error: err.message || '网络无法访问 Emby 服务器' }
  }
}

/**
 * 获取 Emby 媒体库视图 (Views)
 */
export async function fetchEmbyViews(serverUrl, userId, token) {
  const cleanUrl = serverUrl.replace(/\/+$/, '')
  try {
    const res = await fetch(`${cleanUrl}/Users/${userId}/Views`, {
      headers: getEmbyAuthHeaders(token)
    })
    if (!res.ok) return []
    const data = await res.json()
    return data.Items || []
  } catch (err) {
    console.warn('[EmbyClient] fetchEmbyViews error:', err)
    return []
  }
}

/**
 * 获取 Emby 电影和电视剧总量统计
 */
export async function fetchEmbyItemCounts(serverUrl, userId, token) {
  const cleanUrl = serverUrl.replace(/\/+$/, '')
  let movieCount = 0
  let seriesCount = 0

  const headers = getEmbyAuthHeaders(token)

  // 1. 获取电影总数
  try {
    const res = await fetch(`${cleanUrl}/Users/${userId}/Items?Recursive=true&IncludeItemTypes=Movie&Limit=0`, { headers })
    if (res.ok) {
      const data = await res.json()
      movieCount = data.TotalRecordCount || 0
    }
  } catch (e) {
    console.warn('[EmbyClient] 获取电影总数失败:', e)
  }

  // 2. 获取剧集总数
  try {
    const res = await fetch(`${cleanUrl}/Users/${userId}/Items?Recursive=true&IncludeItemTypes=Series&Limit=0`, { headers })
    if (res.ok) {
      const data = await res.json()
      seriesCount = data.TotalRecordCount || 0
    }
  } catch (e) {
    console.warn('[EmbyClient] 获取剧集总数失败:', e)
  }

  return { movieCount, seriesCount }
}

/**
 * 拉取 Emby 真实影视条目并转换为 OnyxVision 标准数据
 */
export async function fetchEmbyItems(serverUrl, userId, token, limit = 60) {
  const cleanUrl = serverUrl.replace(/\/+$/, '')
  const fields = 'PrimaryImageAspectRatio,ProductionYear,CommunityRating,Overview,Genres,ProviderIds,MediaSources,RunTimeTicks'
  const url = `${cleanUrl}/Users/${userId}/Items?Recursive=true&IncludeItemTypes=Movie,Series&Limit=${limit}&Fields=${fields}&SortBy=DateCreated&SortOrder=Descending`

  try {
    const res = await fetch(url, { headers: getEmbyAuthHeaders(token) })
    if (!res.ok) return []
    const data = await res.json()
    const rawItems = data.Items || []

    return rawItems.map(item => {
      const isSeries = item.Type === 'Series'
      const year = item.ProductionYear || (item.PremiereDate ? new Date(item.PremiereDate).getFullYear() : 2024)
      const rating = item.CommunityRating ? Number(item.CommunityRating.toFixed(1)) : 8.5
      const durationSec = item.RunTimeTicks ? Math.floor(item.RunTimeTicks / 10000000) : (isSeries ? 2700 : 7200)

      // 海报图与背景图直链
      const poster = item.ImageTags?.Primary
        ? `${cleanUrl}/Items/${item.Id}/Images/Primary?maxWidth=500&tag=${item.ImageTags.Primary}`
        : ''
      const backdrop = (item.BackdropImageTags && item.BackdropImageTags[0])
        ? `${cleanUrl}/Items/${item.Id}/Images/Backdrop/0?maxWidth=1920&tag=${item.BackdropImageTags[0]}`
        : poster

      // Direct Play 播放直链
      const streamUrl = `${cleanUrl}/Videos/${item.Id}/stream.mp4?static=true&api_key=${token}`

      return {
        id: `emby_${item.Id}`,
        rawId: item.Id,
        title: item.Name || '未知影视',
        originalTitle: item.OriginalTitle || item.Name || '',
        type: isSeries ? 'tv' : 'movie',
        year: year,
        rating: rating,
        overview: item.Overview || '暂无详细剧情简介。',
        genres: (item.Genres && item.Genres.length > 0) ? item.Genres : (isSeries ? ['剧集', '4K 原画'] : ['电影', '4K 原画']),
        poster: poster,
        backdrop: backdrop,
        streamUrl: streamUrl,
        duration: durationSec,
        badges: ['4K UHD', 'HDR10', 'Direct Play'],
        provider: 'emby'
      }
    })
  } catch (err) {
    console.warn('[EmbyClient] fetchEmbyItems error:', err)
    return []
  }
}
