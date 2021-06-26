import subprocess

txt_f = r"C:\work\한글 폴더\한글 문서.txt"
with open(txt_f) as ifp:
    print(ifp.read())

cmd = [
    'notepad',
    txt_f
]
po = subprocess.Popen(cmd)
po.wait()
print(po.returncode)
