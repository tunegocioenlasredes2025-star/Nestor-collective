"""Genera la version publicable (Artifact): inlinea fotos como data URI y quita el esqueleto html/head/body."""
import re, base64, os, sys, mimetypes
here=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(here,'index.html'),encoding='utf-8').read()
def inline(m):
    path=os.path.join(here,m.group(1))
    if not os.path.exists(path): return m.group(0)
    mt={'.webp':'image/webp','.png':'image/png'}.get(os.path.splitext(path)[1].lower()) or mimetypes.guess_type(path)[0] or 'image/jpeg'
    return "img:'data:%s;base64,%s'"%(mt,base64.b64encode(open(path,'rb').read()).decode())
s=re.sub(r"img:'(img/[^']+)'",inline,s)
m=re.search(r'<head>(.*?)</head>\s*<body>(.*)</body>',s,re.S)
head=re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*','',m.group(1))
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'artifact.html')
open(out,'w',encoding='utf-8').write(head.strip()+'\n'+m.group(2))
print('artifact ->',out,len(s)//1024,'KB')
