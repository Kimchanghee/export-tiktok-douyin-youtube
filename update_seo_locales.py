#!/usr/bin/env python3
"""
Update all locale files with SEO fields
Adds seo and faq fields to all 20 language files
"""

import json
import os

# SEO data for each language
SEO_DATA = {
    "ja": {
        "seo": {
            "title": "無料動画ダウンローダー - TikTok、Douyin、YouTube、Threads ダウンロード 2025",
            "description": "TikTok、Douyin、YouTube、Threadsから無料で高画質動画をダウンロード。ウォーターマークなし、高速で安全なオンライン動画ダウンローダー。ログイン不要、無制限ダウンロード。",
            "keywords": "動画ダウンローダー, TikTokダウンロード, YouTubeダウンロード, Douyinダウンロード, Threadsダウンロード, 無料動画保存, ウォーターマーク削除, HD動画",
            "og_title": "無料動画ダウンローダー - TikTok · YouTube · Douyin · Threads",
            "og_description": "ウォーターマークなしで無料で動画をダウンロード。高速で安全なオンラインツール。"
        },
        "faq": [
            {"question": "この動画ダウンローダーは無料ですか？", "answer": "はい、完全に無料です。隠れた費用や購読料はなく、無制限に動画をダウンロードできます。"},
            {"question": "どのプラットフォームに対応していますか？", "answer": "TikTok、Douyin、YouTube（通常動画およびShorts）、Threadsに対応しています。さらに多くのプラットフォームを準備中です。"},
            {"question": "ダウンロードした動画にウォーターマークはありますか？", "answer": "プラットフォームによって異なります。可能な場合はウォーターマークなしのバージョンを提供し、常に最高画質でダウンロードされます。"},
            {"question": "動画をダウンロードするにはログインが必要ですか？", "answer": "いいえ、ログインやサインアップは不要です。動画URLを貼り付けるだけですぐにダウンロードできます。"},
            {"question": "ダウンロード回数に制限はありますか？", "answer": "制限はありません。好きなだけ動画を無制限にダウンロードできます。"},
            {"question": "モバイルでも使用できますか？", "answer": "はい、モバイルブラウザでも完璧に動作します。iOSとAndroidの両方に完全対応しています。"}
        ]
    },
    "zh-CN": {
        "seo": {
            "title": "免费视频下载器 - 下载TikTok、抖音、YouTube、Threads 2025",
            "description": "从TikTok、抖音、YouTube和Threads免费下载高清视频。快速、安全、简单的在线视频下载工具。无水印，无需登录，无限下载。",
            "keywords": "视频下载器, TikTok下载, YouTube下载, 抖音下载, Threads下载, 免费视频保存, 去除水印, 高清视频, 在线下载",
            "og_title": "免费视频下载器 - TikTok · YouTube · 抖音 · Threads",
            "og_description": "免费下载视频，无水印。快速安全的在线工具。"
        },
        "faq": [
            {"question": "这个视频下载器免费吗？", "answer": "是的，完全免费。没有隐藏费用或订阅费，您可以无限下载视频。"},
            {"question": "支持哪些平台？", "answer": "我们支持TikTok、抖音、YouTube（常规视频和Shorts）和Threads。更多平台即将推出。"},
            {"question": "下载的视频有水印吗？", "answer": "这取决于平台。在可能的情况下，我们提供无水印版本，视频始终以最高质量下载。"},
            {"question": "下载视频需要登录吗？", "answer": "不需要，您无需登录或注册。只需粘贴视频URL即可立即开始下载。"},
            {"question": "下载次数有限制吗？", "answer": "没有限制。您可以随时下载任意数量的视频。"},
            {"question": "可以在手机上使用吗？", "answer": "是的，在移动浏览器上完美运行。完全支持iOS和Android。"}
        ]
    },
    "es": {
        "seo": {
            "title": "Descargador de Videos Gratis - Descargar TikTok, Douyin, YouTube, Threads 2025",
            "description": "Descarga videos de alta calidad de TikTok, Douyin, YouTube y Threads gratis. Descargador de videos en línea rápido, seguro y fácil. Sin marca de agua, sin inicio de sesión, descargas ilimitadas.",
            "keywords": "descargador de videos, descargar tiktok, descargar youtube, descargar douyin, descargar threads, guardar video gratis, quitar marca de agua, video HD",
            "og_title": "Descargador de Videos Gratis - TikTok · YouTube · Douyin · Threads",
            "og_description": "Descarga videos gratis sin marcas de agua. Herramienta en línea rápida y segura."
        },
        "faq": [
            {"question": "¿Este descargador de videos es gratis?", "answer": "Sí, es completamente gratis. Sin costos ocultos ni suscripciones, y puedes descargar videos ilimitados."},
            {"question": "¿Qué plataformas son compatibles?", "answer": "Admitimos TikTok, Douyin, YouTube (videos regulares y Shorts) y Threads. Pronto habrá más plataformas."},
            {"question": "¿Los videos descargados tienen marcas de agua?", "answer": "Depende de la plataforma. Cuando es posible, proporcionamos versiones sin marca de agua y los videos siempre se descargan en la máxima calidad disponible."},
            {"question": "¿Necesito iniciar sesión para descargar videos?", "answer": "No, no necesitas iniciar sesión ni registrarte. Solo pega la URL del video y comienza a descargar de inmediato."},
            {"question": "¿Hay un límite en las descargas?", "answer": "Sin límites. Puedes descargar tantos videos como quieras, cuando quieras."},
            {"question": "¿Puedo usarlo en móvil?", "answer": "Sí, funciona perfectamente en navegadores móviles. Totalmente compatible con iOS y Android."}
        ]
    }
}

# Add more languages as needed...

def update_locale_file(lang_code, seo_data):
    """Update a single locale file with SEO data"""
    filepath = f"web/locales/{lang_code}.json"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Add SEO fields if not already present
        if 'seo' not in data and lang_code in seo_data:
            data['seo'] = seo_data[lang_code]['seo']
            data['faq'] = seo_data[lang_code]['faq']

            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"[OK] Updated {lang_code}.json")
            return True
        else:
            print(f"[SKIP] Skipped {lang_code}.json (already has SEO fields)")
            return False

    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return False
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON in {filepath}")
        return False
    except Exception as e:
        print(f"[ERROR] Error updating {lang_code}.json: {e}")
        return False

def main():
    """Main function"""
    print("Updating locale files with SEO data...\n")

    updated = 0
    skipped = 0

    for lang_code in SEO_DATA:
        if update_locale_file(lang_code, SEO_DATA):
            updated += 1
        else:
            skipped += 1

    print(f"\nDone! Updated: {updated}, Skipped: {skipped}")
    print("\nNote: Only Japanese, Chinese (Simplified), and Spanish were updated.")
    print("Add more language data to SEO_DATA dictionary to update other languages.")

if __name__ == "__main__":
    main()
