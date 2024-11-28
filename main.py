import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://pilkada2024.kpu.go.id/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def download_image(image_url, save_path):
    if os.path.exists(save_path):
        print(f"Skip: Gambar sudah ada - {save_path}")
        return

    try:
        response = requests.get(image_url, headers=HEADERS, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Gambar berhasil diunduh: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {image_url}: {e}")

def display_choices(data, level_name):
    print(f"\nPilih salah satu {level_name}:")
    for idx, item in enumerate(data, start=1):
        print(f"{idx}. {item['nama']}")
    
    while True:
        try:
            choice = int(input(f"Masukkan nomor pilihan {level_name}: "))
            if 1 <= choice <= len(data):
                return data[choice - 1]
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan angka yang valid.")

def create_folder(folder_name, parent_folder=None):
    folder_path = folder_name if not parent_folder else os.path.join(parent_folder, folder_name)
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' berhasil dibuat.")
        else:
            print(f"Folder '{folder_path}' sudah ada.")
        return folder_path
    except OSError as e:
        print(f"Gagal membuat folder: {e}")
        return None

def download_tps_images(tps_data, prov_code, city_code, district_code, village_code, tps_base_url, village_folder):
    tps_name = tps_data['nama']
    tps_code = tps_data['kode']

    tps_folder = create_folder(tps_name, parent_folder=village_folder)

    tps_url = f"{tps_base_url}/{prov_code}/{city_code}/{district_code}/{village_code}/{tps_code}.json"
    tps_detail = fetch_data(tps_url)

    if not tps_detail or 'images' not in tps_detail:
        print(f"Skip: Tidak ada gambar untuk TPS {tps_name}.")
        return

    for image_url in tps_detail['images']:
        image_name = os.path.basename(image_url)
        save_path = os.path.join(tps_folder, image_name)
        download_image(image_url, save_path)

def main():
    base_url = "https://sirekappilkada-obj-data.kpu.go.id/wilayah/pilkada/pkwkp"
    tps_base_url = "https://sirekappilkada-obj-data.kpu.go.id/pilkada/hhcw/pkwkp"

    prov_url = f"{base_url}/0.json"
    provinces_data = fetch_data(prov_url)

    if not provinces_data:
        return

    chosen_province = display_choices(provinces_data, "provinsi")
    prov_name = chosen_province['nama']
    prov_code = chosen_province['kode']

    prov_folder = create_folder(prov_name)

    city_url = f"{base_url}/{prov_code}.json"
    cities_data = fetch_data(city_url)

    if not cities_data:
        return

    chosen_city = display_choices(cities_data, "kota")
    city_name = chosen_city['nama']
    city_code = chosen_city['kode']

    city_folder = create_folder(city_name, parent_folder=prov_folder)

    district_url = f"{base_url}/{prov_code}/{city_code}.json"
    districts_data = fetch_data(district_url)

    if not districts_data:
        return

    chosen_district = display_choices(districts_data, "kecamatan")
    district_name = chosen_district['nama']
    district_code = chosen_district['kode']

    district_folder = create_folder(district_name, parent_folder=city_folder)

    village_url = f"{base_url}/{prov_code}/{city_code}/{district_code}.json"
    villages_data = fetch_data(village_url)

    if not villages_data:
        return

    chosen_village = display_choices(villages_data, "kelurahan")
    village_name = chosen_village['nama']
    village_code = chosen_village['kode']

    village_folder = create_folder(village_name, parent_folder=district_folder)

    tps_url = f"{base_url}/{prov_code}/{city_code}/{district_code}/{village_code}.json"
    tps_data = fetch_data(tps_url)

    if not tps_data:
        return

    print(f"\nMengunduh semua gambar TPS di {village_name} menggunakan multithreading...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_tps_images, tps, prov_code, city_code, district_code, village_code, tps_base_url, village_folder)
            for tps in tps_data
        ]

        for future in as_completed(futures):
            future.result()

    print("\nProses selesai. Semua gambar TPS telah diunduh.")

if __name__ == "__main__":
    main()
