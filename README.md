# SharkMap

![image](https://user-images.githubusercontent.com/91490989/188681978-a8f0fca5-3845-4785-bebb-cf6a682bd286.png)

## About
SharkMap is a Wireshark capture visualizer that displays traceable public IP connections on a world map.

## How to Setup the Code
1. Clone the repository: `git clone https://github.com/jakeenea51/SharkMap`
2. Enter the SharkMap directory: `cd SharkMap`
3. Download the dependencies: `pip install -r requirements.txt`

## How to Get the Wireshark Capture
1. Open WireShark with the command: `wireshark`
2. Select the network interface you are currently using.
3. Run Wireshark for a short amount of time, just to get a quick capture of your computer's current connections. Captures that are too big will return an error, so keeping the capture size below 1,500 packets is best.
4. Stop the capture and under *File*, export the packet dissections as CSV.
5. Rename the CSV to something simple, such as "shark.csv", and save it in the SharkMap directory.

## How to Run the Code
1. Run the code with the command: `python3 sharkmap.py`
2. Follow the prompts until the map is generated.

## Map Example

![image](https://user-images.githubusercontent.com/91490989/188692936-f8926665-c75f-4624-8872-ef7881dadcc1.png)

