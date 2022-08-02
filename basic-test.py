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
