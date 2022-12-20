from scripts.args_parser import ArgsParser
from scripts.algorithms.nn import NN

print("[*] ------------------------------------------")
print("[*] Welcome by parodontitis!")
print("[*]         Powered by Krokante Krab 🦀 - 2022")
print("[*] ------------------------------------------")

# Get config based on arguments
parser = ArgsParser()
config = parser.get_config()

# Run selected algorithm
match config['algorithm']:
    case 'nn':
        nn = NN(config)
        nn.train()
