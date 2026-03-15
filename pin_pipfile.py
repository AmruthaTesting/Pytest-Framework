"""
pin_pipfile.py
Pins all installed package versions exactly into Pipfile / Pipfile.lock.
Run once after installing deps:
    pipenv run python pin_pipfile.py
"""
import subprocess
import sys

try:
    import tomllib as tomli
except ImportError:
    import tomli


def get_installed_version(pkg: str) -> str:
    code = (
        "import importlib.metadata as m, sys; "
        f"print(m.version(sys.argv[1]))"
    )
    out = subprocess.check_output(
        ["pipenv", "run", "python", "-c", code, pkg], text=True
    )
    return out.strip()


def pin(section: str, dev: bool = False):
    pkgs = pipfile.get(section, {})
    for name in pkgs.keys():
        ver = get_installed_version(name)
        print(f"[pin] {name}=={ver} {'(dev)' if dev else ''}")
        cmd = ["pipenv", "install"]
        if dev:
            cmd.append("--dev")
        cmd.append(f"{name}=={ver}")
        subprocess.check_call(cmd)


with open("Pipfile", "rb") as f:
    pipfile = tomli.load(f)

pin(section="packages", dev=False)
pin(section="dev-packages", dev=True)
subprocess.check_call(["pipenv", "lock"])
print("\nDone. Pipfile and Pipfile.lock updated with exact versions.")
