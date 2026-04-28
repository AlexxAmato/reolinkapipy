from pathlib import Path

import json

import yaml
import reolinkapi
import urllib3


def load_camera_config():
    config_path = Path(__file__).with_name("camera.secrets.yml")
    if not config_path.exists():
        raise FileNotFoundError(
            f"Missing config file: {config_path}\n"
            "Create it from examples/camera.secrets.example.yml."
        )

    with config_path.open("r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}

    camera = config.get("camera", {})
    required = ["host", "username", "password"]
    missing = [key for key in required if not camera.get(key)]
    if missing:
        raise ValueError(f"Missing required camera config values: {', '.join(missing)}")

    return camera

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    camera = load_camera_config()
    cam = reolinkapi.Camera(
        camera["host"],
        camera["username"],
        camera["password"],
        https=bool(camera.get("https", False)),
        defer_login=False,
    )

    # print(json.dumps(cam.get_device_info(), indent=2))
    dst = cam.get_dst()
    # ok = cam.add_user("foo", "bar", "admin")
    # alarm = cam.get_alarm_motion()
    # cam.set_device_name(name='my_camera')
    print(dst)