import os
from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# Define the path to save the downloaded files
save_path = os.path.join(os.getcwd(), 'downloads', '%(title)s.%(ext)s')

@app.route('/')
def home():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    # Get the URL from the form
    url = request.form.get('url')

    # yt-dlp options to fetch video and audio formats
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            audio_formats = [f for f in formats if f.get('vcodec') == 'none']
            video_formats = [f for f in formats if f.get('acodec') == 'none']
    except Exception as e:
        return jsonify({'error': str(e)})

    # Return the available formats as JSON
    return jsonify({
        'audio_formats': [{'format': f['format_note'], 'url': f['url']} for f in audio_formats],
        'video_formats': [{'format': f['format_note'], 'url': f['url']} for f in video_formats],
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)