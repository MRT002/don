import json
import requests


def get_podcast_episodes(podcast_id):
    # آدرس API رسمی اپل برای جستجوی پادکست بر اساس شناسه
    # مقدار limit=200 حداکثر تعداد اپیزودهای دریافتی در یک درخواست را مشخص می‌کند
    url = f"https://itunes.apple.com/lookup?id={podcast_id}&entity=podcastEpisode&limit=200"

    print("در حال برقراری ارتباط با اپل پادکست...")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if not results:
            print("هیچ اطلاعاتی یافت نشد.")
            return

        # آیتم اول در خروجی API معمولاً اطلاعات خود پادکست (کانال) است
        podcast_info = results[0]
        print(f"\n🎙️ نام پادکست: {podcast_info.get('collectionName')}")
        print(f"👤 سازنده: {podcast_info.get('artistName')}")
        print("-" * 50)

        # آیتم‌های بعدی اپیزودها هستند
        episodes = results[1:]
        print(f"تعداد اپیزودهای یافت شده: {len(episodes)}\n")

        # ذخیره عناوین در یک فایل متنی
        with open("podcast_titles.txt", "w", encoding="utf-8") as file:
            file.write(f"عنوان پادکست: {podcast_info.get('collectionName')}\n")
            file.write("-" * 50 + "\n")

            for index, episode in enumerate(episodes, 1):
                title = episode.get("trackName")
                pub_date = episode.get("releaseDate", "")[
                    :10
                ]  # فقط تاریخ (سال-ماه-روز)
                print(f"{index}. [{pub_date}] - {title}")

                # نوشتن در فایل
                file.write(f"{index}. [{pub_date}] - {title}\n")

        print("\n✅ تمام سرتیترها با موفقیت در فایل 'podcast_titles.txt' ذخیره شدند.")

    else:
        print(f"خطا در دریافت اطلاعات. کد خطا: {response.status_code}")


if __name__ == "__main__":
    # شناسه پادکست پرگار از روی لینکی که فرستادید استخراج شده: id634850665
    PODCAST_ID = "634850665"
    get_podcast_episodes(PODCAST_ID)
