import csv, time
from speedtest import Speedtest


# write a function to find the download and upload speed
# it should also update the csvfile


def network_logger(st):
    # st should be a Speedtest object
    st.get_best_server()
    t = time.time()
    down = f"{st.download()/8000000:.2f}"  # convert to MB/s, round to 2 decimals
    up = f"{st.upload()/8000000:.2f}"  # convert to MB/s, round to 2 decimals
    with open("network-speeds.csv", "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        newrow = [t, down, up]
        writer.writerow(newrow)


st = Speedtest()

# write a loop that will indefinitely run the above function
# determine how often it should run

while True:
    network_logger(st)
    time.sleep(600)
