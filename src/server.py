import bottle
import os
import subprocess

# Process ID of the running process
pid_running = None

@bottle.route("/")
def index():
    return """
    <html>
    <body>
        <a href="/demo_plasma">Plasma</a> <br>
        <a href="/demo_plasma_rotating">Plasma rotierend</a>
    <p>
        <a href="/shutdown">Shutdown</a>
    </p>
    </body>
    </html>
    """

@bottle.route("/demo_plasma")
def demo_plasma_route():
    run_py_process("demo_plasma.py")
    bottle.redirect("/")

@bottle.route("/demo_plasma_rotating")
def demo_plasma_rotating_route():
    run_py_process("demo_plasma_rotating.py")
    bottle.redirect("/")

def run_py_process(prog):
    global pid_running
    if pid_running is not None:
        pid_running.terminate()

    pid_running = subprocess.Popen(["python3", prog])

@bottle.route("/shutdown")
def shutdown_route():
    os.system("shutdown -h now")

def main():
    bottle.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
