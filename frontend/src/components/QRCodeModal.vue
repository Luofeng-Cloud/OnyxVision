<template>
  <div class="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-2xl flex items-center justify-center p-4">
    <div class="relative w-full max-w-md bg-[#0A0B0E] border border-white/10 rounded-3xl overflow-hidden shadow-2xl p-6 sm:p-8 flex flex-col items-center text-center space-y-5 animate-fade-in">
      <!-- 动态环境微光 -->
      <div class="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-[80px] bg-purple-600/20 pointer-events-none"></div>
      <div class="absolute -bottom-20 -left-20 w-60 h-60 rounded-full blur-[80px] bg-cyan-600/20 pointer-events-none"></div>

      <!-- 关闭按钮 -->
      <button
        @click="$emit('close')"
        class="absolute top-5 right-5 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white/80 hover:text-white transition"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>

      <!-- 二维码画布 -->
      <div class="p-3 bg-white rounded-3xl shadow-2xl shadow-purple-500/10 border-4 border-white/20 mt-2">
        <canvas ref="qrCanvas" class="w-48 h-48 sm:w-56 sm:h-56 block rounded-xl"></canvas>
      </div>

      <!-- 标题与说明 -->
      <div class="space-y-1.5 max-w-sm">
        <h4 class="text-base font-bold text-white">
          iPhone / 移动设备连接 OnyxVision 曜石视界
        </h4>
        <p class="text-xs text-white/60 leading-relaxed">
          手机与电脑连接同一个 Wi-Fi 网络，打开相机扫码即可在 Safari 全屏秒开，享受 100% 触控手势（亮度/音量/寻道/2x倍速）。
        </p>
      </div>

      <!-- 访问地址卡片 -->
      <div class="w-full p-3 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between gap-2">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineEmits(['close'])

const copied = ref(false)
const qrCanvas = ref(null)
const lanUrl = ref(`http://${window.location.hostname || '192.168.1.188'}:${window.location.port || '5173'}/`)

function copyUrl() {
  navigator.clipboard.writeText(lanUrl.value).then(() => {
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  })
}

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

onMounted(() => {
  setTimeout(renderQRCode, 50)
})
</script>
