import bottle
import os
import subprocess
import flaschenwand

# Process of the running process
proc_running = None

template = """
    <html>
    <body>
        <a href="/demo/plasma">Plasma</a> <br>
        <a href="/demo/plasma_rotating">Plasma rotierend</a><br>
        <a href="/demo/plasma_circular">Plasma kreis</a>
    <p>
        <a href="/shutdown">Shutdown</a>
    </p>
    <p>
    Farbe:<span style="color:rgb({{red}},{{green}},{{blue}})"> r:{{red}} g: {{green}} b: {{blue}}</span> <br>
    <a href="/color/{{(red+10)%255}}-{{green}}-{{blue}}">r+</a>
    <a href="/color/{{(red-10)%255}}-{{green}}-{{blue}}">r-</a>
    <a href="/color/{{red}}-{{(green+10)%255}}-{{blue}}">g+</a>
    <a href="/color/{{red}}-{{(green-10)%255}}-{{blue}}">g-</a>
    <a href="/color/{{red}}-{{green}}-{{(blue+10)%255}}">b+</a>
    <a href="/color/{{red}}-{{green}}-{{(blue-10)%255}}">b-</a>
    </p>    
    </body>
    </html>

"""

demos = {"plasma":"demo_plasma.py",
         "plasma_rotating": "demo_plasma_rotating.py",
         "plasma_circular": "demo_plasma_rotating.py"}

@bottle.route("/")
def index():
    return bottle.template(template, red=0, green=255, blue=0)

@bottle.route("/demo/<name>")
def demo_plasma_route(name):
    filename = demos[name]
    run_py_process(filename)        
    bottle.redirect("/")

@bottle.route("/color/<red:int>-<green:int>-<blue:int>")
def color_route(red, green, blue):
    stop_process()
    fw = flaschenwand.Flaschenwand()
    fw.set_all_pixels_rgb(red,green,blue)
    fw.show()
    return bottle.template(template, red=red,green=green,blue=blue)


def stop_process():
    global proc_running
    if proc_running is not None:
        proc_running.terminate()    

def run_py_process(prog):
    global proc_running
    stop_process()
    proc_running = subprocess.Popen(["python3", prog])

@bottle.route("/shutdown")
def shutdown_route():
    run_py_process("aus.py")
    os.system("shutdown -h now")

def main():
    bottle.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
