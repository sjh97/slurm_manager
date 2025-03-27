import time

def main():
    print("Hello world")
    time.sleep(10)
    print("Bye world")

def read_txt(path1, path2):
    with open(path1, 'r') as file:
        print(file.read())
    with open(path2, 'r') as file:
        print(file.read())

if __name__ == "__main__":
    main()