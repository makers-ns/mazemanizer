from servo import Servo

def main():
    s = Servo()

    s.starting_position()
    print("start")

    s.using_keys()
    s.cleanup()

if __name__ == "__main__":
    main()
