"""
Video Downloader Web Application
Flask-based web interface for downloading videos with i18n support
Made by WITHYM
"""

import os
import sys
import uuid
import json
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, session, Response
from werkzeug.utils import secure_filename

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller.DouyinExtract import download_tiktok_douyin_video
from controller.ThreadsExtract import download_threads_video, ThreadsDownloadError
import subprocess

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
app.config['DOWNLOAD_FOLDER'] = '/tmp/downloads' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', 'C:\\temp'), 'downloads')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['LOCALES_FOLDER'] = os.path.join(os.path.dirname(__file__), 'locales')
app.config['CONFIG_FOLDER'] = os.path.join(os.path.dirname(__file__), 'config')

# Create download folder
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Language configuration
SUPPORTED_LANGUAGES = [
    {'code': 'ko', 'name': '한국어', 'flag': '🇰🇷'},
    {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
    {'code': 'ja', 'name': '日本語', 'flag': '🇯🇵'},
    {'code': 'zh-CN', 'name': '简体中文', 'flag': '🇨🇳'},
    {'code': 'zh-TW', 'name': '繁體中文', 'flag': '🇹🇼'},
    {'code': 'es', 'name': 'Español', 'flag': '🇪🇸'},
    {'code': 'fr', 'name': 'Français', 'flag': '🇫🇷'},
    {'code': 'de', 'name': 'Deutsch', 'flag': '🇩🇪'},
    {'code': 'it', 'name': 'Italiano', 'flag': '🇮🇹'},
    {'code': 'pt', 'name': 'Português', 'flag': '🇵🇹'},
    {'code': 'ru', 'name': 'Русский', 'flag': '🇷🇺'},
    {'code': 'ar', 'name': 'العربية', 'flag': '🇸🇦'},
    {'code': 'hi', 'name': 'हिन्दी', 'flag': '🇮🇳'},
    {'code': 'th', 'name': 'ไทย', 'flag': '🇹🇭'},
    {'code': 'vi', 'name': 'Tiếng Việt', 'flag': '🇻🇳'},
    {'code': 'id', 'name': 'Indonesia', 'flag': '🇮🇩'},
    {'code': 'tr', 'name': 'Türkçe', 'flag': '🇹🇷'},
    {'code': 'pl', 'name': 'Polski', 'flag': '🇵🇱'},
    {'code': 'nl', 'name': 'Nederlands', 'flag': '🇳🇱'},
    {'code': 'sv', 'name': 'Svenska', 'flag': '🇸🇪'},
]

DEFAULT_LANGUAGE = 'en'

# Cache for translations and configs
translations_cache = {}
config_cache = {}

def load_config(config_name):
    """Load configuration file"""
    if config_name in config_cache:
        return config_cache[config_name]

    config_file = os.path.join(app.config['CONFIG_FOLDER'], f'{config_name}.json')

    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        return {{}}

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            config_cache[config_name] = config
            return config
    except Exception as e:
        print(f"Error loading config {config_name}: {e}")
        return {{}}

def load_translation(lang_code):
    """Load translation file for given language"""
    if lang_code in translations_cache:
        return translations_cache[lang_code]

    locale_file = os.path.join(app.config['LOCALES_FOLDER'], f'{lang_code}.json')

    if not os.path.exists(locale_file):
        # Fallback to default language
        lang_code = DEFAULT_LANGUAGE
        locale_file = os.path.join(app.config['LOCALES_FOLDER'], f'{lang_code}.json')

    try:
        with open(locale_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            translations_cache[lang_code] = translations
            return translations
    except Exception as e:
        print(f"Error loading translation {lang_code}: {e}")
        return {{}}

def get_user_language():
    """Get user's preferred language from session or browser"""
    # Check session
    if 'lang' in session:
        return session['lang']

    # Check Accept-Language header
    lang = request.accept_languages.best_match([l['code'] for l in SUPPORTED_LANGUAGES])

    return lang or DEFAULT_LANGUAGE

def detect_platform(url):
    """Detect video platform from URL"""
    url_lower = url.lower()

    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "douyin.com" in url_lower:
        return "douyin"
    elif "threads.net" in url_lower or "threads.com" in url_lower:
        return "threads"
    else:
        return None

def download_youtube_video(url, output_dir):
    """Download YouTube video using yt-dlp"""
    try:
        output_template = os.path.join(output_dir, "%(title)s_%(id)s.%(ext)s")

        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", output_template,
            "--no-playlist",
            "--merge-output-format", "mp4",
            "--restrict-filenames",
            url
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300
        )

        stdout_str = result.stdout.decode('utf-8', errors='replace')
        stderr_str = result.stderr.decode('utf-8', errors='replace')

        if result.returncode == 0:
            # Try to find the filename from yt-dlp's output
            import re
            output_lines = stdout_str.splitlines()
            for line in output_lines:
                if "[Merger] Merging formats into" in line:
                    match = re.search(r'Merging formats into "(.*)"', line)
                    if match:
                        return match.group(1)
                elif "[download] Destination:" in line:
                    match = re.search(r'Destination: (.*)', line)
                    if match:
                        return match.group(1)

            # Fallback for already downloaded files
            for line in output_lines:
                if "[download]" in line and "has already been downloaded" in line:
                    match = re.search(r'\[download\] (.*) has already been downloaded', line)
                    if match:
                        return os.path.join(output_dir, match.group(1))

            # Fallback to glob if parsing fails
            import glob
            files = glob.glob(os.path.join(output_dir, "*.mp4"))
            if files:
                return max(files, key=os.path.getctime)
        else:
            print(f"yt-dlp stdout: {result.stdout}")
            print(f"yt-dlp stderr: {result.stderr}")

        return None

    except subprocess.TimeoutExpired:
        raise Exception("YouTube download timeout")
    except FileNotFoundError:
        raise Exception("yt-dlp not installed")
    except Exception as e:
        raise Exception(f"YouTube download failed: {str(e)}")

@app.route('/')
def index():
    """Main page"""
    lang = get_user_language()
    translations = load_translation(lang)
    adsense_config = load_config('adsense')
    analytics_config = load_config('analytics')
    ads_config = load_config('ads')

    return render_template(
        'index.html',
        translations=translations,
        languages=SUPPORTED_LANGUAGES,
        current_lang=lang,
        adsense=adsense_config,
        analytics=analytics_config,
        ads=ads_config
    )

@app.route('/api/set-language', methods=['POST'])
def set_language():
    """Set user language preference"""
    data = request.get_json()
    lang = data.get('lang', DEFAULT_LANGUAGE)

    if lang in [l['code'] for l in SUPPORTED_LANGUAGES]:
        session['lang'] = lang
        return jsonify({'success': True, 'lang': lang})

    return jsonify({'error': 'Invalid language'}), 400

@app.route('/api/translations/<lang_code>')
def get_translations(lang_code):
    """Get translations for a specific language"""
    translations = load_translation(lang_code)
    return jsonify(translations)

@app.route('/api/download', methods=['POST'])
def download():
    """Download video endpoint"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        if not url:
            lang = get_user_language()
            translations = load_translation(lang)
            return jsonify({'error': translations.get('error_url_required', 'URL is required')}), 400

        if not url.startswith('http'):
            return jsonify({'error': 'Invalid URL'}), 400

        # Detect platform
        platform = detect_platform(url)
        if not platform:
            return jsonify({'error': 'Unsupported platform'}), 400

        # Create unique download directory
        download_id = str(uuid.uuid4())
        download_dir = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
        os.makedirs(download_dir, exist_ok=True)

        filepath = None

        try:
            if platform == "youtube":
                filepath = download_youtube_video(url, download_dir)

            elif platform in ["tiktok", "douyin"]:
                filepath = download_tiktok_douyin_video(url)
                if filepath and os.path.exists(filepath):
                    # Move to download dir
                    new_path = os.path.join(download_dir, os.path.basename(filepath))
                    shutil.move(filepath, new_path)
                    filepath = new_path

            elif platform == "threads":
                filepath = download_threads_video(url, download_dir)

            if not filepath or not os.path.exists(filepath):
                raise Exception("Download failed - no file created")

            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)

            return jsonify({
                'success': True,
                'platform': platform,
                'filename': filename,
                'size': file_size,
                'download_id': download_id,
                'download_url': f'/api/file/{download_id}/{filename}'
            })

        except ThreadsDownloadError as e:
            shutil.rmtree(download_dir, ignore_errors=True)
            return jsonify({'error': f'Threads error: {str(e)}'}), 500

        except Exception as e:
            shutil.rmtree(download_dir, ignore_errors=True)
            raise e

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file/<download_id>/<filename>')
def download_file(download_id, filename):
    """Download file endpoint"""
    try:
        # Secure the filename
        filename = secure_filename(filename)
        download_dir = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
        filepath = os.path.join(download_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        # Send file and cleanup after
        def cleanup():
            try:
                shutil.rmtree(download_dir, ignore_errors=True)
            except:
                pass

        # Schedule cleanup (will happen after file is sent)
        response = send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )

        # Note: In production, use a background task to cleanup
        # For now, files will be cleaned up manually or via cron

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'video-downloader',
        'languages': len(SUPPORTED_LANGUAGES)
    })

@app.route('/api/languages')
def languages():
    """List supported languages"""
    return jsonify({
        'languages': SUPPORTED_LANGUAGES,
        'default': DEFAULT_LANGUAGE
    })

@app.route('/api/platforms')
def platforms():
    """List supported platforms"""
    return jsonify({
        'platforms': [
            {'id': 'youtube', 'name': 'YouTube', 'types': ['videos', 'shorts']},
            {'id': 'tiktok', 'name': 'TikTok', 'types': ['videos']},
            {'id': 'douyin', 'name': 'Douyin', 'types': ['videos']},
            {'id': 'threads', 'name': 'Threads', 'types': ['videos', 'images']},
        ]
    })

@app.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    return send_file(
        os.path.join(os.path.dirname(__file__), 'static', 'robots.txt'),
        mimetype='text/plain'
    )

@app.route('/ads.txt')
def ads():
    """Serve ads.txt for Google AdSense verification"""
    ads_txt_path = os.path.join(os.path.dirname(__file__), 'static', 'ads.txt')
    try:
        with open(ads_txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        # For debugging, you might want to log this error
        print(f"ads.txt not found at {ads_txt_path}")
        return Response("Not Found", status=404, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml"""
    from flask import make_response
    from datetime import datetime

    # Get base URL from environment or request
    base_url = os.environ.get('BASE_URL', request.url_root.rstrip('/'))

    # Build sitemap XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append(' xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    today = datetime.now().strftime('%Y-%m-%d')

    # Add homepage for each language
    for lang in SUPPORTED_LANGUAGES:
        lang_code = lang['code']

        # Main page URL
        if lang_code == DEFAULT_LANGUAGE:
            url = base_url + '/'
        else:
            url = base_url + f'/?lang={lang_code}'

        xml.append('  <url>')
        xml.append(f'    <loc>{url}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>1.0</priority>')

        # Add alternate language links
        for alt_lang in SUPPORTED_LANGUAGES:
            alt_code = alt_lang['code']
            if alt_code == DEFAULT_LANGUAGE:
                alt_url = base_url + '/'
            else:
                alt_url = base_url + f'/?lang={alt_code}'

            xml.append(f'    <xhtml:link rel="alternate" hreflang="{alt_code}" href="{alt_url}"/>')

        xml.append('  </url>')

    # Add API documentation endpoints
    api_endpoints = ['/api/platforms', '/api/languages', '/api/health']
    for endpoint in api_endpoints:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{endpoint}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append('    <priority>0.5</priority>')
        xml.append('  </url>')

    xml.append('</urlset>')

    response = make_response('\n'.join(xml))
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response

# Cleanup old files (run periodically in production)
def cleanup_old_downloads():
    """Remove downloads older than 1 hour"""
    import time
    download_folder = app.config['DOWNLOAD_FOLDER']

    if not os.path.exists(download_folder):
        return

    current_time = time.time()
    for item in os.listdir(download_folder):
        item_path = os.path.join(download_folder, item)
        if os.path.isdir(item_path):
            # Check if folder is older than 1 hour
            if current_time - os.path.getctime(item_path) > 3600:
                shutil.rmtree(item_path, ignore_errors=True)

if __name__ == '__main__':
    # Run cleanup before starting
    cleanup_old_downloads()

    # Get port from environment (Cloud Run uses PORT env var)
    port = int(os.environ.get('PORT', 8080))

    # Run app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )