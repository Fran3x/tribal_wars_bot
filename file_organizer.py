#modifies the file with village info


def open_file():
        return open("C:/Users/Franex/Desktop/plemiona_bot/village_info.txt", "r+")

def file_to_array(file):
        array = []
        data = file.readlines()
        #print("data", data)
        for line in data:
                #print("B", line)
                array.append(line)
        return array


def village_in_the_file(array, this_village):
        for village in array:
                if this_village in village:
                        print("JEST JUZ")
                        return True
        return False


def add_village_to_file(file, x):
        if file != "":
                file.write("\n")
        file.write(f"{x}")

def sort_distance():
        pass

def close_file(file):
        file.close()

