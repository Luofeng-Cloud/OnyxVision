<template>
  <div
    ref="playerContainer"
    class="fixed inset-0 z-[100] bg-black select-none overflow-hidden touch-player font-apple"
    @pointerdown="handlePointerDown"
    @pointermove="handlePointerMove"
    @pointerup="handlePointerUp"
    @pointercancel="handlePointerUp"
    @mousemove="triggerControlsActive"
  >
    <!-- 视频底层（结合亮度滤镜） -->
    <div
      class="w-full h-full flex items-center justify-center transition-filter duration-75"
      :style="{ filter: `brightness(${brightness})` }"
    >
      <video
        ref="videoRef"
        :src="videoSource"
        class="w-full h-full transition-all duration-300"
        :class="aspectRatioClass"
        playsinline
        webkit-playsinline
        x5-video-player-type="h5"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
        @canplay="onCanPlay"
        @ended="onEnded"
        @play="onPlay"
        @pause="onPause"
      ></video>
    </div>

    <!-- 顶部极速 2.0X 播放呼吸 HUD -->
    <transition name="fade">
      <div
        v-if="isFastForwarding"
        class="absolute top-16 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2.5 px-6 py-2 rounded-full bg-red-600/80 backdrop-blur-xl border border-white/20 text-white shadow-2xl animate-pulse"
      >
        <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
          <path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/>
        </svg>
        <span class="text-sm font-bold tracking-wider">2.0X 极速播放中</span>
      </div>
    </transition>

    <!-- 左侧屏幕亮度调节 HUD -->
    <transition name="fade">
      <div
        v-if="activeGesture === 'brightness'"
        class="absolute top-1/2 -translate-y-1/2 z-50 flex flex-col items-center gap-3 bg-black/60 backdrop-blur-2xl px-3.5 py-6 rounded-2xl border border-white/15 shadow-2xl pointer-events-none transition-all duration-150"
        :style="{ left: 'calc(2.5rem + env(safe-area-inset-left, 0px))' }"
      >
        <!-- 太阳高光图标 -->
        <svg class="w-6 h-6 text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="5" stroke-width="2"/>
          <path stroke-linecap="round" stroke-width="2" d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
        </svg>
        <!-- 竖向胶囊进度槽 -->
        <div class="w-2.5 h-36 bg-white/20 rounded-full overflow-hidden flex flex-col justify-end">
          <div
            class="w-full bg-gradient-to-t from-yellow-400 to-yellow-200 rounded-full transition-all duration-75"
            :style="{ height: `${Math.round(brightness * 100)}%` }"
          ></div>
        </div>
        <span class="text-xs font-mono font-bold text-white">
          {{ Math.round(brightness * 100) }}%
        </span>
      </div>
    </transition>

    <!-- 右侧屏幕音量调节 HUD -->
    <transition name="fade">
      <div
        v-if="activeGesture === 'volume'"
        class="absolute top-1/2 -translate-y-1/2 z-50 flex flex-col items-center gap-3 bg-black/60 backdrop-blur-2xl px-3.5 py-6 rounded-2xl border border-white/15 shadow-2xl pointer-events-none transition-all duration-150"
        :style="{ right: 'calc(2.5rem + env(safe-area-inset-right, 0px))' }"
      >
        <!-- 喇叭图标 -->
        <svg class="w-6 h-6 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" stroke-width="2" fill="currentColor"/>
          <path stroke-linecap="round" stroke-width="2" d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/>
        </svg>
        <!-- 竖向音量槽 -->
        <div class="w-2.5 h-36 bg-white/20 rounded-full overflow-hidden flex flex-col justify-end">
          <div
            class="w-full bg-gradient-to-t from-blue-500 to-cyan-300 rounded-full transition-all duration-75"
            :style="{ height: `${Math.round(volume * 100)}%` }"
          ></div>
        </div>
        <span class="text-xs font-mono font-bold text-white">
          {{ Math.round(volume * 100) }}%
        </span>
      </div>
    </transition>

    <!-- 水平 Seeking 时间轴寻道 HUD -->
    <transition name="fade">
      <div
        v-if="activeGesture === 'seek'"
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 flex flex-col items-center gap-2 bg-black/75 backdrop-blur-3xl px-8 py-5 rounded-3xl border border-white/20 shadow-2xl pointer-events-none"
      >
        <div class="flex items-center gap-2 text-2xl font-bold font-mono tracking-tight" :class="seekDelta >= 0 ? 'text-green-400' : 'text-red-400'">
          <span>{{ seekDelta >= 0 ? '+' : '' }}{{ formatSeekDelta(seekDelta) }}</span>
        </div>
        <div class="flex items-center gap-2 text-sm text-white/90 font-mono">
          <span>{{ formatTime(seekTargetTime) }}</span>
          <span class="text-white/40">/</span>
          <span class="text-white/60">{{ formatTime(duration) }}</span>
        </div>
        <div class="w-48 h-1.5 bg-white/20 rounded-full overflow-hidden mt-1">
          <div
            class="h-full bg-white rounded-full"
            :style="{ width: `${duration > 0 ? (seekTargetTime / duration) * 100 : 0}%` }"
          ></div>
        </div>
      </div>
    </transition>

    <!-- 双击快进 / 快退波纹动效 HUD -->
    <transition name="fade">
      <div
        v-if="doubleTapFeedback.show"
        class="absolute top-1/2 -translate-y-1/2 z-40 pointer-events-none flex flex-col items-center"
        :class="doubleTapFeedback.type === 'forward' ? 'right-20' : 'left-20'"
      >
        <div class="w-20 h-20 rounded-full bg-white/10 backdrop-blur-xl border border-white/20 flex flex-col items-center justify-center animate-ping">
          <span class="text-xs font-black text-white font-mono">
            {{ doubleTapFeedback.type === 'forward' ? '+10s' : '-10s' }}
          </span>
        </div>
      </div>
    </transition>

    <!-- 顶部控制栏 (带返回、影片标题、时钟) -->
    <transition name="fade">
      <div
        v-if="showControls"
        class="absolute top-0 left-0 right-0 z-30 px-6 py-4 bg-gradient-to-b from-black/90 via-black/40 to-transparent flex items-center justify-between transition-all duration-300"
        :style="{
          paddingTop: 'calc(0.75rem + env(safe-area-inset-top, 16px))',
          paddingLeft: 'calc(1.5rem + env(safe-area-inset-left, 0px))',
          paddingRight: 'calc(1.5rem + env(safe-area-inset-right, 0px))'
        }"
      >
        <div class="flex items-center gap-4">
          <button
            @click="$emit('close')"
            class="p-2.5 rounded-full bg-white/10 hover:bg-white/20 backdrop-blur-xl border border-white/15 text-white transition active:scale-95"
            title="退出全屏播放"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <div>
            <h2 class="text-base sm:text-lg font-bold text-white drop-shadow">
              {{ media.title }}
            </h2>
            <span v-if="media.subtitle || media.currentEpisode" class="text-xs text-white/60">
              {{ media.subtitle || (`第 ${media.currentEpisode.episodeNumber} 集 · ${media.currentEpisode.title}`) }}
            </span>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <!-- 杜比视界高亮指示 -->
          <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-white/15 border border-white/20 text-white/90">
            {{ media.badges ? media.badges[1] || 'Dolby Atmos' : '4K HDR' }}
          </span>
          <!-- 当前系统时间 -->
          <span class="text-xs font-mono text-white/70">
            {{ currentTimeString }}
          </span>
        </div>
      </div>
    </transition>

    <!-- 底部控制栏 -->
    <transition name="fade">
      <div
        v-if="showControls"
        class="absolute bottom-0 left-0 right-0 z-30 px-6 pb-6 pt-12 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col gap-3 transition-all duration-300"
        :style="{
          paddingBottom: 'calc(1.25rem + env(safe-area-inset-bottom, 16px))',
          paddingLeft: 'calc(1.5rem + env(safe-area-inset-left, 0px))',
          paddingRight: 'calc(1.5rem + env(safe-area-inset-right, 0px))'
        }"
      >
        <!-- 进度条 -->
        <div class="relative w-full flex items-center group/seek py-2 cursor-pointer" @click="handleProgressBarClick">
          <!-- 底槽 -->
          <div class="w-full h-1.5 group-hover/seek:h-2.5 bg-white/20 rounded-full overflow-hidden transition-all duration-150">
            <div
              class="h-full bg-gradient-to-r from-red-600 to-red-400 rounded-full relative"
              :style="{ width: `${progressPercent}%` }"
            ></div>
          </div>
          <!-- 悬浮小滑块 -->
          <div
            class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white rounded-full shadow-lg scale-0 group-hover/seek:scale-100 transition-transform pointer-events-none"
            :style="{ left: `calc(${progressPercent}% - 8px)` }"
          ></div>
        </div>

        <!-- 底部功能按钮组 -->
        <div class="flex items-center justify-between gap-4">
          <!-- 左侧：播放/暂停、快进快退、时间 -->
          <div class="flex items-center gap-4">
            <!-- 播放/暂停 -->
            <button
              @click="togglePlay"
              class="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center hover:scale-105 active:scale-95 transition"
            >
              <svg v-if="!isPlaying" class="w-5 h-5 fill-current translate-x-0.5" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <svg v-else class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
              </svg>
            </button>

            <!-- 快退 10s -->
            <button
              @click="skipTime(-10)"
              class="text-white/80 hover:text-white p-1.5 transition"
              title="快退 10 秒"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.066 11.2a1 1 0 000 1.6l5.334 4A1 1 0 0019 16V8a1 1 0 00-1.6-.8l-5.333 4zM4.066 11.2a1 1 0 000 1.6l5.334 4A1 1 0 0011 16V8a1 1 0 00-1.6-.8l-5.334 4z"/>
              </svg>
            </button>

            <!-- 快进 10s -->
            <button
              @click="skipTime(10)"
              class="text-white/80 hover:text-white p-1.5 transition"
              title="快进 10 秒"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.933 12.8a1 1 0 000-1.6L6.6 7.2A1 1 0 005 8v8a1 1 0 001.6.8l5.333-4zM19.933 12.8a1 1 0 000-1.6l-5.333-4A1 1 0 0013 8v8a1 1 0 001.6.8l5.333-4z"/>
              </svg>
            </button>

            <!-- 时间轴 -->
            <div class="text-xs font-mono text-white/80 select-none">
              <span>{{ formatTime(currentTime) }}</span>
              <span class="text-white/40 mx-1">/</span>
              <span>{{ formatTime(duration) }}</span>
            </div>
          </div>

          <!-- 右侧：倍速、画幅比例、音轨、字幕、画中画、全屏 -->
          <div class="flex items-center gap-2 sm:gap-3">
            <!-- 倍速选择胶囊 -->
            <div class="relative">
              <button
                @click="showRateMenu = !showRateMenu"
                class="px-2.5 py-1 rounded-full text-xs font-bold border border-white/20 bg-white/10 hover:bg-white/20 text-white backdrop-blur-md transition"
              >
                {{ playbackRate }}x
              </button>

              <div
                v-if="showRateMenu"
                class="absolute bottom-10 right-0 bg-black/90 backdrop-blur-2xl border border-white/15 rounded-xl py-1 w-20 shadow-2xl z-50 flex flex-col"
              >
                <button
                  v-for="r in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]"
                  :key="r"
                  @click="setRate(r)"
                  class="px-3 py-1.5 text-xs text-left hover:bg-white/15 transition flex items-center justify-between"
                  :class="playbackRate === r ? 'text-red-400 font-bold' : 'text-white/80'"
                >
                  <span>{{ r }}x</span>
                  <span v-if="playbackRate === r">✓</span>
                </button>
              </div>
            </div>

            <!-- 画幅比例切换 -->
            <button
              @click="cycleAspectRatio"
              title="切换画面比例 (适应/16:9/4:3/铺满)"
              class="p-2 rounded-full hover:bg-white/15 text-white/80 hover:text-white transition"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="2" y="4" width="20" height="16" rx="2" stroke-width="2"/>
                <path stroke-linecap="round" stroke-width="1.5" d="M7 8h10M7 16h10"/>
              </svg>
            </button>

            <!-- 字幕选择 -->
            <button
              @click="toggleSubtitles"
              :class="subtitlesEnabled ? 'text-red-400' : 'text-white/80 hover:text-white'"
              title="字幕开关"
              class="p-2 rounded-full hover:bg-white/15 transition"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="2" y="5" width="20" height="14" rx="2" stroke-width="2"/>
                <path stroke-linecap="round" stroke-width="2" d="M7 15h3M14 15h3M7 11h10"/>
              </svg>
            </button>

            <!-- 画中画 (PiP) -->
            <button
              @click="togglePiP"
              title="画中画"
              class="p-2 rounded-full hover:bg-white/15 text-white/80 hover:text-white transition"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="2" y="3" width="20" height="14" rx="2" stroke-width="2"/>
                <rect x="12" y="9" width="8" height="6" rx="1" fill="currentColor" stroke="none"/>
              </svg>
            </button>

            <!-- 全屏 -->
            <button
              @click="toggleFullscreen"
              title="全屏切换"
              class="p-2 rounded-full hover:bg-white/15 text-white/80 hover:text-white transition"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { savePlaybackHistory } from '../utils/offlineStore.js'
