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
    
    @AppStorage("skip_intro_seconds") private var skipIntroSeconds = 0
    @State private var showSkipIntroButton = false
    
    public var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            if let config = playerConfig {
                // MARK: - 核心播放器渲染层（无遮挡全功能响应）
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
                .ignoresSafeArea()
                
                // MARK: - 顶部操作栏（左上角安全退出，右上角杜比/全景声黄金指示牌）
                VStack {
                    HStack {
                        Button(action: {
                            PlaybackSyncManager.shared.stopSession()
                            dismiss()
                        }) {
                            Image(systemName: "xmark")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(.white)
                                .frame(width: 32, height: 32)
                                .background(Color.black.opacity(0.6))
                                .clipShape(Circle())
                        }
                        .padding(.leading, 20)
                        .padding(.top, 16)
                        
                        Spacer()
                        
                        HStack(spacing: 6) {
                            if config.isDolbyVision {
                                HStack(spacing: 3) {
                                    Image(systemName: "sparkles")
                                        .font(.system(size: 10, weight: .black))
                                    Text(config.dolbyVisionBadge ?? "DOLBY VISION")
                                        .font(.system(size: 10, weight: .heavy))
                                }
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(
                                    LinearGradient(
                                        colors: [Color(red: 0.98, green: 0.85, blue: 0.35), Color(red: 0.85, green: 0.6, blue: 0.1)],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .foregroundColor(.black)
                                .cornerRadius(5)
                                .shadow(color: Color.yellow.opacity(0.4), radius: 5)
                            }
                            
                            HStack(spacing: 2) {
                                Image(systemName: "waveform")
                                    .font(.system(size: 8, weight: .bold))
                                Text("ATMOS")
                                    .font(.system(size: 9, weight: .heavy))
                            }
                            .padding(.horizontal, 6)
                            .padding(.vertical, 4)
                            .background(Color.blue.opacity(0.4))
                            .foregroundColor(.cyan)
                            .cornerRadius(5)
                            
                            Text("DirectPlay")
                                .font(.system(size: 9, weight: .bold))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 4)
                                .background(Color.green.opacity(0.3))
                                .foregroundColor(.green)
                                .cornerRadius(5)
                        }
                        .allowsHitTesting(false)
                        .padding(.trailing, 20)
                        .padding(.top, 16)
                    }
                    
                    Spacer()
                }
                
                // MARK: - 追剧快捷浮动操作 (右下角非模态按钮)
                if showSkipIntroButton && skipIntroSeconds > 0 {
                    VStack {
                        Spacer()
                        HStack {
                            Button(action: {
                                showSkipIntroButton = false
                            }) {
                                HStack(spacing: 6) {
                                    Image(systemName: "forward.end.fill")
                                    Text("已为您跳过片头 (\(skipIntroSeconds)s)")
                                        .font(.system(size: 12, weight: .bold))
                                }
                                .foregroundColor(.white)
                                .padding(.horizontal, 14)
                                .padding(.vertical, 8)
                                .background(Color.black.opacity(0.75))
                                .cornerRadius(16)
                                .shadow(radius: 4)
                            }
                            .padding(.leading, 24)
                            .padding(.bottom, 60)
                            Spacer()
                        }
                    }
                }
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
        .onReceive(Timer.publish(every: 1.0, on: .main, in: .common).autoconnect()) { _ in
            if isPlaying && !isBuffering && playerConfig != nil {
                currentTime += 1.0
                PlaybackSyncManager.shared.updatePosition(seconds: currentTime, isPaused: false)
            }
        }
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
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
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
                
                var resumeSeconds = item.userData?.playbackPositionSeconds ?? 0.0
                if resumeSeconds < 10 && skipIntroSeconds > 0 && (item.durationSeconds == 0 || item.durationSeconds > Double(skipIntroSeconds) + 30) {
                    resumeSeconds = Double(skipIntroSeconds)
                    await MainActor.run {
                        self.showSkipIntroButton = true
                    }
                }
                
                await MainActor.run {
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
