import socket

class Patlite:
    # default dest
    _host = '106.138.6.12'
    _port = 10000

    # light attributes
    OFF = b'\x00'
    ON = b'\x01'
    BLINK1 = b'\x02' # ----____----____
    BLINK2 = b'\x03' # -_-_____-_-_____

    # buzzer attributes
    SHORT = b'\x01' # --__--__--__--__
    LONG = b'\x02'  # ----____----____
    TINY = b'\x03'  # -_-_____-_-_____
    BEEP = b'\x04' # ----------------

    _sensor = {
        'red': OFF,
        'yellow': OFF,
        'green': OFF,
        'blue': OFF,
        'white': OFF,
        'buzzer': OFF,
    }


    '''
    シングルトーンパターンで設計
    http://www.denzow.me/entry/2018/01/28/171416
    '''
    _unique_instance = None

    def __new__(self):
        raise NotImplementedError('[err] not permitted')

    # create instance for internal class
    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls.__internal_new__()
        
        return cls._unique_instance


    def set_dest(self, host, port):
        if not(0 <= port <= 65535):
            raise ValueError("[err] port must be set integer")
        
        self._host = host
        self._port = port

    def set_status(self, name, value):
        self._sensor[name] = value
    
    def get_status(self):
        return self._sensor

    def reset_status(self):
        for k in self._sensor:
            self._sensor[k] = self.OFF

    def commit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self._host, self._port))
            except OSError as e:
                print("[err] Cannot connect to patlite. Recheck for address or port.")
                return
            
            dat = self._sensor
            s.sendall(b'\x58\x58\x53\x00\x00\x06' + dat['red'] + dat['yellow'] 
                + dat['green'] + dat['blue'] + dat['white'] + dat['buzzer'])
            data = s.recv(1024)
            print('Received', repr(data))

if __name__=="__main__":
    # import subprocess
    # cmd="cat /etc/hosts | awk 'END{print $1}'|sed -r -e 's/[0-9]+$/1/g'"
    # IPADRESS=(subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")
    IPADRESS="localhost"
    PORTNUM=10000
    print(IPADRESS, PORTNUM)
    p = Patlite.get_instance()
    p.set_dest(IPADRESS, PORTNUM)
    p.set_status("red", p.ON)
    p.set_status("yellow", p.BLINK1)
    p.set_status("green", p.BLINK2)
    p.set_status("buzzer", p.ON)
    p.commit()