import { reportPlaybackProgress } from '../api/client.js'

const props = defineProps({
  media: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const videoRef = ref(null)
const playerContainer = ref(null)

const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1.0)
const brightness = ref(1.0)
const playbackRate = ref(1.0)
const isFastForwarding = ref(false)
const normalRateBeforeFF = ref(1.0)

const showControls = ref(true)
let hideControlsTimer = null

const showRateMenu = ref(false)
const subtitlesEnabled = ref(true)

// 画面比例：'contain' (自适应原始), 'cover' (铺满剪裁), '16:9', '4:3'
const aspectRatios = ['contain', 'cover', '16-9', '4-3']
const currentAspectIndex = ref(0)
const aspectRatioClass = computed(() => {
  const current = aspectRatios[currentAspectIndex.value]
  if (current === 'contain') return 'object-contain'
  if (current === 'cover') return 'object-cover'
  if (current === '16-9') return 'object-fill aspect-video'
  if (current === '4-3') return 'object-fill aspect-[4/3]'
  return 'object-contain'
})

function cycleAspectRatio() {
  currentAspectIndex.value = (currentAspectIndex.value + 1) % aspectRatios.length
  triggerControlsActive()
}

// 手势系统
const activeGesture = ref(null) // 'brightness' | 'volume' | 'seek' | null
const seekDelta = ref(0)
const seekTargetTime = ref(0)
let startX = 0
let startY = 0
let startVolume = 1.0
let startBrightness = 1.0
let startTimeVal = 0
let pointerDownTimestamp = 0
let longPressTimer = null
let lastTapTimestamp = 0
let isDragging = false

const doubleTapFeedback = ref({
  show: false,
  type: 'forward'
})

const videoSource = computed(() => {
  const directUrl = props.media.streamUrl || props.media.stream_url || props.media.playback_url || props.media.videoUrl
  if (directUrl && (directUrl.startsWith('http://') || directUrl.startsWith('https://') || directUrl.startsWith('/api/stream/'))) {
    return directUrl
  }
  if (props.media.id && !String(props.media.id).startsWith('media_')) {
    return `/api/stream/${props.media.id}`
  }
  return directUrl || ''
})

const progressPercent = computed(() => {
  if (duration.value <= 0) return 0
  return (currentTime.value / duration.value) * 100
})

const currentTimeString = ref('')
let clockTimer = null

function updateClock() {
  const now = new Date()
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  currentTimeString.value = `${h}:${m}`
}

function triggerControlsActive() {
  showControls.value = true
  clearTimeout(hideControlsTimer)
  hideControlsTimer = setTimeout(() => {
    if (isPlaying.value && !activeGesture.value && !showRateMenu.value) {
      showControls.value = false
    }
  }, 3500)
}

function handlePointerDown(e) {
  startX = e.clientX
  startY = e.clientY
  isDragging = false
  pointerDownTimestamp = Date.now()
  startVolume = volume.value
  startBrightness = brightness.value
  startTimeVal = currentTime.value

  triggerControlsActive()

  // 300ms 长按检测 -> 2.0x 极速快进
  clearTimeout(longPressTimer)
  longPressTimer = setTimeout(() => {
    if (!isDragging) {
      isFastForwarding.value = true
      normalRateBeforeFF.value = playbackRate.value
      if (videoRef.value) {
        videoRef.value.playbackRate = 2.0
      }
    }
  }, 300)
}

function handlePointerMove(e) {
  const dx = e.clientX - startX
  const dy = e.clientY - startY
  const dist = Math.hypot(dx, dy)

  if (dist > 12) {
    isDragging = true
    clearTimeout(longPressTimer)
  }

  if (isFastForwarding.value) return

  if (isDragging && !activeGesture.value) {
    // 首次判定手势方向
    if (Math.abs(dx) > Math.abs(dy)) {
      activeGesture.value = 'seek'
    } else {
      const screenWidth = window.innerWidth || document.documentElement.clientWidth
      if (startX < screenWidth / 2) {
        activeGesture.value = 'brightness'
      } else {
        activeGesture.value = 'volume'
      }
    }
  }

  if (activeGesture.value === 'brightness') {
    // 纵向上滑增加，下滑减小
    const delta = -dy / 250
    brightness.value = Math.min(Math.max(0.1, startBrightness + delta), 1.5)
  } else if (activeGesture.value === 'volume') {
    const delta = -dy / 250
    const newVol = Math.min(Math.max(0, startVolume + delta), 1.0)
    volume.value = newVol
    if (videoRef.value) videoRef.value.volume = newVol
  } else if (activeGesture.value === 'seek') {
    // 横向滑动寻道：灵敏度自适应
    const seekStep = (dx / 3) // 像素转秒
    seekDelta.value = Math.round(seekStep)
    seekTargetTime.value = Math.min(Math.max(0, startTimeVal + seekStep), duration.value)
  }
}

function handlePointerUp(e) {
  clearTimeout(longPressTimer)

  // 释放 2.0x 快进
  if (isFastForwarding.value) {
    isFastForwarding.value = false
    if (videoRef.value) {
      videoRef.value.playbackRate = normalRateBeforeFF.value
    }
    return
  }

  // 结束 Seeking
  if (activeGesture.value === 'seek') {
    if (videoRef.value && duration.value > 0) {
      videoRef.value.currentTime = seekTargetTime.value
    }
    activeGesture.value = null
    return
  }

  if (activeGesture.value) {
    activeGesture.value = null
    return
  }

  // 双击检测
  const now = Date.now()
  const tapInterval = now - lastTapTimestamp
  const screenWidth = window.innerWidth || document.documentElement.clientWidth

  if (tapInterval < 300 && !isDragging) {
    // 双击
    if (startX < screenWidth * 0.35) {
      // 左侧双击：快退 10 秒
      skipTime(-10)
      showDoubleTap('backward')
    } else if (startX > screenWidth * 0.65) {
      // 右侧双击：快进 10 秒
      skipTime(10)
      showDoubleTap('forward')
    } else {
      // 中间双击：播放/暂停
      togglePlay()
    }
    lastTapTimestamp = 0
  } else {
    lastTapTimestamp = now
  }
}

function showDoubleTap(type) {
  doubleTapFeedback.value = { show: true, type }
  setTimeout(() => {
    doubleTapFeedback.value.show = false
  }, 600)
}

function togglePlay() {
  if (!videoRef.value) return
  if (isPlaying.value) {
    videoRef.value.pause()
  } else {
    videoRef.value.play().catch(() => {})
  }
  triggerControlsActive()
}

function skipTime(sec) {
  if (!videoRef.value) return
  videoRef.value.currentTime = Math.min(Math.max(0, videoRef.value.currentTime + sec), duration.value)
  triggerControlsActive()
}

function setRate(rate) {
  playbackRate.value = rate
  if (videoRef.value) {
    videoRef.value.playbackRate = rate
  }
  showRateMenu.value = false
  triggerControlsActive()
}

function toggleSubtitles() {
  subtitlesEnabled.value = !subtitlesEnabled.value
  triggerControlsActive()
}

async function togglePiP() {
  try {
    if (document.pictureInPictureElement) {
      await document.exitPictureInPicture()
    } else if (videoRef.value) {
      await videoRef.value.requestPictureInPicture()
    }
  } catch (err) {
    console.warn('Picture in Picture failed:', err)
  }
  triggerControlsActive()
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    playerContainer.value?.requestFullscreen?.()
  } else {
    document.exitFullscreen?.()
  }
  triggerControlsActive()
}

