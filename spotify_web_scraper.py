import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id = SPOTIFY_CLIENT_ID,
    client_secret = SPOTIFY_CLIENT_SECRET
))

def fetch_playlist():
    playlist_link = entry.get()
    if not playlist_link:
        messagebox.showerror("Error", "Please enter a playlist URL!")
        return
    
    try:
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        results = sp.playlist_tracks(playlist_URI)
        
        songs_data = []
        for item in results['items']:
            track = item['track']
            songs_data.append({
                'Song Name': track['name'],
                'Artist': track['artists'][0]['name'],
                'Album': track['album']['name'],
                'Duration (min)': round(track['duration_ms'] / 60000, 2),
                'Popularity': track['popularity']
            })
        
        df = pd.DataFrame(songs_data)
        display_results(df)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

def display_results(df):
    global playlist_df
    playlist_df = df
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, df.to_string(index=False))
    plot_chart(df)

def plot_chart(df):
    artist_counts = df['Artist'].value_counts().head(5)
    plt.figure(figsize=(6,4))
    artist_counts.plot(kind='bar', color='skyblue')
    plt.title("Top 5 Artists in Playlist")
    plt.xlabel("Artist")
    plt.ylabel("Number of Songs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def save_csv():
    if 'playlist_df' not in globals():
        messagebox.showerror("Error", "No playlist data to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if file_path:
        playlist_df.to_csv(file_path, index=False)
        messagebox.showinfo("Saved", f"Playlist saved to {file_path}")

root = tk.Tk()
root.title("🎵 Spotify Playlist Analyzer")
root.geometry("650x500")
root.configure(bg="#f2f2f2")

title = tk.Label(root, text="Spotify Playlist Analyzer", font=("Arial Rounded MT Bold", 20), bg="#f2f2f2", fg="#1DB954")
title.pack(pady=10)

entry_frame = tk.Frame(root, bg="#f2f2f2")
entry_frame.pack(pady=5)

entry_label = tk.Label(entry_frame, text="Enter Playlist URL:", font=("Arial", 12), bg="#f2f2f2")
entry_label.grid(row=0, column=0, padx=5)

entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
entry.grid(row=0, column=1, padx=5)

fetch_btn = tk.Button(root, text="Fetch Playlist", font=("Arial", 12), bg="#1DB954", fg="white", command=fetch_playlist)
fetch_btn.pack(pady=10)

text_box = tk.Text(root, wrap="word", width=70, height=15, font=("Courier", 10))
text_box.pack(pady=5)

save_btn = tk.Button(root, text="💾 Save as CSV", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_csv)
save_btn.pack(pady=5)

root.mainloop()
