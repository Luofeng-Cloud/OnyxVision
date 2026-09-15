// OnyxVision (曜石视界) 高保真影视库与极客参数数据集
export const mockMediaList = [
  {
    id: 'media_dune2',
    title: '沙丘 2',
    originalTitle: 'Dune: Part Two',
    year: 2024,
    rating: 8.9,
    contentRating: 'PG-13',
    duration: '2小时 46分钟',
    genres: ['科幻', '冒险', '动作', '剧情'],
    ambientColor: '#d4883b',
    poster: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=1600&auto=format&fit=crop',
    progress: 0.68,
    progressTime: '01:52:14 / 02:46:00',
    badges: ['4K UHD', 'Dolby Vision', 'Dolby Atmos', 'HEVC', '42.8 Mbps'],
    overview: '保罗·厄崔迪携手契妮与弗雷曼人，向毁灭其家族的阴谋复仇。面对关于宇宙未来的可怕预知，他必须在毕生挚爱与已知宇宙的命运之间做出决绝抉择。',
    specs: {
      resolution: '3840 x 2160 (4K DCI 宽荧幕)',
      videoCodec: 'HEVC / H.265 (Main 10@L5.1@High)',
      colorSpace: 'BT.2020 / DCI-P3 (10-bit)',
      hdrFormat: 'Dolby Vision (Profile 8.1) + HDR10',
      frameRate: '23.976 fps',
      bitrate: '42.8 Mbps (CBR)',
      audioTrack: 'English Dolby Atmos (TrueHD 7.1) / 中文普通话 5.1',
      audioChannels: '7.1 独立全景声道 (7 Bed + 4 Object Channels)',
      audioBitrate: '4,520 kbps (无损母带)',
      container: 'MKV (Matroska Remux)',
      fileSize: '51.4 GB',
      subtitles: ['中文特效双语 (ASS)', '简中 (SRT)', '繁中 (SUP)', 'English SDH']
    },
    directors: ['丹尼斯·维伦纽瓦 (Denis Villeneuve)'],
    actors: [
      { name: '提莫西·查拉梅', role: '保罗·厄崔迪 (Paul Atreides)', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop' },
      { name: '赞达亚', role: '契妮 (Chani)', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop' },
      { name: '丽贝卡·弗格森', role: '杰西卡女士 (Lady Jessica)', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=200&auto=format&fit=crop' },
      { name: '哈维尔·巴登', role: '斯第尔格 (Stilgar)', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop' },
      { name: '奥斯汀·巴特勒', role: '菲德-罗萨 (Feyd-Rautha)', avatar: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop' }
    ],
    source: 'Emby',
    type: 'movie',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
  },
  {
    id: 'media_interstellar',
    title: '星际穿越',
    originalTitle: 'Interstellar',
    year: 2014,
    rating: 9.4,
    contentRating: 'PG-13',
    duration: '2小时 49分钟',
    genres: ['科幻', '悬疑', '冒险', '家庭'],
    ambientColor: '#1a365d',
    poster: 'https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1600&auto=format&fit=crop',
    progress: 0.85,
    progressTime: '02:24:10 / 02:49:00',
    badges: ['4K UHD', 'IMAX Enhanced', 'HDR10', 'DTS-HD MA', '54.2 Mbps'],
    overview: '在不远的未来，地球环境急剧恶化，沙尘暴肆虐。前 NASA 宇航员库珀穿过土星附近的神秘虫洞，前往未知星系寻找人类延续希望的行星，面对时间的相对性与跨越维度的爱。',
    specs: {
      resolution: '3840 x 2160 (IMAX 动态画幅全开 1.78:1 / 2.39:1)',
      videoCodec: 'HEVC / H.265 (Main 10@L5.1)',
      colorSpace: 'BT.2020 (10-bit Wide Color Gamut)',
      hdrFormat: 'HDR10 (1000 nits Mastering)',
      frameRate: '23.976 fps',
      bitrate: '54.2 Mbps',
      audioTrack: 'English DTS-HD MA 5.1 / 汉语普通话公映',
      audioChannels: '5.1 环绕声通道',
      audioBitrate: '3,840 kbps',
      container: 'MKV',
      fileSize: '68.2 GB',
      subtitles: ['双语特效字幕', '纯英文英文字幕', '国语台词配音字幕']
    },
    directors: ['克里斯托弗·诺兰 (Christopher Nolan)'],
    actors: [
      { name: '马修·麦康纳', role: '库珀 (Cooper)', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop' },
      { name: '安妮·海瑟薇', role: '布兰德 (Brand)', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop' },
      { name: '杰西卡·查斯坦', role: '墨菲 (Murph)', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=200&auto=format&fit=crop' }
    ],
    source: '本地',
    type: 'movie',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'
  },
  {
    id: 'media_oppenheimer',
    title: '奥本海默',
    originalTitle: 'Oppenheimer',
    year: 2023,
    rating: 8.8,
    contentRating: 'R',
    duration: '3小时 00分钟',
    genres: ['传记', '历史', '剧情'],
    ambientColor: '#78350f',
    poster: 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1600&auto=format&fit=crop',
    progress: 0.35,
    progressTime: '01:03:00 / 03:00:00',
    badges: ['4K UHD', 'Dolby Vision', 'DTS-HD MA', 'HEVC', '65.1 Mbps'],
    overview: '聚焦“原子弹之父”罗伯特·奥本海默主导曼哈顿计划、研制出人类第一颗核武器的过程，以及战后麦卡锡主义政治迫害下的道德审判与良知博弈。',
    specs: {
      resolution: '3840 x 2160 (IMAX 65mm 原盘转制)',
      videoCodec: 'HEVC / H.265 (Main 10)',
      colorSpace: 'BT.2020',
      hdrFormat: 'Dolby Vision / HDR10',
      frameRate: '23.976 fps',
      bitrate: '65.1 Mbps (极高码率无损压制)',
      audioTrack: 'English DTS-HD MA 5.1 (48kHz/24bit)',
      audioChannels: '5.1 声道',
      audioBitrate: '4,100 kbps',
      container: 'MKV',
      fileSize: '84.5 GB',
      subtitles: ['中英双语精校', '导评字幕']
    },
    directors: ['克里斯托弗·诺兰'],
    actors: [
      { name: '基里安·墨菲', role: 'J·罗伯特·奥本海默', avatar: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop' },
      { name: '小罗伯特·唐尼', role: '刘易斯·斯特劳斯', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop' },
      { name: '艾米莉·布朗特', role: '凯蒂·奥本海默', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop' }
    ],
    source: 'Emby',
    type: 'movie',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4'
  },
  {
    id: 'media_cyberpunk_edgerunners',
    title: '赛博朋克：边缘跑手',
    originalTitle: 'Cyberpunk: Edgerunners',
    year: 2022,
    rating: 9.0,
    contentRating: 'TV-MA',
    duration: '共 10 集 / 每集 24分钟',
    genres: ['动画', '动作', '科幻', '犯罪'],
    ambientColor: '#065f46',
    poster: 'https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1600&auto=format&fit=crop',
    progress: 0.90,
    progressTime: '第 1 季 第 9 集 21:00 / 24:00',
    badges: ['4K UHD', 'Dolby Vision', 'Dolby Atmos', 'HEVC', '28.0 Mbps'],
    overview: '在一座沉溺于义体改造与金钱的未来之城“夜之城”中，街头孤儿大卫·马丁内斯在遭遇家庭巨变后，选择成为一名亡命之徒——边缘跑手（Edgerunner）。',
    specs: {
      resolution: '3840 x 2160 (原生 4K 锐化母带)',
      videoCodec: 'HEVC / H.265 (Main 10)',
      colorSpace: 'BT.2020 / DCI-P3',
      hdrFormat: 'Dolby Vision Profile 5',
      frameRate: '23.976 fps',
      bitrate: '28.0 Mbps',
      audioTrack: 'Japanese Dolby Atmos (E-AC-3 JOC) / English 5.1',
      audioChannels: '7.1.4 空间音频流',
      audioBitrate: '768 kbps',
      container: 'MP4 / MKV',
      fileSize: '每集约 4.8 GB',
      subtitles: ['日文双语特效字幕', 'Netflix 官方中简/繁']
    },
    directors: ['今石洋之 (Hiroyuki Imaishi)'],
    actors: [
      { name: '大卫·马丁内斯', role: '主角 (David)', avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=200&auto=format&fit=crop' },
      { name: '露西 (Lucy)', role: '女主角 / 黑客', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop' },
      { name: '丽贝卡 (Rebecca)', role: '枪械狂热者', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=200&auto=format&fit=crop' }
    ],
    source: 'Emby',
    type: 'series',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
    seasons: [
      {
        seasonNumber: 1,
        seasonTitle: '第 1 季',
        episodes: [
          {
            episodeNumber: 1,
            title: '无家可归 (No F**ks Given)',
            duration: '25分钟',
            still: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=600&auto=format&fit=crop',
            overview: '大卫在一所名牌学院里苦苦挣扎，但一次致命的枪战导致家庭陷入绝境。',
            progress: 1.0
          },
          {
            episodeNumber: 2,
            title: '义体狂暴 (Like a Boy)',
            duration: '24分钟',
            still: 'https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=600&auto=format&fit=crop',
            overview: '植入斯安威斯坦神经系统的身体展现出超乎常人的耐受性，大卫偶遇了神秘盗贼露西。',
            progress: 1.0
          },
          {
            episodeNumber: 3,
            title: '畅游夜之城 (Smooth Criminal)',
            duration: '24分钟',
            still: 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=600&auto=format&fit=crop',
            overview: '大卫被带入由曼恩领导的雇佣兵小队，接受严苛的街头生存考验。',
            progress: 0.8
          },
          {
            episodeNumber: 4,
            title: '全副武装 (Lucky You)',
            duration: '23分钟',
            still: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop',
            overview: '大卫开始在队伍中挑大梁，与丽贝卡一同出任务，但危险逐渐逼近。',
            progress: 0
          }
        ]
      }
    ]
  },
  {
    id: 'media_bladerunner2049',
    title: '银翼杀手 2049',
    originalTitle: 'Blade Runner 2049',
    year: 2017,
    rating: 8.5,
    contentRating: 'R',
    duration: '2小时 44分钟',
    genres: ['科幻', '剧情', '黑色电影'],
    ambientColor: '#581c87',
    poster: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1508739773434-c26b3d09e071?q=80&w=1600&auto=format&fit=crop',
    progress: 0.15,
    progressTime: '00:25:30 / 02:44:00',
    badges: ['4K UHD', 'Dolby Vision', 'Dolby Atmos', 'HEVC', '48.9 Mbps'],
    overview: '在破败阴郁的洛杉矶，新一代银翼杀手 K 发现了一个埋藏已久的惊人秘密，这个秘密有能力将残存的社会秩序彻底推入混乱深渊。',
    specs: {
      resolution: '3840 x 2160',
      videoCodec: 'HEVC / H.265',
      colorSpace: 'BT.2020',
      hdrFormat: 'Dolby Vision / HDR10',
      frameRate: '23.976 fps',
      bitrate: '48.9 Mbps',
      audioTrack: 'English Dolby Atmos TrueHD 7.1',
      audioChannels: '7.1 声道',
      audioBitrate: '4,280 kbps',
      container: 'MKV',
      fileSize: '58.7 GB',
      subtitles: ['中英双语 (ASS)', '简中 (SRT)']
    },
    directors: ['丹尼斯·维伦纽瓦'],
    actors: [
      { name: '瑞恩·高斯林', role: 'K / 乔 (Joe)', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop' },
      { name: '哈里森·福特', role: '里克·戴克 (Rick Deckard)', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=200&auto=format&fit=crop' },
      { name: '安娜·德·阿玛斯', role: '乔伊 (Joi)', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop' }
    ],
    source: '本地',
    type: 'movie',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4'
  },
  {
    id: 'media_wanderingearth2',
    title: '流浪地球 2',
    originalTitle: 'The Wandering Earth II',
    year: 2023,
    rating: 8.3,
    contentRating: 'PG-13',
    duration: '2小时 53分钟',
    genres: ['科幻', '冒险', '灾难'],
    ambientColor: '#1e3a8a',
    poster: 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?q=80&w=800&auto=format&fit=crop',
    backdrop: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1600&auto=format&fit=crop',
    progress: 0.50,
    progressTime: '01:26:00 / 02:53:00',
    badges: ['4K UHD', 'Dolby Vision', 'Dolby Atmos', 'HEVC', '35.6 Mbps'],
    overview: '太阳即将毁灭，人类在地球表面建造出巨大的推进器，寻找新家园。然而宇宙之路危机四伏，太空电梯危机与月球坠落危机接踵而至，中国航天员与数字生命图恒宇背负起人类命运。',
    specs: {
      resolution: '3840 x 2160',
      videoCodec: 'HEVC / H.265 (10-bit)',
      colorSpace: 'BT.2020',
      hdrFormat: 'Dolby Vision Profile 8.1',
      frameRate: '24.000 fps',
      bitrate: '35.6 Mbps',
      audioTrack: '普通话 Dolby Atmos (全景声) / 粤语 5.1',
      audioChannels: '7.1.4 声道',
      audioBitrate: '768 kbps',
      container: 'MKV',
      fileSize: '46.1 GB',
      subtitles: ['官方公映中英字幕', '盲人视障解说轨']
    },
    directors: ['郭帆'],
    actors: [
      { name: '吴京', role: '刘培强', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop' },
      { name: '刘德华', role: '图恒宇', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop' },
      { name: '李雪健', role: '周喆直', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=200&auto=format&fit=crop' }
    ],
    source: 'Emby',
    type: 'movie',
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4'
  }
]

export const mockMediaSources = [
  {
    id: 'src_all',
    name: '全部媒体库',
    type: 'all',
    count: 284,
    status: 'online'
  },
  {
    id: 'src_emby',
    name: 'Emby 影视中枢',
    type: 'emby',
    host: 'https://emby.lan:8096',
    count: 196,
    status: 'online',
    lastSync: '10分钟前'
  },
  {
    id: 'src_local',
    name: '本地 4K 原盘 (D:/Movies)',
    type: 'local',
    host: '本地驱动器',
    count: 88,
    status: 'online',
    lastSync: '刚刚'
  }
]
