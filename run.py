import argparse

from toy_problems.lollipop_machine import LollipopMachine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type", type=str, default="candy_counter", help="possible args: candy_counter"
    )
    parser.add_argument(
        "--inp",
        type=str,
        help="a string with sequence of symbols (eg: slllss for candy_counter fsm)",
    )
    parser.add_argument("--file", type=str, help="name of the input file")
    parser.add_argument(
        "--persist",
        action="store_true",
        help="if a failure is encountered, then store the state of the fsm as a file: fsm_YY_MM_HH.pkl",
    )
    parser.add_argument("--restore", type=str, help="location of saved fsm to restore")

    args = parser.parse_args()
    if args.type == "candy_counter":
        if args.restore:
            print("Restoring FSM..")
            candy_counter = LollipopMachine().restore_machine(args.restore)
        else:
            candy_counter = LollipopMachine(args.persist)
        if args.inp:
            candy_counter.process_symbols(list(args.inp))
        elif args.file:
            with open(args.file, "r") as f:
                for c in f.read():
                    candy_counter.process_symbols(c)
        else:
            while True:
                try:
                    inp = input()
                    candy_counter.process_symbols(list(inp))
                except KeyboardInterrupt:
                    print("Standard Input interruped")
                    if args.persist:
                        candy_counter.persist_state()
                    exit(-1)
