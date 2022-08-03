from tkinter import Tk, Canvas, Entry, StringVar, Label
import time
import random
# import threading


root = Tk()
root.geometry('950x700')
root.title('Snowflaker')
cv = Canvas(root, bg='#00003B', width=700, height=700)
cv.pack(side='left')
cvh=cv['height']
cvw=cv['width']
Label(root, text='SEED:', font=('courier', 50)).pack(side='top')
rawseed = StringVar()
rawseed.set('hi')
seedbefore = rawseed.get()
en = Entry(root, textvariable=rawseed)
en.pack(side='top')
en.focus()
namelabel = Label(root, text='hi', wraplength=230, font=('微软雅黑', 40))
namelabel.pack(side='top')
rotate = [[1, 0, 0, 1], [-1, 0, 0, -1],
          [-1, 0, 0, 1], [1, 0, 0, -1],
          [0.5, 0.866025404, -0.866025404, 0.5], [0.5,0.866025404, 0.866025404, -0.5],
          [-0.5, -0.866025404, 0.866025404, -0.5], [-0.5, -0.866025404, -0.866025404, 0.5],
          [0.5, -0.866025404, 0.866025404, 0.5], [0.5, -0.866025404, -0.866025404, -0.5],
          [-0.5, 0.866025404, -0.866025404, -0.5], [-0.5, 0.866025404, 0.866025404, 0.5]
          ]
colors = ['red', 'magenta', 'darkmagenta', 'royalblue', 'darkgreen', 'springgreen', 'lightyellow',
          'purple', 'maroon', 'orange', 'coral', 'cyan', 'lightskyblue', 'hotpink', 'forestgreen', 'gold']
entryflag = 1

with open('./list.txt', 'r') as file:
    doc = file.read().split('\n')
    print(doc)

class shape(object):
    def __init__(self, arg, personal):

        def fw(w0, x0):
            w1 = w0 % x0+1
            return w1

        def fh(h0, x0, w0):
            # h1=(h0*x0//20)//(x0-w0)
            h1 = h0//10
            return h1

        def ft(t0, x0):
            fix1 = [int(personal[:3]) % 333+1, int((333-int(personal[:3]) % 333)*int(personal[3:5])/33300)]
            fix2 = [int(personal[5:8]) % 333+1, int(100-int(personal[5:8]) % 333*int(personal[8:10])/33300)]
            if x0-10 <= fix1[0]:
                if t0 <= 100-(100-fix1[1])*x0/fix1[0]:
                    t1 = 0
                elif t0 <= 100-(100-fix2[1])*x0/fix2[0]:
                    t1 = 1
                else:
                    t1 = 2
            elif x0-10 >= fix2[0]:
                if t0 <= fix1[1]-fix1[1]*(x0-10-fix1[0])/333:
                    t1 = 0
                elif t0 <= fix2[1]-fix2[1]*(x0-10-fix2[0])/333:
                    t1 = 1
                else:
                    t1 = 2
            else:
                t1 = 1
            return t1
        random.seed(arg)
        self.str = str(int(1000000000000000*random.random()))
        # x:start coordinates on x axis,w:width,h:height,t:type
        self.x = int(self.str[:3]) % 333+10
        self.w = fw(int(self.str[3:5]), self.x)
        self.h = fh(int(self.str[5:8]), self.x, self.w)
        self.t = ft(int(self.str[8:10]), self.x)


def flake(itemseed, complexity=18, colorindex=0):

    namelabel['text'] = itemseed
    cv.delete('all')
    seedlist = [itemseed]
    # print(seedlist)
    seedn = 0
    while seedn < complexity:
        random.seed(seedlist[-1])
        seedlist.append(int(1000000000000000*random.random()))
        seedn += 1
    print(seedlist)
    shapenum = 0
    xmin = 99999
    xmax = 0
    while shapenum < len(seedlist):
        curshape = shape(seedlist[shapenum], str(seedlist[1]**2)[2:])
        # 根据类型计算直角各点坐标
        
        point = []
        color = "white"
        if curshape.x >= xmax:
            xmax = curshape.x
        point.append([curshape.x, 0])
        if curshape.t == 1:
            point.append([curshape.x, curshape.h])
            point.append([curshape.x-curshape.w//2, curshape.h+curshape.w//2])
            point.append([curshape.x-curshape.w, curshape.h])
            point.append([curshape.x-curshape.w, 0])
            if curshape.x-curshape.w <= xmin:
                xmin = curshape.x-curshape.w
        elif curshape.t == 2:
            point.append([curshape.x-(curshape.h %
                         curshape.w), curshape.h % curshape.w])
            point.append([curshape.x-curshape.w, curshape.h % curshape.w])
            point.append([curshape.x-curshape.w, 0])
            if curshape.x-curshape.w <= xmin:
                xmin = curshape.x-curshape.w
        else:
            point.append([0, curshape.x])
            if curshape.x <= xmin:
                xmin = curshape.x
        # 变换到成xy轴夹角60°的坐标系
        n = 0
        while n < len(point):
            point[n][0] = point[n][0]+point[n][1]//2
            point[n][1] = int(point[n][1]*0.866025404)
            n += 1
        # 绘制直线
        if colorindex > 0:
            color = colors[random.randrange(0, len(colors))]
        section = 0
        while section < len(rotate):
            cv.create_line(int(int(cvh)//2+xmin*rotate[section][0]), int(int(cvh)//2+xmin*rotate[section][2]), int(
            int(cvh)//2+xmax*rotate[section][0]), int(int(cvh)//2+xmax*rotate[section][2]), fill=color)
            pointnum = 0
            while pointnum < len(point)-1:
                cv.create_line(int(int(cvh)//2+point[pointnum][0]*rotate[section][0]+point[pointnum][1]*rotate[section][1]), int(int(cvh)//2+point[pointnum][0]*rotate[section][2]+point[pointnum][1]*rotate[section][3]), int(
                    int(cvh)//2+point[pointnum+1][0]*rotate[section][0]+point[pointnum+1][1]*rotate[section][1]), int(int(cvh)//2+point[pointnum+1][0]*rotate[section][2]+point[pointnum+1][1]*rotate[section][3]), fill=color)
                pointnum += 1
            section += 1
        shapenum += 1

    root.update()


def playslides(event):
    docline = 0
    entryflag = 0
    while docline < len(doc):
        item = doc[docline].split(',')
        itemseed = item[0]
        itemcomplexity = 18
        itemcolor = 0
        if len(item) > 1:
            itemcomplexity = int(item[1])
        if len(item) > 2:
            itemcolor = int(item[2])
        # print(item, itemseed)
        flake(itemseed, complexity=itemcomplexity,colorindex=itemcolor)
        entryflag = 1
        time.sleep(3)
        #print(doc[docline])
        docline += 1



playlabel = Label(root, text='PLAY SLIDES', font=('微软雅黑', 20),bg="lightblue")
playlabel.pack(side='bottom')
playlabel.bind('<Button-1>', playslides)


def refreshFlake():
	global seedbefore
	seednow = rawseed.get()
	if entryflag and seednow != seedbefore:
		flake(seednow)
		seedbefore = seednow
	root.after(500, refreshFlake)


# 创建线程，不能使用target=dataget_main(52190805, 1, 0)
# t = threading.Thread(target=refreshFlake)
# t.daemon = True     # 线程配置
# t.start()           # 启动线程
flake(rawseed.get())
refreshFlake()
root.mainloop()
