<template>
  <section class="max-w-[1720px] mx-auto px-4 sm:px-8 lg:px-12 py-6">
    <!-- 分区头部标题与总数 -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2.5">
        <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-white/95">
          {{ title }}
        </h2>
        <span v-if="count" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-white/10 text-white/60">
          {{ count }}
        </span>
      </div>
      <slot name="action"></slot>
    </div>

    <!-- 2:3 黄金比例瀑布流响应式网格 -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-7 gap-4 sm:gap-6">
      <MediaCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @play="$emit('play', $event)"
        @open-detail="$emit('open-detail', $event)"
      />
    </div>
  </section>
</template>

<script setup>
import MediaCard from './MediaCard.vue'

defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: [Number, String],
    default: null
  },
  items: {
    type: Array,
    default: () => []
  }
})

defineEmits(['play', 'open-detail'])
</script>