function handleProgressBarClick(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  const clickX = e.clientX - rect.left
  const ratio = clickX / rect.width
  if (videoRef.value && duration.value > 0) {
    videoRef.value.currentTime = ratio * duration.value
  }
  triggerControlsActive()
}

let initialSeekDone = false

function applyInitialSeek() {
  if (initialSeekDone || !videoRef.value) return
  const targetSeek = props.media.initialSeekTime ?? props.media.currentTime ?? props.media.playback?.position_seconds
  if (targetSeek !== undefined && targetSeek > 0) {
    videoRef.value.currentTime = targetSeek
    currentTime.value = targetSeek
    initialSeekDone = true
  } else {
    const rawProgress = props.media.progress ?? (props.media.playback?.playback_percentage ? props.media.playback.playback_percentage / 100 : 0)
    if (rawProgress > 0 && duration.value > 0 && rawProgress < 0.98) {
      const pSeek = rawProgress * duration.value
      videoRef.value.currentTime = pSeek
      currentTime.value = pSeek
      initialSeekDone = true
    }
  }
}

let lastHistorySaveTime = 0

function recordPlaybackProgress() {
  if (currentTime.value > 0 && duration.value > 0) {
    const progress = currentTime.value / duration.value
    const progressTime = `${formatTime(currentTime.value)} / ${formatTime(duration.value)}`
    savePlaybackHistory(props.media, progress, progressTime, currentTime.value, duration.value)

    if (props.media.id && !String(props.media.id).startsWith('media_')) {
      reportPlaybackProgress({
        item_id: props.media.id,
        position_seconds: Math.round(currentTime.value),
        duration_seconds: Math.round(duration.value),
        is_paused: !isPlaying.value
      })
    }
  }
}

