A Streamlit web app that summarizes YouTube videos using their transcripts and Hugging Face's BART model.

## Features
- Extracts transcript from YouTube videos
- Summarizes using a transformer-based model (BART)
- Displays video title and thumbnail
- Provides downloadable summary

## Technologies Used
- Streamlit  
- YouTube Transcript API  
- yt-dlp  
- Hugging Face Transformers  
- BART model (`facebook/bart-large-cnn`)  
- PyTorch  

## Installation
1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer
```
2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
3. **Run the Application**
```bash
streamlit run final.py
```

## Demo
https://github.com/user-attachments/assets/1aa84d27-f8e7-4a0d-90aa-67f56843cfe5

