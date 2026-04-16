#!/usr/bin/env python3
"""
生成 Open Graph 预览图 (og-preview.png)
用于社交媒体分享时显示
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def generate_og_image(output_path="og-preview.png"):
    """生成 1200x630 的 Open Graph 预览图"""
    
    # 图片尺寸 (Open Graph 标准)
    width, height = 1200, 630
    
    # 创建图片
    img = Image.new('RGB', (width, height), color='#0a0e27')
    draw = ImageDraw.Draw(img)
    
    # 渐变背景效果
    for y in range(height):
        # 从顶部到底部的渐变
        ratio = y / height
        r = int(10 + (26 - 10) * ratio)
        g = int(14 + (31 - 14) * ratio)
        b = int(39 + (58 - 39) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 尝试加载字体
    try:
        # 尝试使用系统字体
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        try:
            # Windows 字体
            font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 72)
            font_subtitle = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
            font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
        except:
            # 使用默认字体
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 标题
    title = "Crypto Risk Radar"
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = 150
    
    # 绘制标题（带发光效果）
    # 外发光
    for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
        draw.text((x + offset[0], y + offset[1]), title, font=font_title, fill='#1a3a5c')
    # 主文字
    draw.text((x, y), title, font=font_title, fill='#00d4ff')
    
    # 副标题
    subtitle = "Daily On-Chain Quant Analysis"
    bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = 280
    draw.text((x, y), subtitle, font=font_subtitle, fill='#ffffff')
    
    # 描述文字
    description = "Bitcoin • Ethereum • Scam Detection"
    bbox = draw.textbbox((0, 0), description, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = 380
    draw.text((x, y), description, font=font_small, fill='#8b9dc3')
    
    # 底部信息
    footer = "Updated every 12 hours | Free Data Sources"
    bbox = draw.textbbox((0, 0), footer, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = 520
    draw.text((x, y), footer, font=font_small, fill='#5a6a8a')
    
    # 装饰元素 - 雷达扫描线效果
    center_x, center_y = width - 200, 150
    # 外圈
    draw.ellipse([center_x-80, center_y-80, center_x+80, center_y+80], outline='#00d4ff', width=3)
    # 内圈
    draw.ellipse([center_x-50, center_y-50, center_x+50, center_y+50], outline='#00d4ff', width=2)
    # 中心点
    draw.ellipse([center_x-10, center_y-10, center_x+10, center_y+10], fill='#00d4ff')
    # 扫描线
    draw.line([(center_x, center_y), (center_x+70, center_y-70)], fill='#00d4ff', width=3)
    
    # 保存图片
    img.save(output_path, 'PNG')
    print(f"[SUCCESS] OG image generated: {output_path}")
    print(f"  Size: {width}x{height}")
    return output_path

if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "og-preview.png"
    generate_og_image(output)
