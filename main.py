from concurrent.futures import ThreadPoolExecutor
from requests import get, head
import time



class downloader:
    def __init__(self, url, num, name):
        self.url = url
        self.num = num
        self.name = name
        self.getsize = 0
        r = head(self.url, allow_redirects=True)
        self.size = int(r.headers['Content-Length'])

    def down(self, start, end, chunk_size=10240):
        headers = {'range': f'bytes={start}-{end}'}
        r = get(self.url, headers=headers, stream=True)
        with open(self.name, "rb+") as f:
            f.seek(start)
            for chunk in r.iter_content(chunk_size):
                f.write(chunk)
                self.getsize += chunk_size



    def main(self):
        start_time = time.time()
        f = open(self.name, 'wb')
        f.truncate(self.size)
        f.close()
        tp = ThreadPoolExecutor(max_workers=self.num)
        futures = []
        start = 0
        for i in range(self.num):
            end = int((i+1)/self.num*self.size)
            future = tp.submit(self.down, start, end)
            futures.append(future)
            start = end+1
        while True:
            process = self.getsize/self.size*100
            last = self.getsize
            time.sleep(1)
            curr = self.getsize
            down = (curr-last)/1024
            if down > 1024:
                speed = f'{down/1024:6.2f}MB/s'
                print(f'process: {process:6.2f}% | speed: {speed}', end='\r')
                
            else:
                speed = f'{down:6.2f}KB/s'
                print(f'process: {process:6.2f}% | speed: {speed}', end='\r')
                
            if process >= 100:
                print(f'process: {100.00:6}% | speed:  00.00KB/s', end=' | ')
                
                break

        tp.shutdown()
        end_time = time.time()
        total_time = end_time-start_time
        average_speed = self.size/total_time/1024/1024
        print(f'总耗时: {total_time:.0f}s | 平均下载速率: {average_speed:.2f}MB/s')
        ed = input("请按空格键结束")


if __name__ == '__main__':
    url = str(input("请输入下载地址："))
    dn = url[url.rfind('/')+1 :]
    start_pos  = url.find('//')
    end_pos = url.find('/',start_pos)
    domain = url[start_pos:end_pos]
    end_pos = url.find('/',start_pos)
    down = downloader(url,12, dn)
    down.main()
    multiprocessing.freeze_support()  
