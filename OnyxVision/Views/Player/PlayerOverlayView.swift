import SwiftUI
import UIKit

public enum VideoAspectRatio: String, CaseIterable {
    case fit = "原始比例"
    case crop = "智能去黑边"
    case stretch = "全屏填充"
}

public struct PlayerOverlayView: View {
    public let title: String
    public let isDolbyVision: Bool
    public let dvBadgeText: String?
    public let resolutionBadge: String
    
    @Binding public var currentTime: Double
    @Binding public var duration: Double
    @Binding public var isPlaying: Bool
    @Binding public var isBuffering: Bool
    @Binding public var showControls: Bool
    @Binding public var isLocked: Bool
    @Binding public var aspectRatio: VideoAspectRatio
    
    public let audioStreams: [MediaStream]
    public let subtitleStreams: [MediaStream]
    @Binding public var selectedAudioIndex: Int
    @Binding public var selectedSubtitleIndex: Int
    
    public let onDismiss: () -> Void
    public let onSeek: (Double) -> Void
    public let onTogglePlayPause: () -> Void
    public let onSeekBy: (Double) -> Void
    public var onNextEpisode: (() -> Void)? = nil
    
    @State private var isDraggingSlider = false
    @State private var dragSliderValue: Double = 0.0
    @State private var showAudioSheet = false
    @State private var showSubtitleSheet = false
    @State private var showSleepTimerSheet = false
    
    // 手势调整亮度与音量
    @State private var gestureBrightness: CGFloat = UIScreen.main.brightness
    @State private var showBrightnessHUD = false
    @State private var gestureVolume: CGFloat = 0.5
    @State private var showVolumeHUD = false
    
    // 长按 2.0x 极速快进
    @State private var isFastForwarding = false
    
    // 字幕延迟微调 (±0.1s)
    @State private var subtitleDelaySeconds: Double = 0.0
    
    // 睡眠定时器
    @State private var sleepTimerRemainingMinutes: Int = 0
    
    public var body: some View {
        ZStack {
            // 背景遮罩手势（点击切换显示/隐藏控制栏，左右滑动调光调音）
            Color.black.opacity(showControls ? 0.45 : 0.001)
                .ignoresSafeArea()
                .onTapGesture {
                    withAnimation(.easeInOut(duration: 0.25)) {
                        showControls.toggle()
                    }
                }
                .gesture(
                    DragGesture(minimumDistance: 15)
                        .onChanged { value in
                            guard !isLocked else { return }
                            let screenWidth = UIScreen.main.bounds.width
                            let translation = -value.translation.height / 250.0
                            
                            // 屏幕左半边调节亮度
                            if value.startLocation.x < screenWidth * 0.5 {
                                let newBrightness = max(0.0, min(1.0, UIScreen.main.brightness + translation * 0.03))
                                UIScreen.main.brightness = newBrightness
                                gestureBrightness = newBrightness
                                showBrightnessHUD = true
                            } else {
                                // 屏幕右半边调节音量提示
                                gestureVolume = max(0.0, min(1.0, gestureVolume + translation * 0.03))
                                showVolumeHUD = true
                            }
                        }
                        .onEnded { _ in
                            DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) {
                                showBrightnessHUD = false
                                showVolumeHUD = false
                            }
                        }
                )
                .simultaneousGesture(
                    LongPressGesture(minimumDuration: 0.4)
                        .onEnded { _ in
                            guard !isLocked else { return }
                            let generator = UIImpactFeedbackGenerator(style: .medium)
                            generator.impactOccurred()
                            isFastForwarding = true
                        }
                )
            
            // 长按 2.0X 极速快进 HUD
            if isFastForwarding {
                VStack {
                    HStack(spacing: 6) {
                        Image(systemName: "forward.fill")
                            .font(.system(size: 14, weight: .black))
                        Text("2.0X 极速快进中")
                            .font(.system(size: 14, weight: .bold))
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(.ultraThinMaterial)
                    .foregroundColor(.yellow)
                    .cornerRadius(20)
                    .shadow(color: Color.yellow.opacity(0.3), radius: 8)
                    .padding(.top, 40)
                    
                    Spacer()
                }
                .onTapGesture {
                    isFastForwarding = false
                }
            }
            
            // 亮度和音量手势浮动 HUD
            if showBrightnessHUD {
                HStack(spacing: 8) {
                    Image(systemName: "sun.max.fill")
                        .foregroundColor(.yellow)
                    ProgressView(value: Double(gestureBrightness))
                        .frame(width: 120)
                        .tint(.yellow)
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 10)
                .background(.ultraThinMaterial)
                .cornerRadius(12)
                .transition(.opacity)
            }
            
            if showVolumeHUD {
                HStack(spacing: 8) {
                    Image(systemName: "speaker.wave.3.fill")
                        .foregroundColor(.white)
                    ProgressView(value: Double(gestureVolume))
                        .frame(width: 120)
                        .tint(.white)
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 10)
                .background(.ultraThinMaterial)
                .cornerRadius(12)
                .transition(.opacity)
            }
            
            // 追剧：自动跳过片头浮动按钮（播放前 90 秒自动浮现）
            if currentTime < 90 && duration > 120 && showControls && !isLocked {
                VStack {
                    Spacer()
                    HStack {
                        Button(action: {
                            onSeek(90)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "forward.end.fill")
                                Text("跳过片头 (90s)")
                                    .font(.system(size: 13, weight: .bold))
                            }
                            .foregroundColor(.white)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 8)
                            .background(Color.black.opacity(0.7))
                            .overlay(RoundedRectangle(cornerRadius: 18).stroke(Color.white.opacity(0.3), lineWidth: 1))
                            .cornerRadius(18)
                        }
                        .padding(.leading, 24)
                        .padding(.bottom, 75)
                        Spacer()
                    }
                }
            }
            
