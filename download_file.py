import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

save_dir = r"D:\Solar"
os.makedirs(save_dir, exist_ok=True)

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# 날짜별로 mp4 파일이 저장된 디렉토리 URL 패턴 (예시)
# 실제 경로와 파일명 패턴은 사이트에서 확인 후 수정 필요!
list_url_pattern = "https://sdo.oma.be/movies/{year}/{month:02d}/{day:02d}/"

date = start_date
while date <= end_date:
    list_url = list_url_pattern.format(year=date.year, month=date.month, day=date.day)
    try:
        resp = requests.get(list_url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            mp4_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.mp4')]
            if mp4_links:
                # 첫 번째 mp4 파일만 다운로드
                mp4_url = list_url + mp4_links[0]
                filename = os.path.join(save_dir, mp4_links[0])
                mp4_resp = requests.get(mp4_url, stream=True)
                if mp4_resp.status_code == 200:
                    with open(filename, 'wb') as f:
                        for chunk in mp4_resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {mp4_url}")
            else:
                print(f"No mp4 files found for {date.strftime('%Y-%m-%d')}")
        else:
            print(f"Directory not found: {list_url}")
    except Exception as e:
        print(f"Error on {date.strftime('%Y-%m-%d')}: {e}")
    date += timedelta(days=1)
