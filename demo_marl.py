import argparse

import xuance.torch.agents
from xuance import get_runner


def parse_args():
    parser = argparse.ArgumentParser("Run an MARL demo.")
    parser.add_argument("--method", type=str, default="mappo")
    parser.add_argument("--env", type=str, default="football")
    parser.add_argument("--env-id", type=str, default="3v1")
    parser.add_argument("--test", type=int, default=1)
    parser.add_argument("--seed", type=int, default=10)
    parser.add_argument("--device", type=str, default="cuda:0")
    return parser.parse_args()


if __name__ == '__main__':
    parser = parse_args()
    runner = get_runner(method=parser.method,
                        env=parser.env,
                        env_id=parser.env_id,
                        parser_args=parser,
                        is_test=parser.test)
    runner.run()
