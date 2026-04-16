#!/usr/bin/env python3
"""
区块链Reels视频生成脚本 - 深度增强版 v2.0
支持: 英文输出、雷达图、动态效果、分段音频
"""

import os
import sys
import json
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime

# 配置路径
BASE_DIR = Path("F:/stepclaw/agents/blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
SCRIPT_DIR = OUTPUT_DIR / "scripts"
DATA_DIR = OUTPUT_DIR / "data"
CHART_DIR = OUTPUT_DIR / "charts"

def ensure_dirs():
    """确保输出目录存在"""
    for d in [OUTPUT_DIR, AUDIO_DIR, VIDEO_DIR, SCRIPT_DIR, DATA_DIR, CHART_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def generate_tts_audio(text: str, output_path: Path, voice: str = "en-US-AriaNeural"):
    """
    使用 edge-tts 生成音频 (英文)
    """
    try:
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", str(output_path),
            "--write-subtitles", str(output_path.with_suffix('.vtt'))
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ TTS generated: {output_path}")
            return True
        else:
            print(f"❌ TTS failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def get_audio_duration(audio_path: Path):
    """获取音频时长"""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(str(audio_path))
        return len(audio) / 1000.0  # 转换为秒
    except:
        return None

def generate_chart_matplotlib(chart_type: str, data: dict, output_path: Path):
    """
    使用 matplotlib 生成动态图表 - 增强版
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(9, 16), dpi=100)
        
        if chart_type == "radar_chart":
            # 雷达图 - 量化因子
            factors = ['On-chain', 'Market Micro', 'Macro', 'Risk']
            scores = [
                data['factors']['on_chain_behavior'],
                data['factors']['market_microstructure'],
                data['factors']['macro_sentiment'],
                data['factors']['risk_special']
            ]
            
            # 归一化到0-1
            normalized = [(s + 2) / 4 for s in scores]
            
            angles = np.linspace(0, 2 * np.pi, len(factors), endpoint=False).tolist()
            normalized += normalized[:1]
            angles += angles[:1]
            
            ax = plt.subplot(111, projection='polar')
            ax.plot(angles, normalized, 'o-', linewidth=2, color='#FF3366')
            ax.fill(angles, normalized, alpha=0.25, color='#FF3366')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(factors, fontsize=12)
            ax.set_ylim(0, 1)
            ax.set_title(f"Quant Score: {data['value']:.1f} ({data['label']})\n30-day low, down {abs(data['historical_context']['change_from_last_week']):.1f} from last week", 
                        fontsize=14, fontweight='bold', pad=20)
            
        elif chart_type == "bar_chart":
            # 柱状图 - 交易所净流量（带阈值线）
            days = data.get('days', [])
            values = data.get('values', [])
            threshold = data.get('warning_threshold', 5000)
            
            colors = ['#00FF88' if v < 0 else '#FF3366' for v in values]
            bars = ax.barh(days, values, color=colors, alpha=0.7)
            
            # 阈值线
            ax.axvline(x=threshold, color='#FF3366', linestyle='--', linewidth=2, label=f'Warning: {threshold} BTC/day')
            ax.axvline(x=-threshold, color='#00FF88', linestyle='--', linewidth=2)
            ax.axvline(x=0, color='white', linewidth=1)
            
            ax.set_xlabel('Net Inflow/Outflow (BTC)', fontsize=12, color='white')
            ax.set_title('Exchange Net Flow (7 Days)\n3 days above warning line', fontsize=16, fontweight='bold', color='white')
            ax.legend(loc='lower right')
            ax.tick_params(colors='white')
            
            # 背景色
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
            
        elif chart_type == "area_chart":
            # 面积图 - 巨鲸持仓
            dates = data.get('dates', [])
            values = data.get('values', [])
            
            x = range(len(dates))
            ax.plot(x, values, linewidth=3, color='#FF3366')
            ax.fill_between(x, values, alpha=0.4, color='#FF3366')
            
            # 标注变化
            change = values[-1] - values[0]
            ax.annotate(f'{change:+.1f}%', 
                       xy=(len(dates)-1, values[-1]),
                       xytext=(len(dates)-2, values[-1] + 0.3),
                       fontsize=14, fontweight='bold', color='#FF3366',
                       arrowprops=dict(arrowstyle='->', color='#FF3366'))
            
            ax.set_ylabel('Top 100 Holdings (%)', fontsize=12, color='white')
            ax.set_title('Whale Holdings Trend\nQuiet exit while retail FOMOs in', fontsize=16, fontweight='bold', color='white')
            ax.set_xticks(x[::2])
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45)
            ax.tick_params(colors='white')
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
            
        elif chart_type == "scam_card":
            # 骗局预警卡片
            risk_level = data.get('level', 'Low')
            risk_color = {'High': '#FF3366', 'Medium': '#FFAA00', 'Low': '#00FF88'}.get(risk_level, '#00FF88')
            
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.8, 0.4, 
                                      facecolor=risk_color, alpha=0.2, edgecolor=risk_color, linewidth=3))
            
            ax.text(0.5, 0.65, '⚠️', ha='center', va='center', fontsize=80)
            ax.text(0.5, 0.5, f"{data.get('type', 'Scam')} Risk", 
                   ha='center', va='center', fontsize=20, fontweight='bold', color='white')
            ax.text(0.5, 0.4, f"Level: {risk_level}", 
                   ha='center', va='center', fontsize=16, color=risk_color, fontweight='bold')
            ax.text(0.5, 0.3, f"Signal: {data.get('specific_signal', '')}", 
                   ha='center', va='center', fontsize=12, color='white')
            ax.text(0.5, 0.2, f"💡 Tip: {data.get('actionable_advice', '')}", 
                   ha='center', va='center', fontsize=11, color='#AAAAAA', style='italic')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
            
        elif chart_type == "thermometer":
            # 温度计 - 资金费率
            value = data.get('value', 0)
            
            # 温度计主体
            ax.add_patch(plt.Rectangle((0.45, 0.1), 0.1, 0.7, 
                                      facecolor='#333333', edgecolor='white', linewidth=2))
            
            # 温度填充
            center = 0.45
            height = 0.35 + (value * 2000) * 0.35  # 缩放
            color = '#4444FF' if value < 0 else '#FF3366'
            ax.add_patch(plt.Rectangle((0.45, 0.1), 0.1, max(0.05, height), 
                                      facecolor=color, alpha=0.8))
            
            # 数值
            ax.text(0.5, 0.05, f'{value*100:.3f}%', ha='center', va='top', fontsize=18, fontweight='bold', color=color)
            ax.text(0.5, 0.9, 'Funding Rate', ha='center', va='bottom', fontsize=14, color='white')
            ax.text(0.5, 0.85, data.get('interpretation', ''), ha='center', va='top', fontsize=12, color=color)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
            
        elif chart_type == "conclusion":
            # 结论卡片
            conclusion = data.get('summary', '')
            judgment = data.get('judgment', '')
            
            ax.text(0.5, 0.7, 'BOTTOM LINE', ha='center', va='center', fontsize=24, fontweight='bold', color='#FF3366')
            ax.text(0.5, 0.55, conclusion, ha='center', va='center', fontsize=18, fontweight='bold', color='white')
            ax.text(0.5, 0.4, judgment, ha='center', va='center', fontsize=14, color='#AAAAAA')
            
            # 关键信号列表
            signals = [
                "❌ Bounce: Fake",
                "✅ Distribution: Real",
                "⚠️ Risk > Reward"
            ]
            y_pos = 0.25
            for signal in signals:
                ax.text(0.5, y_pos, signal, ha='center', va='center', fontsize=12, color='white')
                y_pos -= 0.05
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        
        print(f"✅ Chart generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Chart generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_video_with_moviepy(video_data: dict, output_path: Path):
    """
    使用 moviepy 合成视频 - 增强版
    """
    try:
        from moviepy.editor import (
            AudioFileClip, TextClip, ImageClip,
            CompositeVideoClip, concatenate_videoclips, ColorClip
        )
        from moviepy.video.fx.all import blink
        
        clips = []
        W, H = 1080, 1920
        
        # 为每个clip生成音频并计算时长
        clips_data = video_data.get('clips', [])
        
        for i, clip_data in enumerate(clips_data):
            text = clip_data.get('text', '')
            visual_type = clip_data.get('visual_type', '')
            
            # 生成音频
            audio_path = AUDIO_DIR / f"clip_{i:02d}.mp3"
            if generate_tts_audio(text, audio_path):
                duration = get_audio_duration(audio_path) or (clip_data.get('end', 10) - clip_data.get('start', 0))
            else:
                duration = clip_data.get('end', 10) - clip_data.get('start', 0)
            
            # 生成视觉
            chart_path = CHART_DIR / f"{visual_type}.png"
            
            if visual_type == "alert":
                # Hook - 红色警报
                bg = ColorClip(size=(W, H), color=(30, 20, 20)).set_duration(duration)
                txt = TextClip(text, fontsize=70, color='#FF3366', font='Arial-Bold',
                              size=(W, H), method='caption').set_duration(duration)
                clip = CompositeVideoClip([bg, txt.set_position('center')])
                
            elif visual_type in ["radar_chart", "bar_chart", "area_chart", "scam_card", "thermometer", "conclusion"]:
                # 图表
                if chart_path.exists():
                    img = ImageClip(str(chart_path)).set_duration(duration).resize(height=H)
                    clip = img
                else:
                    # 备用：纯色背景+文字
                    bg = ColorClip(size=(W, H), color=(26, 26, 46)).set_duration(duration)
                    txt = TextClip(text[:100], fontsize=50, color='white', font='Arial',
                                  size=(W, H), method='caption').set_duration(duration)
                    clip = CompositeVideoClip([bg, txt.set_position('center')])
            else:
                # 默认
                bg = ColorClip(size=(W, H), color=(26, 26, 46)).set_duration(duration)
                txt = TextClip(text[:100], fontsize=50, color='white', font='Arial',
                              size=(W, H), method='caption').set_duration(duration)
                clip = CompositeVideoClip([bg, txt.set_position('center')])
            
            # 添加音频
            if audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                clip = clip.set_audio(audio)
            
            clips.append(clip)
        
        # 合成最终视频
        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")
            
            final_clip.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(AUDIO_DIR / 'temp_audio.m4a'),
                remove_temp=True
            )
            
            final_clip.close()
            print(f"✅ Video generated: {output_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Video composition failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_reels_from_data(video_data: dict):
    """
    主流程：从 video_data.json 生成完整 Reels
    """
    ensure_dirs()
    
    date_str = datetime.now().strftime("%Y%m%d")
    print(f"🎬 Generating Reels for {date_str}...")
    
    # 1. 生成图表
    print("📊 Generating charts...")
    
    if 'quant_score' in video_data:
        generate_chart_matplotlib("radar_chart", video_data['quant_score'], CHART_DIR / "radar_chart.png")
    
    if 'exchange_flow' in video_data:
        generate_chart_matplotlib("bar_chart", video_data['exchange_flow'], CHART_DIR / "bar_chart.png")
    
    if 'whale_holdings' in video_data:
        generate_chart_matplotlib("area_chart", video_data['whale_holdings'], CHART_DIR / "area_chart.png")
    
    if 'scam_alert' in video_data:
        generate_chart_matplotlib("scam_card", video_data['scam_alert'], CHART_DIR / "scam_card.png")
    
    if 'funding_rate' in video_data:
        generate_chart_matplotlib("thermometer", video_data['funding_rate'], CHART_DIR / "thermometer.png")
    
    if 'conclusion' in video_data:
        generate_chart_matplotlib("conclusion", video_data['conclusion'], CHART_DIR / "conclusion.png")
    
    # 2. 合成视频
    print("🎬 Composing video...")
    output_video = VIDEO_DIR / f"blockchain_reels_{date_str}.mp4"
    
    if create_video_with_moviepy(video_data, output_video):
        print(f"\n🎉 Reels video completed!")
        print(f"   Output: {output_video}")
        return True
    else:
        print("\n❌ Video generation failed")
        return False

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        data_file = DATA_DIR / "video_data.json"
        if not data_file.exists():
            print(f"❌ Data file not found: {data_file}")
            sys.exit(1)
    else:
        data_file = Path(sys.argv[1])
    
    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        sys.exit(1)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        video_data = json.load(f)
    
    success = generate_reels_from_data(video_data)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