function onTimeUpdate() {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    const now = Date.now()
    if (now - lastHistorySaveTime > 2500) {
      lastHistorySaveTime = now
      recordPlaybackProgress()
    }
  }
}

function onLoadedMetadata() {
  if (videoRef.value) {
    duration.value = videoRef.value.duration
    applyInitialSeek()
    videoRef.value.play().catch(() => {})
  }
}

function onCanPlay() {
  applyInitialSeek()
}

// iOS & 移动端全屏防熄屏常亮 (Screen WakeLock API)
let wakeLock = null

async function requestWakeLock() {
  try {
    if ('wakeLock' in navigator && !wakeLock) {
      wakeLock = await navigator.wakeLock.request('screen')
      wakeLock.addEventListener('release', () => {
        wakeLock = null
      })
    }
  } catch (e) {
    // WakeLock not supported or user low battery mode
  }
}

function releaseWakeLock() {
  if (wakeLock) {
    wakeLock.release().catch(() => {})
    wakeLock = null
  }
}

function onPlay() {
  isPlaying.value = true
  requestWakeLock()
}

function onPause() {
  isPlaying.value = false
  releaseWakeLock()
  recordPlaybackProgress()
}

function onEnded() {
  isPlaying.value = false
  releaseWakeLock()
  showControls.value = true
  recordPlaybackProgress()
}

function handleVisibilityChange() {
  if (document.visibilityState === 'visible' && isPlaying.value) {
    requestWakeLock()
  }
}

function formatTime(sec) {
  if (!sec || isNaN(sec)) return '00:00'
  const total = Math.floor(sec)
  const h = Math.floor(total / 3600)
  const m = Math.floor((total % 3600) / 60)
  const s = total % 60
  if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  }
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function formatSeekDelta(delta) {
  const abs = Math.abs(delta)
  const m = Math.floor(abs / 60)
  const s = abs % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

onMounted(() => {
  updateClock()
  clockTimer = setInterval(updateClock, 30000)
  triggerControlsActive()
  document.addEventListener('visibilitychange', handleVisibilityChange)
  if (videoRef.value && videoRef.value.readyState >= 1) {
    duration.value = videoRef.value.duration
    applyInitialSeek()
  }
})

onUnmounted(() => {
  recordPlaybackProgress()
  releaseWakeLock()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  clearInterval(clockTimer)
  clearTimeout(hideControlsTimer)
  clearTimeout(longPressTimer)
})
</script>