            // 追剧：下集连播倒计时悬浮卡片（最后 30 秒自动浮现）
            if duration > 60 && (duration - currentTime) <= 30 && (duration - currentTime) > 2 {
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        Button(action: {
                            onNextEpisode?()
                        }) {
                            HStack(spacing: 8) {
                                Image(systemName: "play.circle.fill")
                                    .font(.title3)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("下一集即将播放")
                                        .font(.caption2)
                                        .foregroundColor(.white.opacity(0.8))
                                    Text("点击立即连播 (\(Int(duration - currentTime))s)")
                                        .font(.footnote)
                                        .fontWeight(.bold)
                                        .foregroundColor(.white)
                                }
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 10)
                            .background(
                                LinearGradient(
                                    colors: [Color.blue.opacity(0.9), Color.purple.opacity(0.9)],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(16)
                            .shadow(color: Color.blue.opacity(0.4), radius: 8)
                        }
                        .padding(.trailing, 24)
                        .padding(.bottom, 75)
                    }
                }
            }
            
            // 锁定按钮 (悬浮于左下角)
            VStack {
                Spacer()
                HStack {
                    Button(action: {
                        withAnimation { isLocked.toggle() }
                    }) {
                        Image(systemName: isLocked ? "lock.fill" : "lock.open")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(isLocked ? .yellow : .white)
                            .padding(12)
                            .background(.ultraThinMaterial)
                            .clipShape(Circle())
                    }
                    .padding(.leading, 24)
                    .padding(.bottom, 24)
                    Spacer()
                }
            }
            
            // 核心控制层（未锁定时显示）
            if showControls && !isLocked {
                VStack(spacing: 0) {
                    // MARK: 顶部控制栏
                    topBar
                    
                    Spacer()
                    
                    // MARK: 中间快进/快退/播放/缓冲状态
                    centerControls
                    
                    Spacer()
                    
                    // MARK: 底部进度条与音轨字幕控制栏
                    bottomBar
                }
                .transition(.opacity)
            }
        }
        .sheet(isPresented: $showAudioSheet) {
            audioTrackPickerView
        }
        .sheet(isPresented: $showSubtitleSheet) {
            subtitlePickerView
        }
        .sheet(isPresented: $showSleepTimerSheet) {
            sleepTimerPickerView
        }
    }
    
    // MARK: - 顶部导航栏
    private var topBar: some View {
        HStack(spacing: 12) {
            Button(action: onDismiss) {
                Image(systemName: "chevron.left")
                    .font(.system(size: 20, weight: .bold))
                    .foregroundColor(.white)
                    .padding(8)
            }
            
            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(.headline)
                    .foregroundColor(.white)
                    .lineLimit(1)
                
                HStack(spacing: 6) {
                    // 杜比视界高动态黄金徽章
                    if isDolbyVision {
                        HStack(spacing: 3) {
                            Image(systemName: "sparkles")
                                .font(.system(size: 9, weight: .black))
                            Text(dvBadgeText ?? "DOLBY VISION")
                                .font(.system(size: 9, weight: .heavy))
                        }
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(
                            LinearGradient(
                                colors: [Color(red: 0.98, green: 0.85, blue: 0.35), Color(red: 0.85, green: 0.6, blue: 0.1)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .foregroundColor(.black)
                        .cornerRadius(4)
                        .shadow(color: Color.yellow.opacity(0.3), radius: 4)
                    }
                    
                    // 杜比全景声徽章
                    HStack(spacing: 2) {
                        Image(systemName: "waveform")
                            .font(.system(size: 8, weight: .black))
                        Text("ATMOS")
                            .font(.system(size: 9, weight: .bold))
                    }
                    .padding(.horizontal, 5)
                    .padding(.vertical, 2)
                    .background(Color.blue.opacity(0.3))
                    .foregroundColor(.cyan)
                    .cornerRadius(4)
                    
                    if !resolutionBadge.isEmpty {
                        Text(resolutionBadge)
                            .font(.system(size: 9, weight: .bold))
                            .padding(.horizontal, 5)
                            .padding(.vertical, 2)
                            .background(Color.white.opacity(0.18))
                            .foregroundColor(.white)
                            .cornerRadius(3)
                    }
                    
                    Text("直链 0 转码")
                        .font(.system(size: 9, weight: .medium))
                        .padding(.horizontal, 5)
                        .padding(.vertical, 2)
                        .background(Color.green.opacity(0.25))
                        .foregroundColor(.green)
                        .cornerRadius(3)
                }
            }
            
            Spacer()
            
            // 画面比例切换（原始 / 智能去黑边 / 满屏）
            Button(action: {
                cycleAspectRatio()
            }) {
                HStack(spacing: 3) {
                    Image(systemName: "aspectratio")
                    Text(aspectRatio.rawValue)
                        .font(.caption2)
                }
                .foregroundColor(.white)
                .padding(.horizontal, 8)
                .padding(.vertical, 6)
                .background(.ultraThinMaterial)
                .cornerRadius(8)
            }
            
            // 睡眠定时器
            Button(action: { showSleepTimerSheet = true }) {
                Image(systemName: sleepTimerRemainingMinutes > 0 ? "timer.circle.fill" : "timer")
                    .foregroundColor(sleepTimerRemainingMinutes > 0 ? .yellow : .white)
                    .padding(8)
                    .background(.ultraThinMaterial)
                    .clipShape(Circle())
            }
            
            // 音轨选择
            Button(action: { showAudioSheet = true }) {
                HStack(spacing: 3) {
                    Image(systemName: "waveform")
                    Text("音轨")
                        .font(.footnote)
                }
                .foregroundColor(.white)
                .padding(.horizontal, 8)
                .padding(.vertical, 6)
                .background(.ultraThinMaterial)
                .cornerRadius(8)
            }
            
            // 字幕与微调
            Button(action: { showSubtitleSheet = true }) {
                HStack(spacing: 3) {
                    Image(systemName: "captions.bubble.fill")
                    Text("字幕")
                        .font(.footnote)
                }
                .foregroundColor(.white)
                .padding(.horizontal, 8)
                .padding(.vertical, 6)
                .background(.ultraThinMaterial)
                .cornerRadius(8)
            }
        }
        .padding(.horizontal, 16)
        .padding(.top, 16)
    }
    
    // MARK: - 中间播放暂停与快进快退
    private var centerControls: some View {
        HStack(spacing: 48) {
            Button(action: { onSeekBy(-10) }) {
                Image(systemName: "gobackward.10")
                    .font(.system(size: 30, weight: .medium))
                    .foregroundColor(.white)
            }
            
            if isBuffering {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(1.6)
                    .frame(width: 60, height: 60)
            } else {
                Button(action: onTogglePlayPause) {
                    Image(systemName: isPlaying ? "pause.fill" : "play.fill")
                        .font(.system(size: 44, weight: .bold))
                        .foregroundColor(.white)
                        .frame(width: 60, height: 60)
                }
            }
            
            Button(action: { onSeekBy(10) }) {
                Image(systemName: "goforward.10")
                    .font(.system(size: 30, weight: .medium))
                    .foregroundColor(.white)
            }
        }
    }
    
    // MARK: - 底部进度条栏
    private var bottomBar: some View {
        VStack(spacing: 6) {
            HStack(spacing: 12) {
                Text(formatTime(isDraggingSlider ? dragSliderValue : currentTime))
                    .font(.caption)
                    .monospacedDigit()
                    .foregroundColor(.white)
                
                Slider(
                    value: Binding(
                        get: { isDraggingSlider ? dragSliderValue : currentTime },
                        set: { dragSliderValue = $0 }
                    ),
                    in: 0...max(duration, 1.0),
                    onEditingChanged: { editing in
                        isDraggingSlider = editing
                        if !editing {
                            onSeek(dragSliderValue)
                        }
                    }
                )
                .accentColor(isDolbyVision ? .yellow : .blue)
                
                Text(formatTime(duration))
                    .font(.caption)
                    .monospacedDigit()
                    .foregroundColor(.white.opacity(0.8))
            }
            .padding(.horizontal, 24)
            .padding(.bottom, 24)
        }
    }
    
    private func cycleAspectRatio() {
        let all = VideoAspectRatio.allCases
        if let idx = all.firstIndex(of: aspectRatio) {
            let nextIdx = (idx + 1) % all.count
            aspectRatio = all[nextIdx]
        }
    }
    
    // MARK: - 音轨选择弹窗
    private var audioTrackPickerView: some View {
        NavigationView {
            List {
                ForEach(Array(audioStreams.enumerated()), id: \.offset) { index, stream in
                    Button(action: {
                        selectedAudioIndex = index
                        showAudioSheet = false
                    }) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(stream.displayTitle ?? stream.title ?? "音轨 \(index + 1)")
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                
                                HStack(spacing: 6) {
                                    if let codec = stream.codec {
                                        Text(codec.uppercased())
                                            .font(.caption2)
                                            .padding(3)
                                            .background(Color.gray.opacity(0.2))
                                            .cornerRadius(3)
                                    }
                                    Text(stream.channelDescription)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                            }
                            Spacer()
                            if selectedAudioIndex == index {
                                Image(systemName: "checkmark")
                                    .foregroundColor(.blue)
                                    .font(.headline)
                            }
                        }
                    }
                }
            }
            .navigationTitle("选择音轨")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("关闭") { showAudioSheet = false }
                }
            }
        }
    }
    
    // MARK: - 字幕选择与微调弹窗
    private var subtitlePickerView: some View {
        NavigationView {
            List {
                Section(header: Text("字幕时间轴微调 (±0.1s 步进)")) {
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("当前偏移: ")
                                .font(.subheadline)
                            Text(String(format: "%+.1f 秒", subtitleDelaySeconds))
                                .font(.headline)
                                .foregroundColor(subtitleDelaySeconds == 0 ? .primary : .blue)
                            Spacer()
                            Button("重置") {
                                subtitleDelaySeconds = 0.0
                            }
                            .font(.caption)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.gray.opacity(0.15))
                            .cornerRadius(6)
                        }
                        
                        HStack(spacing: 12) {
                            Button("-0.5s") { subtitleDelaySeconds -= 0.5 }
                                .buttonStyle(.bordered)
                            Button("-0.1s") { subtitleDelaySeconds -= 0.1 }
                                .buttonStyle(.borderedProminent)
                            Button("+0.1s") { subtitleDelaySeconds += 0.1 }
                                .buttonStyle(.borderedProminent)
                            Button("+0.5s") { subtitleDelaySeconds += 0.5 }
                                .buttonStyle(.bordered)
                        }
                    }
                    .padding(.vertical, 6)
                }
                
                Section(header: Text("字幕轨道")) {
                    Button(action: {
                        selectedSubtitleIndex = -1
                        showSubtitleSheet = false
                    }) {
                        HStack {
                            Text("关闭字幕")
                                .foregroundColor(.primary)
                            Spacer()
                            if selectedSubtitleIndex == -1 {
                                Image(systemName: "checkmark")
                                    .foregroundColor(.blue)
                            }
                        }
                    }
                    
                    ForEach(Array(subtitleStreams.enumerated()), id: \.offset) { index, stream in
                        Button(action: {
                            selectedSubtitleIndex = index
                            showSubtitleSheet = false
                        }) {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(stream.displayTitle ?? stream.title ?? "字幕 \(index + 1)")
                                        .font(.headline)
                                        .foregroundColor(.primary)
                                    
                                    HStack(spacing: 6) {
                                        if let lang = stream.language {
                                            Text(lang)
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }
                                        if stream.isDefault {
                                            Text("默认")
                                                .font(.caption2)
                                                .padding(2)
                                                .background(Color.blue.opacity(0.2))
                                                .cornerRadius(3)
                                        }
                                    }
                                }
                                Spacer()
                                if selectedSubtitleIndex == index {
                                    Image(systemName: "checkmark")
                                        .foregroundColor(.blue)
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("字幕与特效调节")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("完成") { showSubtitleSheet = false }
                }
            }
        }
    }
    
    // MARK: - 睡眠定时器弹窗
    private var sleepTimerPickerView: some View {
        NavigationView {
            List {
                Button("关闭睡眠定时器") {
                    sleepTimerRemainingMinutes = 0
                    showSleepTimerSheet = false
                }
                .foregroundColor(.red)
                
                ForEach([15, 30, 45, 60, 90], id: \.self) { mins in
                    Button("\(mins) 分钟后停止播放") {
                        sleepTimerRemainingMinutes = mins
                        showSleepTimerSheet = false
                    }
                    .foregroundColor(.primary)
                }
            }
            .navigationTitle("睡眠定时器")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("取消") { showSleepTimerSheet = false }
                }
            }
        }
    }
    
    private func formatTime(_ seconds: Double) -> String {
        guard !seconds.isNaN && !seconds.isInfinite && seconds >= 0 else { return "00:00" }
        let total = Int(seconds)
        let s = total % 60
        let m = (total / 60) % 60
        let h = total / 3600
        if h > 0 {
            return String(format: "%d:%02d:%02d", h, m, s)
        } else {
            return String(format: "%02d:%02d", m, s)
        }
    }
}
