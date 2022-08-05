# Basic Network Speed Logging with Python

The goal by the end of this project is to have a functional script logging network speeds, emailing daily reports, and emailing alerts when the speed drops below a certain threshold.

## Part 1: Install the required libraries

We first need to install `speedtest-cli` and `matplotlib`. To do this open a command prompt and enter the following

```console
pip install speedtest-cli
```

and

```console
pip install matplotlib
```

More info about speedtest-cli can be found [here](https://github.com/sivel/speedtest-cli), and more info about matplotlib can be found [here](https://matplotlib.org/stable/index.html)

## Part 2: Working with CSVs

The easiest way to store spreadsheet like data is using CSV (Comma Separated Values) files. Python has a built in module named "csv" for working with these files. You can find the documentation [here](https://docs.python.org/3/library/csv.html).

To explore the CSV module a bit we have the nile.csv file. This is historical flood height level for The Nile. In each row, the first entry is year and the second entry is flood height. To read this file in python we need to open it and create a `reader` object.

```python
import csv

with open("nile.csv", "r") as csvfile:
    reader = csv.reader(csvfile)

```

There are several things going on here. First the `open` function will open whatever file we put in. `newline=""` is recommended to use whenever opening CSVs. The `"r"` specifies how that file is opened. What that does is open the file and specify that we can only *read* the file. We cannot make any changes to the file, only read it. All of the available permissions and what they do can be found [here](https://tutorial.eyehunts.com/python/python-file-modes-open-write-append-r-r-w-w-x-etc/). One very important thing to note is that `w` will overwrite the existing file.

The reader object allows us to iterate over the lines of a csv file. Each line is turned into a list. It is also possible to use `DictReader` instead to turn each line into a dictionary. To illustrate this, let's print each row.

```python
import csv

with open("nile.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
```

If you look at the print output, you'll notice that each item in the lists is a string. So it's important to remember if you want to average out the flood heights you first need to turn each one into a float. Another thing to notice, the first row of this file is labels, so we need to skip it to work with the data. For example, here is how we can print out the average.

```python
import csv

total = 0
lines = 0
with open("nile.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the first line
    for row in reader:
        total += float(row[1])  # need float for the decimals 
        lines += 1
print(total / lines)
```

We can also use the `a` file permission to easily add a new line to the end of the file.

```python
import csv

total = 0
lines = 0
with open("nile.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the first line
    for row in reader:
        total += float(row[1])  # need float for the decimals
        lines += 1
average = total / lines

with open("nile.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    newrow = ["Average", average]
    writer.writerow(newrow)
```

## Part 3: Test the speedtest-cli library

Now that we know a bit of how we are going to store the data, let's look at where we're going to get the data from. For the purposes of this project, we are going to look at just download speed and upload speed.

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
