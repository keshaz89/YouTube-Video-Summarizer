import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, BartTokenizer
import yt_dlp

# Initialize summarizer and tokenizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"Error fetching transcript: {e}"

def summarize_text(text):
    max_token_limit = 1024
    max_chunk_length = max_token_limit - 50
    tokens = tokenizer.encode(text, truncation=True)
    summaries = []
    
    for i in range(0, len(tokens), max_chunk_length):
        chunk_tokens = tokens[i:i + max_chunk_length]
        chunk = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        try:
            summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            summaries.append(f"Error during summarization of chunk: {e}")
    return " ".join(summaries)

def get_video_info(video_url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', 'No title found')
            thumbnail_url = info_dict.get('thumbnail', None)
            return title, thumbnail_url
    except Exception as e:
        st.error(f"Error retrieving video info: {e}")
        return None, None

def main():
    st.title("YouTube Video Summarizer")
    
    video_url = st.text_input("Enter YouTube Video URL:", key="video_input")
    
    if st.button("Summarize"):
        if video_url:
            title, thumbnail_url = get_video_info(video_url)
            if title and thumbnail_url:
                st.image(thumbnail_url, caption=title, use_column_width=True)
                st.subheader(title)
                
                video_id = video_url.split("v=")[-1].split("&")[0]
                transcript = get_transcript(video_id)
                
                if "Error" not in transcript:
                    summary = summarize_text(transcript)

                    st.subheader("Summary")
                    st.write(summary)

                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(transcript)
            else:
                st.error("Could not retrieve video title and thumbnail. Please check the URL.")
        else:
            st.error("Please enter a valid YouTube video URL.")

if __name__ == "__main__":
    main()