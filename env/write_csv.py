import csv
def write_csv(ads):
    with open('results.csv', 'a+', encoding='utf-8') as f:
        fields = ['title', 'price', 'link', 'site']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)