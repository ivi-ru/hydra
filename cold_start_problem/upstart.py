from subprocess import call
from argparse import ArgumentParser

PROJECT_NAME = 'cold_start_model'

docker_run = f"""
    docker run -v $(pwd)/cold_start_model:/srv/{PROJECT_NAME} \
    -v $(pwd)/data:/srv/data \
"""
docker_run_postfix = f" -it --rm {PROJECT_NAME}:1.0 "

scenarios = {
    "build": f"docker build -t {PROJECT_NAME}:1.0 . ; " + docker_run,
    "bash": docker_run,
    "train_als": docker_run,
    "train_cold_start": docker_run,
    "pipeline": ("train_als", "train_cold_start"),
    "jupyter": docker_run
}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий работы')
    args = parser.parse_args()

    if args.scenario in scenarios:
        if args.scenario == 'build':
            call(scenarios[args.scenario] + docker_run_postfix + args.scenario, shell=True)
        elif args.scenario == 'pipeline':
            # специальный мета-сценарий: препроцессинг, обучение, экспорт
            for stage in scenarios[args.scenario]:
                call(
                    scenarios[stage] + docker_run_postfix + stage,
                    shell=True
                )
        elif args.scenario == 'jupyter':
            call(
                scenarios[args.scenario] + ' -p 8889:8888 ' + docker_run_postfix + args.scenario,
                shell=True
            )
        else:
            call(
                scenarios[args.scenario] + docker_run_postfix + args.scenario,
                shell=True
            )
    else:
        print('Ошибочный сценарий: %s' % args.scenario)
