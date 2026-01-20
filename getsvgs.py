import sys

n=1
with open(sys.argv[1]) as f:
    s = f.read()
    for svg in s.split("</svg>"):
        k = svg.find("<svg")
        #print(n,k,svg[:100])
        if k>=0:
            with open(f"svg{n}.svg",mode="w") as of:
                print(svg[k:]+"</svg>",file=of)
            n+=1

