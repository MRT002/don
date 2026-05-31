import xml.etree.ElementTree as ET
import requests


def get_all_podcast_episodes(rss_url):
    print("در حال دریافت فید کامل پادکست پرگار... (لطفاً چند ثانیه صبر کنید)")

    # دانلود فید RSS پادکست
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(rss_url, headers=headers)

    if response.status_code != 200:
        print(f"خطا در اتصال. کد خطا: {response.status_code}")
        return

    # پارس کردن فایل XML فید
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        print("خطا در خواندن اطلاعات پادکست.")
        return

    # پیدا کردن تمام آیتم‌ها (اپیزودها)
    channel = root.find("channel")
    if channel is None:
        print("ساختار پادکست یافت نشد.")
        return

    podcast_title = channel.find("title").text
    episodes = channel.findall("item")

    print(f"\n🎙️ نام پادکست: {podcast_title}")
    print(f"📊 تعداد کل اپیزودهای یافت شده: {len(episodes)}\n")

    # ذخیره در فایل متنی
    with open("podcast_titles.txt", "w", encoding="utf-8") as file:
        file.write(f"عنوان پادکست: {podcast_title}\n")
        file.write(f"تعداد کل اپیزودها: {len(episodes)}\n")
        file.write("-" * 80 + "\n\n")

        # حرکت از قدیمی‌ترین به جدیدترین یا بالعکس (اینجا به همان ترتیب فید است)
        for index, episode in enumerate(episodes, 1):
            title = episode.find("title").text
            pub_date = episode.find("pubDate").text[
                :16
            ]  # گرفتن تاریخ مختصر انتشار

            # پیدا کردن لینک فایل صوتی اپیزود
            enclosure = episode.find("enclosure")
            audio_link = (
                enclosure.get("url")
                if enclosure is not None
                else "لینکی یافت نشد"
            )

            # چاپ در کنسول برای تست
            print(f"{index}. [{pub_date}] {title}")
            print(f"   🔗 Link: {audio_link}\n")

            # نوشتن در فایل متنی
            file.write(f"{index}. [{pub_date}] {title}\n")
            file.write(f"   🔗 Link: {audio_link}\n\n")

    print("✅ تمام اپیزودها به همراه لینک در فایل 'podcast_titles.txt' ذخیره شدند.")


if __name__ == "__main__":
    # فید RSS رسمی پادکست پرگار بی‌بی‌سی
    PERGAR_RSS_URL = "https://podcasts.files.bbci.co.uk/p02pc9sn.rss"
    get_all_podcast_episodes(PERGAR_RSS_URL)
