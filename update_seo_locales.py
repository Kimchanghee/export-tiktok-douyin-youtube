#!/usr/bin/env python3
"""
Utility script to backfill SEO + FAQ blocks for locale files.
Only runs for locales missing the `seo` field.
"""

import json
from pathlib import Path


SEO_DATA = {
    "ja": {
        "seo": {
            "title": "無料動画ダウンローダー - TikTok、Douyin、Threads、Twitter、Instagram ダウンロード 2025",
            "description": "TikTok、Douyin、Threads、Twitter、Instagramから無料で高画質動画をダウンロード。ウォーターマークなしで高速かつ安全。ログイン不要・無制限ダウンロード対応。",
            "keywords": "動画ダウンローダー, TikTokダウンロード, Douyinダウンロード, Threadsダウンロード, Twitterダウンロード, Instagramダウンロード, 無料動画保存, ウォーターマーク削除, HD動画",
            "og_title": "無料動画ダウンローダー - TikTok · Threads · Douyin · Twitter · Instagram",
            "og_description": "ウォーターマークなしで無料ダウンロード。高速で安全なオンラインツール。"
        },
        "faq": [
            {
                "question": "この動画ダウンローダーは無料ですか？",
                "answer": "はい、完全に無料です。隠れた費用や購読料はなく、無制限に動画をダウンロードできます。"
            },
            {
                "question": "どのプラットフォームに対応していますか？",
                "answer": "TikTok、Douyin、Threads、Twitter/X、Instagramに対応しています。さらに多くのプラットフォームを準備中です。"
            },
            {
                "question": "ダウンロードした動画にウォーターマークは付きますか？",
                "answer": "プラットフォームによります。可能な場合はウォーターマークなしのバージョンを提供し、常に最高画質でダウンロードします。"
            },
            {
                "question": "動画をダウンロードするのにログインは必要ですか？",
                "answer": "いいえ、ログインやサインアップは不要です。動画URLを貼り付けるだけですぐにダウンロードを開始できます。"
            },
            {
                "question": "ダウンロード回数に制限はありますか？",
                "answer": "ありません。好きなだけ動画をダウンロードできます。"
            },
            {
                "question": "モバイルでも使用できますか？",
                "answer": "はい、モバイルブラウザでも完全に動作し、iOSとAndroidの両方に対応しています。"
            }
        ]
    },
    "zh-CN": {
        "seo": {
            "title": "免费视频下载器 - 下载TikTok、抖音、Threads、Twitter、Instagram 2025",
            "description": "从TikTok、抖音、Threads、Twitter和Instagram免费下载高清视频。快速、安全、简单的在线视频下载工具。无水印、无需登录、无限下载。",
            "keywords": "视频下载器, TikTok下载, Douyin下载, Threads下载, Twitter下载, Instagram下载, 免费保存视频, 去除水印, 高清视频",
            "og_title": "免费视频下载器 - TikTok · Threads · 抖音 · Twitter · Instagram",
            "og_description": "免费视频下载，无水印，快速安全的在线工具。"
        },
        "faq": [
            {
                "question": "这个视频下载器免费吗？",
                "answer": "是的，完全免费。没有隐藏费用或订阅，可以无限制下载视频。"
            },
            {
                "question": "支持哪些平台？",
                "answer": "我们支持TikTok、抖音、Threads、Twitter/X和Instagram。更多平台即将推出。"
            },
            {
                "question": "下载的视频有水印吗？",
                "answer": "这取决于平台。在可能的情况下，我们提供无水印版本，始终以最高质量下载。"
            },
            {
                "question": "下载视频需要登录吗？",
                "answer": "不需要，无需登录或注册。只需粘贴视频URL即可立即开始下载。"
            },
            {
                "question": "下载次数有限制吗？",
                "answer": "没有限制。您可以随时下载任意数量的视频。"
            },
            {
                "question": "可以在手机上使用吗？",
                "answer": "当然可以，在移动浏览器上运行良好，完全支持iOS和Android。"
            }
        ]
    },
    "es": {
        "seo": {
            "title": "Descargador de Videos Gratis - TikTok, Douyin, Threads, Twitter, Instagram 2025",
            "description": "Descarga videos de alta calidad de TikTok, Douyin, Threads, Twitter e Instagram gratis. Descargador online rápido, seguro y fácil. Sin marca de agua, sin inicio de sesión, descargas ilimitadas.",
            "keywords": "descargador de videos, descargar tiktok, descargar threads, descargar twitter, descargar instagram, descargar douyin, guardar video gratis, quitar marca de agua, video HD",
            "og_title": "Descargador de Videos Gratis - TikTok · Threads · Douyin · Twitter · Instagram",
            "og_description": "Descarga videos gratis sin marcas de agua. Herramienta en línea rápida y segura."
        },
        "faq": [
            {
                "question": "¿Este descargador de videos es gratis?",
                "answer": "Sí, es completamente gratis. Sin costos ocultos ni suscripciones, y puedes descargar videos ilimitados."
            },
            {
                "question": "¿Qué plataformas son compatibles?",
                "answer": "Admitimos TikTok, Douyin, Threads, Twitter/X e Instagram. Pronto habrá más plataformas."
            },
            {
                "question": "¿Los videos descargados tienen marcas de agua?",
                "answer": "Depende de la plataforma. Cuando es posible, proporcionamos versiones sin marca de agua y siempre descargamos en la máxima calidad disponible."
            },
            {
                "question": "¿Necesito iniciar sesión para descargar videos?",
                "answer": "No, no necesitas iniciar sesión ni registrarte. Solo pega la URL del video y comienza a descargar de inmediato."
            },
            {
                "question": "¿Hay un límite en las descargas?",
                "answer": "Sin límites. Puedes descargar tantos videos como quieras, cuando quieras."
            },
            {
                "question": "¿Puedo usarlo en móvil?",
                "answer": "Sí, funciona perfectamente en navegadores móviles. Totalmente compatible con iOS y Android."
            }
        ]
    }
}


def update_locale_file(lang_code: str) -> bool:
    """Update a single locale file with SEO data if missing."""
    path = Path("web/locales") / f"{lang_code}.json"
    if not path.exists():
        print(f"[MISS] {path} not found")
        return False

    data = json.loads(path.read_text(encoding="utf-8"))
    if "seo" in data:
        print(f"[SKIP] {lang_code}.json already has SEO data")
        return False

    seo_payload = SEO_DATA.get(lang_code)
    if not seo_payload:
        print(f"[SKIP] No SEO template for {lang_code}")
        return False

    data["seo"] = seo_payload["seo"]
    data["faq"] = seo_payload["faq"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK]   Updated {lang_code}.json")
    return True


def main() -> None:
    updated = sum(update_locale_file(code) for code in SEO_DATA)
    print(f"\nDone. Updated {updated} locale files.")


if __name__ == "__main__":
    main()
