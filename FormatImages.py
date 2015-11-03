import Image, os

if os.path.exists('C:\Users\Matthew\PycharmProjects\EPL_visualize\crests'):
    for filename in os.listdir('C:\Users\Matthew\PycharmProjects\EPL_visualize\crests'):
        img = Image.open('crests/' + filename)
        if min(img.size) >= 150:
            img = img.resize((img.size[0]/2, img.size[1]/2))
            img.save('crests/' + filename)
else:
    print "Nah"
