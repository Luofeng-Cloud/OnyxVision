import SwiftUI
import MediaPlayer
import AVFoundation

public struct VideoPlayerContainerView: View {
    public let server: EmbyServer
    public let item: EmbyItem
    @Environment(\.dismiss) private var dismiss
    
    @State private var playerConfig: PlayerConfiguration?
    @State private var isLoading = true
    @State private var errorMessage: String?
    
    @State private var currentTime: Double = 0.0
    @State private var duration: Double = 0.0
    @State private var isPlaying: Bool = true
    @State private var isBuffering: Bool = false
    @State private var showControls: Bool = true
    @State private var isLocked: Bool = false
    @State private var aspectRatio: VideoAspectRatio = .fit
    
    @State private var audioStreams: [MediaStream] = []
    @State private var subtitleStreams: [MediaStream] = []
    @State private var selectedAudioIndex: Int = 0
    @State private var selectedSubtitleIndex: Int = -1
    
    public var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            if let config = playerConfig {
                // 视频内核渲染层，带画面比例变换
                GeometryReader { geo in
                    VideoPlayerCoreView(
                        config: config,
                        currentTime: $currentTime,
                        duration: $duration,
                        isPlaying: $isPlaying,
                        isBuffering: $isBuffering,
                        onPlaybackEnded: {
                            dismiss()
                        }
                    )
                    .aspectRatio(aspectRatio == .crop ? nil : (16.0 / 9.0), contentMode: aspectRatio == .crop ? .fill : .fit)
                    .frame(width: geo.size.width, height: geo.size.height)
                    .clipped()
                }
                .ignoresSafeArea()
                
                // 旗舰交互控制与手势浮层 (集成 Infuse/VidHub/SenPlayer 核心体验)
                PlayerOverlayView(
                    title: item.name,
                    isDolbyVision: config.isDolbyVision,
                    dvBadgeText: config.dolbyVisionBadge,
                    resolutionBadge: item.resolutionBadge,
                    currentTime: $currentTime,
                    duration: $duration,
                    isPlaying: $isPlaying,
                    isBuffering: $isBuffering,
                    showControls: $showControls,
                    isLocked: $isLocked,
                    aspectRatio: $aspectRatio,
                    audioStreams: audioStreams,
                    subtitleStreams: subtitleStreams,
                    selectedAudioIndex: $selectedAudioIndex,
                    selectedSubtitleIndex: $selectedSubtitleIndex,
                    onDismiss: {
                        PlaybackSyncManager.shared.stopSession()
                        dismiss()
                    },
                    onSeek: { targetSeconds in
                        // 定位逻辑
                        currentTime = targetSeconds
                    },
                    onTogglePlayPause: {
                        isPlaying.toggle()
                    },
                    onSeekBy: { delta in
                        currentTime = max(0, min(duration, currentTime + delta))
                    },
                    onNextEpisode: {
                        // 连播下一集
                        dismiss()
                    }
                )
            } else if isLoading {
                VStack(spacing: 16) {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        .scaleEffect(1.5)
                    Text("正在获取原画直链与杜比视界码流...")
                        .font(.footnote)
                        .foregroundColor(.gray)
                }
            } else if let error = errorMessage {
                VStack(spacing: 16) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 44))
                        .foregroundColor(.yellow)
                    Text(error)
                        .font(.headline)
                        .foregroundColor(.white)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 32)
                    Button("返回") {
                        dismiss()
                    }
                    .padding(.horizontal, 24)
                    .padding(.vertical, 10)
                    .background(Color.white.opacity(0.2))
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
            }
        }
        .statusBar(hidden: true)
        .onAppear {
            setupAudioSessionAndNowPlaying()
            loadPlaybackInfo()
        }
        .onDisappear {
            PlaybackSyncManager.shared.stopSession()
            clearNowPlaying()
        }
    }
    
    private func setupAudioSessionAndNowPlaying() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .moviePlayback, options: [.allowAirPlay, .allowBluetoothA2DP])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("音频 Session 初始化: \(error)")
        }
        
        // 注册锁屏控制中心
        let commandCenter = MPRemoteCommandCenter.shared()
        commandCenter.playCommand.addTarget { _ in
            self.isPlaying = true
            return .success
        }
        commandCenter.pauseCommand.addTarget { _ in
            self.isPlaying = false
            return .success
        }
        commandCenter.togglePlayPauseCommand.addTarget { _ in
            self.isPlaying.toggle()
            return .success
        }
        
        var nowPlayingInfo = [String: Any]()
        nowPlayingInfo[MPMediaItemPropertyTitle] = item.name
        nowPlayingInfo[MPMediaItemPropertyPlaybackDuration] = item.durationSeconds
        nowPlayingInfo[MPNowPlayingInfoPropertyElapsedPlaybackTime] = 0.0
        nowPlayingInfo[MPNowPlayingInfoPropertyPlaybackRate] = 1.0
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nowPlayingInfo
    }
    
    private func clearNowPlaying() {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
    }
    
    private func loadPlaybackInfo() {
        Task {
            do {
                let startTicks = item.userData?.playbackPositionTicks ?? 0
                let playbackInfo = try await EmbyAPIService.shared.getPlaybackInfo(
                    server: server,
                    itemId: item.id,
                    startPositionTicks: startTicks
                )
                
                guard let firstSource = playbackInfo.mediaSources.first,
                      let directUrl = firstSource.resolveDirectPlayUrl(serverUrl: server.url, itemId: item.id, token: server.token) else {
                    await MainActor.run {
                        self.errorMessage = "无法解析到有效的视频直链"
                        self.isLoading = false
                    }
                    return
                }
                
                let streams = firstSource.mediaStreams ?? item.mediaStreams ?? []
                let audios = streams.filter { $0.type == .audio }
                let subs = streams.filter { $0.type == .subtitle }
                let isDV = item.isDolbyVision || streams.contains { $0.dynamicRange.isDolbyVision }
                let dvBadge = item.dolbyVisionBadge ?? streams.first(where: { $0.dynamicRange.isDolbyVision })?.dolbyVisionBadgeText
                
                let resumeSeconds = item.userData?.playbackPositionSeconds ?? 0.0
                
                await MainActor.run {
                    self.audioStreams = audios
                    self.subtitleStreams = subs
                    self.playerConfig = PlayerConfiguration(
                        url: directUrl,
                        title: item.name,
                        isDolbyVision: isDV,
                        dolbyVisionBadge: dvBadge,
                        initialPositionSeconds: resumeSeconds,
                        audioStreams: audios,
                        subtitleStreams: subs
                    )
                    self.isLoading = false
                    
                    PlaybackSyncManager.shared.startSession(
                        server: server,
                        itemId: item.id,
                        playSessionId: playbackInfo.playSessionId,
                        initialSeconds: resumeSeconds
                    )
                }
            } catch {
                await MainActor.run {
                    self.errorMessage = "加载失败: \(error.localizedDescription)"
                    self.isLoading = false
                }
            }
        }
    }
}
