import os, shutil

KILO_BYTES = 1_000
MEGA_BYTES = 1_000_000
GIGA_BYTES = 1_000_000_000

# os.chdir('module/root_folder')

print("Input the command ")


def mass_rm(extension, file_lst):
    is_there_ex = False

    for file in file_lst:
        if file.endswith(extension):
            is_there_ex = True
            os.remove(file)

    if not is_there_ex:
        print(f"File extension {extension} not found in this directory")


def mass_cp(extension, file_lst, dst_path):
    is_there_ex = False

    for file in file_lst:
        if file.endswith(extension):
            is_there_ex = True
            if os.path.exists(f"{dst_path}/{file}"):
                while True:
                    answer = input(f"{file} already exists in this directory. Replace? (y/n) ")
                    if answer == 'y':
                        shutil.copy(file, dst_path)
                        break
                    elif answer == 'n':
                        break
            else:
                shutil.copy(file, dst_path)


    if not is_there_ex:
        print(f"File extension {extension} not found in this directory")


def mass_mv(extension, file_lst, dst_path):
    is_there_ex = False

    for file in file_lst:
        if file.endswith(extension):
            is_there_ex = True
            if os.path.exists(f"{dst_path}/{file}"):
                while True:
                    answer = input(f"{file} already exists in this directory. Replace? (y/n) ")
                    if answer == 'y':
                        shutil.copy(file, dst_path)
                        os.remove(file)
                        break
                    elif answer == 'n':
                        break
            else:
                shutil.move(file, dst_path)

    if not is_there_ex:
        print(f"File extension {extension} not found in this directory")


def pwd():
    print(os.getcwd())


def sort_lst(lst):
    dir_lst = []
    file_lst = []

    for file in lst:
        if os.path.isdir(f"./{file}"):
            dir_lst.append(file)
        else:
            file_lst.append(file)

    dir_lst.sort()
    file_lst.sort()

    return dir_lst + file_lst


while True:

    command = input()

    file_list = os.listdir()

    try:

        if command == 'pwd':
            pwd()

        elif command == 'cd ..':
            os.chdir(f'./..')
            pwd()

        elif command[:3] == 'cd ':
            os.chdir(command[3:])
            pwd()

        elif command == 'quit':
            break

        elif command == 'ls':
            for file in sort_lst(file_list):
                print(file)

        elif command == 'ls -l':
            for file in sort_lst(file_list):

                if os.path.isdir(f"./{file}"):
                    print(file)
                else:
                    print(file, os.stat(file).st_size)

        elif command == 'ls -lh':

            for file in sort_lst(file_list):
                file_size = os.stat(file).st_size

                if os.path.isdir(f"./{file}"):
                    print(file)
                else:
                    if file_size > KILO_BYTES:
                        print(file, f"{round(file_size / KILO_BYTES)}KB")
                    elif file_size > MEGA_BYTES:
                        print(file, f"{round(file_size / MEGA_BYTES)}MB")
                    elif file_size > GIGA_BYTES:
                        print(file, f"{round(file_size / GIGA_BYTES)}GB")
                    else:
                        print(file, f"{file_size}B")

        elif command[:3] == 'rm ' or command == 'rm':
            file_name = command[3:]

            if file_name.startswith('.') and len(file_name) >= 2:
                mass_rm(file_name, file_list)
            elif os.path.isdir(file_name) and len(file_name) > 0 and not file_name.startswith('.'):
                shutil.rmtree(file_name)
            elif len(file_name) > 0 and not file_name.startswith('.'):
                os.remove(file_name)
            else:
                print("Specify the file or directory")


        elif command[:3] == 'mv ' or command == 'mv':
            full_path = command[3:].split()

            try:
                src_path = full_path[0]
                dst_path = full_path[1]

                if len(full_path) > 2:
                    print("Specify the current name of the file or directory and the new location and/or name")
                elif os.path.isfile(dst_path) and os.path.exists(dst_path):
                    print("The file or directory already exists")
                elif src_path.startswith('.') and len(src_path) >= 2:
                    mass_mv(src_path, file_list, dst_path)
                else:
                    shutil.move(src_path, dst_path)

            except IndexError:
                print("Specify the current name of the file or directory and the new location and/or name")

        elif command[:6] == 'mkdir ' or command == 'mkdir':

            dir_name = command[6:]

            if len(dir_name) > 0:
                os.mkdir(dir_name)
            else:
                print("Specify the name of the directory to be made")


        elif command[:3] == 'cp ' or command == 'cp':
            full_path = command[3:].split()

            try:
                src_path = full_path[0]
                dst_path = full_path[1]

                if len(full_path) > 2:
                    print("Specify the current name of the file or directory and the new location and/or name")
                elif not os.path.exists(dst_path):
                    print("No such file or directory")
                elif src_path.count('/') > 0 or dst_path.count('/') > 0:
                    file_name = src_path.split("/")[-1]
                    if os.path.exists(f"{dst_path}/{file_name}"):
                        print(f"{file_name} already exists in this directory")
                    else:
                        shutil.copy(src_path, dst_path)
                elif os.path.exists(f"{dst_path}/{src_path}"):
                    print(f"{src_path} already exists in this directory")
                elif src_path.startswith('.') and len(src_path) >= 2:
                    mass_cp(src_path, file_list, dst_path)
                else:
                    shutil.copy(src_path, dst_path)

            except IndexError:
                print("Specify the file")
        else:
            print("\nInvalid command")


    except FileNotFoundError:
        print("No such file or directory")
    except shutil.Error:
        print("The file or directory already exists")
    except FileExistsError:
        print("The directory already exists")