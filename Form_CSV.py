import csv

CSV_PATH = 'products_with_price.csv'

def write_in_file(filename, data_matrix):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter = ";")
        writer.writerow(["Articul", "Name", "Short description", "Image", "Description", "Adv image", "Price", "Adv price", "Documents", "", "", "Categories", "Group", "Brand"])
        writer.writerows(data_matrix)

def Pick_color_name_uplast(filename_csv_input):
    with open(filename_csv_input) as file:
        input = csv.reader(file, delimiter=',')
        print(input)
        for row in input:
            product = row[1]

            color = product[product.find('—')+2:]
            new_color = color
            if color[-2:] == 'ая' and color[-3] != 'к':
                new_color = color[:-2] + 'ый'
            elif (color[-2:] == 'яя' or color[-3] == 'к') and len(color.split(' ')) == 1:
                new_color = color[:-2] + 'ий'

            print(new_color)


def Make_full_category(filename_csv_input):
    with open(filename_csv_input) as file:
        input = csv.reader(file, delimiter=',')
        print(input)
        for row in input:
            category = row[11]

            if category == 'Аксессуары':
                full_category = 'Все комплектующие>Комплектация сайдинг Ю-пласт'
            else:
                full_category = category + ">Ю-Пласт"
            print(full_category)

if __name__ == '__main__':
    Pick_color_name_uplast(CSV_PATH)
    #Make_full_category(CSV_PATH)