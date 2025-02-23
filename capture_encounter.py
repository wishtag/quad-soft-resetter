from PIL import ImageGrab, Image
window_1 = [[664,94,957,270], [664,272,957,492], [1,94,664,492]]
window_2 = [[1624,94,1917,270], [1624,272,1917,492], [961,94,1624,492]]
window_3 = [[664,607,957,783], [664,785,957,1005], [1,607,664,1005]]
window_4 = [[1624,607,1917,783], [1624,785,1917,1005], [961,607,1624,1005]]

encounter = ImageGrab.grab(bbox=(window_1[0]))
encounter.save("img/window1top.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_1[1]))
encounter.save("img/window1bottom.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_1[2]))
encounter.save("img/window1topbig.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_2[0]))
encounter.save("img/window2top.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_2[1]))
encounter.save("img/window2bottom.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_2[2]))
encounter.save("img/window2topbig.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_3[0]))
encounter.save("img/window3top.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_3[1]))
encounter.save("img/window3bottom.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_3[2]))
encounter.save("img/window3topbig.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_4[0]))
encounter.save("img/window4top.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_4[1]))
encounter.save("img/window4bottom.png")
encounter.close()

encounter = ImageGrab.grab(bbox=(window_4[2]))
encounter.save("img/window4topbig.png")
encounter.close()