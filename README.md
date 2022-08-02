# Basic Network Speed Logging with Python

The goal by the end of this project is to have a functional script logging network speeds, emailing daily reports, and emailing alerts when the speed drops below a certain threshold.

## Step 1: Install the required libraries

We first need to install `speedtest-cli` and `matplotlib`. To do this open a command prompt and enter the following

```console
pip install speedtest-cli
```

and

```console
pip install matplotlib
```

More info about speedtest-cli can be found [here](https://github.com/sivel/speedtest-cli), and more info about matplotlib can be found [here](https://matplotlib.org/stable/index.html)

## Step 2: Test the speedtest-cli library

Open a python file in your favorite editor and let's test out the speedtest library

```python
from speedtest import Speedtest

st = Speedtest()

print("Download speed ", st.download())
print("Upload speed ", st.upload())
```

Run this script and look at what it prints out

```text
Download speed  28426305.567623887
Upload speed  5886609.301300182
```

If you're generally familiar with internet speeds you'll notice these results are in bits. To instead give the numbers in a more manageable megabytes, change the print lines to

```python
print(f"Download speed   {st.download()/8000000:.2f}MB/s")
print(f"Upload speed   {st.upload()/8000000:.2f}MB/s")
```

The `Speedtest` class has a bulit in method for finding the best server for testing, so we will add that

```python
from speedtest import Speedtest

st = Speedtest()

st.get_best_server()
print(f"Download speed   {st.download()/8000000:.2f}MB/s")
print(f"Upload speed   {st.upload()/8000000:.2f}MB/s")
```

If we import the built in `time` module, we can add some functionality to our script. First, we can use the time module to see how long it takes the script to test both download and upload speeds. Second we can use the `time` module to run these tests on an interval loop.

```python
from speedtest import Speedtest
import time

st = Speedtest()

while True:
    st.get_best_server()
    t = time.time()
    print(f"Download speed   {st.download()/8000000:.2f}MB/s")
    print(f"Upload speed   {st.upload()/8000000:.2f}MB/s")
    print(f"The test took {time.time()-t} seconds")
    time.sleep(60)
```

Before executing, let's look at exactly what this code is doing. `while True` is creating a while loop based on a condition that is *always* true. This will cause the loop to run indefinitely, which can be very dangerous. The only way to stop the script outside of force closing python is to use `Ctrl+C` to force stop. Always be careful with while loops that do not have a way to stop.

Beyond that, the `time.sleep(60)` is the most important part of the code. This line tells python to stop doing things for 60 seconds before continuing to execute. So as setup, we are going to be testing our download and upload speeds every 60 seconds. This can be adusted to whatever time interval we choose. Keep in mind, tests are not instant so the tests don't begin every 60 seconds, but 60 seconds after one ends the next will begin.

## Step 3: Logging the results
