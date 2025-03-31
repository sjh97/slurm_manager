import time
import random

def main():
    print("Hello world")
    time.sleep(10)
    print("Bye world")

def read_txt(path1, path2):
    with open(path1, 'r') as file:
        print(file.read())
    with open(path2, 'r') as file:
        print(file.read())

def delay():
    seconds = random.randint(5, 10)
    print(f"Delaying for {seconds} seconds...")
    time.sleep(seconds)
    print("Delay complete.")

if __name__ == "__main__":
    main()