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
        <a href="/demo/plasma">Plasma</a> <br>
        <a href="/demo/plasma_rotating">Plasma rotierend</a><br>
        <a href="/demo/plasma_circular">Plasma kreis</a>
    <p>
        <a href="/shutdown">Shutdown</a>
    </p>
    </body>
    </html>
    """

@bottle.route("/demo/<name>")
def demo_plasma_route(name):
    if name == "plasma":
        run_py_process("demo_plasma.py")
    elif name == "plasma_rotating":
        run_py_process("demo_plasma_rotating.py")
    elif name == "plasma_circular":
        run_py_process("demo_plasma_circular.py")
        
    bottle.redirect("/")

def run_py_process(prog):
    global pid_running
    if pid_running is not None:
        pid_running.terminate()

    pid_running = subprocess.Popen(["python3", prog])

@bottle.route("/shutdown")
def shutdown_route():
    run_py_process("aus.py")
    os.system("shutdown -h now")

def main():
    bottle.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
