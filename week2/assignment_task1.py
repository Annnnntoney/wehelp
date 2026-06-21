#Position
"""
1.Assume that coordinate of 悟空 is (0, 0).
2.Assume that each cell is 1 distance unit.
3.Characters move only horizontally and vertically.
4.If a character moves to the other side, add additional 2 distance units.
5. If there are multiple characters at the same distance, print them all."""

positions = {
    "悟空": (0, 0),
    "丁滿":(-1, 4),
    "辛巴":(-3, 3),
    "貝吉塔":(-4, -1),
    "弗利沙":(4, -1),
    "特南克斯":(1, -2)
}

def func1(name):
    # your code here
    ax, ay = positions[name]
    a_side = (ax + ay) > 1

    dists = {}
    for other in positions:
        if other == name:
            continue
        bx, by = positions[other]
        b_side = (bx + by) > 1
        d = abs(ax - bx) + abs(ay - by)
        if a_side != b_side:
            d += 2
        dists[other] = d

    far = max(dists.values())
    near = min(dists.values())
    farthest = [n for n in dists if dists[n] == far]
    closest  = [n for n in dists if dists[n] == near]
    print("最遠" + "、".join(farthest) + "；最近" + "、".join(closest))


func1("辛巴")     # print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空")     # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")   # print 最遠辛巴；最近特南克斯
func1("特南克斯") # print 最遠丁滿；最近悟空
