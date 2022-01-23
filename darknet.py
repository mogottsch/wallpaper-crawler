import subprocess
import os
import json
import pathlib

project_path = pathlib.Path(__file__).parent.resolve()
darknet_path = f"{project_path}/darknet"
darknet_config_path = f"{darknet_path}/cfg"
darknet_weights_path = f"{project_path}/yolov3.weights"
results_path = "/tmp/wallpaper_crawler_results.json"


def get_results() -> dict:
    with open(results_path, "r") as f:
        results = json.loads(f.read())[0]["objects"]
    return results


def image_contains_people(path):
    subprocess.run(
        [
            f"darknet detector test "
            + f"{darknet_config_path}/coco.data {darknet_config_path}/yolov3.cfg {darknet_weights_path} "
            + f"-ext_output -dont_show -out {results_path} "
            + f"{path}",
        ],
        cwd=darknet_path,
        shell=True,
        stdout=open(os.devnull, "wb"),
        stderr=subprocess.STDOUT,
    )

    results = get_results()
    n_people = list(map(lambda obj: obj["name"], results)).count("person")

    return n_people > 0
