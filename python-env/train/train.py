from scripts.args_parser import ArgsParser
from scripts.algorithms.nn import NN
from scripts.algorithms.rf import RF
from scripts.algorithms._shared.base_algorithm import BaseAlgorithm

print("[*] ------------------------------------------")
print("[*] Welcome by parodontitis!")
print("[*]         Powered by Krokante Krab 🦀 - 2022")
print("[*] ------------------------------------------")

# Get config based on arguments
parser = ArgsParser()
config = parser.get_config()
algorithm = config['algorithm']

# Run selected algorithm
algorithms = {
    'nn': NN,
    'rf': RF
}

algorithms[algorithm]().train(base=BaseAlgorithm(config))
