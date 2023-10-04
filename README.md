# White Cane Detection Server

- This repository is about white cane detection flask server empowered by running YOLOX inference with openvino runtime.

# Prequisites
- docker
- make
- ubuntu 20.04 and above

# Environment setup and run
- Clone this repository and navigate to this [current directory](./)
- To spin up the white cane detection server, please run (with sudo if your docker needs sudo)
```bash
[sudo] make run-white-cane-openvino-env 
```
- Above command includes
  1. Download openvino weights
  2. Build ready-to-use docker env with dependencies
  3. Start the white cane detection inference server

- If you see something like this in your console, you are good to go!
```console
* Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8081
 * Running on http://172.17.0.2:8081
[ INFO ] Press CTRL+C to quit
```


