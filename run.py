import argparse 
from api import start_stream

# args
parser = argparse.ArgumentParser()
parser.add_argument('topic', help='a twitter trend you\'d like to analyze')
args = parser.parse_args()

if __name__ == '__main__':
    start_stream(args.topic)