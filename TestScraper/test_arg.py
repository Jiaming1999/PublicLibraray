import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('num1', help='Search the database')
    parser.add_argument('num2', help='Search the database')
    parser.add_argument('num3', help='Search the database')
    parser.add_argument('-s', '--search', help='Search the database')
    args = parser.parse_args()
    print(args)