<template>
  <div
    v-if="displayItems.length > 0"
    class="relative w-full overflow-hidden select-none cursor-pointer"
    @click="handleBannerClick"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
    @pointerdown="handlePointerDown"
    @pointerup="handlePointerUp"
  >
    <!-- 轮播图列表 (支持平滑滑动与切换) -->
    <div
      v-for="(item, index) in displayItems"
      :key="item.id"
      class="relative w-full transition-opacity duration-700 ease-in-out"
      :class="[currentIndex === index ? 'block opacity-100' : 'hidden opacity-0']"
    >
      <!-- 背景主图 (1:1 像素级原画海报) -->
      <div class="relative w-full aspect-[470/570] max-h-[560px] overflow-hidden">
        <img
          :src="item.backdrop || item.poster"
          :alt="item.title"
          class="w-full h-full object-cover object-top transition-transform duration-700"
          loading="lazy"
        />

        <!-- 顶部通透微渐变与底部消融渐变 (对齐截图 4) -->
        <div class="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-[#0A0B0E] via-[#0A0B0E]/70 to-transparent"></div>
        <div class="absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-black/40 via-transparent to-transparent"></div>

        <!-- 左右滑动辅助微箭头 (桌面端悬浮可见) -->
        <button
          v-if="displayItems.length > 1"
          @click.stop="prevSlide"
          class="hidden sm:flex absolute left-4 top-1/2 -translate-y-1/2 z-20 w-9 h-9 rounded-full bg-black/40 hover:bg-black/70 backdrop-blur-md border border-white/15 items-center justify-center text-white/80 hover:text-white transition"
          title="上一部"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <polyline points="15 18 9 12 15 6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button
          v-if="displayItems.length > 1"
          @click.stop="nextSlide"
          class="hidden sm:flex absolute right-4 top-1/2 -translate-y-1/2 z-20 w-9 h-9 rounded-full bg-black/40 hover:bg-black/70 backdrop-blur-md border border-white/15 items-center justify-center text-white/80 hover:text-white transition"
          title="下一部"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <polyline points="9 18 15 12 9 6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- 文字与评分区 (1:1 像素级对齐截图 4 居中排版) -->
      <div class="px-5 -mt-6 relative z-10 text-center space-y-2 max-w-sm mx-auto">
        <!-- 评分与类型行: ★ 8.8 | 2023 | 动画,喜剧,Sci-Fi & Fantasy,动作冒险 -->
        <div class="flex items-center justify-center gap-1.5 text-xs text-white/90">
          <span v-if="item.rating" class="text-[#FFCC00] font-bold">★ {{ item.rating }}</span>
          <span v-if="item.rating && item.year" class="text-white/40">|</span>
          <span v-if="item.year" class="font-medium">{{ item.year }}</span>
          <span v-if="item.genres && item.genres.length > 0" class="text-white/40">|</span>
          <span v-if="item.genres" class="text-white/75 truncate max-w-[200px]">{{ Array.isArray(item.genres) ? item.genres.join(',') : item.genres }}</span>
        </div>

        <!-- 剧情简介 (对齐截图 4 截断样式) -->
        <p v-if="item.overview" class="text-xs text-white/70 line-clamp-2 leading-relaxed font-normal">
          {{ item.overview }}
        </p>

        <!-- 轮播小圆点 (支持滑动联动高亮) -->
        <div v-if="displayItems.length > 1" class="flex items-center justify-center gap-1.5 pt-1" @click.stop>
          <button
            v-for="(_, dotIdx) in Math.min(displayItems.length, 8)"
            :key="dotIdx"
            @click="selectSlide(dotIdx)"
            class="transition-all duration-300 rounded-full"
            :class="[
              (currentIndex % Math.min(displayItems.length, 8)) === dotIdx
                ? 'w-1.5 h-1.5 bg-white shadow-sm scale-110'
                : 'w-1.5 h-1.5 bg-white/35 hover:bg-white/60'
            ]"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['play', 'open-detail'])

const displayItems = computed(() => {
  return props.items.length > 0 ? props.items : []
})

const currentIndex = ref(0)
const currentItem = computed(() => displayItems.value[currentIndex.value] || displayItems.value[0])

let timer = null
let wasSwiped = false

function handleBannerClick() {
  if (wasSwiped) {
    wasSwiped = false
    return
  }
  emit('play', currentItem.value)
}

// 移动端手势滑动手势支持
let touchStartX = 0
let touchStartY = 0
let isDragging = false

function handleTouchStart(e) {
  if (e.touches && e.touches[0]) {
    touchStartX = e.touches[0].clientX
    touchStartY = e.touches[0].clientY
  }
}

function handleTouchMove(e) {
  // 不阻止纵向滚动，仅在横向位移显著时捕获
}

function handleTouchEnd(e) {
  if (e.changedTouches && e.changedTouches[0]) {
    const deltaX = e.changedTouches[0].clientX - touchStartX
    const deltaY = e.changedTouches[0].clientY - touchStartY
    // 如果横向滑动距离大于 40px 且明显大于纵向位移
    if (Math.abs(deltaX) > 40 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
      wasSwiped = true
      if (deltaX < 0) {
        nextSlide()
      } else {
        prevSlide()
      }
      resetTimer()
      setTimeout(() => { wasSwiped = false }, 350)
    }
  }
}

// 鼠标手势支持 (桌面端拖拽)
function handlePointerDown(e) {
  touchStartX = e.clientX
  touchStartY = e.clientY
  isDragging = true
}

function handlePointerUp(e) {
  if (!isDragging) return
  isDragging = false
  const deltaX = e.clientX - touchStartX
  if (Math.abs(deltaX) > 30) {
    wasSwiped = true
    if (deltaX < 0) {
      nextSlide()
    } else {
      prevSlide()
    }
    resetTimer()
    setTimeout(() => { wasSwiped = false }, 350)
  }
}

function selectSlide(index) {
  if (index < displayItems.value.length) {
    currentIndex.value = index
    resetTimer()
  }
}

function nextSlide() {
  if (displayItems.value.length > 0) {
    currentIndex.value = (currentIndex.value + 1) % displayItems.value.length
  }
}

function prevSlide() {
  if (displayItems.value.length > 0) {
    currentIndex.value = (currentIndex.value - 1 + displayItems.value.length) % displayItems.value.length
  }
}

function startTimer() {
  timer = setInterval(nextSlide, 15000)
}

function resetTimer() {
  clearInterval(timer)
  startTimer()
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>
