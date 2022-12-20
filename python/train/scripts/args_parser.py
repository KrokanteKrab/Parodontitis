import sys


class ArgsParser:
    def get_config(self):
        cmdargs = sys.argv

        # Defaults
        user = None
        algorithm = 'nn'
        iterations = 5

        try:
            if cmdargs.count("--help") > 0:
                self.help()

            if cmdargs.count("--user") > 0:
                user_param_index = cmdargs.index("--user") + 1
                match cmdargs[user_param_index]:
                    case 'iza' | 'tim' | 'youri' | 'leander':
                        print(f'[*] User is: {cmdargs[user_param_index]}!')
                    case _:
                        print("[*] Param value for --user is invalid, needs to be your name in lower case.")
                        sys.exit()

                # Set value from arg
                user = cmdargs[user_param_index]

            if user is None:
                print("[*] Param value for --user is required.")
                sys.exit()

            if cmdargs.count("--algorithm") > 0:
                algorithm_param_index = cmdargs.index("--algorithm") + 1
                match cmdargs[algorithm_param_index]:
                    case 'nn' | 'rf':
                        print(f'[*] Algorithm is: {cmdargs[algorithm_param_index]}!')
                    case _:
                        print("[*] Param value for --algorithm is invalid, needs to be nn or rf.")
                        sys.exit()

                # Set value from arg
                algorithm = cmdargs[algorithm_param_index]
            else:
                print(f'[*] Algorithm is: {algorithm}!')

            if cmdargs.count("--iterations") > 0:
                iterations_param_index = cmdargs.index("--iterations") + 1
                match cmdargs[iterations_param_index]:
                    case '5' | '10' | '15':
                        print(f'[*] Iterations is: {cmdargs[iterations_param_index]}!')
                    case _:
                        print("[*] Param value for --algorithm is invalid, needs to be 5, 10 or 15.")
                        sys.exit()

                # Set value from arg
                iterations = int(cmdargs[iterations_param_index])
            else:
                print(f'[*] Iterations is: {iterations}!')

        except Exception:
            print("[*] Could not set-up training! Some went wrong...")

        return {
            'user': user,
            'algorithm': algorithm,
            'iterations': iterations
        }

    def help(self):
        print("[*] Every possible parameter:")
        print("[*] --user (your_name) (required)")
        print("[*] --algorithm (nn/rf) (default: nn)")
        print("[*] --iterations (5/10/15) (default: 5)")
        sys.exit()
