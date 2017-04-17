import paho.mqtt.client as mqtt
import configparser
import rtmidi.midiutil as midi
import time
import flaschenwand
import os

class Midi2Broker:
    """Receiving MIDI events and sending them to an MQTT broker."""
    
    def __init__(self, host, port, midi_port):
        self.midiin, port_name = midi.open_midiinput(midi_port)
        print("listening to midi device", port_name)
        self.midiin.set_callback(self.on_midi_event)

        print("connecting and sending msgs to", host, port)
        self.mqtt = mqtt.Client()
        self.mqtt.connect(host, port)


    def on_midi_event(self, event, data=None):
        message, _ = event
        chan, note, val = message

        self.publish("midi/chan/{0}/note/{1}/".format(chan,note), val)

    def publish(self, topic, payload):
        self.mqtt.publish(topic, payload)

        
class Broker2Flaschenwand:
    """Listening for broker messages and using them to control a flaschenand."""
    
    def __init__(self, host, port, topic2rgb, shutdown_topic):        
        self._topic2rgb = topic2rgb
        self.shutdown_topic = shutdown_topic
        
        print("listening for msgs on", host, port)
        self.mqtt = mqtt.Client()
        self.mqtt.connect(host, port)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message

        self.worker = flaschenwand.FlaschenwandWorker()
        self.worker.start()
        self.worker.scroll("midi")

    def start(self):
        self.mqtt.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.mqtt.subscribe("midi/#")

    def on_message(self, client, userdata, msg):
        #print("received", userdata, msg.topic, msg.payload)
        # val in [0,128], therefore take the double
        val = 2 * int(msg.payload)

        if msg.topic == self.shutdown_topic:
            self._handle_shutdown()
            
        elif msg.topic in self._topic2rgb:            
            col = self._topic2rgb[msg.topic]
            # Check if topic maps to frequency (redf, greenf, bluef)
            if col.endswith("f"):
                col = col[0:-1] # remove last 'f'
                self.worker.freqs[col] = val
            else:
                self.worker.colors[col] = val
    
    def _handle_shutdown(self):
        self.worker.scroll("bye")
        os.system("shutdown -h now")
        
        
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("midi.ini")
    
    client = Midi2Broker(config["mqtt"]["host"],
                         config.getint("mqtt", "port"),
                         config.getint("hardware", "port"))

    print('Use a client to watch mqtt messages: mosquitto_sub -h {} -t "midi/#" -v'.
          format(config["mqtt"]["host"]))

    topic2rgb = {config["mqtt_topics"]["redf"]: "redf",
                 config["mqtt_topics"]["greenf"]: "greenf",
                 config["mqtt_topics"]["bluef"]: "bluef",
                 config["mqtt_topics"]["red"]: "red",
                 config["mqtt_topics"]["green"]: "green",
                 config["mqtt_topics"]["blue"]: "blue"}
    fw_controller = Broker2Flaschenwand(config["mqtt"]["host"],
                                        config.getint("mqtt", "port"),
                                        topic2rgb,
                                        config["mqtt_topics"]["shutdown"])
    fw_controller.start()

    print("finished")
