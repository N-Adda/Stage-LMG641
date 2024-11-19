#!/usr/bin/python

# lmg670.py
#
# Implement interface to ZES Zimmer LMG670 1 to 7 Channel Power Analyzer
#
# 2015-01, Jan de Cuveland

import socket

EOS = "\n"
TIMEOUT = 2

class lmg641_socket:
    def __init__(self, host = ""):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host != "":
            self.connect(host, 5025)

    def connect(self, host, port):
        self._s.connect((host, port))
        self._host = host
        self._port = port
        self._s.settimeout(TIMEOUT)
        
    def send(self, msg):
        self._s.sendall((msg + EOS).encode())

    def recv_str(self):
        response = b""  # Initialise response comme bytes
        while True:
            try:
                response += self._s.recv(4096) 
                if response.endswith(EOS.encode()):
                    break
            except Exception as e:
                print("Erreur lors de la réception des données :", e)
                return response.decode() if response else "vide" 
        return response[:-len(EOS)].decode() 



    def send_cmd(self, cmd):
        result = self.query(cmd + ";*opc?")
        if result != "1":
            print ("opc returned unexpected value:"), result

    def send_brk(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._host, self._port + 1))
        s.settimeout(TIMEOUT)
        s.sendall(b"break\n")
        response = b""
        while response[-len(EOS):] != EOS.encode():
            try:
                response += s.recv(256)
            except socket.timeout as e:
                print ("error:"), e
                s.close()
                return False
        s.close()
        return (response[:-len(EOS)] == b"0 ok")

    def query(self, msg):
        self.send(msg)
        return self.recv_str()

    def close(self):
        self._s.close()
    
    def __del__(self):
        self.close()


class lmg641(lmg641_socket):
    _short_commands_enabled = False

    def reset(self):
        self.send_brk()
        self._short_commands_enabled = False
        self.send_cmd("*rst;*cls")

    def goto_short_commands(self):
        if not self._short_commands_enabled:
            self.send("*zlang short")
        self._short_commands_enabled = True

    def goto_scpi_commands(self):
        if self._short_commands_enabled:
            self.send("*zlang scpi")
        self._short_commands_enabled = False

    def send_short(self, msg):
        self.goto_short_commands()
        self.send(msg)

    def send_scpi(self, msg):
        self.goto_scpi_commands()
        self.send(msg)

    def send_short_cmd(self, cmd):
        self.goto_short_commands()
        self.send_cmd(cmd)

    def send_scpi_cmd(self, cmd):
        self.goto_scpi_commands()
        self.send_cmd(cmd)

    def query_short(self, msg):
        self.goto_short_commands()
        return self.query(msg)

    def query_scpi(self, msg):
        self.goto_scpi_commands()
        return self.query(msg)

    def goto_local(self):
        self.send("gtl")

    def read_id(self):
        return self.query("*idn?").split(",")

    def read_errors(self):
        return self.query_scpi("syst:err:all?")

    def set_ranges(self, current, voltage):
            cmd = "iauto{0} 0;uauto{0} 0;irng{0} {1};urng{0} {2}".format(1, current, voltage)
            self.send_short_cmd(cmd)

    def select_values(self, values):
        
        self.send_short('actn;' + "?;".join(values) + "?")


    def read_raw_values(self):
        return self.recv_str().split(";")
        #if not rep:
         #   print ("donnée vide")
          #  return []
        #print ("donnée présente")
        #return rep.split(";")
        
    #def read_float_values(self):
     #   values_raw = self.read_raw_values()
      #  return [ float(x) for x in values_raw ]

    def read_float_values(self):
        values_raw = self.read_raw_values()
        cleaned_values = []
        for value in values_raw:
            try:
                segments = value.strip().split("\n")
                for segment in segments:
                    cleaned_values.append(float(segment))
            except ValueError:
                print(f"Impossible de convertir la valeur en float : {value}")
        return cleaned_values



    def cont_on(self):
        self.send_short("cont on")

    def cont_off(self):
        self.send_short("cont off")
    
    def track(self):
        self.send_short('GLCTRAC0,"U1111"')
    
    def rate(self):
        self.send_short("GLCSR100")
    
    def length(self):
        self.send_short("CYCLMODSCOPE")
    
    def inim(self):
        self.send_short("INIM")
    
    def fetch(self):
        self.send_short("GLPTLEN?")
    
    def read_graph(self):
        self.query("GLPTLEN?")
    
        
    def disconnect(self):
        self.read_errors()
        self.goto_local()
